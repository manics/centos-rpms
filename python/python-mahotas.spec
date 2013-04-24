%define pyname mahotas

Summary: Mahotas: Computer Vision Library
Name: python-%{pyname}
Version: 0.9.7
Release: 1
Source0: %{pyname}-%{version}.tar.gz
License: MIT
Group: Development/Libraries
Vendor: Luis Pedro Coelho <luis@luispedro.org>
Url: http://luispedro.org/software/mahotas

BuildRequires: python-setuptools >= 0.6
BuildRequires: python-devel >= 2.6
BuildRequires: numpy >= 1.4.1

Requires: numpy >= 1.4.1


%description

This library of fast computer vision algorithms (all implemented in C++)
operates over numpy arrays for convenience.

Notable algorithms:
 - watershed.
 - convex points calculations.
 - hit & miss. thinning.
 - Zernike & Haralick, LBP, and TAS features.
 - freeimage based numpy image loading (requires freeimage libraries to be
   installed).
 - Speeded-Up Robust Features (SURF), a form of local features.
 - thresholding.
 - convolution.
 - Sobel edge detection.
 - spline interpolation

Mahotas currently has over 100 functions for image processing and computer
vision and it keeps growing.

The release schedule is roughly one release a month and each release brings new
functionality and improved performance. The interface is very stable, though,
and code written using a version of mahotas from years back will work just fine
in the current version, except it will be faster (some interfaces are
deprecated and will be removed after a few years, but in the meanwhile, you
only get a warning). In a few unfortunate cases, there was a bug in the old
code and your results will change for the better.



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
