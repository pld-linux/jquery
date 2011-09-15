# TODO
# - drop the addon plugins, say in 1.7?

# jquery plugin version
%define		field_ver	0.9.2
%define		form_ver	2.18

Summary:	jQuery JavaScript Library
Summary(pl.UTF-8):	Biblioteka JavaScriptu jQuery
Name:		jquery
Version:	1.6.4
Release:	1
License:	MIT / GPL
Group:		Applications/WWW
Source0:	http://code.jquery.com/%{name}-%{version}.min.js
# Source0-md5:	9118381924c51c89d9414a311ec9c97f
Source10:	http://code.jquery.com/%{name}-%{version}.js
# Source10-md5:	c677462551f4cc0f2af192497b50f3f5
Source1:	http://plugins.jquery.com/files/%{name}.field.%{field_ver}.zip
# Source1-md5:	1bd5d766f79034904a07ddbbab5cb27a
Source2:	http://plugins.jquery.com/files/%{name}.form.js_0.txt
# Source2-md5:	8720eac9985a6b33e4f4087f2e01ce23
Source3:	http://marcgrabanski.com/code/ui-datepicker/core/core.ui.datepicker.zip
# Source3-md5:	46967b9c5ee626697b977e2909fb00b1
Source4:	http://www.mikage.to/jquery/%{name}.history.js
# Source4-md5:	d035c1f13f1795e6d739cd045d6dfb9b
Patch0:		%{name}.history.konqueror.patch
URL:		http://www.jquery.com/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
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

%description -l pl.UTF-8
jQuery to szybka biblioteka Javascriptu upraszczająca przetwarzanie
dokumentów HTML, obsługę zdarzeń, animacji oraz akcji AJAX w serwisach
internetowych.

jQuery został zaprojektowany tak, by zmienić sposób pisania kodu w
JavaScripcie.

Pakiet ten dostarcza także dodatkowe wtyczki jQuery:
- jquery.field v%{field_ver},
- jquery.form v%{form_ver}

%prep
%setup -qcT -a1 -a3
cp -a %{SOURCE4} .
%patch0 -p1

# apache1/apache2 conf
cat > apache.conf <<'EOF'
Alias /js/jquery %{_appdir}
# legacy
Alias /jquery %{_appdir}
<Directory %{_appdir}>
	Allow from all
	Options +FollowSymLinks
</Directory>
EOF

# lighttpd conf
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/js/jquery" => "%{_appdir}",
	# legacy
    "/jquery" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}/plugins
# core
cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_appdir}/jquery-%{version}.min.js
cp -p %{SOURCE10} $RPM_BUILD_ROOT%{_appdir}/jquery-%{version}.src.js
mver=%(echo %{version} | cut -d. -f1,2)
ln -s jquery-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/jquery-$mver.js
ln -s jquery-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/jquery.js

# plugins

# http://plugins.jquery.com/project/field, MIT/GPL v0.7
cp -p jquery.field.min.js $RPM_BUILD_ROOT%{_appdir}/plugins/field.js

# http://plugins.jquery.com/project/form, MIT/GPL v2.04
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_appdir}/plugins/form.js

# http://www.mikage.to/jquery/jquery_history.html, MIT
cp -p jquery.history.js $RPM_BUILD_ROOT%{_appdir}/plugins/history.js

# http://marcgrabanski.com/pages/code/jquery-ui-datepicker, MIT/GPL v3.4.3
cp -p ui.datepicker.{js,css} $RPM_BUILD_ROOT%{_appdir}/plugins

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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
