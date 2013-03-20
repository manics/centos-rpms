# Get Python and Ruby packages into sitearch (see Fedora Wiki)
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?ruby_vendorarchdir: %define ruby_vendorarchdir %(ruby -rrbconfig -e 'puts Config::CONFIG["vendorarchdir"]' 2> /dev/null)}

%global php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global systemddir /lib/systemd/system

Name:           ice
Version:        3.4.2
Release:        18%{?dist}
Summary:        ZeroC Object-Oriented middleware

Group:          System Environment/Libraries
License:        GPLv2 with exceptions
URL:            http://www.zeroc.com/
Source0:        http://zeroc.com/download/Ice/3.4/Ice-%{version}.tar.gz
# Man pages courtesy of Francisco Moya's Debian packages
Source1:        ice-3.4.2-man-pages.tar.gz
Source2:        icegridgui
Source3:        IceGridAdmin.desktop
Source4:        Ice-README.Fedora
Source5:        glacier2router.conf
Source6:        glacier2router.service
Source7:        icegridnode.conf
Source8:        icegridnode.service
Source9:        icegridregistry.conf
Source10:       icegridregistry.service
Source11:       ice.ini
Source12:       ice.pth
# Remove reference to Windows L&F
Patch0:         ice-3.4.2-jgoodies.patch
# fix gcc46 issue
Patch1:         ice-3.4.2-gcc46.patch
# Add support for the s390/s390x architecture
Patch2:         ice-3.4.2-s390.patch
# don't build demo/test
# TODO: should we keep it or not ?
# significantly reduce compile time but shipping demos could be useful
Patch3:         ice-3.4.2-dont-build-demo-test.patch
# disable the CSharp interface
Patch4:         ice-3.4.2-no-mono.patch
# fix java 7 compilation
Patch5:         ice-3.4.2-java7.patch
# fix php 5.4 compilation (from upstream)
Patch6:         ice-3.4.2-php54.patch
# fixed slice2cpp float literals generation fixed upstream in next release RHBZ #812156
# http://www.zeroc.com/forums/bug-reports/5431-default-vaules-slice.html
Patch7:         ice-3.4.2-slice2cpp.patch
# See: http://www.zeroc.com/forums/patches/5647-patch-compiling-ice-clang-gcc4-7-a.html
Patch8:         ice-3.4.2-gcc47.patch
# ARM
Patch9:         ice-3.4.2-arm.patch
# libdb4
#Patch10:        ice-3.4.2-libdb4.patch

# Ice doesn't officially support ppc64 at all
ExcludeArch:    ppc64

# mono exists only on these
%ifarch %{ix86} x86_64 ppc ppc64 ia64 %{arm} sparcv9 alpha s390x
%global with_mono 1
%endif

# Some file suffixes we need to grab the right stuff for the file lists
%define soversion 34

#BuildRequires: libdb4-cxx-devel, expat-devel, openssl-devel, bzip2-devel
BuildRequires: db4-devel, expat-devel, openssl-devel, bzip2-devel
#BuildRequires: ant, ant-nodeps, jpackage-utils, libdb4-java
BuildRequires: ant, ant-nodeps, jpackage-utils, db4-java
BuildRequires: php, php-devel
#BuildRequires: ruby, ruby(abi) = 1.9.1, ruby-devel
BuildRequires: ruby, ruby-devel
BuildRequires: python-devel
%if 0%{?with_mono}
BuildRequires: mono-core, mono-devel
%endif
BuildRequires: libmcpp-devel >= 2.7.2
BuildRequires: dos2unix
#BuildRequires: java-devel >= 1:1.6.0
BuildRequires: java7-devel >= 1:1.7.0
BuildRequires: jgoodies-forms jgoodies-looks
BuildRequires: /usr/bin/convert
BuildRequires: desktop-file-utils

%description
Ice is a modern alternative to object middleware such as CORBA or
COM/DCOM/COM+.  It is easy to learn, yet provides a powerful network
infrastructure for demanding technical applications. It features an
object-oriented specification language, easy to use C++, C#, Java,
Python, Ruby, PHP, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic
transport plug-ins, TCP/IP and UDP/IP support, SSL-based security, a
firewall solution, and much more.

# All of the other Ice packages also get built by this SRPM.

%package servers
Summary: ICE systemd services
Group: Development/Tools
Requires: ice%{?_isa} = %{version}-%{release}
# Requirements for the users
Requires(pre): shadow-utils%{?isa}
# Requirements for the systemd services
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description servers
Ice services (systemd)

