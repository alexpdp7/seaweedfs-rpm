%undefine _disable_source_fetch

Name:    seaweedfs
Version: $VERSION$
Release: 1.0
Summary: SeaweedFS is a fast distributed storage system for blobs, objects, files, and data lake, for billions of files
URL: https://github.com/seaweedfs/seaweedfs
License: Apache-2.0 license
Source0: weed
Source1: weed.service
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
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/weed.service
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/{lib,log}/weed

%files
%defattr(755,root,root)
%{_bindir}/weed
%defattr(644,root,root)
%{_unitdir}/weed.service
%dir %attr(750,weed,weed) %{_localstatedir}/lib/weed
%dir %attr(750,weed,weed) %{_localstatedir}/log/weed

%pre
getent group weed >/dev/null || groupadd -r weed
getent passwd weed >/dev/null || \
    useradd -r -g weed -d /var/lib/weed -s /sbin/nologin \
    -c "SeaweedFS Daemon" weed
exit 0

%post
%systemd_post weed.service

%preun
%systemd_preun weed.service

%postun
%systemd_postun_with_restart weed.service

%changelog
