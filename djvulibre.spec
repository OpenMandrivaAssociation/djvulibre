%define _mozillapath	%{_libdir}/mozilla/plugins

%define name		djvulibre
%define release		%mkrel 1
%define version		3.5.19

%define major		15
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:		DjVu viewers, encoders and utilities
Name:			%{name}
Version:		%{version}
Release:		%{release}
# homepage doesn't link to the most recent files
URL:			http://sourceforge.net/project/showfiles.php?group_id=32953
License:		GPL
Group:			Publishing
Source:			http://download.sourceforge.net/djvu/%{name}-%{version}.tar.bz2

BuildRequires:		imagemagick
BuildRequires:		qt3-devel
BuildRequires:		libxt-devel
BuildRequires:		xdg-utils
BuildRequires:		gnome-mime-data
BuildRequires:		kdelibs-common
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot

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
Summary:		DjVulibre library
Group:			System/Libraries

%description -n %{libname}
Djvulibre shared libraries.

%package -n %{develname}
Summary:		DjVulibre development files
Group:			Development/Other
Requires:		%{libname} = %{version}-%{release}
Provides:		libdjvulibre-devel = %{version}-%{release}
Provides:		%{name}-devel = %{version}-%{release}
Obsoletes:		%mklibname %{name} 15 -d

%description -n %{develname}
DjVulibre development files.

%package browser-plugin
Summary:		DjVulibre browser plugin
Group:			Publishing
Requires:		%{name} = %{version}

%description browser-plugin
A browser plugin that works with most Unix browsers.

%prep
%setup -q

%build
export QT_CFLAGS="-I%{_prefix}/lib/qt3/include"
export QT_LIBS="-L%{_prefix}/lib/qt3/%{_lib} -lqt-mt"
export MOC="L%{_prefix}/lib/qt3/bin/moc"
%configure2_5x --enable-shared \
	   --enable-djview \
	   --enable-xmltools \
	   --enable-threads \
	   --enable-debug \
	   --enable-i18n \
	   --enable-desktopfiles
#	   --enable-rpo \


# Don't use %%make here
%make depend
%make

%install
rm -rf %{buildroot}
%makeinstall_std
# Quick fix to stop ldconfig from complaining
find %{buildroot}%{_libdir} -name "*.so*" -exec chmod 755 {} \;
# Quick cleanup of the docs
rm -rf doc/CVS 2>/dev/null || :
# fix wrong-script-end-of-line-encoding 
find %{buildroot}%{_datadir}/djvu/osi -type f -name '*.xml' -exec \
%{__perl} -pi -e 's|\r||g' {} ';'

mkdir -p %{buildroot}%{_mozillapath}
mv %{buildroot}%{_libdir}/netscape/plugins/nsdejavu.so \
	%{buildroot}%{_mozillapath}/
ln -s %{_mozillapath}/nsdejavu.so \
         %{buildroot}%{_libdir}/netscape/plugins/nsdejavu.so

# remove original menu (sorry)
#rm -rf %{buildroot}%{_menudir}/*

#gw don't rely on xdg-utils but install them manually
mkdir %buildroot%_datadir/applications
mv %buildroot%_datadir/djvu/djview3/desktop/djvulibre-djview3.desktop %buildroot%_datadir/applications/
mkdir -p %buildroot%_datadir/icons/hicolor/32x32/apps
mv %buildroot%_datadir/djvu/djview3/desktop/hi32-djview3.png %buildroot%_datadir/icons/hicolor/32x32/apps/djvulibre-djview3.png
mkdir -p %buildroot%_datadir/icons/hicolor/32x32/mimetypes
mv %buildroot%_datadir/djvu/osi/desktop/hi32-djvu.png %buildroot%_datadir/icons/hicolor/32x32/mimetypes/image-vnd.djvu.mime.png
mkdir -p %buildroot%_datadir/icons/hicolor/22x22/mimetypes
mv %buildroot%_datadir/djvu/osi/desktop/hi22-djvu.png %buildroot%_datadir/icons/hicolor/22x22/mimetypes/image-vnd.djvu.mime.png
mkdir -p %buildroot%_datadir/icons/hicolor/48x48/mimetypes
mv %buildroot%_datadir/djvu/osi/desktop/hi48-djvu.png %buildroot%_datadir/icons/hicolor/48x48/mimetypes/image-vnd.djvu.mime.png
mkdir -p %buildroot%_datadir/mime/packages
mv %buildroot%_datadir/djvu/osi/desktop/djvulibre-mime.xml %buildroot%_datadir/mime/packages


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Qt" \
  --add-category="Graphics" \
  --add-category="Viewer" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%post
%{update_menus}
%update_icon_cache hicolor
%{update_mime_database}
%{update_desktop_database}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%postun
%{clean_menus}
%clean_icon_cache hicolor
%{clean_mime_database}
%{clean_desktop_database}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README COPYRIGHT COPYING INSTALL NEWS TODO doc
%{_bindir}/*
%{_datadir}/djvu
%{_mandir}/man1/*
%{_datadir}/applications/djvulibre-djview3.desktop
%_datadir/mime/packages/*.xml
%_datadir/icons/hicolor/32x32/apps/*
%{_iconsdir}/hicolor/22x22/mimetypes/*
%{_iconsdir}/hicolor/32x32/mimetypes/*
%{_iconsdir}/hicolor/48x48/mimetypes/*

%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.*a
%{_includedir}/libdjvu
%_libdir/pkgconfig/*.pc

%files browser-plugin
%defattr(-, root, root)
%{_libdir}/netscape/plugins/nsdejavu.so
%{_mozillapath}/nsdejavu.so
