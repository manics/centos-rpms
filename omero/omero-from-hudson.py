#!/usr/bin/env python
#

# Instructions
# ------------
#
# Use this script to help create a set of installable OMERO rpms using the
# prebuilt binaries from the latest Hudson stable job.
#
# This assumes a standard rpmbuild directory structure:
#     rpmbuild/
#         BUILD/
#         BUILDROOT/
#         RPMS/
#         SOURCES/
#         SPECS/
#         SRPMS/
#         tmp/
#
# Change into the SPECS directory:
#     cd rpmbuild/SPECS
# Run:
#     omero-from-hudson.py
# This will download the last successful OMERO-stable Hudson artifacts sources
# to rpmbuild/SOURCES and create a rpm spec file in the current directory.
#
# Copy the following files from the directory containing this script into into
# rpmbuild/SOURCES
#     omero-init.d
#     omero-web-init.d
#     omero-firstrun.sh
# The first two are the modified init.d scripts based on the files in
# docs/install/VM/
#
# Build the source RPM:
#     rpmbuild -bs omero-bin-[VERSION].spec
# Now build the binary rpm, either directly:
#     rpmbuild -bb ../SRPMS/omero-bin-[VERSION].[DIST].src.rpm
# or using mock (this assumes a customised mock setup called omelocal-6-x86_64,
# see the mock-configs directory):
#     mock -r omelocal-6-x86_64 --rebuild \
#         ../SRPMS/omero-bin-[VERSION].[DIST].src.rpm

import ast
import os
import re
import shutil
import sys
import time
import urllib2


# Allow the hudson build number to be overridden
if len(sys.argv) > 2:
    sys.stderr.write('Usage: %s [buildnum]\n' % os.path.basename(sys.argv[0]))
    sys.exit(1)

try:
    buildnum = sys.argv[1]
except IndexError:
    buildnum = None

if buildnum:
    url = 'http://hudson.openmicroscopy.org.uk/view/2.%20Stable/job/OMERO-stable-ice34/' + str(buildnum) + '/api/python?depth=1'
else:
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

# Example version strings:
# 4.4.6-916-6fe6155-ice34-b202
# 4.4.7-RC1-ice34-b241
# 4.4.7-RC1-46-708f7f0-ice34-b243
# 4.4.7-ice34-b245
versionre = '((\d+\.\d+\.\d+)-((\w+)-)?([\w-]+)?ice34-b(\d+))'
required = [('OMERO.server-', '.zip'),
            ('OMERO.insight-', '.zip'),
            ('OMERO.importer-', '.zip')]

a = ast.literal_eval(urllib2.urlopen(url).read())
if buildnum:
    lastSuccess = a
else:
    lastSuccess = a['lastSuccessfulBuild']

if lastSuccess['result'] != 'SUCCESS':
    print 'ERROR: Hudson build was not successful: %s' % lastSuccess['result']

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

build_version = version[0]
rpm_version = version[1]
rpm_release = version[5]
if version[3] is not None:
    rpm_release += '.' + version[3]

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
Source3:        omero-init.d
Source4:        omero-web-init.d
Source5:        omero-firstrun.sh
Source6:        omero-httpd.conf

%if 0%{?fedora}
#BuildRequires:  java-devel >= 1:1.7.0
%else
#BuildRequires:  java7-devel >= 1:1.7.0
%endif



# This is a metapackage, which just requires it's subpackages
Requires:       omero-server = %{version}
Requires:       omero-web = %{version}
Requires:       omero-clients = %{version}

%global omerodir /opt/omero
# Binaries are prebuilt, so don't do any post-processing
%global __os_install_post %{nil}
# We don't want internal libraries to be used by any other packages
AutoProv:       no


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
Requires:       ice-servers >= 3.4

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

After installing this for the first time run the commands listed in
%{omerodir}/server/bin/omero-firstrun.sh to setup the database and configure
OMERO.




%pre server
getent group omero > /dev/null || groupadd -r omero
#getent passwd omero > /dev/null || \
#    useradd -r -g omero -d %{omerodir}/server/var -s /sbin/nologin \
#    -c "omero server" omero
getent passwd omero > /dev/null || \
    useradd -r -g omero -d %{omerodir}/server/var -c "omero server" omero
exit 0

%post server
/sbin/chkconfig --add omero

%preun server
if [ $1 = 0 ] ; then
	/sbin/service omero stop >/dev/null 2>&1
	/sbin/chkconfig --del omero
fi

#postun server
#if [ $1 -ge 1 ] ; then
#	/sbin/service omero condrestart >/dev/null 2>&1 || :
#fi



%package web
Summary:        OMERO web

Requires:       httpd >= 2.2
Requires:       mod_fastcgi >= 2.4

Requires:       omero-server = %{version}
Provides:       omero-web = %{version}

%description web
OMERO web startup scripts.
This RPM is created from Hudson build %HUDSON_SOURCE_URL%


%post web
/sbin/chkconfig --add omero-web

%preun web
if [ $1 = 0 ] ; then
	/sbin/service omero-web stop >/dev/null 2>&1
	/sbin/chkconfig --del omero-web
fi

