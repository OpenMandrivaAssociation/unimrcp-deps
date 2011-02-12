%define name unimrcp-deps
%define devel %mklibname %{name} -d
%define libs %mklibname %{name}

Name: %{name}
Version: 1.0.2
Release: %mkrel 2

Summary: Media Resource Control Protocol Stack
License: Apache
Group: System/Libraries
Url: http://unimrcp.org
BuildRoot: %{_tmppath}/%{name}-%{version}

Source: http://unimrcp.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0: sofia-sip-1.12.10-undefined-non-weak-symbol.patch

BuildRequires:  glib2-devel
BuildRequires:  libopenssl-devel
BuildRequires:  pkgconfig
BuildRequires:  autoconf
BuildRequires:  automake

%package -n %{libs}
Summary: UniMRCP depends Stack shared librarries
Group: System/Libraries
Provides: lib%{name} = %{version}-%{release}

%package -n %{devel}
Summary: UniMRCP depends Stack development
Group: Development/C
Provides: lib%{name}-devel = %{version}-%{release}
Requires: lib%{name} = %{version}-%{release}, pkgconfig

%description
UniMRCP depends on a number of third party tools and libraries, which are required and must be installed first.
Alternatively, the original packages of APR, APR-Util and Sofia-SIP libraries and patches for them
can be downloaded from http://www.unimrcp.org/dependencies/

%description -n %{libs}
UniMRCP depends on a number of third party tools and libraries, which are required and must be installed first.
Alternatively, the original packages of APR, APR-Util and Sofia-SIP libraries and patches for them
can be downloaded from http://www.unimrcp.org/dependencies/

%description -n %{devel}
UniMRCP depends on a number of third party tools and libraries, which are required and must be installed first.
Alternatively, the original packages of APR, APR-Util and Sofia-SIP libraries and patches for them
can be downloaded from http://www.unimrcp.org/dependencies/

%prep
%setup -q
cd libs/sofia-sip
%patch0 -p0 -b .weak-symbol

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
install -d -m1775 %{buildroot}%{_datadir}/%{name}

cd libs/apr
%makeinstall_std
cd ../apr-util
%makeinstall_std
cd ../sofia-sip
%makeinstall_std

%clean
rm -fr %{buildroot}

%files -n %{libs}
%defattr(-,root,root)
%{_datadir}/%{name}/lib

%files -n %{devel}
%defattr(-,root,root)
%{_datadir}/%{name}/include
%{_datadir}/%{name}/build-1
%{_datadir}/%{name}/bin
%{_datadir}/%{name}/sofia-sip
