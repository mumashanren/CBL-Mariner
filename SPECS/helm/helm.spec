%global debug_package %{nil}
Name:           helm
Version:        3.4.1
Release:        17%{?dist}
Summary:        The Kubernetes Package Manager
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/helm/helm
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/helm/helm/archive/v3.4.1.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2021-21303.patch
Patch1:         CVE-2021-32690.patch
Patch2:         CVE-2022-23525.patch
Patch3:         CVE-2022-23526.patch
Patch4:         CVE-2022-23524.patch
Patch5:         CVE-2023-25165.patch
BuildRequires:  golang >= 1.15.5

%description
Helm is a tool that streamlines installing and managing Kubernetes applications. Think of it like apt/yum/homebrew for Kubernetes.

%prep
%autosetup -p1

%build
tar -xf %{SOURCE1} --no-same-owner
export VERSION=%{version}
for cmd in cmd/* ; do
    go build -tags '' -ldflags '-w -s -X helm.sh/helm/v3/internal/version.version=v$VERSION -X helm.sh/helm/v3/internal/version.metadata= -X helm.sh/helm/v3/internal/version.gitCommit= -X helm.sh/helm/v3/internal/version.gitTreeState=clean ' \
    -mod=vendor -v -o $(basename $cmd) ./$cmd
done

%install
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 ./helm %{buildroot}%{_bindir}

%files
%license LICENSE
%doc ADOPTERS.md SECURITY.md code-of-conduct.md CONTRIBUTING.md README.md
%{_bindir}/helm


%check
go test -v ./cmd/helm

%changelog
* Thu Jun 22 2023 Mitch Zhu <mitchzhu@microsoft.com> - 3.4.1-17
- Bump release to rebuild with go 1.19.10

* Wed Mar 01 2023 Mitch Zhu <mitchzhu@microsoft.com> - 3.4.1-16
- Add patch to fix CVE-2023-25165

* Fri Feb 10 2023 Dan Streetman <ddstreet@microsoft.com> - 3.4.1-15
- CVE-2022-23524

* Wed Dec 21 2022 Jon Slobodzian <joslobo@microsoft.com> - 3.4.1-14
- Patch CVE-2022-23525, CVE-2022-23526
- Added Check Section

* Tue Dec 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 3.4.1-13
- Bump release to rebuild with go 1.18.8-2

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.4.1-12
- Bump release to rebuild with go 1.18.8

* Wed Aug 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.4.1-11
- Bump to rebuild with golang 1.18.5-1

* Tue Jun 07 2022 Andrew Phelps <anphel@microsoft.com> - 3.4.1-10
- Bumping release to rebuild with golang 1.18.3

* Fri Apr 29 2022 chalamalasetty <chalamalasetty@live.com> - 3.4.1-9
- Bumping 'Release' to rebuild with updated Golang version 1.16.15-2.

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 3.4.1-8
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 3.4.1-7
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 3.4.1-6
- Increment release for force republishing using golang 1.16.12

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 3.4.1-5
- Increment release for force republishing using golang 1.16.9

* Mon Sep 20 2021 Henry Beberman <henry.beberman@microsoft.com> - 3.4.1-4
- Patch CVE-2021-32690

* Mon Sep 20 2021 Henry Beberman <henry.beberman@microsoft.com> - 3.4.1-3
- Patch CVE-2021-21303

* Tue Aug 17 2021 Henry Li <lihl@microsoft.com> - 3.4.1-2
- Update and rename vendor source tarball
- Use go to build the project from vendor source
- Remove glide and ca-certificates from BR
- Modify file section to add license and document files

* Wed Nov 25 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 3.4.1-1
- Update helm version 3

* Tue Jun 02 2020 Paul Monson <paulmon@microsoft.com> 2.14.3-2
- Rename go to golang
- Add ca-certificates temporarily

* Thu Oct 17 2019 Andrew Phelps <anphel@microsoft.com> 2.14.3-1
- Original version for CBL-Mariner
