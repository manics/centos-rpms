Name:           omero-dependencies
Version:        0.1
Release:        1%{?dist}
Summary:        Metapackage for OMERO runtime dependencies
License:        GPLv3
URL:            http://www.openmicroscopy.org/

Requires:       java7 >= 1:1.7.0

Requires:       ice >= 3.4
Requires:       ice-java >= 3.4
Requires:       ice-python >= 3.4
#Requires:       ice-servers >= 3.4

Requires:       python >= 2.6
# If pytables 2.4 is required then it will also require numpy and
# numexpr >= 1.4.1, though rpm/yum should handle this automatically.
Requires:       numpy >= 1.2.0
Requires:       scipy
Requires:       python-tables >= 2.1.0
Requires:       python-matplotlib 
Requires:       python-imaging

Requires:       postgresql-server >= 8.4
Requires:       postgresql >= 8.4



%description
This is a metapackage to automatically install the main dependencies required
to run OMERO. It does not install OMERO.

%files



%package devel
Summary:        Metapackage for OMERO development dependencies

%description devel
This is a metapackage to automatically install some of the main dependencies
required to contribute to the development of OMERO.

Requires:       omero-dependencies = %{version}-%{release}

Requires:       java7-devel >= 1:1.7.0
Requires:       ant
Requires:       gcc
Requires:       gcc-c++
Requires:       git

Requires:       ice-devel >= 3.4
Requires:       ice-java-devel >= 3.4
Requires:       ice-python-devel >= 3.4
#Requires:       ice-servers-devel >= 3.4

%files devel


%changelog
* Wed Mar 20 2013 Simon Li <spli@dundee.ac.uk> - 3.4.2-18a
- Initial attempt at a metapackage to install OMERO dependencies on CentOS 6.3
