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

# This is a metapackage, which just requires it's subpackages
Requires:       omero-server = %{version}-%{release}
Requires:       omero-client = %{version}-%{release}

%global omerodir %{buildroot}/opt/omero
%global __jar_repack 0

%description
OMERO is client-server software for visualization, management and analysis of
biological microscope images.

%package server
Summary:        OMERO server

%description server
OMERO server components.

%package clients
Summary:        OMERO clients

%description clients
OMERO clients (Insight).


%prep
%setup -q -n omero-stable


%build
./build.py build-all release-clients release-webstart release-zip


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{omerodir}
unzip -d %{buildroot}/%{omerodir} target/OMERO.insight-UNKNOWN.zip
unzip -d %{buildroot}/%{omerodir} target/OMERO.importer-UNKNOWN.zip
unzip -d %{buildroot}/%{omerodir} target/OMERO.server-UNKNOWN.zip


%files
#doc

%files server
%defattr(-,root,root)
%dir %{omerodir}
%{omerodir}/OMERO.server-UNKNOWN

%files clients
%defattr(-,root,root)
%dir %{omerodir}
%{omerodir}/OMERO.importer-UNKNOWN
%{omerodir}/OMERO.insight-UNKNOWN


%changelog
* Sat Apr  6 2013 Simon Li <spli@dundee.ac.uk> - 0.1-1
- Created initial RPM

