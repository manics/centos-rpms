%define pyname ricerca
%define pyversion 1.1

Summary: Content based search based on the FALCON algorithm
Name: python-%{pyname}
# Experimental with custom modfications, so use a low version for now
Version: 0.0.2
Release: 1
Source0: http://hudson.openmicroscopy.org.uk/job/ANALYSIS-OMERO-RICERCA-merge/lastSuccessfulBuild/artifact/src/dist/ricerca-1.1-7e673d1-b36.tar.gz
License: GPLv3
Group: Development/Libraries
BuildArch: noarch
Vendor: Robert F. Murphy <murphy@cmu.edu>
Url: http://murphylab.web.cmu.edu/software/

Requires: numpy >= 1.4.1
Requires: scipy >= 0.7.2

%description

Content based search based on the algorithm from Wu, Faloutsos, Sycara and Payne. FALCON: Feedback Adaptive Loop for Content-Based Retrieval. Proceeding VLDB 2000 Proceedings of the 26th International Conference on Very Large Data Bases.

Built from the OMERO Hudson CI ANALYSIS-OMERO-RICERCA-merge job.

%prep
%setup -n %{pyname}-%{pyversion}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Fri Sep  6 2013  <spli@dundee.ac.uk> - 0.0.1-2
- Switch to using package created by Hudson CI merge build
  ANALYSIS-OMERO-RICERCA-merge


%files -f INSTALLED_FILES
%defattr(-,root,root)
