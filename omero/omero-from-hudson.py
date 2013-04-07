#!/usr/bin/env python
#

import ast
import os
import re
import shutil
import time
import urllib2

url = 'http://hudson.openmicroscopy.org.uk/view/2.%20Stable/job/OMERO-stable-ice34/api/python?depth=1'

rpm_source_dir = '../SOURCES/'

def downloadArtifact(url, dest, overwrite=False):
    if not overwrite:
        if os.path.exists(dest):
            print '%s exists, not overwriting' % dest
            return
    r = urllib2.urlopen(url)
    print 'Downloading to %s' % dest
    with open(dest, 'wb') as f:
        try:
            shutil.copyfileobj(r, f)
        finally:
            r.close()

versionre = '((\d+\.\d+\.\d+)-(\d+)-(\w+)-ice34-b(\d+))'
required = [('OMERO.server-', '.zip'),
            ('OMERO.insight-', '.zip'),
            ('OMERO.importer-', '.zip')]

a = ast.literal_eval(urllib2.urlopen(url).read())
lastSuccess = a['lastSuccessfulBuild']
baseurl = lastSuccess['url'] + 'artifact/'
arts = [(b['fileName'], baseurl + b['relativePath'])
        for b in lastSuccess['artifacts']]

version = None
for art in arts:
    for req in required:
        m = re.match(req[0] + versionre + req[1], art[0])
        if m:
            if not version:
                version = m.groups()
            else:
                assert(m.groups() == version)
            downloadArtifact(art[1], rpm_source_dir + art[0])


rpmspec = """
Name:           omero-bin
Version:        %VERSION%
Release:        %RELEASE%%{?dist}
Summary:        Open Microscopy Environment

License:        GPLv2
URL:            http://www.openmicroscopy.org/
Source0:        %HUDSON_SOURCE_URL%OMERO.server-%BUILD_VERSION%.zip
Source1:        %HUDSON_SOURCE_URL%OMERO.insight-%BUILD_VERSION%.zip
Source2:        %HUDSON_SOURCE_URL%OMERO.importer-%BUILD_VERSION%.zip

%if 0%{?fedora}
BuildRequires:  java-devel >= 1:1.7.0
%else
BuildRequires:  java7-devel >= 1:1.7.0
%endif

# This is a metapackage, which just requires it's subpackages
Requires:       omero-server = %{version}
Requires:       omero-clients = %{version}

%global omerodir /opt/omero
%global __os_install_post %{nil}


%description
OMERO is client-server software for visualization, management and analysis of
biological microscope images.

%package server
Summary:        OMERO server

%if 0%{?fedora}
Requires:       java >= 1:1.7.0
%else
Requires:       java7 >= 1:1.7.0
%endif

Requires:       ice >= 3.4
Requires:       ice-java >= 3.4
Requires:       ice-python >= 3.4
#Requires:       ice-servers >= 3.4

Requires:       python >= 2.6
# If pytables 2.4 is required then it will also require numpy and
# numexpr >= 1.4.1, though rpm/yum should handle this automatically.
Requires:       numpy >= 1.2.0
Requires:       scipy
Requires:       python-tables >= 2.1.0
Requires:       python-matplotlib 
Requires:       python-imaging

Requires:       postgresql-server >= 8.4
Requires:       postgresql >= 8.4

Provides:       omero-server = %{version}

%description server
OMERO server components.
This RPM is created from Hudson build %HUDSON_SOURCE_URL%


%pre server
getent group omero > /dev/null || groupadd -r omero
#getent passwd omero > /dev/null || \
#    useradd -r -g omero -d %{omerodir}/server/var -s /sbin/nologin \
#    -c "omero server" omero
getent passwd omero > /dev/null || \
    useradd -r -g omero -d %{omerodir}/server/var -c "omero server" omero
exit 0

%post server
su - postgres -c "createuser -DRS omero"
su - postgres -c "createdb -O omero omero"



%package clients
Summary:        OMERO clients

%if 0%{?fedora}
Requires:       java >= 1:1.7.0
%else
Requires:       java7 >= 1:1.7.0
%endif

Provides:       omero-clients = %{version}

%description clients
OMERO clients (Insight).
This RPM is created from Hudson build %HUDSON_SOURCE_URL%


%prep
%setup -c
%setup -D -T -a 1
%setup -D -T -a 2

%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{omerodir}
cp -a OMERO.server-%BUILD_VERSION% %{buildroot}%{omerodir}/server
cp -a OMERO.insight-%BUILD_VERSION% %{buildroot}%{omerodir}/insight
cp -a OMERO.importer-%BUILD_VERSION% %{buildroot}%{omerodir}/importer
mkdir %{buildroot}%{omerodir}/server/var
mkdir %{buildroot}/omero


%files


%files server
%defattr(-,root,root)
%dir %{omerodir}
%dir %{omerodir}/server
%{omerodir}/server/bin
%{omerodir}/server/etc
%{omerodir}/server/include
%{omerodir}/server/lib
%{omerodir}/server/licenses
%{omerodir}/server/LICENSE.txt
%{omerodir}/server/sql
%attr(-,omero,omero) %{omerodir}/server/var
%attr(-,omero,omero) /omero


%files clients
%defattr(-,root,root)
%dir %{omerodir}
%{omerodir}/importer
%{omerodir}/insight


%changelog
* %DATE% Simon Li <spli@dundee.ac.uk> - %VERSION%-%RELEASE%
- Created RPM for Hudson build %BUILD_VERSION%

"""


rpmspec = rpmspec.replace('%BUILD_VERSION%', version[0])
rpmspec = rpmspec.replace('%HUDSON_SOURCE_URL%', baseurl)
rpmspec = rpmspec.replace('%VERSION%', version[1] + '.'+ version[2])
rpmspec = rpmspec.replace('%RELEASE%', version[4])
rpmspec = rpmspec.replace('%DATE%',
                          time.strftime('%a %b %e %Y', time.localtime()))
specfile = 'omero-bin-%s.spec' % version[0]
print 'Writing %s' % specfile
with open(specfile, 'w') as f:
    f.write(rpmspec)
