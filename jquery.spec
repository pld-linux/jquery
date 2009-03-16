#
# jquery plugins
%define		field_ver	0.9.2
%define		form_ver	2.18
#
Summary:	jQuery JavaScript Library
Summary(pl.UTF-8):	Biblioteka JavaScriptu jQuery
Name:		jquery
Version:	1.3.2
Release:	0.1
License:	MIT / GPL
Group:		Applications/WWW
Source0:	http://jqueryjs.googlecode.com/files/%{name}-%{version}-release.zip
# Source0-md5:	4ad8132094787af619df708dbf7f1880
Source1:	http://plugins.jquery.com/files/%{name}.field.%{field_ver}.zip
# Source1-md5:	1bd5d766f79034904a07ddbbab5cb27a
Source2:	http://plugins.jquery.com/files/%{name}.form.js_0.txt
# Source2-md5:	8720eac9985a6b33e4f4087f2e01ce23
URL:		http://jquery.com/
BuildRequires:	rpmbuild(macros) > 1.268
Requires:	webserver(access)
Requires:	webserver(alias)
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
- jquery.form v%{form_ver}

%description -l pl.UTF_8
jQuery to szybka biblioteka Javascriptu upraszczająca przetwarzanie
dokumentów HTML, obsługę zdarzeń, animacji oraz akcji AJAX w
serwisach internetowych.

jQuery został zaprojektowany tak, by zmienić sposób pisania kodu w
JavaScripcie.

Pakiet ten dostarcza także dodatkowe wtyczki jQuery:
- jquery.field v%{field_ver},
- jquery.form v%{form_ver}

%prep
%setup -qc -a1

# apache1/apache2 conf
cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# lighttpd conf
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}/plugins
# core
cp -a dist/jquery.min.js $RPM_BUILD_ROOT%{_appdir}/jquery.js

# plugins

# http://plugins.jquery.com/project/field, MIT/GPL v0.7
cp -a jquery.field.min.js $RPM_BUILD_ROOT%{_appdir}/plugins/field.js

# http://plugins.jquery.com/project/form, MIT/GPL v2.04
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_appdir}/plugins/form.js

# http://malsup.com/jquery/form/
# TODO

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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
