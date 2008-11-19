Summary:	jQuery JavaScript Library
Name:		jquery
Version:	1.2.6
Release:	3
License:	MIT / GPL
Group:		Applications/WWW
Source0:	http://jqueryjs.googlecode.com/files/%{name}-%{version}-release.zip
# Source0-md5:	e52c549f2865700c13cb81325a49a314
Source1:	http://plugins.jquery.com/files/%{name}.field.js_4.txt
# Source1-md5:	0266a3bef437a17a44cdcad1aa3908de
Source2:	http://jqueryjs.googlecode.com/svn/trunk/plugins/form/%{name}.form.js
# Source2-md5:	a5f1e11a042a60bc1557a0c7460db46c
Source3:	http://marcgrabanski.com/code/ui-datepicker/core/core.ui.datepicker.zip
# Source3-md5:	46967b9c5ee626697b977e2909fb00b1
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

%prep
%setup -qc -a3

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
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_appdir}/plugins/field.js

# http://plugins.jquery.com/project/form, MIT/GPL v2.04
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_appdir}/plugins/form.js

# http://malsup.com/jquery/form/
# TODO

# http://marcgrabanski.com/code/ui-datepicker/, MIT/GPL v3.4.3
cp -a ui.datepicker.{js,css} $RPM_BUILD_ROOT%{_appdir}/plugins

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
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/*.js
%dir %{_appdir}/plugins
%{_appdir}/plugins/*.js
%{_appdir}/plugins/*.css
