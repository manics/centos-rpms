Name:           wensleydale-release
Version:        6
Release:        1%{?dist}
Summary:        Custom packages for running OMERO on CentOS %{version}

Group:          System Environment/Base
License:        GPLv3

URL:            http://users.openmicroscopy.org.uk/~spli
Source0:        wensleydale.repo

BuildArch:     noarch
Requires:      redhat-release >=  %{version}
Conflicts:     fedora-release

%description
This package contains the Extra Packages for Enterprise Linux (EPEL) repository
GPG key as well as configuration for yum and up2date.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .

%build


%install
rm -rf $RPM_BUILD_ROOT

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*


%changelog
* Wed Mar 20 2013 Simon Li <spli@dundee.ac.uk> - 6-1
- Initial Package
