# Install

```
$ sudo dnf copr enable koalillo/seaweedfs rhel-9-x86_64
$ sudo dnf install seaweedfs
$ sudo systemctl start weed
```

# Notes

## Distro packages

* [Alpine](https://git.alpinelinux.org/aports/tree/testing/seaweedfs?h=master)
* [Debian](https://salsa.debian.org/go-team/packages/seaweedfs)
* [AUR](https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=seaweedfs)
* [Void](https://github.com/void-linux/void-packages/blob/master/srcpkgs/seaweedfs/template)
* [NixOS](https://github.com/NixOS/nixpkgs/blob/master/pkgs/applications/networking/seaweedfs/default.nix)

## seaweed-up

https://github.com/seaweedfs/seaweed-up/ creates systemd units, etc.
