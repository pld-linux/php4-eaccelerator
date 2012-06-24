%define		_name		eaccelerator
%define		_pkgname	eaccelerator
%define		php_ver		%(rpm -q --qf '%%{epoch}:%%{version}' php4-devel)

Summary:	eAccelerator module for PHP
Summary(pl):	Modu� eAccelerator dla PHP
Name:		php4-%{_name}
Version:	0.9.1
Release:	1
Epoch:		0
License:	GPL
Vendor:		Turck Software
Group:		Libraries
Source0:	http://osdn.dl.sourceforge.net/eaccelerator/%{_pkgname}-%{version}.tar.gz
# Source0-md5:	638c9949ea9d7254127aac9504c07013
URL:		http://eaccelerator.sourceforge.net/
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	php4-devel >= 4.1
Requires:	apache >= 1.3
Requires:	php4 = %{php_ver}
Requires:	php4-zlib
Requires(post,preun):	php4-common >= 4.1
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php4
%define		extensionsdir	%{_libdir}/php4

%description
eAccelerator is a further development from mmcache PHP Accelerator &
Encoder. It increases performance of PHP scripts by caching them in
compiled state, so that the overhead of compiling is almost completely
eliminated.

%description -l pl
eAccelerator to dalsze stadium rozwoju akceleratora i kodera PHP
mmcache. Zwi�ksza wydajno�� skrypt�w PHP poprzez zapami�tywanie ich w
postaci skompilowanej, dzi�ki czemu narzut potrzebny na kompilacj�
jest prawie ca�kowicie wyeliminowany.

%prep
%setup -q -n %{_pkgname}

%build
phpize
%{__aclocal}
%configure \
	--enable-mmcache=shared \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}
install -d $RPM_BUILD_ROOT%{_bindir}

install ./modules/eaccelerator.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php4-module-install install eaccelerator %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php4-module-install remove eaccelerator %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{extensionsdir}/eaccelerator.so
%attr(755,root,root) %{_bindir}/encoder.php
