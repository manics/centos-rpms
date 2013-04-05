Name:           omero
Version:        0.1
Release:        1%{?dist}
Summary:        Open Microscopy Environment

License:        GPLv2
URL:            http://www.openmicroscopy.org/
Source0:        omero-stable.tar.gz

BuildRequires:  java-devel >= 1:1.7.0
#BuildRequires:  java7-devel >= 1:1.7.0
BuildRequires:  ant
BuildRequires:  gcc
#BuildRequires:  gcc-c++
#BuildRequires:  git

BuildRequires:  ice-devel >= 3.4
BuildRequires:  ice-java-devel >= 3.4
BuildRequires:  ice-python-devel >= 3.4

%description
OMERO is client-server software for visualization, management and analysis of
biological microscope images.

%prep
%setup -q -n omero-stable


%build
./build.py build-all release-clients release-tar release-webstart


%install
rm -rf %{buildroot}


%files
%doc



%changelog
* Fri Apr  5 2013 Simon Li <spli@dundee.ac.uk> - 0.1-1
- Created initial RPM

