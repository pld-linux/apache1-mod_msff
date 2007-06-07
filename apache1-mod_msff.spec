%define		mod_name	msff
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: Microsoft Free Fridays: reject MSIE on Friday
Summary(pl.UTF-8):	Moduł do apache: Wolne Piątki Microsoftu: odrzuca MSIE w piątki
Name:		apache1-mod_%{mod_name}
Version:	0.1
Release:	1.2
License:	GPL
Group:		Networking/Daemons
Source0:	http://unlikely.org/mike/hacks/mod_%{mod_name}.c
# Source0-md5:	28bf69adb4beb41d82f16c2cc2e9d656
URL:		http://davenet.userland.com/2001/06/13
BuildRequires:	apache1-apxs
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1 >= 1.3.33-2
Obsoletes:	apache-mod_msff <= 0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_msff.c: Microsoft Free Fridays: reject MSIE on Friday.

More info: <http://davenet.userland.com/2001/06/13>

%description -l pl.UTF-8
Moduł do serwera Apache zabraniający w piątki dostępu do serwera
przeglądarkom Microsoftu, pomagający zarządowi tej firmy w pełnej
realizacji Wolnych Piątków (czyli dni luźniejszych, w których _nawet_
można przyjść do pracy w dżinsach :-))))).

Więcej informacji: <http://davenet.userland.com/2001/06/13>

%prep
%setup -q -T -c
cp %{SOURCE0} .

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
