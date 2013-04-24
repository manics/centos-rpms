%define pyname ricerca
%define pyversion 1.0.0

Summary: Content based search based on the FALCON algorithm
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

Requires: numpy >= 1.4.1
Requires: scipy >= 0.7.2

%description

Content based search based on the algorithm from Wu, Faloutsos, Sycara and Payne. FALCON: Feedback Adaptive Loop for Content-Based Retrieval. Proceeding VLDB 2000 Proceedings of the 26th International Conference on Very Large Data Bases.

Built from
https://github.com/manics/ricerca/commit/2e626656c414c0344d7ddaf634efab55d47ed936

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
