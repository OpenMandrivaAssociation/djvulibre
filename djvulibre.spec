%define major	21
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	DjVu encoders and utilities
Name:		djvulibre
Version:	3.5.25.3
Release:	5
License:	GPLv2+
Group:		Publishing
Url:		http://djvu.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/djvu/DjVuLibre/3.5.25/%{name}-%{version}.tar.gz
#Patch1:		djvulibre-3.5.2-fix-link.patch
Patch2:		djvulibre-3.5.22-cdefs.patch

BuildRequires:	gnome-mime-data
BuildRequires:	imagemagick
BuildRequires:	xdg-utils
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(xt)

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

%package -n %{devname}
Summary:	DjVulibre development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
DjVulibre development files.

%prep
%setup -qn %{name}-3.5.25
%apply_patches

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
%doc README COPYRIGHT COPYING INSTALL NEWS doc
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
%{_libdir}/libdjvulibre.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/libdjvu
%{_libdir}/pkgconfig/*.pc

