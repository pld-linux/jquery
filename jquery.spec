Summary:	jQuery JavaScript Library
Name:		jquery
Version:	1.2.6
Release:	1
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
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}

%description
jQuery is a fast, concise, JavaScript Library that simplifies how you
traverse HTML documents, handle events, perform animations, and add
Ajax interactions to your web pages.

jQuery is designed to change the way that you write JavaScript.

%prep
%setup -qc -a3

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

# http://marcgrabanski.com/code/ui-datepicker/, MIT/GPL v3.4.3
cp -a ui.datepicker.{js,css} $RPM_BUILD_ROOT%{_appdir}/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_appdir}
%{_appdir}/*.js
%dir %{_appdir}/plugins
%{_appdir}/plugins/*.js
%{_appdir}/plugins/*.css
