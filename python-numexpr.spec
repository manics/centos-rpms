%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup}

%global	module	numexpr

Summary:	Fast numerical array expression evaluator for Python and NumPy
Name:		python-%{module}
Version:	1.4.2
Release:	1%{?dist}
Source0:	http://numexpr.googlecode.com/files/%{module}-%{version}.tar.gz
License:	MIT
Group:		Development/Languages
URL:		http://numexpr.googlecode.com/

Requires:	numpy >= 1.4.1
BuildRequires:	numpy >= 1.4.1
BuildRequires:	python-devel


%description
The numexpr package evaluates multiple-operator array expressions many
times faster than NumPy can. It accepts the expression as a string,
analyzes it, rewrites it more efficiently, and compiles it to faster
Python code on the fly. It's the next best thing to writing the
expression in C and compiling it with a specialized just-in-time (JIT)
compiler, i.e. it does not require a compiler at runtime.

%prep
%setup -q -n %{module}-%{version}

sed -i "s|/usr/bin/env |/usr/bin/|" %{module}/cpuinfo.py

%build
python setup.py build 

%check
libdir=`ls build/|grep lib`
export PYTHONPATH=`pwd`/build/$libdir
python bench/timing.py

%install
rm -rf %{buildroot}

python setup.py install -O1 --skip-build  --root=%{buildroot}
#This could be done more properly ?
chmod 0644 %{buildroot}%{python_sitearch}/%{module}/cpuinfo.py
chmod 0755 %{buildroot}%{python_sitearch}/%{module}/*.so

%files
%doc ANNOUNCE.txt LICENSE.txt RELEASE_NOTES.txt README.txt
%{python_sitearch}/numexpr/
%{python_sitearch}/numexpr-%{version}-py*.egg-info/

%changelog
* Wed Mar 20 2013 Simon Li <spli@dundee.ac.uk> - 1.4.2-1
- Convert spec file from Fedora 18 numexpr-2.0.1 to CentOS 6 numexpr-1.4.2
