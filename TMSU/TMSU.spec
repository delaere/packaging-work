Name:		TMSU
Version:	0.6.1
Release:	1%{?dist}
Summary:	Lets you tag your files and access them through a semantic file-system

Group:		Applications/File
License:	GPLv3
URL:		http://tmsu.org
Source0:	https://github.com/oniony/TMSU/archive/v%{version}.tar.gz
# All patches should have an upstream bug link or comment
Patch0:		tmsu.useDestdir.patch
Patch1:		tmsu.wrong-script-interpreter.patch

BuildRequires:	golang
BuildRequires:	golang-github-mattn-go-sqlite3-devel
BuildRequires:	golang-github-hanwen-go-fuse-devel
Requires:	fuse, zsh

%description
TMSU is a tool for tagging your files. It provides a simple command-line 
utility for applying tags and a virtual file-system to give you a tag-based 
view of your files from any other program

TMSU does not alter your files in any way: they remain unchanged on disk, 
or on the network, wherever your put them. TMSU maintains its own database 
and you simply gain an additional view, which you can mount where you like, 
based upon the tags you set up.

%global _hardened_build 1

%prep
%autosetup -p0
rm -rf %{_builddir}/go
mkdir  %{_builddir}/go

%build
export GOPATH=%{_builddir}/go:/usr/share/gocode
# this is probably not allowed for central builds
#go get -u github.com/mattn/go-sqlite3
#go get -u github.com/hanwen/go-fuse/fuse
/usr/bin/make -O -j4 clean compile dist

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/sbin/
mkdir -p %{buildroot}/usr/share/man/man1/
mkdir -p %{buildroot}/usr/share/zsh/site-functions/
make install DESTDIR=%{buildroot}
gunzip %{buildroot}/usr/share/man/man1/tmsu.1.gz

%check
export GOPATH=%{_builddir}/go:/usr/share/gocode
make test

%files
%doc README.md
%license COPYING.md
%{_bindir}/tmsu
%{_bindir}/tmsu-fs-merge
%{_bindir}/tmsu-fs-mv
%{_bindir}/tmsu-fs-rm
%{_sbindir}/mount.tmsu
%{_mandir}/man1/tmsu.1*
%{_datarootdir}/zsh/site-functions/_tmsu


%changelog
* Sun Dec 18 2016 Christophe Delaere <christophe.delaere@gmail.com> - 0.6.1-1
- Initial Packaging


