%define pyname PySLIC

Summary: Subcellular Location Image Classifier
Name: python-%{pyname}
Version: 0.6.1
Release: 1
Source0: %{pyname}-%{version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildArch: noarch
Vendor: Murphy Lab <murphy@cmu.edu>
Url: http://murphylab.cbi.cmu.edu/

BuildRequires: python-setuptools >= 0.6
BuildRequires: numpy >= 1.4.1

Requires: numpy >= 1.4.1
Requires: scipy >= 0.7.2
Requires: python-mahotas >= 0.5.2
Requires: python-milk >= 0.3.1
Requires: python-pymorph >= 0.95


%description
UNKNOWN

%prep
%setup -n %{pyname}-%{version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
