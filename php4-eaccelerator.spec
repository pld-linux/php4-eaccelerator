%define		_name		eaccelerator
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	eAccelerator module for PHP
Summary(pl.UTF-8):	Moduł eAccelerator dla PHP
Name:		php4-%{_name}
Version:	0.9.5
Release:	7
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/eaccelerator/%{_name}-%{version}.tar.bz2
# Source0-md5:	dad54af67488b83a2af6e30f661f613b
Source1:	%{name}.ini
URL:		http://eaccelerator.sourceforge.net/
BuildRequires:	php4-devel >= 3:4.1
BuildRequires:	rpmbuild(macros) >= 1.322
%requires_eq	php4-common
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Requires:	php(zlib)
Conflicts:	php-mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eAccelerator is a further development from mmcache PHP Accelerator &
Encoder. It increases performance of PHP scripts by caching them in
compiled state, so that the overhead of compiling is almost completely
eliminated.

%description -l pl.UTF-8
eAccelerator to dalsze stadium rozwoju akceleratora i kodera PHP
mmcache. Zwiększa wydajność skryptów PHP poprzez zapamiętywanie ich w
postaci skompilowanej, dzięki czemu narzut potrzebny na kompilację
jest prawie całkowicie wyeliminowany.

%package webinterface
Summary:	WEB interface for PHP Accelerator
Summary(pl.UTF-8):	Interfejs WWW dla PHP Acceleratora
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description webinterface
PHP Accelerator can be managed through web interface script
eaccelerator.php. So you need to put this file on your web site. For
security reasons it is recommended to restrict the usage of this
script by your local IP and setup password based access.

More information you can find at %{url}.

%description webinterface -l pl.UTF-8
PHP Accelerator może być sterowany ze strony internetowej z
wykorzystaniem skryptu eaccelerator.php. Jedyne co trzeba zrobić, to
umieścić plik we właściwym miejscu na stronie internetowej. Z powodów
bezpieczeństwa zalecane jest, aby ograniczyć korzystanie ze skryptu do
lokalnego adresu i ustawić autoryzację hasłem.

Więcej informacji można znaleźć pod %{url}.

%prep
%setup -q -n %{_name}-%{version}

%build
phpize
%configure \
	--enable-eaccelerator=shared \
		--with-eaccelerator-shared-memory \
		--with-eaccelerator-sessions \
		--with-eaccelerator-content-caching \
		--with-eaccelerator-userid=http \
		--with-php-config=%{_bindir}/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{extensionsdir},%{_bindir},%{_sysconfdir}/conf.d,/var/cache/%{_name}}

install ./modules/eaccelerator.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_name}.ini

install -d $RPM_BUILD_ROOT/home/services/httpd/html/eaccelerator
cp -a doc/php/* $RPM_BUILD_ROOT/home/services/httpd/html/eaccelerator

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_name}.ini
%attr(755,root,root) %{extensionsdir}/eaccelerator.so
%attr(755,root,root) %{_bindir}/encoder.php
%attr(770,root,http) /var/cache/%{_name}

%files webinterface
%defattr(644,root,root,755)
/home/services/httpd/html/eaccelerator