#postun web
#if [ $1 -ge 1 ] ; then
#	/sbin/service omero-web condrestart >/dev/null 2>&1 || :
#fi



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
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .
cp %{SOURCE6} .

%build
rm OMERO.server-%BUILD_VERSION%/lib/python/omeroweb/.gitignore

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{omerodir}
cp -a OMERO.server-%BUILD_VERSION% %{buildroot}%{omerodir}/server
cp -a OMERO.insight-%BUILD_VERSION% %{buildroot}%{omerodir}/insight
cp -a OMERO.importer-%BUILD_VERSION% %{buildroot}%{omerodir}/importer

# The following directories need to be writable by omero. Create them
# here so that we can set the required permissions.
mkdir %{buildroot}%{omerodir}/server/var
mkdir %{buildroot}/OMERO
mkdir %{buildroot}%{omerodir}/server/lib/scripts/.omero
mkdir %{buildroot}%{omerodir}/server/lib/python/omeroweb/static

mkdir -p %{buildroot}%{omerodir}/server/etc/init.d
mkdir -p %{buildroot}%{_initddir}
cp omero-init.d %{buildroot}%{omerodir}/server/etc/init.d/omero
ln -s %{omerodir}/server/etc/init.d/omero %{buildroot}%{_initddir}/omero
cp omero-firstrun.sh %{buildroot}%{omerodir}/server/bin

cp omero-web-init.d %{buildroot}%{omerodir}/server/etc/init.d/omero-web
ln -s %{omerodir}/server/etc/init.d/omero-web %{buildroot}%{_initddir}/omero-web
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
cp omero-httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/omero.conf


%files


%files server
%defattr(-,root,root)
%dir %{omerodir}
%dir %{omerodir}/server
%{omerodir}/server/bin
%dir %attr(-,omero,omero) %{omerodir}/server/etc/grid
%config(noreplace) %attr(-,omero,omero) %{omerodir}/server/etc/grid/*.xml
%{omerodir}/server/etc/grid/README
%config %{omerodir}/server/etc/*.bat
%config %{omerodir}/server/etc/*.cfg
%config %{omerodir}/server/etc/*.config
%config %{omerodir}/server/etc/*.properties*
%config %{omerodir}/server/etc/*.sh
%config %{omerodir}/server/etc/*.template
%config %{omerodir}/server/etc/*.types
%config %{omerodir}/server/etc/*.xml
%dir %{omerodir}/server/etc/profiles
%config %{omerodir}/server/etc/profiles/*
%{omerodir}/server/include
%dir %{omerodir}/server/lib
%{omerodir}/server/lib/client
%{omerodir}/server/lib/fallback
%{omerodir}/server/lib/insight
%{omerodir}/server/lib/prefs.class
%dir %{omerodir}/server/lib/python
%{omerodir}/server/lib/python/*.*
%{omerodir}/server/lib/python/django
%{omerodir}/server/lib/python/flup
%{omerodir}/server/lib/python/omero
%{omerodir}/server/lib/python/omero_ext
%dir %{omerodir}/server/lib/python/omeroweb/
%{omerodir}/server/lib/python/omeroweb/*.*
%{omerodir}/server/lib/python/omeroweb/feedback
%{omerodir}/server/lib/python/omeroweb/license
%{omerodir}/server/lib/python/omeroweb/web*
%attr(-,omero,omero) %{omerodir}/server/lib/python/omeroweb/static
%{omerodir}/server/lib/server
%dir %{omerodir}/server/lib/scripts
%{omerodir}/server/lib/scripts/omero
%{omerodir}/server/lib/scripts/README.txt
%{omerodir}/server/lib/scripts/.git*
%attr(-,omero,omero) %{omerodir}/server/lib/scripts/.omero
%{omerodir}/server/licenses
%{omerodir}/server/LICENSE.txt
%{omerodir}/server/sql
%attr(-,omero,omero) %{omerodir}/server/var
%attr(-,omero,omero) /OMERO
%dir %{omerodir}/server/etc/init.d
%{_initddir}/omero
%config %{omerodir}/server/etc/init.d/omero


%files web
%{_initddir}/omero-web
%config %{omerodir}/server/etc/init.d/omero-web
%config %{_sysconfdir}/httpd/conf.d/omero.conf


%files clients
%defattr(-,root,root)
%dir %{omerodir}
%{omerodir}/importer
%{omerodir}/insight


%changelog
* %DATE% Simon Li <spli@dundee.ac.uk> - %VERSION%-%RELEASE%
- Created RPM for Hudson build %BUILD_VERSION%

"""


rpmspec = rpmspec.replace('%BUILD_VERSION%', build_version)
rpmspec = rpmspec.replace('%HUDSON_SOURCE_URL%', baseurl)
rpmspec = rpmspec.replace('%VERSION%', rpm_version)
rpmspec = rpmspec.replace('%RELEASE%', rpm_release)
rpmspec = rpmspec.replace('%DATE%',
                          time.strftime('%a %b %e %Y', time.localtime()))
specfile = 'omero-bin-%s.spec' % build_version
print 'Writing %s' % specfile
with open(specfile, 'w') as f:
    f.write(rpmspec)

