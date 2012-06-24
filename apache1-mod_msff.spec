%define		mod_name	msff
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Microsoft Free Fridays: reject MSIE on Friday
Summary(pl):	Modu� do apache: Wolne Pi�tki Microsoftu: odrzuca MSIE w pi�tki
Name:		apache-mod_%{mod_name}
Version:	0.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://unlikely.org/mike/hacks/mod_%{mod_name}.c
# Source0-md5:	28bf69adb4beb41d82f16c2cc2e9d656
URL:		http://davenet.userland.com/2001/06/13
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Requires(post,preun):	%{apxs}
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

%description
mod_msff.c: Microsoft Free Fridays: reject MSIE on Friday.

More info: http://davenet.userland.com/2001/06/13

%description -l pl
Modu� do serwera Apache zabraniaj�cy w pi�tki dost�pu do serwera
przegl�darkom Microsoftu, pomagaj�cy zarz�dowi tej firmy w pe�nej
realizacji Wolnych Pi�tk�w (czyli dni lu�niejszych, w kt�rych _nawet_
mo�na przyj�� do pracy w d�insach :-))))).

Wi�cej informacji: http://davenet.userland.com/2001/06/13

%prep
%setup -q -T -c
cp %{SOURCE0} .

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

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

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*
