%define pyname milk

Summary: Machine Learning Toolkit
Name: python-%{pyname}
Version: 0.4.3
Release: 1
Source0: %{pyname}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
Prefix: %{_prefix}
Vendor: Luis Pedro Coelho <luis@luispedro.org>
Url: http://luispedro.org/software/milk

BuildRequires: python-setuptools >= 0.6
BuildRequires: python-devel >= 2.6
BuildRequires: numpy >= 1.4.1

Requires: numpy >= 1.4.1


%description
Milk is a machine learning toolkit in Python.

Its focus is on supervised classification with several classifiers available:
SVMs (based on libsvm), k-NN, random forests, decision trees. It also performs
feature selection. These classifiers can be combined in many ways to form
different classification systems.

For unsupervised learning, milk supports k-means clustering and affinity
propagation.

Milk is flexible about its inputs. It optimised for numpy arrays, but can often
handle anything (for example, for SVMs, you can use any dataype and any kernel
and it does the right thing).

There is a strong emphasis on speed and low memory usage. Therefore, most of
the performance sensitive code is in C++. This is behind Python-based
interfaces for convenience.



%prep
%setup -n %{pyname}-%{version}

%build
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
