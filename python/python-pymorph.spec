%define pyname pymorph

Summary: Image Morphology Toolbox
Name: python-%{pyname}
Version: 0.96
Release: 1
Source0: %{pyname}-%{version}.tar.gz
License: BSD
Group: Development/Libraries
BuildArch: noarch
Vendor: Luis Pedro Coelho <lpc@cmu.edu>
Url: http://luispedro.org/software/pymorph/

BuildRequires: python-setuptools >= 0.6
BuildRequires: python-devel >= 2.6

Requires: numpy >= 1.4.1


%description

This image morphology toolbox implements the basic binary and greyscale
morphology operations, working with numpy arrays representing images.

This is a pure Python package which is the companion package
to the book "Hands-on Morphological Image Processing." It has been
updated to work with numpy and the names and interfaces have been
Pythonised.


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
