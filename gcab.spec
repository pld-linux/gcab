#
# Conditional build:
%bcond_without	apidocs		# API docs
%bcond_without	static_libs	# static library
%bcond_without	vala		# Vala binding
#
Summary:	Cabinet file library
Summary(pl.UTF-8):	Biblioteka obsługi plików cabinet
Name:		gcab
Version:	0.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gcab/0.4/%{name}-%{version}.tar.xz
# Source0-md5:	27c9f182bd279bedae3ba2fc5734c651
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	gobject-introspection-devel >= 0.9.4
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.40.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
%{?with_vala:BuildRequires:	vala >= 2:0.14}
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.22.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cabinet file library.

%description -l pl.UTF-8
Biblioteka obsługi plików cabinet.

%package devel
Summary:	Header files for gcab library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gcab
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.22.0

%description devel
Header files for gcab library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gcab.

%package static
Summary:	Static gcab library
Summary(pl.UTF-8):	Statyczna biblioteka gcab
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gcab library.

%description static -l pl.UTF-8
Statyczna biblioteka gcab.

%package apidocs
Summary:	gcab API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki gcab
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for gcab library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki gcab.

%package -n vala-gcab
Summary:	Vala API for gcab library
Summary(pl.UTF-8):	API języka Vala dla biblioteki gcab
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.14

%description -n vala-gcab
Vala API for gcab library.

%description -n vala-gcab -l pl.UTF-8
API języka Vala dla biblioteki gcab.

%prep
%setup -q

%build
# disabling fast install in configure breaks DESTDIR install
# (libtool tries to relink gcab and fails, leaving temporary script instead of binary)
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--enable-fast-install \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgcab-1.0.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS
%attr(755,root,root) %{_bindir}/gcab
%attr(755,root,root) %{_libdir}/libgcab-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcab-1.0.so.0
%{_libdir}/girepository-1.0/GCab-1.0.typelib
%{_mandir}/man1/gcab.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgcab-1.0.so
%{_includedir}/libgcab-1.0
%{_datadir}/gir-1.0/GCab-1.0.gir
%{_pkgconfigdir}/libgcab-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgcab-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gcab
%endif

%if %{with vala}
%files -n vala-gcab
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libgcab-1.0.vapi
%endif
