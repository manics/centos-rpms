%define githash a65d06d

Summary: OMERO.searcher
Name: omero-searcher
Version: 0.0.5
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
git archive --prefix=omero_searcher/ -o omero-searcher-`git describe --always`.tar.gz a0db01f89818535260ca86dc51ef3ebb6bc81324

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

* Wed Jun 19 2013 Simon Li <spli@dundee.ac.uk> - 0.0.5-1
- Filter by channel names
- UI cleanups
- Built from https://github.com/manics/omero_searcher/tree/a0db01f89818535260ca86dc51ef3ebb6bc81324

* Fri Jun 14 2013 Simon Li <spli@dundee.ac.uk> - 0.0.4-1
- Script UI improvements
- More feature calculation error handling
- Built from https://github.com/manics/omero_searcher/tree/d612eed69564bce1f82a6e69dba0eb30615667b4

* Thu Jun 13 2013 Simon Li <spli@dundee.ac.uk> - 0.0.3-1
- Script improvements
- User filtering
- Built from https://github.com/manics/omero_searcher/tree/48fb37bc461bae88f716ab5d81736741801e2642

* Wed Jun 05 2013 Simon Li <spli@dundee.ac.uk> - 0.0.2-1
- Support for C/Z/T selection
- Built from https://github.com/manics/omero_searcher/tree/0f8ba30de6d8089215464de14899539026e6d2bf

* Wed Apr 24 2013 Simon Li <spli@dundee.ac.uk> - 0.0.1-1
- Initial package
- Built from https://github.com/manics/omero_searcher/tree/05de4c65838ddc80eae9ea2d7c0c1b0da80afd6f
