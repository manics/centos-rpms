Name:           omero-dependencies
Version:        0.1
Release:        1%{?dist}
Summary:        Metapackage for OMERO dependencies
#Source:
License:        GPLv3
URL:            http://www.openmicroscopy.org/
#Source0:        

Requires:       java-1.7.0-openjdk  

Requires:       ice = 3.4
Requires:       ice-java = 3.4
Requires:       ice-python = 3.4
Requires:       ice-servers = 3.4

Requires:       python >= 2.6
# pytables 2.4 requires numpy and numexpr >= 1.4.1
Requires:       numpy >= 1.4.1
Requires:       tables >= 2.4.0
Requires:       python-matplotlib 
Requires:       python-imaging

Requires:       postgresql-server >= 8.4
Requires:       postgresql >= 8.4


# numpy:
BuildRequires:  gcc python-devel rpm-build
# Also brings in cloog-ppl cpp glibc-devel glibc-headers kernel-headers libgomp mpfr ppl
# numpy also requires:
Requires:       atlas
Requires:       libgfortran

#python setup.py bdist_rpm
# requires:
# rpm-build
# Brings in elfutils elfutils-libs gdb patch
# install rpm, then test: import numpy, numpy.test()

# numexpr required by tables
# http://code.google.com/p/numexpr/
#python setup.py bdist_rpm

# tables:
Requires:       Cython
Requires:       hdf5 >= 1.8.4
Requires:       numexpr >= 1.4.1
Requires:       lzo
Requires:       bzip2
#(lzo* and bzip2* are optional)
#rpm -ivh http://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
BuildRequires:  hdf5-devel lzo-devel bzip2-devel
# also brings in lzo-minilzo
#python setup.py bdist_rpm



%description
This is a metapackage to automatically install the dependencies required to
run OMERO.server. It does not install OMERO.


#%prep
#%setup -q


#%build
#%configure
#make %{?_smp_mflags}


#%install
#rm -rf $RPM_BUILD_ROOT
#%make_install


%files
%doc



%changelog
