#Module-Specific definitions
%define mod_name mod_activex_filter
%define mod_conf A17_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module that filter ActiveX on a proxy
Name:		apache-%{mod_name}
Version:	0.2b
Release:	%mkrel 10
Group:		System/Servers
License:	Apache License
URL:		http://brice.free.fr
Source0:	mod_activex_%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_activex_0.2-apx1.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Requires:	apache-mod_proxy
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
It's only a simple hack of mod_case_filter to get a way to filter
ActiveX on a proxy. Actualy, the only way to filter ActiveX if
your proxy is unable to do it is to use a TIS module chained with
your proxy. But the TIS is only capable of doing HTTP/1.0. If you
need real performances, you'll want to use HTTP/1.1.

%prep

%setup -q -n mod_activex_0.2
%patch0 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
mv activex_filter/mod_activex_filter.c .
%{_sbindir}/apxs -c mod_activex_filter.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
