%define pyname pyslid
%define pyversion 0.0.2

Summary: Protein Subcellular Location Image Database for OMERO
Name: python-%{pyname}
# Experimental with custom modfications, so use a low version for now
Version: 0.0.1
Release: 1
Source0: %{pyname}-%{pyversion}.tar.gz
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

Built from
https://github.com/manics/pyslid/commit/38ea5ba4c3f8e7c90a0bf002b7bbce3200a66bed

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
