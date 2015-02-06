%if %{_use_internal_dependency_generator}
%define __noautoprov '(.*)apr(.*)|(.*)sofia(.*)'
%else
%define __find_provides %{nil}
%endif

%define devel %mklibname %{name} -d
%define libs %mklibname %{name}

Name:		unimrcp-deps
Version:	1.1.0
Release:	3

Summary:	Media Resource Control Protocol Stack
License:	Apache
Group:		System/Libraries
Url:		http://unimrcp.org

Source:		http://unimrcp.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	autoconf
BuildRequires:	automake

%package -n %{libs}
Summary:	UniMRCP depends Stack shared librarries
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%package -n %{devel}
Summary:	UniMRCP depends Stack development
Group:		Development/C
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	lib%{name} = %{version}-%{release}

%description
UniMRCP depends on a number of third party tools and libraries, which are
required and must be installed first. Alternatively, the original packages
of APR, APR-Util and Sofia-SIP libraries and patches for them
can be downloaded from http://www.unimrcp.org/dependencies/

%description -n %{libs}
UniMRCP depends on a number of third party tools and libraries, which are
required and must be installed first. Alternatively, the original packages
of APR, APR-Util and Sofia-SIP libraries and patches for them
can be downloaded from http://www.unimrcp.org/dependencies/

%description -n %{devel}
UniMRCP depends on a number of third party tools and libraries, which are
required and must be installed first. Alternatively, the original packages
of APR, APR-Util and Sofia-SIP libraries and patches for them
can be downloaded from http://www.unimrcp.org/dependencies/

%prep
%setup -q

%build
cd libs/apr
%configure2_5x --enable-threads \
--includedir=%{_datadir}/%{name}/include \
--libdir=%{_datadir}/%{name}/lib \
--bindir=%{_datadir}/%{name}/bin \
--datadir=%{_datadir}/%{name} \
--prefix=%{_datadir}/%{name}
%make

cd ../apr-util
%configure2_5x --with-apr=../apr \
--includedir=%{_datadir}/%{name}/include \
--libdir=%{_datadir}/%{name}/lib \
--bindir=%{_datadir}/%{name}/bin \
--datadir=%{_datadir}/%{name} \
--prefix=%{_datadir}/%{name}
%make

cd ../sofia-sip
libtoolize --automake --force
aclocal -I m4 --force
autoheader --force
autoconf --force
automake --gnu --force-missing --add-missing
%configure2_5x --disable-rpath --with-glib=no \
--includedir=%{_datadir}/%{name}/include \
--libdir=%{_datadir}/%{name}/lib \
--bindir=%{_datadir}/%{name}/bin \
--datadir=%{_datadir}/%{name} \
--prefix=%{_datadir}/%{name}
%make

%install
install -d -m1775 %{buildroot}%{_datadir}/%{name}

cd libs/apr
%makeinstall_std
cd ../apr-util
%makeinstall_std
cd ../sofia-sip
%makeinstall_std

%files -n %{libs}
%{_datadir}/%{name}/lib

%files -n %{devel}
%{_datadir}/%{name}/include
%{_datadir}/%{name}/build-1
%{_datadir}/%{name}/bin
%{_datadir}/%{name}/sofia-sip


%changelog
* Thu Feb 16 2012 Denis Silakov <dsilakov@mandriva.org> 1.1.0-1mdv2012.0
+ Revision: 775094
- Reformat description to shorten lines

  + zamir <zamir@mandriva.org>
    - search build error
    - clear provides

* Sun Aug 21 2011 zamir <zamir@mandriva.org> 1.1.0-0
+ Revision: 695980
- may be need expat source?.. try
- try again
- try again
- try fix script creating dir
- build new pkg version

* Mon Feb 28 2011 Funda Wang <fwang@mandriva.org> 1.0.2-3
+ Revision: 640872
- rebuild

* Sat Feb 12 2011 zamir <zamir@mandriva.org> 1.0.2-2
+ Revision: 637390
- change depend
- fixed requires

* Fri Feb 11 2011 zamir <zamir@mandriva.org> 1.0.2-1
+ Revision: 637315
- changed provide information
- changed provide information

* Fri Feb 11 2011 zamir <zamir@mandriva.org> 1.0.2-0
+ Revision: 637269
- first build
- create unimrcp-deps

