%define		_name		eaccelerator
%define		_pkgname	eaccelerator
%define		_sysconfdir	/etc/php4

Summary:	eAccelerator module for PHP
Summary(pl):	Modu³ eAccelerator dla PHP
Name:		php4-%{_name}
Version:	0.9.3
Release:	1.5
Epoch:		0
License:	GPL
Vendor:		Turck Software
Group:		Libraries
Source0:	http://dl.sourceforge.net/eaccelerator/%{_pkgname}-%{version}.tar.gz
# Source0-md5:	b17ddf953f18ee6df5c2c24ffccb37d9
Source1:	%{_name}.ini
URL:		http://eaccelerator.sourceforge.net/
BuildRequires:	php4-devel >= 3:4.1
%requires_eq_to php4 php4-devel
Requires:	php4-zlib
Requires:	%{_sysconfdir}/conf.d
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

%description
eAccelerator is a further development from mmcache PHP Accelerator &
Encoder. It increases performance of PHP scripts by caching them in
compiled state, so that the overhead of compiling is almost completely
eliminated.

%description -l pl
eAccelerator to dalsze stadium rozwoju akceleratora i kodera PHP
mmcache. Zwiêksza wydajno¶æ skryptów PHP poprzez zapamiêtywanie ich w
postaci skompilowanej, dziêki czemu narzut potrzebny na kompilacjê
jest prawie ca³kowicie wyeliminowany.


%package webinterface
Summary:    WEB interface for PHP Accelerator
Summary(pl):    Interfejs WEB dla PHP Accelerator
Group:      Libraries
Requires:   %{name} = %{epoch}:%{version}-%{release}

%description webinterface
PHP Accelerator can be managed through web interface script mmcache.php.
So you need to put this file on your web site. For security reasons it
is recommended to restrict the usage of this script by your local IP and
setup password based access.

More information you can find at %{url}.

%description webinterface -l pl
PHP Accelerator mo¿e byæ sterowany ze strony internetowej z
wykorzystaniem skryptu eaccelerator.php. Jedyne co trzeba zrobiæ, to
umie¶ciæ plik we w³a¶ciwym miejscu na stronie internetowej. Z powodów
bezpieczeñstwa zalecane jest, aby ograniczyæ korzystanie ze skryptu do
lokalnego adresu i ustawiæ autoryzacjê has³em

Wiêcej informacji mo¿na znale¼æ %{url}.

%prep
%setup -q -n %{_pkgname}-%{version}

%build
phpize
%configure \
	--enable-eaccelerator=shared \
	--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{extensionsdir},%{_bindir},%{_sysconfdir}/conf.d,/var/cache/%{_name}}

install ./modules/eaccelerator.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}
install ./eaccelerator_password.php $RPM_BUILD_ROOT%{_bindir}
install ./eaccelerator.php $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_name}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%preun
if [ "$1" = 0 ]; then
	# remove last pieces of cache
	rm -f /var/cache/%{_name}/*
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{extensionsdir}/eaccelerator.so
%attr(755,root,root) %{_bindir}/*
%attr(770,root,http) /var/cache/%{_name}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) /etc/php4/conf.d/eaccelerator.ini

%files webinterface
%defattr(644,root,root,755)
# FIXME: czy tak rzeczywi¶cie powinno/mo¿e byæ??
%doc eaccelerator{,_password}.php
