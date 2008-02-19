Summary:	jQuery JavaScript Library
Name:		jquery
Version:	1.2.3
Release:	0.1
License:	MIT / GPL
Group:		Applications/WWW
Source0:	http://jqueryjs.googlecode.com/files/%{name}-%{version}-release.zip
# Source0-md5:	24ff20d524fa2affb1d6eb217797341c
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
%setup -qc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a dist/jquery.min.js $RPM_BUILD_ROOT%{_appdir}/jquery.js

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_appdir}
