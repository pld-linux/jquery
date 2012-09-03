# TODO
# - drop the addon plugins, say in 2.0?

# jquery plugin version
%define		field_ver	0.9.2

Summary:	jQuery JavaScript Library
Summary(pl.UTF-8):	Biblioteka JavaScriptu jQuery
Name:		jquery
Version:	1.8.1
Release:	1
License:	MIT
Group:		Applications/WWW
Source0:	http://code.jquery.com/%{name}-%{version}.min.js
# Source0-md5:	a9a0cc296e96bbeaa0f82498e2da0917
Source10:	http://code.jquery.com/%{name}-%{version}.js
# Source10-md5:	a7c6119e69953bd4f9cafc3910fe4eb7
Source11:	apache.conf
Source12:	lighttpd.conf
Source1:	http://plugins.jquery.com/files/%{name}.field.%{field_ver}.zip
# Source1-md5:	1bd5d766f79034904a07ddbbab5cb27a
Source3:	http://marcgrabanski.com/code/ui-datepicker/core/core.ui.datepicker.zip
# Source3-md5:	46967b9c5ee626697b977e2909fb00b1
Source4:	http://www.mikage.to/jquery/%{name}.history.js
# Source4-md5:	d035c1f13f1795e6d739cd045d6dfb9b
URL:		http://www.jquery.com/
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
Requires:	webserver(alias)
Suggests:	webserver(access)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{name}

%description
jQuery is a fast, concise, JavaScript Library that simplifies how you
traverse HTML documents, handle events, perform animations, and add
Ajax interactions to your web pages.

jQuery is designed to change the way that you write JavaScript.

This package also provides following jQuery plugins:
- jquery.field v%{field_ver},

%description -l pl.UTF-8
jQuery to szybka biblioteka Javascriptu upraszczająca przetwarzanie
dokumentów HTML, obsługę zdarzeń, animacji oraz akcji AJAX w serwisach
internetowych.

jQuery został zaprojektowany tak, by zmienić sposób pisania kodu w
JavaScripcie.

Pakiet ten dostarcza także dodatkowe wtyczki jQuery:
- jquery.field v%{field_ver},

%prep
%setup -qcT -a1 -a3
cp -p %{SOURCE4} .
cp -p %{SOURCE0} jquery.min.js
cp -p %{SOURCE10} jquery.src.js
%undos -f js

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}/plugins
# core
cp -p jquery.min.js $RPM_BUILD_ROOT%{_appdir}/jquery-%{version}.min.js
cp -p jquery.src.js $RPM_BUILD_ROOT%{_appdir}/jquery-%{version}.js
mver=%(echo %{version} | cut -d. -f1,2)
ln -s jquery-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/jquery-$mver.js
ln -s jquery-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/jquery.min.js
ln -s jquery-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/jquery.js

# plugins

# http://plugins.jquery.com/project/field, MIT/GPL v0.7
cp -p jquery.field.min.js $RPM_BUILD_ROOT%{_appdir}/plugins/field.js

# http://www.mikage.to/jquery/jquery_history.html, MIT
cp -p jquery.history.js $RPM_BUILD_ROOT%{_appdir}/plugins/history.js

# http://marcgrabanski.com/pages/code/jquery-ui-datepicker, MIT/GPL v3.4.3
cp -p ui.datepicker.{js,css} $RPM_BUILD_ROOT%{_appdir}/plugins

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc field.plugin.htm
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/*.js
%dir %{_appdir}/plugins
%{_appdir}/plugins/*.js
%{_appdir}/plugins/*.css