%package devel
Summary: C++ tools for developing Ice applications
Group: Development/Tools
Provides: ice-c++-devel = %{version}-%{release}
Obsoletes: ice-c++-devel < %{version}-%{release}
Requires: ice%{?isa} = %{version}-%{release}
%description devel
Tools for developing Ice applications in C++.

%package java
Summary: Java runtime for Ice applications
Group: System Environment/Libraries
Requires: java >= 1:1.6.0
Requires: ice%{?_isa} = %{version}-%{release}
#Requires: libdb4-java%{?_isa}
Requires: db4-java%{?_isa}
%description java
The Ice runtime for Java

%package java-devel
Summary: Java tools for developing Ice Applications
Group: Development/Tools
Requires: ice-java%{?_isa} = %{version}-%{release}
%description java-devel
Tools for developing Ice applications in Java.

%package -n icegrid-gui
Summary: IceGrid Admin Tool
Group: Development/Tools
Requires: ice-java%{?_isa} = %{version}-%{release}
Requires: jgoodies-forms, jgoodies-looks
Requires: jpackage-utils
%description -n icegrid-gui
Graphical administration tool for IceGrid

%if 0%{?with_mono}
%package csharp
Summary: C# runtime for Ice applications
Group: System Environment/Libraries
Provides: ice-dotnet = %{version}-%{release}
Obsoletes: ice-dotnet < %{version}-%{release}
Requires: ice%{?_isa} = %{version}-%{release}
Requires: mono-core%{?_isa} >= 1.2.2
%description csharp
The Ice runtime for C#

%package csharp-devel
Summary: C# tools for developping Ice applications
Group: Development/Tools
Requires: ice-csharp%{?_isa} = %{version}-%{release}
%description csharp-devel
Tools for developing Ice applications in C#.
%endif

%package ruby
Summary: Ruby runtime for Ice applications
Group: Development/Tools
Requires: ice%{?_isa} = %{version}-%{release}
#Requires: ruby(abi) = 1.9.1
%description ruby
The Ice runtime for Ruby applications.

%package ruby-devel
Summary: Ruby tools for developping Ice applications
Group: Development/Tools
Requires: ice-ruby%{?_isa} = %{version}-%{release}
%description ruby-devel
Tools for developing Ice applications in Ruby.

%package python
Summary: Python runtime for Ice applications
Group: Development/Tools
Requires: ice%{?_isa} = %{version}-%{release}
Requires: python >= 2.3.4
%description python
The Ice runtime for Python applications.

%package python-devel
Summary: Python tools for developping Ice applications
Group: Development/Tools
Requires: ice-python%{?_isa} = %{version}-%{release}
%description python-devel
Tools for developing Ice applications in Python.

%package php
Summary: PHP runtime for developping Ice applications
Group: System Environment/Libraries
Requires: ice%{?_isa} = %{version}-%{release}
%if %{?php_zend_api:1}%{!?php_zend_api:0}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
%else
Requires:       php-api = %{php_apiver}
%endif
%description php
The Ice runtime for PHP applications.

%package php-devel
Summary: PHP tools for developping Ice applications
Group: Development/Tools
Requires: ice-php%{?_isa} = %{version}-%{release}
%description php-devel
Tools for developing Ice applications in PHP.

%prep
%setup -q -n Ice-%{version}
%patch0 -p1 -b .jgoodies
%patch1 -p1 -b .gcc46
%patch2 -p1 -b .s390
%patch3 -p1 -b .demo
%if ! 0%{?with_mono}
%patch4 -p1 -b .no-mono
%endif
%patch5 -p1 -b .java7
%patch6 -p1 -b .php54
%patch7 -p1 -b .slice2cpp
%patch8 -p1 -b .gcc47
%patch9 -p1 -b .arm
#patch10 -p1 -b .libdb4

tar xf %{SOURCE1}
rm -f ice-3.4.2-man-pages/slice2docbook.1


%build
# Set the CLASSPATH correctly for the Java compile
export CLASSPATH=`build-classpath db jgoodies-forms jgoodies-looks`

# Compile the main Ice runtime
make CXXFLAGS="%{optflags} -fPIC -fpermissive" CFLAGS="%{optflags} -fPIC -fpermissive" embedded_runpath_prefix="" libsubdir=%{_lib}

