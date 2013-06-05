%define githash 0f8ba30

Summary: OMERO.searcher
Name: omero-searcher
Version: 0.0.2
Release: 1%{?dist}
Source0: omero-searcher-%{githash}.tar.gz
License: GPLv3
Group: Development/Libraries
BuildArch: noarch
Url: http://murphylab.web.cmu.edu/software/

%global omerodir /opt/omero

Requires:       omero-server >= 4.4.7
Requires:       python-pyslid >= 0.0.2
Requires:       python-ricerca

%description
Image search for OMERO.

Source archive created using
git archive --prefix=omero_searcher/ -o omero-searcher-`git describe --always`.tar.gz 0f8ba30de6d8089215464de14899539026e6d2bf


%prep
%setup -n omero_searcher

%build

%install
mkdir -p %{buildroot}%{omerodir}/server/lib/python/omeroweb/omero_searcher
cp -a *.py templates \
    %{buildroot}%{omerodir}/server/lib/python/omeroweb/omero_searcher
mkdir -p %{buildroot}%{omerodir}/server/lib/scripts/searcher
cp -a scripts/*.py %{buildroot}%{omerodir}/server/lib/scripts/searcher
mkdir -p %{buildroot}/OMERO/pyslid.data


%post
APPS=`su - omero -c "%{omerodir}/server/bin/omero config get omero.web.apps"`
APPCFG=`cat <<EOF | %{__python}
import sys
apps = '$APPS'
apps = [a.strip('" ') for a in apps.lstrip('[\'').rstrip(']\'').split(',')]
apps = filter(lambda x: bool(x), apps)
if 'omero_searcher' in apps:
    sys.exit(0)
apps.append('omero_searcher')
print '[' + ','.join( ['"%s"' % a for a in apps] ) + ']'
EOF`
if [ -n "$APPCFG" ]; then
    su - omero -c "%{omerodir}/server/bin/omero config set omero.web.apps '$APPCFG'"
fi
service omero-web restart


%files
%{omerodir}/server/lib/python/omeroweb/omero_searcher
%{omerodir}/server/lib/scripts/searcher
%attr(-,omero,omero) /OMERO/pyslid.data

%changelog

* Wed Jun 05 2013 Simon Li<spli@dundee.ac.uk> - 0.0.2-1
- Support for C/Z/T selection
- Built from https://github.com/manics/omero_searcher/tree/0f8ba30de6d8089215464de14899539026e6d2bf

* Wed Apr 24 2013 Simon Li<spli@dundee.ac.uk> - 0.0.1-1
- Initial package
- Built from https://github.com/manics/omero_searcher/tree/05de4c65838ddc80eae9ea2d7c0c1b0da80afd6f
