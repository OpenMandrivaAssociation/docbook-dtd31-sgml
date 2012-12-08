%define name docbook-dtd31-sgml
%define version 1.0
%define release %mkrel 21
%define dtdver 3.1
%define mltyp sgml
%define sgmlbase %{_datadir}/sgml

Name:		%{name}
Version:	%{version}
Release:	%{release}
Group       	: Publishing

Summary     	: SGML document type definition for DocBook %{dtdver}

License   	: Artistic
URL         	: http://www.oasis-open.org/docbook/

Provides        : docbook-dtd-sgml
Requires(postun)	: sgml-common
Requires(post)	: sgml-common
BuildRequires: 	dos2unix

BuildRoot   	: %{_tmppath}/%{name}-%{version}-buildroot

# Zip file downloadable at http://www.oasis-open.org/docbook/sgml/%{dtdver}/
Source0		: docbk31.tar.bz2 
Patch0          : %{name}-%{version}.catalog.patch
BuildArch	: noarch  

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is SGML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.

%prep
%setup -q
%patch0 -p1 

%build

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT%{sgmlbase}/docbook/sgml-dtd-%{dtdver}
mkdir -p $DESTDIR
dos2unix *.txt
install *.dcl $DESTDIR
install docbook.cat $DESTDIR/catalog
install *.dtd $DESTDIR
install *.mod $DESTDIR
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sgml
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/catalog

%post
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
if [ -e %{sgmlbase}/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/openjade/catalog
fi

if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/dsssl-stylesheets/catalog
fi

%postun
# Do not remove if upgrade
if [ "$1" = "0" -a -x %{_bindir}/xmlcatalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

  # The following lines are for the case in which the style sheets
  # were not uninstalled because there is still another DTD
  if [ -e  %{sgmlbase}/openjade/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
  		  %{sgmlbase}/openjade/catalog
  fi

  if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
      %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/docbook/dsssl-stylesheets/catalog
  fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0644,root,root,0755)
%doc *.txt ChangeLog
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
%ghost %config(noreplace) %{_sysconfdir}/sgml/catalog
%{sgmlbase}/docbook/sgml-dtd-%{dtdver}



%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-19mdv2011.0
+ Revision: 663801
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-18mdv2011.0
+ Revision: 604800
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-17mdv2010.1
+ Revision: 520685
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-16mdv2010.0
+ Revision: 413363
- rebuild

* Sat Mar 21 2009 Funda Wang <fwang@mandriva.org> 1.0-15mdv2009.1
+ Revision: 359883
- bunzip patch

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.0-15mdv2009.0
+ Revision: 220669
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0-14mdv2008.1
+ Revision: 149187
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Jun 26 2007 Adam Williamson <awilliamson@mandriva.org> 1.0-13mdv2008.0
+ Revision: 44224
- rearrange spec, update requires, rebuild for 2008
- Import docbook-dtd31-sgml



 
* Tue Jun  6 2006 Camille Begnis <camille@mandriva.com> 1.0-12mdv2007.0
- builrequires dos2unix

* Mon Jun  5 2006 Camille Begnis <camille@mandriva.com> 1.0-11mdv2007.0
- rebuild
- use mkrel
- dos2unix text files

* Mon May 16 2005 Camille Begnis <camille@mandriva.com> 1.0-10mdk
- rebuild

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-9mdk
- Fix uninstall when xmlcatalog is no longer present 

* Mon Jul 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-8mdk
- Add some ghost/config files to package
- Fix upgrade
- Use more macros

* Mon May  5 2003  <camille@ke.mandrakesoft.com> 1.0-7mdk
- rebuild

* Tue Mar 21 2002 Camille Begnis <camille@mandrakesoft.com> 1.0-6mdk
- remove old {openjadever} not used anymore (Thanks fcrozat)

* Thu Jan 24 2002 Camille Begnis <camille@mandrakesoft.com> 1.0-5mdk
- use xmlcatalog from libxml-utils instead of install-catalog

* Mon Jun 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0-4mdk
- Merge patches from Abel Cheung:
- s/Copyright/License/
- Simplify %%files
- Source0 is not downloadable itself, it's just a re-compressed archive
- Corrected file permissions
- Removed useless variable
- More macros
- Rearrange BuildArch to bottom, no idea why source and patch refuses to be
  removed otherwise
* Tue Mar 13 2001 Camille Begnis <camille@mandrakesoft.com> 1.0-3mdk
- Redirect install-catalog output to /dev/null

* Thu Oct 19 2000 Camille Begnis <camille@mandrakesoft.com> 1.0-2mdk
- put DTD version in %%{dtdver}

* Wed Aug 23 2000 Camille Begnis <camille@mandrakesoft.com> 1.0-1mdk
- adapt spec from Eric Bischoff <ebisch@cybercable.tm.fr>
- Obsoletes docbook
- Pre-LSB compliance