# Rebuild the Java ImportKey class
pushd cpp/src/ca
rm *.class
javac ImportKey.java
popd

# Create the IceGrid icon
pushd java
cd resources/icons
convert icegrid.ico temp.png
mv temp-8.png icegrid.png
rm temp*.png
popd

%install
mkdir -p %{buildroot}
# Do the basic "make install"
make prefix=%{buildroot} GACINSTALL=yes GAC_ROOT=%{buildroot}%{_prefix}/lib embedded_runpath_prefix="" libsubdir=%{_lib} install

## install java bindings in the right place
mkdir -p %{buildroot}%{_javadir}
mv %{buildroot}/lib/ant-ice.jar %{buildroot}%{_javadir}/ant-ice-%{version}.jar
ln -s ant-ice-%{version}.jar %{buildroot}%{_javadir}/ant-ice.jar
mv %{buildroot}/lib/Ice.jar %{buildroot}%{_javadir}/Ice-%{version}.jar
ln -s Ice-%{version}.jar %{buildroot}%{_javadir}/Ice.jar
mv %{buildroot}/lib/Freeze.jar %{buildroot}%{_javadir}/Freeze-%{version}.jar
ln -s Freeze-%{version}.jar %{buildroot}%{_javadir}/Freeze.jar


## install IceGrid GUI in the right place
mkdir -p %{buildroot}%{_datadir}/Ice-%{version}
mv %{buildroot}/lib/IceGridGUI.jar %{buildroot}%{_datadir}/Ice-%{version}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
cp -p java/resources/icons/icegrid.png \
   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
mkdir -p %{buildroot}%{_bindir}
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_bindir}
sed -i -e "s#DIR#%{_datadir}/Ice-%{version}#" $RPM_BUILD_ROOT%{_bindir}/icegridgui

%if 0%{?rhel}
desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications \
        --vendor=zeroc \
        %{SOURCE3}
%else
desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications \
        %{SOURCE3}
%endif

# Move other rpm-specific files into the right place (README, service stuff)
mkdir -p %{buildroot}%{_defaultdocdir}/Ice-%{version}
cp -p %{SOURCE4} %{buildroot}/%{_defaultdocdir}/Ice-%{version}/README.Fedora

