#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	OSTree - Git for operating system binaries
Summary(pl.UTF-8):	OSTree - Git dla binariów systemów operacyjnych
Name:		ostree
Version:	2023.7
Release:	6
License:	LGPL v2+
Group:		Libraries
#Source0Download: https://github.com/ostreedev/ostree/releases
Source0:	https://github.com/ostreedev/ostree/releases/download/v%{version}/libostree-%{version}.tar.xz
# Source0-md5:	343d92730484b0ed7052c51a8393b59e
# for non-release checkouts
#Source1:	https://github.com/GNOME/libglnx/archive/03138641298fd6799f46b16423871f959332bacf/libglnx.tar.gz
## Source1-md5:	c7234e0156af5480e9fa8eef85f7d107
#Source2:	https://github.com/mendsley/bsdiff/archive/1edf9f656850c0c64dae260960fabd8249ea9c60/bsdiff.tar.gz
## Source2-md5:	38464abb5e66b0c8dfbcf94fba6a8004
Patch0:		grub2-pld.patch
URL:		https://wiki.gnome.org/OSTree
BuildRequires:	attr-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.13
BuildRequires:	avahi-devel >= 0.6.31
BuildRequires:	avahi-glib-devel >= 0.6.31
BuildRequires:	bison
BuildRequires:	curl-devel >= 7.29.0
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel >= 1:2.66.0
BuildRequires:	gobject-introspection-devel >= 1.51.5
BuildRequires:	gpgme-devel >= 1.8.0
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libarchive-devel >= 2.8.0
BuildRequires:	libfuse3-devel >= 3.1.1
BuildRequires:	libgpg-error-devel
BuildRequires:	libmount-devel >= 2.23.0
BuildRequires:	libselinux-devel >= 2.2
BuildRequires:	libsodium-devel >= 1.0.14
# for ostree-trivial-httpd
BuildRequires:	libsoup3-devel >= 3.0.0
BuildRequires:	libtool >= 2:2.2.4
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel >= 1:5.0.5
BuildRequires:	zlib-devel
Requires:	curl-libs >= 7.29.0
Requires:	glib2 >= 1:2.66.0
Requires:	gpgme >= 1.8.0
Requires:	libarchive >= 2.8.0
Requires:	libfuse3 >= 3.1.1
Requires:	libmount >= 2.23.0
Requires:	libselinux >= 2.2
Requires:	libsodium >= 1.0.14
Requires:	xz-libs >= 1:5.0.5
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
Requires:	glib2-devel >= 1:2.66.0

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
BuildArch:	noarch

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
BuildArch:	noarch

%description grub2
GRUB2 integration for OSTree.

%description grub2 -l pl.UTF-8
Integracja bootloadera GRUB2 z OSTree.

%package -n bash-completion-ostree
Summary:	Bash completion for ostree command
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów polecenia ostree
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-ostree
Bash completion for ostree command.

%description -n bash-completion-ostree -l pl.UTF-8
Bashowe uzupełnianie parametrów polecenia ostree.

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
%setup -q -n libostree-%{version}
%patch0 -p1

# for non-release checkouts
#rmdir libglnx bsdiff
#%{__mv} libglnx-* libglnx
#%{__mv} bsdiff-* bsdiff

# see autogen.sh
sed -e 's,$(libglnx_srcpath),libglnx,g' < libglnx/Makefile-libglnx.am >libglnx/Makefile-libglnx.am.inc
sed -e 's,$(libbsdiff_srcpath),bsdiff,g' < bsdiff/Makefile-bsdiff.am >bsdiff/Makefile-bsdiff.am.inc

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal} -I buildutil -I libglnx
%{__autoconf}
%{__autoheader}
%{__automake}
# use curl in libostree to avoid libsoup2/libsoup3 conflicts in clients
%configure \
	GJS=/usr/bin/gjs \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-curl \
	--with-dracut \
	--with-ed25519-libsodium \
	--with-html-dir=%{_gtkdocdir} \
	--with-soup3 \
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
%attr(755,root,root) %{_bindir}/rofiles-fuse
%attr(755,root,root) %{_libdir}/libostree-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libostree-1.so.1
%{_libdir}/girepository-1.0/OSTree-1.0.typelib
%dir %{_libexecdir}/libostree
%{_datadir}/ostree
%{_mandir}/man1/ostree.1*
%{_mandir}/man1/ostree-*.1*
%{_mandir}/man1/rofiles-fuse.1*
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
%attr(755,root,root) %{_libexecdir}/libostree/grub2-15_ostree

%files -n bash-completion-ostree
%defattr(644,root,root,755)
%{bash_compdir}/ostree

%files -n dracut-ostree
%defattr(644,root,root,755)
%dir %{_prefix}/lib/ostree
%attr(755,root,root) %{_prefix}/lib/ostree/ostree-prepare-root
%attr(755,root,root) %{_prefix}/lib/ostree/ostree-remount
%{systemdunitdir}/ostree-boot-complete.service
%{systemdunitdir}/ostree-finalize-staged.path
%{systemdunitdir}/ostree-finalize-staged.service
%{systemdunitdir}/ostree-finalize-staged-hold.service
%{systemdunitdir}/ostree-prepare-root.service
%{systemdunitdir}/ostree-remount.service
%{systemdtmpfilesdir}/ostree-tmpfiles.conf
%attr(755,root,root) /lib/systemd/system-generators/ostree-system-generator
%dir %{_prefix}/lib/dracut/modules.d/98ostree
%attr(755,root,root) %{_prefix}/lib/dracut/modules.d/98ostree/module-setup.sh
%config(noreplace) %verify(not md5 mtime size) /etc/dracut.conf.d/ostree.conf
