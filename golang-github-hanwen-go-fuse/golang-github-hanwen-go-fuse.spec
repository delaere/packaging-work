# no binary...
%global _enable_debug_package 0
%global debug_package %{nil}

# git commit used for the package
%global commit          0ad840cf1c835844c01474aba565475b03909a01
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

# switch to enable checks.
# since it requires fuse, it doesn't work in mock
%bcond_with checks

# standard package information
Name:           golang-github-hanwen-go-fuse
Version:        0
Release:        1.git%{shortcommit}%{?dist}
Group:          Development/Libraries
Summary:        Native bindings for the FUSE kernel module
License:        BSD
URL:            https://github.com/hanwen/go-fuse
Source0:        https://github.com/hanwen/go-fuse/archive/%{commit}/go-fuse-%{shortcommit}.tar.gz

# go Language Architectures (https://fedoraproject.org/wiki/PackagingDrafts/Go)
# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# if go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
%if %{with checks}
BuildRequires:  fuse
%endif

%description
%{summary}

########################################################
# devel package declaration
########################################################
%package devel
Summary:       %{summary}
BuildArch:     noarch
Requires:      golang

Provides:      golang(github.com/hanwen/go-fuse/benchmark) = %{version}-%{release}
Provides:      golang(github.com/hanwen/go-fuse/fuse) = %{version}-%{release}
Provides:      golang(github.com/hanwen/go-fuse/fuse/nodefs) = %{version}-%{release}
Provides:      golang(github.com/hanwen/go-fuse/fuse/pathfs) = %{version}-%{release}
Provides:      golang(github.com/hanwen/go-fuse/fuse/test) = %{version}-%{release}
Provides:      golang(github.com/hanwen/go-fuse/splice) = %{version}-%{release}
Provides:      golang(github.com/hanwen/go-fuse/unionfs) = %{version}-%{release}
Provides:      golang(github.com/hanwen/go-fuse/zipfs) = %{version}-%{release}

%description devel
%{summary}

This package contains library sources for go-fuse, the Go language 
bindings for File System in Userspace (FUSE) utilities.

########################################################
# unit-test-devel package declaration
########################################################
%package unit-test-devel
Summary:       Unit tests for %{name} package
BuildArch:     noarch
Requires:      %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}

This package contains unit tests for go-fuse, the Go language
bindings for File System in Userspace (FUSE) utilities.

########################################################
# prepare and install files
########################################################
%prep
%setup -q -n go-fuse-%{commit}

%build

%install
# source codes for building projects
install -d -p %{buildroot}/%{gopath}/src/github.com/hanwen/go-fuse/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/github.com/hanwen/go-fuse/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/github.com/hanwen/go-fuse/$file
    echo "%%{gopath}/src/github.com/hanwen/go-fuse/$file" >> devel.file-list
done

# testing files for this project
install -d -p %{buildroot}/%{gopath}/src/github.com/hanwen/go-fuse/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/github.com/hanwen/go-fuse/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/github.com/hanwen/go-fuse/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/github.com/hanwen/go-fuse/$file
    echo "%%{gopath}/src/github.com/hanwen/go-fuse/$file" >> unit-test-devel.file-list
done

# directories
echo "%%dir %%{gopath}/src/github.com/hanwen/go-fuse/." >> devel.file-list
for reldir in $(find . -type d); do
    echo "%%dir %%{gopath}/src/github.com/hanwen/go-fuse/$reldir" >> devel.file-list
done

# final sort of the list of files
sort -u -o devel.file-list devel.file-list

########################################################
# final checks and declarations
########################################################
%check
%if %{with checks}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%gotest github.com/hanwen/go-fuse/benchmark
%gotest github.com/hanwen/go-fuse/fuse
%gotest github.com/hanwen/go-fuse/fuse/nodefs
%gotest github.com/hanwen/go-fuse/fuse/pathfs
%gotest github.com/hanwen/go-fuse/fuse/test
%gotest github.com/hanwen/go-fuse/splice
#these two tests are known not to work.
#%%gotest github.com/hanwen/go-fuse/unionfs
#%%gotest github.com/hanwen/go-fuse/zipfs
%endif

%files devel -f devel.file-list
%license LICENSE
%doc README AUTHORS
%dir %{gopath}/src/github.com/hanwen

%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README AUTHORS

%changelog
* Wed Jan 04 2017 Christophe Delaere <christophe.delaere@gmail.com> - 0-1.git0ad840c
- First package for Fedora

