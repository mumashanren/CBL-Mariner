Summary:        A highly-available key value store for shared configuration
Name:           etcd
Version:        3.4.23
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/etcd-io/etcd/
#Source0:       https://github.com/etcd-io/etcd/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        etcd.service
BuildRequires:  git
BuildRequires:  golang >= 1.13

%description
A highly-available key value store for shared configuration and service discovery.

%package tools
Summary:        Diagnostic tools for etcd
Group:          System Environment/Security
Requires:       %{name} = %{version}-%{release}

%description tools
A highly-available key value store for shared configuration and service discovery.
The etcd-tools package contains the etcd-dump-db and etcd-dump-logs diagnostic
tools.

%prep
%setup -q

%build
# Turn off auto moduling. golang 1.13 does not automatically consider the vendor folder (it does as of 1.14).
# To successfully build, manually hydrate the go package cache (GOPATH) with the included vendor folder and
# etcd's source code before invoking the build script.
export GO111MODULE=off

%define OUR_GOPATH %{_topdir}/.gopath
mkdir -p "%{OUR_GOPATH}/vendor" "%{OUR_GOPATH}/etcd_src/src/go.etcd.io"
export GOPATH=%{OUR_GOPATH}/vendor:%{OUR_GOPATH}/etcd_src

ln -s "%{_builddir}/%{name}-%{version}/vendor" "%{OUR_GOPATH}/vendor/src"
ln -s "%{_builddir}/%{name}-%{version}" "%{OUR_GOPATH}/etcd_src/src/go.etcd.io/etcd"
# Disable DWARF compression
sed -i 's/GO_LDFLAGS -X/GO_LDFLAGS -compressdwarf=false -X/g' Makefile ./build
./build
# Now build the etcd-dump* tools
source ./build
tools_build

%install
install -vdm755 %{buildroot}%{_bindir}
install -vdm755 %{buildroot}/%{_docdir}/%{name}-%{version}
install -vdm755 %{buildroot}/lib/systemd/system
install -vdm 0755 %{buildroot}%{_sysconfdir}/etcd
install -vpm 0755 -T etcd.conf.yml.sample %{buildroot}%{_sysconfdir}/etcd/etcd-default-conf.yml

chown -R root:root %{buildroot}%{_bindir}
chown -R root:root %{buildroot}/%{_docdir}/%{name}-%{version}

mv %{_builddir}/%{name}-%{version}/bin/etcd %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/bin/etcdctl %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/
mv %{_builddir}/%{name}-%{version}/etcdctl/README.md %{buildroot}/%{_docdir}/%{name}-%{version}/README-etcdctl.md
mv %{_builddir}/%{name}-%{version}/etcdctl/READMEv2.md %{buildroot}/%{_docdir}/%{name}-%{version}/READMEv2-etcdctl.md
mv %{_builddir}/%{name}-%{version}/bin/tools/etcd-dump-logs %{buildroot}%{_bindir}/
mv %{_builddir}/%{name}-%{version}/bin/tools/etcd-dump-db %{buildroot}%{_bindir}/


install -vdm755 %{buildroot}/lib/systemd/system-preset
echo "disable etcd.service" > %{buildroot}/lib/systemd/system-preset/50-etcd.preset

cp %{SOURCE1} %{buildroot}/lib/systemd/system
install -vdm755 %{buildroot}%{_sharedstatedir}/etcd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*



%files
%license LICENSE
%{_bindir}/etcd
%{_bindir}/etcdctl
/%{_docdir}/%{name}-%{version}/*
/lib/systemd/system/etcd.service
/lib/systemd/system-preset/50-etcd.preset
%dir %{_sharedstatedir}/etcd
%config(noreplace) %{_sysconfdir}/etcd/etcd-default-conf.yml

%files tools
%{_bindir}/etcd-dump-*

%changelog
* Thu Jun 22 2023 Mitch Zhu <mitchzhu@microsoft.com> - 3.4.23-2
- Bump release to rebuild with go 1.19.10
  Disable DWARF compression in go 1.19.10

* Fri Jan 27 2023 Muhammad Falak <mwani@microsoft.com> - 3.4.23-1
- Bump version to address CVE-2022-3064

* Tue Dec 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 3.4.13-14
- Bump release to rebuild with go 1.18.8-2

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.4.13-13
- Bump release to rebuild with go 1.18.8

* Wed Aug 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.4.13-12
- Bump to rebuild with golang 1.18.5-1

* Tue Jun 07 2022 Andrew Phelps <anphel@microsoft.com> - 3.4.13-11
- Bumping release to rebuild with golang 1.18.3

* Fri Apr 29 2022 chalamalasetty <chalamalasetty@live.com> - 3.4.13-10
- Bumping 'Release' to rebuild with updated Golang version 1.16.15-2.

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 3.4.13-9
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 3.4.13-8
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 3.4.13-7
- Increment release for force republishing using golang 1.16.12
- Update Source0 URL

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 3.4.13-6
- Increment release for force republishing using golang 1.16.9

*   Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.13-5
-   Increment release to force republishing using golang 1.16.7.

*   Thu Aug 05 2021 Tom Fay <tomfay@microsoft.com> - 3.4.13-4
-   Add etcd-tools package.

*   Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 3.4.13-3
-   Increment release to force republishing using golang 1.15.13.

*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.13-2
-   Increment release to force republishing using golang 1.15.11.

*   Mon Jan 25 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.13-1
-   Update to version 3.4.13.

*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 3.3.25-2
-   Increment release to force republishing using golang 1.15.

*   Thu Sep 03 2020 Joe Schmitt <joschmit@microsoft.com> 3.3.25-1
-   Update to version 3.3.25 which fixes CVE-2020-15106, CVE-2020-15112, CVE-2020-15114, and CVE-2020-15115.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.3.11-2
-   Added %%license line automatically

*   Thu May 07 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.3.11-1
-   Upgrade to version 3.3.11, which fixes CVE-2018-16886.
-   Update summary.

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.3.9-4
-   Renaming go to golang

*   Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.3.9-3
-   Fixed "Source0" tag.
-   License verified and "License" tag updated.
-   Removed "%%define sha1".

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.3.9-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 3.3.9-1
-   Bump etcd version to 3.3.9

*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1.5-4
-   Remove shadow requires

*   Sun Aug 27 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.1.5-3
-   File based configuration for etcd service.

*   Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.5-2
-   Provide preset file to disable service by default

*   Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 3.1.5-1
-   Upgraded to version 3.1.5, build from sources

*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.9-1
-   Upgraded to version 3.0.9

*   Fri Jun 24 2016 Xiaolin Li <xiaolinl@vmware.com> 2.3.7-1
-   Upgraded to version 2.3.7

*   Wed May 25 2016 Nick Shi <nshi@vmware.com> 2.2.5-3
-   Changing etcd service type from simple to notify

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.5-2
-   GA - Bump release of all rpms

*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.5-1
-   Upgraded to version 2.2.5

*   Tue Jul 28 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.1-2
-   Adding etcd service file

*   Tue Jul 21 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.1-1
-   Update to version etcd v2.1.1

*   Tue Mar 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.4-1
-   Initial build.  First version
