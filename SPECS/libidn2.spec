%global package_speccommit b78e52cca00c7062e19b1ca871222426948998d7
%global usver 2.3.4
%global xsver 4
%global xsrel %{xsver}%{?xscount}%{?xshash}

Summary:          Library to support IDNA2008 internationalized domain names
Name:             libidn2
Version:          2.3.4
Release: %{?xsrel}~XCPNG2698.2%{?dist}
License:          (GPL-2.0-or-later OR LGPL-3.0-or-later) AND GPL-3.0-or-later
URL:              https://www.gnu.org/software/libidn/#libidn2
Source0: libidn2-2.3.4.tar.gz

BuildRequires:    gnupg2
BuildRequires:    gcc
BuildRequires:    make
BuildRequires:    gettext
BuildRequires:    libunistring-devel
BuildRequires:    texinfo
Provides:         bundled(gnulib)

%description
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package devel
Summary:          Development files for libidn2
Requires:         %{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description devel
The libidn2-devel package contains libraries and header files for
developing applications that use libidn2.

%package -n idn2
Summary:          IDNA2008 internationalized domain names conversion tool
License:          GPL-3.0-or-later
Requires:         %{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires(post):   /sbin/install-info
Requires(preun):  /sbin/install-info
%endif

%description -n idn2
The idn2 package contains the idn2 command line tool for testing
IDNA2008 conversions.

%prep
%autosetup

%build
%configure --disable-static
# Avoid (unnecessary) full autoreconf
%make_build AUTOMAKE=true
%make_build AUTOMAKE=true -C doc html

%install
%make_install AUTOMAKE=true

# Clean-up examples for documentation
%make_build -C examples distclean
rm -f examples/Makefile*

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Some file cleanups
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%find_lang %{name}

%check
%make_build -C tests check

%ldconfig_scriptlets

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -n idn2
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun -n idn2
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi
%endif

%files -f %{name}.lang
%license COPYING COPYING.LESSERv3 COPYING.unicode COPYINGv2
%doc AUTHORS NEWS README.md
%{_libdir}/%{name}.so.0*

%files devel
%doc doc/%{name}.html examples
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/idn2.h
%{_mandir}/man3/idn2_*.3*
%{_datadir}/gtk-doc/

%files -n idn2
%{_bindir}/idn2
%{_mandir}/man1/idn2.1*
%{_infodir}/%{name}.info*

%changelog
* Thu Jan 16 2025 XenServer Rebuild <rebuild@xenserver.com> - 2.3.4-4
- CP-53241: XenServer 9 rebuild

* Thu Jul 13 2023 Lin Liu <lin.liu@citrix.com> - 2.3.4-3
- Remove gpgcheck and rebuild

* Tue Jun 27 2023 Lin Liu <lin.liu@citrix.com> - 2.3.4-2
- Add source code checksum

* Tue Jun 27 2023 Lin Liu <lin.liu@citrix.com> - 2.3.4-1
- First imported release

