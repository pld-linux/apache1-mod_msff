%define		mod_name	msff
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Microsoft Free Fridays: reject MSIE on Friday
Summary(pl):	Modu³ do apache: Wolne Pi±tki Microsofta: odrzuca MSIE w pi±tki
Name:		apache-mod_%{mod_name}
Version:	0.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://unlikely.org/mike/hacks/mod_%{mod_name}.c
URL:		http://davenet.userland.com/2001/06/13
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

%description
mod_msff.c: Microsoft Free Fridays: reject MSIE on Friday.
More info: http://davenet.userland.com/2001/06/13

%description -l pl
Modu³ do serwera Apache zabraniaj±cy w pi±tki dostêpu do
serwera  przegl±darkom Microsofta,  pomagaj±cy zarz±dowi
tej firmy w pe³nej realizacji Wolnych Pi±tków [czyli dni
lu¼niejszych, w których _nawet_ mo¿na przyj¶æ do pracy w
d¿insach :-))))] 
Wiêcej: http://davenet.userland.com/2001/06/13

%prep
%setup -q -T -c
cp %{SOURCE0} .

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
