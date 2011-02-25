%define major     21
%define libname   %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Name:           djvulibre
Version:        3.5.22
Release:        %mkrel 5
Summary:        DjVu viewers, encoders and utilities
License:        GPLv2+
Group:          Publishing
URL:            http://djvu.sourceforge.net/
Source0:        http://download.sourceforge.net/djvu/%{name}-%{version}.tar.gz
Patch0:		djvulibre-3.5.2-str-fmt.patch
Patch1:		djvulibre-3.5.2-fix-link.patch
BuildRequires:  imagemagick
BuildRequires:  qt3-devel
BuildRequires:  libxt-devel
BuildRequires:  xdg-utils
BuildRequires:  tiff-devel
BuildRequires:  gnome-mime-data
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

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
- a standalone DjVu viewer based on the Qt library. 
- A browser plugin that works with most Unix browsers.
- A full-fledged wavelet-based compressor for pictures. 
- A simple compressor for bitonal (black and white) scanned pages. 
- A compressor for palettized images (a la GIF/PNG). 
- A set of utilities to manipulate and assemble DjVu images and documents. 
- A set of decoders to convert DjVu to a number of other formats. 
- An up-to-date version of the C++ DjVu Reference Library.

%package -n %{libname}
Summary:        DjVulibre library
Group:          System/Libraries

%description -n %{libname}
Djvulibre shared libraries.

%package -n %{develname}
Summary:        DjVulibre development files
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
Provides:       djvulibre-devel = %{version}-%{release}
Obsoletes:      %{mklibname %{name} 15 -d}

%description -n %{develname}
DjVulibre development files.

%package browser-plugin
Summary:        DjVulibre browser plugin
Group:          Publishing
Requires:       %{name} = %{version}-%{release}

%description browser-plugin
A browser plugin that works with most Unix browsers.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
export QTDIR=%qt3dir
export QT_LIBS=-lqt-mt
export QT_CFLAGS=-I%{qt3include}
%configure2_5x \
    --prefix=%_prefix \
    --enable-djview \
    --enable-xmltools \
    --with-qt \
    --enable-threads \
    --enable-debug \
    --enable-i18n \
    --enable-desktopfiles \
    --with-tiff

%make depend
%make

%install
rm -rf %{buildroot}
%makeinstall_std
# Quick fix to stop ldconfig from complaining
find %{buildroot}%{_libdir} -name "*.so*" -exec chmod 755 {} \;
# Quick cleanup of the docs
rm -rf doc/CVS 2>/dev/null || :

# conflicts with djview4
rm -f %buildroot%{_bindir}/djview %buildroot%{_mandir}/man1/djview.1*

mkdir -p %{buildroot}%{_libdir}/mozilla/plugins
mv %{buildroot}%{_libdir}/netscape/plugins/nsdejavu.so \
        %{buildroot}%{_libdir}/mozilla/plugins/
ln -s %{_libdir}/mozilla/plugins/nsdejavu.so \
         %{buildroot}%{_libdir}/netscape/plugins/nsdejavu.so

#gw don't rely on xdg-utils but install them manually
mkdir -p %buildroot%_datadir/applications
mv %buildroot%_datadir/djvu/djview3/desktop/djvulibre-djview3.desktop %buildroot%_datadir/applications/
mkdir -p %buildroot%_iconsdir/hicolor/32x32/apps
mv %buildroot%_datadir/djvu/djview3/desktop/hi32-djview3.png %buildroot%_iconsdir/hicolor/32x32/apps/djvulibre-djview3.png
mkdir -p %buildroot%_iconsdir/hicolor/32x32/mimetypes
mv %buildroot%_datadir/djvu/osi/desktop/hi32-djvu.png %buildroot%_iconsdir/hicolor/32x32/mimetypes/image-vnd.djvu.mime.png
mkdir -p %buildroot%_iconsdir/hicolor/22x22/mimetypes
mv %buildroot%_datadir/djvu/osi/desktop/hi22-djvu.png %buildroot%_iconsdir/hicolor/22x22/mimetypes/image-vnd.djvu.mime.png
mkdir -p %buildroot%_iconsdir/hicolor/48x48/mimetypes
mv %buildroot%_datadir/djvu/osi/desktop/hi48-djvu.png %buildroot%_iconsdir/hicolor/48x48/mimetypes/image-vnd.djvu.mime.png
mkdir -p %buildroot%_datadir/mime/packages
mv %buildroot%_datadir/djvu/osi/desktop/djvulibre-mime.xml %buildroot%_datadir/mime/packages


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Qt" \
  --add-category="Graphics" \
  --add-category="Viewer" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README COPYRIGHT COPYING INSTALL NEWS TODO doc
%{_bindir}/any2djvu
%{_bindir}/bzz
%{_bindir}/c44
%{_bindir}/cjb2
%{_bindir}/cpaldjvu
%{_bindir}/csepdjvu
%{_bindir}/ddjvu
%{_bindir}/djview3
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
%{_mandir}/man1/djview3.1*
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
%{_datadir}/applications/djvulibre-djview3.desktop
%_datadir/mime/packages/*.xml
%_datadir/icons/hicolor/32x32/apps/*
%{_iconsdir}/hicolor/22x22/mimetypes/*
%{_iconsdir}/hicolor/32x32/mimetypes/*
%{_iconsdir}/hicolor/48x48/mimetypes/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%attr(0755,root,root) %{_libdir}/*.la
%{_includedir}/libdjvu
%_libdir/pkgconfig/*.pc

%files browser-plugin
%defattr(-, root, root)
%{_libdir}/netscape/plugins/nsdejavu.so
%{_libdir}/mozilla/plugins/nsdejavu.so
%{_mandir}/man1/nsdejavu.1*

