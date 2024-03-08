%undefine _disable_source_fetch

Name:    seaweedfs
Version: $VERSION$
Release: 1.0
Summary: SeaweedFS is a fast distributed storage system for blobs, objects, files, and data lake, for billions of files
URL: https://github.com/seaweedfs/seaweedfs
License: Apache-2.0 license
Source0: weed
BuildRoot: %{_topdir}/BUILD/%{name}-%{version}-%{release}
BuildArch: x86_64
Requires(pre): shadow-utils

%{?systemd_requires}
BuildRequires: systemd

AutoReqProv: no

%define __strip /bin/true
%define __os_install_post %{nil}

%description
%{summary}

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/weed

%files
%defattr(755,root,root)
%{_bindir}/weed

%pre
getent group weed >/dev/null || groupadd -r weed
getent passwd weed >/dev/null || \
    useradd -r -g weed -d /dev/null -s /sbin/nologin \
    -c "SeaweedFS Daemon" weed
exit 0

%changelog
