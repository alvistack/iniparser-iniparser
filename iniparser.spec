# Copyright 2026 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: iniparser
Epoch: 100
Version: 4.2.6
Release: 1%{?dist}
Summary: C library for parsing "INI-style" files
License: MIT
URL: https://gitlab.com/iniparser/iniparser/-/tags
Source0: %{name}_%{version}.orig.tar.gz
%if 0%{?rhel} == 7
BuildRequires: devtoolset-11
BuildRequires: devtoolset-11-gcc
BuildRequires: devtoolset-11-gcc-c++
BuildRequires: devtoolset-11-libatomic-devel
%endif
BuildRequires: cmake4
BuildRequires: fdupes
BuildRequires: gcc
BuildRequires: gcc-c++

%description
iniParser is an ANSI C library to parse "INI-style" files, often used to
hold application configuration information.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-11/enable
%endif
mkdir -p build
pushd build && \
    cmake \
        .. \
        -DBUILD_TESTING=OFF \
        -DBUILD_EXAMPLES=OFF \
        -DBUILD_DOCS=OFF \
        -DBUILD_SHARED_LIBS=ON \
        -DBUILD_STATIC_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr && \
popd
pushd build && \
    cmake \
        --build . \
        --parallel 10 \
        --config Release && \
popd

%install
pushd build && \
    export DESTDIR=%{buildroot} && \
    cmake \
        --install . && \
popd
fdupes -qnrps %{buildroot}

%if 0%{?suse_version} >= 1500
%package -n libiniparser4
Summary: Library to parse ini files
Group: System/Libraries

%description -n libiniparser4
Libiniparser offers parsing of ini files from the C level.

This package includes the libiniparser4 library.

%package -n libiniparser-devel
Summary: Libraries and Header Files to Develop Programs with libiniparser Support
Group: Development/Libraries/C and C++
Requires: libiniparser4 = %{epoch}:%{version}-%{release}

%description -n libiniparser-devel
This package contains the static libraries and header files needed to
develop programs which make use of the libiniparser programming
interface.

The libiniparser offers parsing of ini files from the C level.	See a
complete documentation in HTML format, from the
%{_docdir}/libiniparser-devel directory open the file
html/index.html with any HTML-capable browser.

Libraries and Header Files to Develop Programs with iniparser Support.

%post -n libiniparser4 -p /sbin/ldconfig
%postun -n libiniparser4 -p /sbin/ldconfig

%files -n libiniparser4
%license LICENSE
%{_libdir}/*.so.*

%files -n libiniparser-devel
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/iniparser
%{_includedir}/iniparser
%{_libdir}/*.so
%{_libdir}/cmake/iniparser/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%endif

%if !(0%{?suse_version} >= 1500)
%package -n iniparser-devel
Summary: Header files, libraries and development documentation for iniparser
Requires: iniparser = %{epoch}:%{version}-%{release}

%description -n iniparser-devel
This package contains the header files, static libraries and development
documentation for iniparser. If you like to develop programs using
iniparser, you will need to install iniparser-devel.

%package -n iniparser-static
Summary: C library for parsing "INI-style" files - static library
Requires: iniparser-devel = %{epoch}:%{version}-%{release}

%description -n iniparser-static
Static library (.a) version of libiniparser.

%post -n iniparser -p /sbin/ldconfig
%postun -n iniparser -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/*.so.*

%files -n iniparser-devel
%dir %{_libdir}/cmake
%dir %{_libdir}/cmake/iniparser
%{_includedir}/iniparser
%{_libdir}/*.so
%{_libdir}/cmake/iniparser/*
%{_libdir}/pkgconfig/*.pc

%files -n iniparser-static
%{_libdir}/*.a
%endif

%changelog
