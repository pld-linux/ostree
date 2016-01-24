#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	OSTree - Git for operating system binaries
Summary(pl.UTF-8):	OSTree - Git dla binariów systemów operacyjnych
Name:		ostree
Version:	2016.1
Release:	1
License:	LGPL v2+
Group:		Libraries
#Source0:	http://ftp.gnome.org/pub/GNOME/sources/ostree/%{version}/%{name}-%{version}.tar.xz
Source0:	https://github.com/GNOME/ostree/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	57d48d855980b85be992cc7050026314
# official https://git.gnome.org/browse/libglnx
Source1:	https://github.com/GNOME/libglnx/archive/03138641298fd6799f46b16423871f959332bacf/libglnx.tar.gz
# Source1-md5:	c7234e0156af5480e9fa8eef85f7d107
Source2:	https://github.com/mendsley/bsdiff/archive/1edf9f656850c0c64dae260960fabd8249ea9c60/bsdiff.tar.gz
# Source2-md5:	38464abb5e66b0c8dfbcf94fba6a8004
Patch0:		grub2-pld.patch
URL:		https://wiki.gnome.org/OSTree
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.13
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gobject-introspection-devel >= 1.34.0
BuildRequires:	gpgme-devel >= 1.1.8
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libarchive-devel >= 2.8.0
BuildRequires:	libgsystem-devel >= 2015.1
BuildRequires:	libselinux-devel >= 2.2
BuildRequires:	libsoup-devel >= 2.39.1
BuildRequires:	libtool >= 2:2.2.4
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel >= 5.0.5
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.40.0
Requires:	gpgme >= 1.1.8
Requires:	libarchive >= 2.8.0
Requires:	libselinux >= 2.2
Requires:	libsoup >= 2.39.1
Requires:	xz-libs >= 5.0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OSTree is a tool for managing bootable, immutable, versioned
filesystem trees. While it takes over some of the roles of tradtional
"package managers" like dpkg and rpm, it is not a package system; nor
is it a tool for managing full disk images. Instead, it sits between
those levels, offering a blend of the advantages (and disadvantages)
of both.

%description -l pl.UTF-8
OSTree to narzędzie do zarządzania uruchamialnymi, niezmiennymi,
wersjonowanymi drzewami systemów plików. O ile przejmuje niektóre
funkcje tradycyjnych "zarządców pakietów", takich jak dpkg i rpm, nie
jest to system pakietów; nie jest to także narzędzie do zarządzania
pełnymi obrazami dysków. Jest to poziom pośredni, oferujący połączenie
zalet (i wad) obu.

%package devel
Summary:	Header files for OSTree library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OSTree
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.40.0

%description devel
Header files for OSTree library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OSTree.

%package static
Summary:	Static OSTree library
Summary(pl.UTF-8):	Statyczna biblioteka OSTree
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OSTree library.

%description static -l pl.UTF-8
Statyczna biblioteka OSTree.

%package apidocs
Summary:	OSTree API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki OSTree
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
OSTree API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki OSTree.

%package grub2
Summary:	GRUB2 integration for OSTree
Summary(pl.UTF-8):	Integracja bootloadera GRUB2 z OSTree
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	grub2

%description grub2
GRUB2 integration for OSTree.

%description grub2 -l pl.UTF-8
Integracja bootloadera GRUB2 z OSTree.

%package -n dracut-ostree
Summary:	OSTree support for Dracut
Summary(pl.UTF-8):	Obsługa OSTree dla Dracuta
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	dracut

%description -n dracut-ostree
OSTree support for Dracut.

%description -n dracut-ostree -l pl.UTF-8
Obsługa OSTree dla Dracuta.

%prep
%setup -q -a1 -a2
%patch0 -p1
rmdir libglnx bsdiff
%{__mv} libglnx-* libglnx
%{__mv} bsdiff-* bsdiff

# see autogen.sh
sed -e 's,$(libglnx_srcpath),'./libglnx,g < libglnx/Makefile-libglnx.am >libglnx/Makefile-libglnx.am.inc
sed -e 's,$(libbsdiff_srcpath),'./bsdiff,g < bsdiff/Makefile-bsdiff.am >bsdiff/Makefile-bsdiff.am.inc

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	GJS=/usr/bin/gjs \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-dracut \
	--with-html-dir=%{_gtkdocdir} \
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libostree-1.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md TODO
%attr(755,root,root) %{_bindir}/ostree
%attr(755,root,root) %{_libdir}/libostree-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libostree-1.so.1
%{_libdir}/girepository-1.0/OSTree-1.0.typelib
%{_datadir}/ostree
%{_mandir}/man1/ostree.1*
%{_mandir}/man1/ostree-*.1*
%{_mandir}/man5/ostree.repo.5*
%{_mandir}/man5/ostree.repo-config.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libostree-1.so
%{_includedir}/ostree-1
%{_datadir}/gir-1.0/OSTree-1.0.gir
%{_pkgconfigdir}/ostree-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libostree-1.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/ostree

%files grub2
%defattr(644,root,root,755)
/lib/grub.d/15_ostree
%dir %{_libexecdir}/ostree
%attr(755,root,root) %{_libexecdir}/ostree/grub2-15_ostree

%files -n dracut-ostree
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ostree-prepare-root
%attr(755,root,root) %{_sbindir}/ostree-remount
%{systemdunitdir}/ostree-prepare-root.service
%{systemdunitdir}/ostree-remount.service
%dir %{_prefix}/lib/dracut/modules.d/98ostree
%attr(755,root,root) %{_prefix}/lib/dracut/modules.d/98ostree/module-setup.sh
%config(noreplace) %verify(not md5 mtime size) /etc/dracut.conf.d/ostree.conf
