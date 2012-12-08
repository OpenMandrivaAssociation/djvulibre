%define major		21
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		djvulibre
Version:	3.5.24
Release:	4
Summary:	DjVu encoders and utilities
License:	GPLv2+
Group:		Publishing
URL:		http://djvu.sourceforge.net/
Source0:	http://download.sourceforge.net/djvu/%{name}-%{version}.tar.gz
Patch1:		djvulibre-3.5.2-fix-link.patch
Patch2:		djvulibre-3.5.22-cdefs.patch
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(xt)
BuildRequires:	xdg-utils
BuildRequires:	tiff-devel
BuildRequires:	gnome-mime-data

%description
DjVu is a web-centric format and software platform for distributing 
documents and images.  DjVu content downloads faster, displays and 
renders faster, looks nicer on a screen, and consume less client 
resources than competing formats. DjVu was originally developed at AT&T 
Labs-Research by Leon Bottou, Yann LeCun, Patrick Haffner, and many 
others.  In March 2000, AT&T sold DjVu to LizardTech Inc. who now 
distributes Windows/Mac plug-ins, and commercial encoders (mostly on 
Windows)

In an effort to promote DjVu as a Web standard, the LizardTech 
management was enlightened enough to release the reference 
implementation of DjVu under the GNU GPL in October 2000.  DjVuLibre 
(which means free DjVu), is an enhanced version of that code maintained 
by the original inventors of DjVu. It is compatible with version 3.5 of 
the LizardTech DjVu software suite.

DjVulibre-3.5 contains:
- A full-fledged wavelet-based compressor for pictures. 
- A simple compressor for bitonal (black and white) scanned pages. 
- A compressor for palettized images (a la GIF/PNG). 
- A set of utilities to manipulate and assemble DjVu images and documents. 
- A set of decoders to convert DjVu to a number of other formats. 
- An up-to-date version of the C++ DjVu Reference Library.

%package -n %{libname}
Summary:	DjVulibre library
Group:		System/Libraries

%description -n %{libname}
Djvulibre shared libraries.

%package -n %{develname}
Summary:	DjVulibre development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	djvulibre-devel = %{version}-%{release}
Obsoletes:	%{mklibname djvulibre 15 -d} < 3.5.24

%description -n %{develname}
DjVulibre development files.

%prep
%setup -q
%patch1 -p0
%patch2 -p1

%build
%configure2_5x \
    --prefix=%{_prefix} \
    --enable-xmltools \
    --enable-threads \
    --enable-debug \
    --enable-i18n \
    --enable-desktopfiles \
    --with-tiff \
    --disable-static

%make depend
%make

%install
%makeinstall_std
# Quick fix to stop ldconfig from complaining
find %{buildroot}%{_libdir} -name "*.so*" -exec chmod 755 {} \;
# Quick cleanup of the docs
rm -rf doc/CVS 2>/dev/null || :
rm -rf doc/minilisp/.cvsignore 2 > /dev/null || :

#gw don't rely on xdg-utils but install them manually
mkdir -p %{buildroot}%{_iconsdir}/hicolor/32x32/mimetypes
mv %{buildroot}%{_datadir}/djvu/osi/desktop/hi32-djvu.png %{buildroot}%{_iconsdir}/hicolor/32x32/mimetypes/image-vnd.djvu.mime.png
mkdir -p %{buildroot}%{_iconsdir}/hicolor/22x22/mimetypes
mv %{buildroot}%{_datadir}/djvu/osi/desktop/hi22-djvu.png %{buildroot}%{_iconsdir}/hicolor/22x22/mimetypes/image-vnd.djvu.mime.png
mkdir -p %{buildroot}%{_iconsdir}/hicolor/48x48/mimetypes
mv %{buildroot}%{_datadir}/djvu/osi/desktop/hi48-djvu.png %{buildroot}%{_iconsdir}/hicolor/48x48/mimetypes/image-vnd.djvu.mime.png
mkdir -p %{buildroot}%{_datadir}/mime/packages
mv %{buildroot}%{_datadir}/djvu/osi/desktop/djvulibre-mime.xml %{buildroot}%{_datadir}/mime/packages

