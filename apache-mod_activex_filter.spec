#Module-Specific definitions
%define mod_name mod_activex_filter
%define mod_conf A17_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module that filter ActiveX on a proxy
Name:		apache-%{mod_name}
Version:	0.2b
Release:	17
Epoch:		1
Group:		System/Servers
License:	Apache License
URL:		http://brice.free.fr
Source0:	mod_activex_%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_activex_0.2-apx1.diff
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file

Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_proxy

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
apxs -c mod_activex_filter.c

%install
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

%files
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-15mdv2012.0
+ Revision: 772546
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-14
+ Revision: 678248
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-13mdv2011.0
+ Revision: 587906
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-12mdv2010.1
+ Revision: 516031
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-11mdv2010.0
+ Revision: 406513
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-10mdv2009.1
+ Revision: 325514
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-9mdv2009.0
+ Revision: 234607
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-8mdv2009.0
+ Revision: 215519
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-7mdv2008.1
+ Revision: 181661
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-6mdv2008.0
+ Revision: 82506
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-5mdv2008.0
+ Revision: 65614
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2b-4mdv2007.1
+ Revision: 140601
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-3mdv2007.1
+ Revision: 79304
- Import apache-mod_activex_filter

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-3mdv2007.0
- rebuild

* Thu Dec 15 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.2b-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.2b-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com>  2.0.54_0.2b-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2b-5mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2b-4mdk
- fix %%post and %%postun to prevent double restarts

* Fri Feb 25 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_0.2b-3mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2b-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.2b-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.2b-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.2b-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.2b-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.2b-1mdk
- built for apache 2.0.49

* Tue Mar 30 2004 Michael Scherer <misc@mandrake.org> 2.0.48_0.2b-2mdk
- enhance Summary

