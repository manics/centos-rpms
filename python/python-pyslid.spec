%define pyname pyslid
%define pyversion 0.0.2
%define githash 63d49e9

Summary: Protein Subcellular Location Image Database for OMERO
Name: python-%{pyname}
# Experimental with custom modfications, so use a low version for now
Version: 0.0.2
Release: 2
# Source archive created with
# $ python setup.py sdist
# $ mv dist/pyslid-0.0.2.tar.gz dist/pyslid-0.0.2-`git describe --always`.tar.gz
Source0: %{pyname}-%{pyversion}-%{githash}.tar.gz
License: GPLv3
Group: Development/Libraries
BuildArch: noarch
Vendor: Robert F. Murphy <murphy@cmu.edu>
Url: http://murphylab.web.cmu.edu/software/

Requires: omero-server >= 4.4.7

Requires: numpy >= 1.4.1
Requires: scipy >= 0.7.2
Requires: python-PySLIC = 0.6.1

%description
Protein Subcellular Location Image Database for OMERO

This is a forked version with additional bug fixes and workarounds.

%prep
%setup -n %{pyname}-%{pyversion}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)


%changelog

* Wed Jun 12 2013 Simon Li <spli@dundee.ac.uk> - 0.0.2-2
- Fix order of parameters passed to getPlane in feature calculation
- Use conn.SERVICE_OPTS in QueryService calls
- Built from https://github.com/manics/pyslid/tree/63d49e94591d6711301e2963735a843b704b6324

* Tue Jun 04 2013 Simon Li <spli@dundee.ac.uk> - 0.0.2-1
- Additional workarounds for problems with the pyslid scale parameter
- Built from https://github.com/manics/pyslid/tree/9edbcc5b0acc33adfeb43c5c29e29bf36f46d793

* Thu Apr 25 2013 Simon Li <spli@dundee.ac.uk> - 0.0.1-1
- Built from https://github.com/manics/pyslid/tree/38ea5ba4c3f8e7c90a0bf002b7bbce3200a66bed