%files
%doc README COPYRIGHT COPYING INSTALL NEWS TODO doc
%{_bindir}/any2djvu
%{_bindir}/bzz
%{_bindir}/c44
%{_bindir}/cjb2
%{_bindir}/cpaldjvu
%{_bindir}/csepdjvu
%{_bindir}/ddjvu
%{_bindir}/djvm
%{_bindir}/djvmcvt
%{_bindir}/djvudigital
%{_bindir}/djvudump
%{_bindir}/djvuextract
%{_bindir}/djvumake
%{_bindir}/djvups
%{_bindir}/djvused
%{_bindir}/djvuserve
%{_bindir}/djvutoxml
%{_bindir}/djvutxt
%{_bindir}/djvuxmlparser
%{_datadir}/djvu
%{_mandir}/man1/any2djvu.1*
%{_mandir}/man1/bzz.1*
%{_mandir}/man1/c44.1*
%{_mandir}/man1/cjb2.1*
%{_mandir}/man1/cpaldjvu.1*
%{_mandir}/man1/csepdjvu.1*
%{_mandir}/man1/ddjvu.1*
%{_mandir}/man1/djvm.1*
%{_mandir}/man1/djvmcvt.1*
%{_mandir}/man1/djvu.1*
%{_mandir}/man1/djvudigital.1*
%{_mandir}/man1/djvudump.1*
%{_mandir}/man1/djvuextract.1*
%{_mandir}/man1/djvumake.1*
%{_mandir}/man1/djvups.1*
%{_mandir}/man1/djvused.1*
%{_mandir}/man1/djvuserve.1*
%{_mandir}/man1/djvutoxml.1*
%{_mandir}/man1/djvutxt.1*
%{_mandir}/man1/djvuxml.1*
%{_mandir}/man1/djvuxmlparser.1*
%{_datadir}/mime/packages/*.xml
%{_iconsdir}/hicolor/22x22/mimetypes/*
%{_iconsdir}/hicolor/32x32/mimetypes/*
%{_iconsdir}/hicolor/48x48/mimetypes/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_includedir}/libdjvu
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Dec 22 2011 Oden Eriksson <oeriksson@mandriva.com> 3.5.24-2
+ Revision: 744432
- various fixes
- rebuilt against libtiff.so.5

* Mon Jun 27 2011 Tomas Kindl <supp@mandriva.org> 3.5.24-1
+ Revision: 687520
- update to 3.5.24

* Tue May 03 2011 Funda Wang <fwang@mandriva.org> 3.5.23-3
+ Revision: 664124
- fix build with gcc 4.6

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Mon Feb 28 2011 Tomas Kindl <supp@mandriva.org> 3.5.23-2
+ Revision: 641042
- bump release
- minor cleanup, remove obsolete patch

* Sat Feb 26 2011 Tomas Kindl <supp@mandriva.org> 3.5.23-1
+ Revision: 639823
- bump to 3.5.23, drop QT3 viewer and deps

* Fri Feb 25 2011 Tomas Kindl <supp@mandriva.org> 3.5.22-5
+ Revision: 639806
-fix for #62253

* Mon Dec 20 2010 Funda Wang <fwang@mandriva.org> 3.5.22-4mdv2011.0
+ Revision: 623257
- fix link
- fix link
- update file list

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 3.5.22-3mdv2010.1
+ Revision: 488747
- rebuilt against libjpeg v8

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 3.5.22-2mdv2010.0
+ Revision: 416612
- rebuilt against libjpeg v7

* Thu Jun 25 2009 Frederik Himpe <fhimpe@mandriva.org> 3.5.22-1mdv2010.0
+ Revision: 389198
- Update to new version 3.5.22

* Mon Feb 09 2009 Helio Chissini de Castro <helio@mandriva.com> 3.5.21-3mdv2009.1
+ Revision: 338866
- Get rid of kde3 dependency

* Sun Sep 07 2008 Frederik Himpe <fhimpe@mandriva.org> 3.5.21-1mdv2009.0
+ Revision: 282351
- Update to new version (new major)
- Fix Source0 to use gz tarball
- Better URL

* Fri Jun 20 2008 Pixel <pixel@mandriva.com> 3.5.20-5mdv2009.0
+ Revision: 227421
- rebuild for fixed %%update_icon_cache/%%clean_icon_cache/%%post_install_gconf_schemas
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 3.5.20-4mdv2009.0
+ Revision: 220637
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - fixes bug #40569
    - enable browser plugin

* Tue Mar 11 2008 Erwan Velu <erwan@mandriva.org> 3.5.20-2mdv2008.1
+ Revision: 186732
- Rebuild

* Wed Jan 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 3.5.20-1mdv2008.1
+ Revision: 140272
- new version
- new license policy

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.5.19-3mdv2008.0
+ Revision: 89602
- rebuild

* Fri Aug 17 2007 David Walluck <walluck@mandriva.org> 3.5.19-2mdv2008.0
+ Revision: 64686
- disable browser plugin (obsoleted by djview4)
- fix file conflicts with djview4

* Tue Jul 17 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 3.5.19-1mdv2008.0
+ Revision: 52878
- new version
- new devel library policy
- drop old menu style
- drop X-MandrivaLinux category from desktop file
- add more provides


* Thu Mar 01 2007 Götz Waschk <waschk@mandriva.org> 3.5.18-2mdv2007.0
+ Revision: 130390
- remove libdjvulibre.so from the plugin package
- Import djvulibre

* Sun Feb 04 2007 G�tz Waschk <waschk@mandriva.org> 3.5.18-1mdv2007.1
- fix mime, icons and desktop entry
- fix buildrequires
- New version 3.5.18

* Wed Sep 06 2006 Nicolas L�cureuil <neoclust@mandriva.org> 3.5.17-5mdv2007.0
- XDG

* Wed Jun 07 2006 Götz Waschk <waschk@mandriva.org> 3.5.17-4mdv2007.0
- fix buildrequires

* Sun May 28 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 3.5.17-3mdk
- add BuildRequires: kdelibs-common

* Wed May 24 2006 Götz Waschk <waschk@mandriva.org> 3.5.17-2mdk
- fix devel provides

* Wed May 24 2006 Götz Waschk <waschk@mandriva.org> 3.5.17-1mdk
- update file list
- disable -frepo
- New release 3.5.17

* Fri Mar 03 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 3.5.16-3mdk
- add BuildRequires: gnome-mime-data

* Tue Nov 22 2005 Laurent MONTEL <lmontel@mandriva.com> 3.5.16-2
- Remove conflict

* Wed Nov 02 2005 David Walluck <walluck@mandriva.org> 3.5.16-1mdk
- 3.5.16
- add menu icons

* Thu Mar 17 2005 David Walluck <walluck@mandrake.com> 3.5.14-4mdk
- fix ldconfig location

* Wed Mar 16 2005 David Walluck <walluck@mandrake.com> 3.5.14-3mdk
- fix summary-ended-with-dot
- fix wrong-script-end-of-line-encoding 
- replace hardcoded paths with the correct macro-based paths

* Wed Mar 16 2005 David Walluck <walluck@mandrake.com> 3.5.14-2mdk
- rebuild to fix unresolved symbols
- use %%configure macro

* Fri Aug 27 2004 Lenny Cartier <lenny@mandrakesoft.com> 3.5.14-1mdk
- 3.5.14

* Fri May 28 2004 Lenny Cartier <lenny@mandrakesoft.com> 3.5.13-2mdk
- browser plugin is back
- add link to mozilla plugin path

* Tue May 25 2004 Lenny Cartier <lenny@mandrakesoft.com> 3.5.13-1mdk
- 3.5.13

* Thu May 13 2004 Lenny Cartier <lenny@mandrakesoft.com> 3.5.12-2mdk
- rebuild
- remove explicit lib dependency