# "make install" assumes it's going into a directory under /opt.
# Move things to where they should be in an RPM setting (adapted from
# the original ZeroC srpm).
install -p -m0755 -t %{buildroot}%{_bindir} %{buildroot}/bin/*
rm -rf %{buildroot}/bin
mkdir -p %{buildroot}%{_includedir}
mv %{buildroot}/include/* %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
# There are a couple of files that end up installed in /lib, not %%{_libdir},
# so we try this move too.
%if 0%{?with_mono}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -p -m0644 -t %{buildroot}%{_libdir}/pkgconfig \
         %{buildroot}/lib/pkgconfig/*.pc
%endif
install -p -m0755 -t %{buildroot}%{_libdir}/ \
         %{buildroot}/%{_lib}/*.so*
# Move the ImportKey.class file
mkdir -p %{buildroot}%{_datadir}/Ice-%{version}
mv %{buildroot}/lib/ImportKey.class %{buildroot}%{_datadir}/Ice-%{version}
rm -rf %{buildroot}/%{_lib} %{buildroot}/lib

mkdir -p %{buildroot}%{_defaultdocdir}/Ice-%{version}
mv %{buildroot}/help/IceGridAdmin %{buildroot}%{_defaultdocdir}/Ice-%{version}

# Copy the man pages into the correct directory
mkdir -p %{buildroot}%{_mandir}/man1
cp -p ice-3.4.2-man-pages/*.1 %{buildroot}%{_mandir}/man1

# Fix the encoding and line-endings of all the IceGridAdmin documentation files
pushd %{buildroot}%{_defaultdocdir}/Ice-%{version}/IceGridAdmin
chmod a-x *
for f in *.js *.css *.js;
do
    dos2unix $f
done
for f in helpman_topicinit.js icegridadmin_navigation.js \
    IceGridAdmin_popup_html.js zoom_pageinfo.js highlight.js;
do
    iconv -f ISO88591 -t UTF8 $f -o $f.tmp
    mv $f.tmp $f
done
popd

## Mono bindings
%if 0%{?with_mono}
# .NET spec files (for csharp-devel) -- convert the paths
for f in IceGrid Glacier2 IceBox Ice IceStorm IcePatch2;
do
    mv %{buildroot}%{_bindir}/$f.xml \
       %{buildroot}%{_prefix}/lib/mono/gac/$f/%{version}.*/
    # fix xml files permissions
    chmod 0644 %{buildroot}%{_prefix}/lib/mono/gac/$f/%{version}.*/*.xml
done
%else
# clean some files when building without mono
rm %{buildroot}%{_bindir}/slice2cs
rm %{buildroot}%{_mandir}/man1/iceboxnet.exe.1*
rm %{buildroot}%{_mandir}/man1/slice2cs.1*
%endif

## install PHP bindings in the right place
install -D -p -m0644 %{SOURCE11} \
           %{buildroot}%{_sysconfdir}/php.d/%{name}.ini
install -D -p -m0755 %{buildroot}/php/IcePHP.so \
        %{buildroot}%{php_extdir}/IcePHP.so
rm -f %{buildroot}/php/IcePHP.so
mkdir -p %{buildroot}%{_datadir}/php
mv %{buildroot}/php/* %{buildroot}%{_datadir}/php


## install Python and Ruby bindings in the right place
# remove shebangs from python/ruby modules
for f in %{buildroot}/python/Ice.py %{buildroot}/ruby/*.rb;
do
    grep -v '/usr/bin/env' $f > $f.tmp
    mv $f.tmp $f
done
mkdir -p %{buildroot}%{ruby_vendorarchdir}
mv %{buildroot}/ruby/* %{buildroot}%{ruby_vendorarchdir}
mkdir -p %{buildroot}%{python_sitearch}/Ice
mv %{buildroot}/python/* %{buildroot}%{python_sitearch}/Ice
cp -p %{SOURCE12} %{buildroot}%{python_sitearch}
# fix permissions for Python/Ruby C extensions libraries
chmod 0755 %{buildroot}%{python_sitearch}/Ice/IcePy.so*
chmod 0755 %{buildroot}%{ruby_vendorarchdir}/IceRuby.so*

mkdir -p %{buildroot}%{_datadir}/Ice-%{version}
mv %{buildroot}/config/* %{buildroot}%{_datadir}/Ice-%{version}
mv %{buildroot}/slice %{buildroot}%{_datadir}/Ice-%{version}
# Somehow, some files under "slice" end up with executable permissions -- ??
find %{buildroot}%{_datadir}/Ice-%{version} -name "*.ice" | xargs chmod a-x


# Move license files into the documentation directory
mkdir -p %{buildroot}%{_defaultdocdir}/Ice-%{version}
mv %{buildroot}/ICE_LICENSE %{buildroot}%{_defaultdocdir}/Ice-%{version}/ICE_LICENSE
mv %{buildroot}/LICENSE %{buildroot}%{_defaultdocdir}/Ice-%{version}/LICENSE
# Copy in the other files too
cp CHANGES RELEASE_NOTES  %{buildroot}%{_defaultdocdir}/Ice-%{version}/

## install systemd services configuration
mkdir -p %{buildroot}%{systemddir}
mkdir -p %{buildroot}%{_sysconfdir}
## glacier2router
install -p -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}
install -p -m0644 %{SOURCE6} %{buildroot}%{systemddir}
## icegridnode
install -p -m0644 %{SOURCE7} %{buildroot}%{_sysconfdir}
install -p -m0644 %{SOURCE8} %{buildroot}%{systemddir}
## icegridregistry
install -p -m0644 %{SOURCE9} %{buildroot}%{_sysconfdir}
install -p -m0644 %{SOURCE10} %{buildroot}%{systemddir}
mkdir -p %{buildroot}%{_localstatedir}/lib/icegrid


%check
# Minimum check for php extension
LD_LIBRARY_PATH=%{buildroot}%{_libdir} php -n -d extension_dir=%{buildroot}%{php_extdir} -d extension=IcePHP.so -m | grep ice


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post servers
%systemd_post icegridregistry.service
%systemd_post icegridnode.service
%systemd_post glacier2router.service

%preun servers
%systemd_preun icegridregistry.service
%systemd_preun icegridnode.service
%systemd_preun glacier2router.service

%postun servers
%systemd_postun icegridregistry.service
%systemd_postun icegridnode.service
%systemd_postun glacier2router.service

%files
%defattr(-,root,root,-)
%{_defaultdocdir}/Ice-%{version}
%doc %{_mandir}/man1/dumpdb.1.gz
%doc %{_mandir}/man1/glacier2router.1.gz
%doc %{_mandir}/man1/icebox.1.gz
%doc %{_mandir}/man1/iceboxadmin.1.gz
%doc %{_mandir}/man1/iceca.1.gz
%doc %{_mandir}/man1/icegridadmin.1.gz
%doc %{_mandir}/man1/icegridnode.1.gz
%doc %{_mandir}/man1/icegridregistry.1.gz
%doc %{_mandir}/man1/icepatch2calc.1.gz
%doc %{_mandir}/man1/icepatch2client.1.gz
%doc %{_mandir}/man1/icepatch2server.1.gz
%doc %{_mandir}/man1/icestormadmin.1.gz
%doc %{_mandir}/man1/slice2html.1.gz
%doc %{_mandir}/man1/transformdb.1.gz
%{_bindir}/dumpdb
%{_bindir}/glacier2router
%{_bindir}/icebox
%{_bindir}/iceboxadmin
%{_bindir}/iceca
%{_bindir}/icegridadmin
%{_bindir}/icegridnode
%{_bindir}/icegridregistry
%{_bindir}/icepatch2calc
%{_bindir}/icepatch2client
%{_bindir}/icepatch2server
%{_bindir}/icestormadmin
%{_bindir}/icestormmigrate
%{_bindir}/slice2html
%{_bindir}/transformdb
%{_libdir}/lib*.so.%{version}
%{_libdir}/lib*.so.%{soversion}
%{_datadir}/Ice-%{version}
# Exclude the stuff that's in IceGrid
%exclude %{_defaultdocdir}/Ice-%{version}/IceGridAdmin
%exclude %{_datadir}/Ice-%{version}/IceGridGUI.jar

%files servers
%defattr(-,root,root,-)
%{systemddir}/icegridregistry.service
%{systemddir}/icegridnode.service
%{systemddir}/glacier2router.service
%config(noreplace) %{_sysconfdir}/icegridregistry.conf
%config(noreplace) %{_sysconfdir}/icegridnode.conf
%config(noreplace) %{_sysconfdir}/glacier2router.conf
%dir %{_localstatedir}/lib/icegrid

%files devel
%defattr(-,root,root,-)
%doc %{_mandir}/man1/slice2cpp.1.gz
%doc %{_mandir}/man1/slice2freeze.1.gz
%{_bindir}/slice2cpp
%{_bindir}/slice2freeze
%{_includedir}/Freeze
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil
%{_includedir}/IceXML
%{_includedir}/Slice
%{_libdir}/lib*.so

%files java
%defattr(-,root,root,-)
%{_javadir}/*.jar

%files -n icegrid-gui
%defattr(-,root,root,-)
%{_datadir}/Ice-%{version}/IceGridGUI.jar
%attr(755,root,root) %{_bindir}/icegridgui
%doc %{_mandir}/man1/icegridgui.1.gz
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/48x48/apps/icegrid.png
%doc %{_defaultdocdir}/Ice-%{version}/IceGridAdmin

%files java-devel
%defattr(-,root,root,-)
%doc %{_mandir}/man1/slice2java.1.gz
%doc %{_mandir}/man1/slice2freezej.1.gz
%{_bindir}/slice2java
%{_bindir}/slice2freezej
%{_javadir}/ant-ice-%{version}.jar
%{_javadir}/ant-ice.jar

%if 0%{?with_mono}
%files csharp
%defattr(-,root,root,-)
%{_prefix}/lib/mono/Glacier2/
%{_prefix}/lib/mono/Ice/
%{_prefix}/lib/mono/IceBox/
%{_prefix}/lib/mono/IceGrid/
%{_prefix}/lib/mono/IcePatch2/
%{_prefix}/lib/mono/IceStorm/
%{_prefix}/lib/mono/gac/Glacier2
%{_prefix}/lib/mono/gac/Ice
%{_prefix}/lib/mono/gac/IceBox
%{_prefix}/lib/mono/gac/IceGrid
%{_prefix}/lib/mono/gac/IcePatch2
%{_prefix}/lib/mono/gac/IceStorm
%{_prefix}/lib/mono/gac/policy*
%{_bindir}/iceboxnet.exe
%doc %{_mandir}/man1/iceboxnet.exe.1.gz

%files csharp-devel
%defattr(-,root,root,-)
%doc %{_mandir}/man1/slice2cs.1.gz
%{_bindir}/slice2cs
%{_libdir}/pkgconfig/Glacier2.pc
%{_libdir}/pkgconfig/Ice.pc
%{_libdir}/pkgconfig/IceBox.pc
%{_libdir}/pkgconfig/IceGrid.pc
%{_libdir}/pkgconfig/IcePatch2.pc
%{_libdir}/pkgconfig/IceStorm.pc
%endif

%files python
%defattr(-,root,root,-)
%{python_sitearch}/Ice/
%{python_sitearch}/%{name}.pth

%files python-devel
%defattr(-,root,root,-)
%{_bindir}/slice2py
%doc %{_mandir}/man1/slice2py.1.gz

%files ruby
%defattr(-,root,root,-)
%{ruby_vendorarchdir}/*

%files ruby-devel
%defattr(-,root,root,-)
%{_bindir}/slice2rb
%doc %{_mandir}/man1/slice2rb.1.gz

%files php
%defattr(-,root,root,-)
%{php_extdir}/IcePHP.so
%{_datadir}/php/*
%config(noreplace) %{_sysconfdir}/php.d/ice.ini

%files php-devel
%defattr(-,root,root,-)
%{_bindir}/slice2php
%{_mandir}/man1/slice2php.1.gz


%changelog
* Wed Oct 17 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-18
- use macroized systemd directives (closes RHBZ #850152)

* Sat Aug 04 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-17
- fix package requirements to follow the db4 -> libdb4 rename

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.4.2-15
- Add patch to fix build on ARM

* Tue May 29 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-14
- refresh all patches

* Tue May 22 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-13
- fix slice2cpp patch

* Mon Apr 16 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-12
- fix float literals generation (RHBZ #812156)
- fix systemd services (RHBZ #789712)

* Fri Mar 16 2012 Tom Callaway <spot@fedoraproject.org> 3.4.2-11
- fix issue where upCast is used before being declared with gcc 4.7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-10
- Rebuilt for c++ ABI breakage
 
* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> 3.4.2-9
- Resolves rhbz#791372
- Patch from Omair Majid <omajid@redhat.com> to remove explicit Java 6 req.

* Tue Feb 07 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.2-8
- Rebuilt for Ruby 1.9.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-6
- move services from upstart to systemd
- fix build with java7
- fix build with php54 (patch contributed by Remi Collet)
- spec cleaning

* Tue Nov 29 2011 Christian Krause <chkr@fedoraproject.org> - 3.4.2-5
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Mon Oct 31 2011 Dan Horák <dan[at]danny.cz> - 3.4.2-4
- fix libsubdir path on non-x86 64-bit arches
- fix build without Mono

* Wed Aug 31 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-3
- remove arch-dependency on java requires

* Sun Aug 28 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-2
- ice-java: bump java requires epoch

* Fri Aug 05 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.2-1
- upstream 3.4.2
- refresh gcc 4.6/jgoodies patch
- retrieved updated debian man pages
- fix permissions
- use %%{?_isa} for arch-dependent requires
- spec cleanup

* Tue Mar 22 2011 Dan Horák <dan[at]danny.cz> - 3.4.1-2
- conditionalize CSharp/Mono support

* Sat Feb 12 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 3.4.1-1
- upstream 3.4.1
- fix gcc46 build issue
- some spec cleaning and patches revamping (dropped: java, openssl)
- updated man pages from Francisco Moya Debian's package

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jun 20 2010 Dan Horák <dan[at]danny.cz> - 3.4.0-2
- add support for the s390/s390x architectures

* Fri Mar 12 2010 Mary Ellen Foster <mefoster at gmail.com> - 3.4.0-1
- Update to new upstream release -- complete release notes at
  http://www.zeroc.com/download/Ice/3.4/Ice-3.4.0-RELEASE_NOTES
- Of particular note:
  - There is a completely new AMI facility for C++, C#, Java, and Python
  - The PHP support has changed significantly (note the new ice-php-devel
    package).
  - The slice2docbook command is no longer included
  - The Java2 mapping has been removed -- Java5 only

* Tue Feb 16 2010 Mary Ellen Foster <mefoster at gmail.com> - 3.3.1-7
- Add a couple of changes to allow the RPM to be rebuilt on RHEL
  (bugs 511068, 565411)

* Mon Feb  1 2010 Mary Ellen Foster <mefoster at gmail.com> - 3.3.1-6
- Fix the user name in the server scripts (bug 557411)

* Sat Aug 22 2009 Tomas Mraz <tmraz@redhat.com> - 3.3.1-5
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 3.3.1-3
- rebuild for new PHP 5.3.0 ABI (20090626) + ice-php53.patch
- add PHP ABI check
- use php_extdir

* Wed Jul  8 2009 Mary Ellen Foster <mefoster at gmail.com> - 3.3.1-2
- Include upstream patches:
  - slice2html creates bad links
  - slice compilers abort on symlinks and double backslashes
  - random endpoint selection in .Net
  See http://www.zeroc.com/forums/patches/ for details

* Wed Mar 25 2009 Mary Ellen Foster <mefoster at gmail.com> - 3.3.1-1
- Update to new upstream 3.3.1 release
  - Includes all previous patches
  - Support for serializable Java and .NET types in your Slice definitions
  - Ability to use Ice for Java in an applet and to load IceSSL files, such
    as keystores, from class path resources
- Details at http://www.zeroc.com/download/Ice/3.3/Ice-3.3.1-RELEASE_NOTES

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Mary Ellen Foster <mefoster at gmail.com> - 3.3.0-13
- Explicitly BuildRequire OpenJDK to fix a build failure on rawhide
- Fix author name in previous change log
- No longer include ant.jar in the CLASSPATH for building (unnecessary)

* Fri Feb  6 2009 Mary Ellen Foster <mefoster at gmail.com> - 3.3.0-12
- Include Debian patch for GCC 4.4

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 3.3.0-11
- rebuild with new openssl

* Sat Jan 10 2009 Dennis Gilmore <dennis@ausil.us> - 3.3.0-10
- ExcludeArch sparc64 no mono there

* Thu Dec  4 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.3.0-9
- Rebuild for Python 2.6

* Thu Dec  4 2008 <mefoster at gmail.com> - 3.3.0-8
- Add all accumulated upstream patches

* Thu Dec  4 2008 <mefoster at gmail.com> - 3.3.0-7
- (Tiny) patch to support Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.3.0-6
- Rebuild for Python 2.6

* Tue Aug 12 2008 Mary Ellen Foster <mefoster at gmail.com> 3.3.0-5
- Explicitly create build root so it builds on F10
- Patch to build against DB4.7

* Wed Jul 30 2008 Mary Ellen Foster <mefoster at gmail.com> 3.3.0-4
- Re-add .pth file -- the alternative method involves editing auto-generated
  files that say "don't edit" and I don't want to break other parts of Ice

* Fri Jun 27 2008 Mary Ellen Foster <mefoster at gmail.com> 3.3.0-3
- Bump release to fix tag problem and bad date
- Add dist back to release field

* Wed Jun 25 2008 Mary Ellen Foster <mefoster at gmail.com> 3.3.0-2
- Add patch from ZeroC

* Mon Jun  9 2008 Mary Ellen Foster <mefoster at gmail.com> 3.3.0-1
- Update for 3.3 final
- Fix ppc64 issues with directories in Mono .pc files (I hope)
- Incorporate patches and man pages from Debian package

* Tue May 06 2008 Mary Ellen Foster <mefoster at gmail.com> 3.3-0.1.b
- Update for 3.3 beta prerelease
- Fix Python sitelib/sitearch issues

* Fri Feb 22 2008 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-17
- Improved, less invasive patch based on the Debian one

* Fri Feb 22 2008 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-16
- Add includes so that it compiles with GCC 4.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.2.1-15
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-14
- Version bump to rebuild because of changed OpenSSL in rawhide

* Tue Nov 20 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-13
- Enable the IceGrid GUI
- Fix a problem with Python on 64-bit systems (bz #392751)
- Incorporate one more Mono patch from ZeroC

* Tue Oct 30 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-12
- Put the slice2java classes into a .jar file instead of as bare classes
- Incorporate all Ice 3.2.1 patches from ZeroC
- Fix templates path in icegridregistry.conf

* Fri Sep  7 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-11
- Also add Obsoletes: for the old zeroc names
- Fix bad date in changelog

* Wed Aug 29 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-9
- Add "with exceptions" to license tag
- Minor typo corrections in README.Fedora
- Move ruby sitearch files out of an "Ice/" subdirectory so that they're
  actually useful

* Tue Aug 28 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-8
- Remove parallel make to see if that fixes build errors

* Mon Aug 27 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-7
- Fix over-zealous patch in csharp IceBox Makefile

* Mon Aug 27 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-6
- Put IcePy.so* into sitearch, not sitelib
- Use %%ifarch in python file list to avoid duplicate warnings
- Actually use gacutil for the Mono dlls instead of faking it

* Fri Aug 24 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-5
- Clean up packaging of icegridgui: it's a gui app, so we should treat it as
  such (NB: building this package is still disabled by default because it needs
  jgoodies)
- Actually create the working directory for the Ice services
- Remove redundant requires on java-devel and csharp-devel packages
- Fix file list for python package to own directories too
- Modified the README to accurately reflect what's in the Fedora package

* Thu Aug 23 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-4
- Whoops, ruby(abi) doesn't pull in ruby ...
- Redirect getent output to /dev/null
- Try again to remove execute permission on all *.ice files (????)
- Move ImportKey.class out of bin and into share (not sure what it does, but I'm
  pretty sure it doesn't belong in bin!)

* Wed Aug 22 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-3
- Changed BuildRequires on ruby to ruby(abi) = 1.8
- Fixed all dependencies between subpackages: everything requires the base
  package, and -devel packages should all require their corresponding non-devel
  package now
- Made ice-csharp require pkgconfig
- Modified the user/group creation process based on the wiki
- Removed ldconfig for ice-c++-devel subpackage
- Made the python_sitelib subdirectory owned by ice-python
- Removed executable permission on all files under slice (how did that happen?)
- Fixed typo on ice-csharp group
- Changed license tag to GPLv2
- Removed macros in changelog
- Set CFLAGS as well as CPPFLAGS for make so that building icecpp gets the
  correct flags too
- Renamed ice-c++-devel to ice-devel
- Added Provides: for ice-c++-devel and ice-dotnet for people moving from the
  ZeroC RPMs
- Also don't build "test" or "demo" for IceCS

* Sun Aug 18 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-2
- ExcludeArch ppc64
- Fix one more hard-coding problem for x86_64

* Thu Aug 16 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.1-1
- Update to 3.2.1

* Wed Aug  1 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.0-7
- Fixed arch-specific issues:
  - %%ifnarch ppc64 in a lot of places; it doesn't have db4-java or mono-core,
    so no Java or CSharp packages
  - Replaced one literal "lib" with %%{_lib}
- Added IceGrid registry patch from ZeroC forum
- Don't build "test" or "demo" subdirectories
- Use "/sbin/ldconfig" instead of %%{_sbindir} because that's /usr/sbin (also
  for other things like /sbin/service etc)
- Removed useless "dotnetversion" define (it's the same as "version")
- Remove executable bit on all "*.ice" files (it gets set somehow on a few)

* Tue Jul 31 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.0-6
- Updated to incorporate more suggestions from Mamoru Tasaka (sorry for the delay!)
- Include Java and C# stuff in the single SRPM (NB: they'll no longer be noarch)

* Mon Jul  9 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.0-5
- Updated following review comments from Mamoru Tasaka
- Renamed file to "ice.spec"
- Use %%{_libdir} instead of literal "lib"/"lib64" (not yet tested on 64-bit
  system)
- Changed "make" calls to use the correct compiler flags (including -fPIC)
- Changed "cp" to "cp -p" everywhere for timestamps
- Use more macros instead of hard-coded directory names:
  %%_prefix, %%_libdir, %%_initrddir, %%_localstatedir, %%_sbindir
- Un-excluded *.pyo files

* Wed Jun 13 2007 Mary Ellen foster <mefoster at gmail.com> 3.2.0-4
- Removed cruft so that it no longer tries to build Java stuff (whoops)

* Wed Apr 18 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.0-3
- Use RPM macros instead of /etc and /usr/bin (Thanks to Peter Lemenkov)
- Suggestions from ZeroC forum (http://zeroc.com/forums/showthread.php?t=3095):
  - Use Python site-packages directory
  - Create "iceuser" user
  - Split /etc/init.d services into a separate sub-package
- Follow guidelines from Fedora wiki about packaging Ruby
  - Use Ruby site-arch directory
  - Depend on ruby(abi)
- Make sure to compile all Java files with -source 1.4 -target 1.4

* Wed Apr 11 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.0-2
- Remove "assert" in Java classes for compilation with Java 1.4

* Fri Mar 30 2007 Mary Ellen Foster <mefoster at gmail.com> 3.2.0-1
- Initial spec, based on spec distributed by ZeroC
