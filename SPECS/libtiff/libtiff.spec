Summary:        TIFF libraries and associated utilities.
Name:           libtiff
Version:        4.5.1
Release:        1%{?dist}
License:        libtiff
URL:            https://gitlab.com/libtiff/libtiff
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://gitlab.com/libtiff/libtiff/-/archive/v%{version}/libtiff-v%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libjpeg-turbo-devel

Requires:       libjpeg-turbo

%description
The LibTIFF package contains the TIFF libraries and associated utilities. The libraries are used by many programs for reading and writing TIFF files and the utilities are used for general work with TIFF files.

%package        devel
Summary:        Header and development files

Requires:       %{name} = %{version}-%{release}
Requires:       libjpeg-turbo-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1 -n libtiff-v%{version}

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
sed -i "s/for file.*/for false/g" autogen.sh
./autogen.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE.md
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/*

%changelog
* Mon Jul 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.5.1-1
- Auto-upgrade to 4.5.1 - patch CVE-2023-26966

* Fri May 26 2023 Rachel Menge <rachelmenge@microsoft.com> - 4.5.0-3
- Patch CVE-2023-2731

* Fri May 12 2023 Aadhar Agarwal <aadagarwal@microsoft.com> - 4.5.0-2
- Patch CVE-2023-0795 CVE-2023-0796 CVE-2023-0797 CVE-2023-0798 CVE-2023-0799

* Tue Feb 28 2023 Mitch Zhu <mitchzhu@microsoft.com> - 4.5.0-1
- Upgrade version to 4.5.0 to fix CVE-2023-0796,  CVE-2023-0797, CVE-2023-0798,
- CVE-2023-0799, CVE-2023-0801, CVE-2023-0802, CVE-2023-0803, CVE-2023-0804
- Remove patches that no longer apply
- Repatched CVE-2022-48281

* Thu Feb 16 2023 Dallas Delaney <dadelan@microsoft.com> - 4.4.0-9
- Patch CVE-2023-0795 CVE-2023-0796 CVE-2023-0797 CVE-2023-0798 CVE-2023-0799

* Thu Feb 16 2023 Dallas Delaney <dadelan@microsoft.com> - 4.4.0-8
- Patch CVE-2023-0800 CVE-2023-0801 CVE-2023-0802 CVE-2023-0803 CVE-2023-0804

* Thu Feb 02 2023 Henry Li <lihl@microsoft.com> - 4.4.0-7
- Patch CVE-2022-48281

* Fri Nov 18 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 4.4.0-6
- Patching CVE-2022-3970.

* Mon Nov 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.4.0-5
- Patching CVE-2022s: 3597, 3598, 3599, 3626, and 3627.

* Mon Oct 24 2022 Sean Dougherty <sdougherty@microsoft.com> - 4.4.0-4
- Patch CVE-2022-3570

* Fri Oct 07 2022 Bala <balakumaran.kannan@microsoft.com> - 4.4.0-3
- Patch CVE-2022-2953

* Fri Jul 15 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 4.4.0-2
- Patch CVE-2022-2056, CVE-2022-2057, and CVE-2022-2058

* Tue Jun 28 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.4.0-1
- Upgrade version to 4.4.0 to fix CVE-2022-0908
- Remove patches that no longer apply
- Add autoconf, libtool, automake as BR
- Use autosetup and modify build steps

* Thu Mar 17 2022 Muhammad Falak <mwani@microsoft.com> - 4.1.0-3
- Backport patches from upstream to fix CVE-2022-0561, CVE-2022-0562 & CVE-2022-0891

* Fri Mar 19 2021 Jon Slobodzian <joslobo@microsoft.com> - 4.1.0-2
- Add patches for CVE-2020-35521, CVE-2020-35522, CVE-2020-35523, CVE-2020-35524

* Tue May 26 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.1.0-1
- Update to 4.1.0

* Wed May 13 2020 Nick Samson <nisamson@microsoft.com> - 4.0.10-6
- Added %%license line automatically

* Mon May 11 2020 Nicolas Ontiveros <niontive@microsoft.com> 4.0.10-5
- Fix CVE-2019-17546.
- Remove sha1 macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.0.10-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Feb 05 2019 Keerthana K <keerthanak@vmware.com> 4.0.10-3
- Fix for CVE-2019-6128.

* Mon Jan 28 2019 Keerthana K <keerthanak@vmware.com> 4.0.10-2
- Fix for CVE-2018-12900

* Mon Dec 10 2018 Ashwin H <ashwinh@vmware.com> 4.0.10-1
- Update to 4.0.10

* Sun Dec 02 2018 Ashwin H <ashwinh@vmware.com> 4.0.9-5
- Fix CVE-2018-17100, CVE-2018-17101

* Mon May 14 2018 Xiaolin Li <xiaolinl@vmware.com> 4.0.9-4
- Fix CVE-2018-7456, CVE-2018-8905, CVE-2018-5784, CVE-2017-11613

* Wed Feb 14 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-3
- Patch for CVE-2017-17095

* Wed Jan 31 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-2
- Repatched CVE-2017-9935

* Wed Jan 17 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-1
- Updated to version 4.0.9 to fix CVE-2017-11613, CVE-2017-9937,
- CVE-2017-17973. Added a patch for CVE-2017-18013

* Mon Dec 11 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-7
- Added patch for CVE-2017-9935

* Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-6
- Added patches for CVE-2017-13726, CVE-2017-13727

* Mon Nov 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.0.8-5
- Patch : CVE-2017-12944

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.8-4
- Use standard configure macros

* Wed Aug 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.8-3
- Added patch for CVE-2017-9936, CVE-2017-11335

* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 4.0.8-2
- Applied patch for CVE-2017-10688

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-1
- Updated to version 4.0.8.

* Tue May 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.7-4
- Added patch for CVE-2016-10266, CVE-2016-10268, CVE-2016-10269, CVE-2016-10267 and libtiff-heap-buffer-overflow patch

* Mon Apr 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.0.7-3
- Patch : CVE-2016-10092, CVE-2016-10093, CVE-2016-10094

* Thu Jan 19 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.0.7-2
- Patch : CVE-2017-5225

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.0.7-1
- Update to 4.0.7. It fixes CVE-2016-953[3456789] and CVE-2016-9540
- Remove obsolete patches

* Wed Oct 12 2016 Dheeraj Shetty <dheerajs@vmware.com> 4.0.6-3
- Fixed security issues : CVE-2016-3945, CVE-2016-3990, CVE-2016-3991

* Thu Sep 22 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.6-2
- Fixed security issues : CVE-2015-8668, CVE-2015-7554, CVE-2015-8683+CVE-2015-8665,CVE-2016-3186
- CVE-2015-1547

* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.0.6-1
- Initial version
