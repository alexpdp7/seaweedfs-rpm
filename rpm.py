#!/usr/bin/env python3
import contextlib
import pathlib
import shutil
import subprocess
import tempfile
import urllib.request


"""
Heavily inspired in https://github.com/miniflux/v2/tree/main/packaging/rpm
"""


@contextlib.contextmanager
def get_files_from_archive_url(archive_url, files) -> pathlib.Path:
    with tempfile.TemporaryDirectory() as tempdir:
        tempdir = pathlib.Path(tempdir)
        archive = tempdir / "archive.tar.gz"
        with urllib.request.urlopen(archive_url) as u:
            with open(archive, "wb") as t:
                shutil.copyfileobj(u, t)
        shutil.unpack_archive(archive, tempdir)
        yield [tempdir / f for f in files]


def build_container():
    subprocess.run(["podman", "build", "--pull=always", "-t", "rpm-builder:latest", "."], check=True)

version = "3.95"
output = pathlib.Path.cwd() / "output"
output.mkdir(parents=True)

with get_files_from_archive_url(f"https://github.com/seaweedfs/seaweedfs/releases/download/{version}/linux_amd64.tar.gz", ["weed"]) as fs:
    assert len(fs) == 1
    weed = fs[0]
    spec = pathlib.Path("seaweedfs.spec").read_text()
    with tempfile.TemporaryDirectory() as rpm_build_tempdir:
        rpm_build_tempdir = pathlib.Path(rpm_build_tempdir)
        shutil.copyfile(weed, rpm_build_tempdir / "weed")
        pathlib.Path(rpm_build_tempdir / "seaweedfs.spec").write_text(spec.replace("$VERSION$", version))
        weed_service = pathlib.Path("weed.service").absolute()

        build_container()

        subprocess.run([
            'podman', 'run', '-it', '--rm',
            '--security-opt', 'label=disable',
            '-v', f'{rpm_build_tempdir}:/build',
            '-v', f'{rpm_build_tempdir}/weed:/root/rpmbuild/SOURCES/weed',
            '-v', f'{weed_service}:/root/rpmbuild/SOURCES/weed.service',
            '-v', f'{output}:/root/rpmbuild/SRPMS/',
            '-v', f'{output}:/root/rpmbuild/RPMS/',
            '-w', '/build',
            'rpm-builder:latest',
            'rpmbuild', '-ba', 'seaweedfs.spec'
        ], check=True)
