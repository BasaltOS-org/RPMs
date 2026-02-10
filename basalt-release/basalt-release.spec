%global distro  BasaltOS
%define release_name    Version 10.1
%global major   10
%global minor   1

Name:           basalt-release
Version:        %{major}.%{minor}
Release:        16%{?dist}
Summary:        %{distro} release files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://basaltdev.tech

Provides:       centos-release = %{version}-%{release}

# Required for a lorax run (to generate install media)
Requires:       basalt-repos = %{version}-%{release}
Provides:       centos-release-eula
Provides:       redhat-release-eula

# required by epel-release
Provides:       redhat-release = %{version}-%{release}

# required by dnf
# https://github.com/rpm-software-management/dnf/blob/4.2.23/dnf/const.py.in#L26
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{major}
Provides:       system-release(releasever_major) = %{major}
Provides:       system-release(releasever_minor) = %{minor}

# required by libdnf
# https://github.com/rpm-software-management/libdnf/blob/0.48.0/libdnf/module/ModulePackage.cpp#L472
Provides:       base-module(platform:el%{major})

Source200:      EULA
Source201:      LICENSE

Source300:      85-display-manager.preset
Source301:      90-default.preset
Source302:      90-default-user.preset
Source303:      99-default-disable.preset
Source304:      50-redhat.conf

Source400:      alsecurebootca1.cer
# kernel signing certificate
Source401:      alsecureboot1.cer
# grub2 signing certificate
Source402:      alsecureboot1.cer
# Fwupd signing certificate
Source403:      alsecureboot1.cer
# UKI signing certificate
Source404:      alsecureboot1.cer

Source500:      basalt-appstream.repo
Source501:      basalt-baseos.repo
Source502:      basalt-crb.repo
Source503:      basalt-extras-common.repo
Source600:      RPM-GPG-KEY-AlmaLinux-10

Source700:      macros.x86_64_v2

%package -n basalt-sb-certs
Summary: %{distro} public secureboot certificates
Group: System Environment/Base
Provides: system-sb-certs = %{version}-%{release}
Provides: redhat-sb-certs = %{version}-%{release}
Provides: centos-sb-certs = %{version}-%{release}
Provides: basalt-sb-certs = %{version}-%{release}

%package -n basalt-repos
Summary:        %{distro} package repositories
Requires:       basalt-release = %{version}-%{release}
Requires:       basalt-gpg-keys = %{version}-%{release}
# Required by CentOS SIGs release packages
Provides:       centos-stream-repos = %{version}-%{release}

%package -n basalt-gpg-keys
Summary:        %{distro} RPM keys
# Required by CentOS SIGs release packages
Provides:       centos-gpg-keys = %{version}-%{release}

%description
%{distro} release files.

%description -n basalt-sb-certs
%{distro} secureboot certificates

%description -n basalt-repos
This package provides the package repository files for %{distro}.

%description -n basalt-gpg-keys
This package provides the RPM signature keys for %{distro}.

%install
# copy license and contributors doc here for %%license and %%doc macros
mkdir -p ./docs
cp %{SOURCE201} ./docs

# create /etc/system-release and /etc/redhat-release
install -d -m 0755 %{buildroot}%{_sysconfdir}
echo "%{distro} release %{major}.%{minor}%{?beta: %{beta}} (%{release_name})" > %{buildroot}%{_sysconfdir}/basalt-release
ln -s basalt-release %{buildroot}%{_sysconfdir}/system-release
ln -s basalt-release %{buildroot}%{_sysconfdir}/redhat-release

# -------------------------------------------------------------------------
# Definitions for /etc/os-release and for macros in macros.dist.  These
# macros are useful for spec files where distribution-specific identifiers
# are used to customize packages.

# Name of vendor / name of distribution. Typically used to identify where
# the binary comes from in --help or --version messages of programs.
# Examples: gdb.spec, clang.spec
%global dist_vendor BasaltOS Community
%global dist_name   %{distro}

# The namespace for purl
# https://github.com/package-url/purl-spec
# for example as in: pkg:rpm/almalinux/python-setuptools@69.2.0-10.el10?arch=src"
%global dist_purl_namespace basaltos

# URL of the homepage of the distribution
# Example: gstreamer1-plugins-base.spec
%global dist_home_url https://basaltdev.tech

# Bugzilla / bug reporting URLs shown to users.
# Examples: gcc.spec
%global dist_bug_report_url https://basaltdev.tech

# debuginfod server, as used in elfutils.spec.
# %global dist_debuginfod_url https://debuginfod.centos.org/
# -------------------------------------------------------------------------


# Create the os-release file
install -d -m 0755 %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="%{dist_name}"
VERSION="%{major}.%{minor} (%{release_name})"
ID="basalt"
ID_LIKE="almalinux rhel centos fedora"
VERSION_ID="%{major}.%{minor}"
PLATFORM_ID="platform:el%{major}"
PRETTY_NAME="%{distro} %{major}.%{minor}%{?beta: %{beta}} (%{release_name})"
ANSI_COLOR="0;34"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:basalt:basalt:%{major}.%{minor}"
HOME_URL="%{dist_home_url}"
DOCUMENTATION_URL="https://basaltdev.tech"
VENDOR_NAME="Basalt"
VENDOR_URL="%{dist_home_url}"
BUG_REPORT_URL="%{dist_bug_report_url}"

BASALT_MANTISBT_PROJECT="Basalt-%{major}"
BASALT_MANTISBT_PROJECT_VERSION="%{major}.%{minor}"
REDHAT_SUPPORT_PRODUCT="%{distro}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{major}.%{minor}%{?beta: %{beta}}"
EOF

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:basalt:basalt:%{major}.%{minor}" > %{buildroot}%{_sysconfdir}/system-release-cpe

# create /etc/issue, /etc/issue.net and /etc/issue.d
echo '\S' > %{buildroot}%{_sysconfdir}/issue
echo 'Kernel \r on an \m' >> %{buildroot}%{_sysconfdir}/issue
cp %{buildroot}%{_sysconfdir}/issue{,.net}
echo >> %{buildroot}%{_sysconfdir}/issue
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

# set up the dist tag macros
mkdir -p %{buildroot}%{_rpmmacrodir}
cat > %{buildroot}%{_rpmmacrodir}/macros.dist << EOF
# dist macros.

%%__bootstrap ~bootstrap
%%basalt_ver %{major}
%%basalt %{major}
%%centos_ver %{major}
%%centos %{major}
%%rhel %{major}
%%el%{major} 1
%%distcore            .el%{major}
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%%{distcore}%%{?distsuffix}%%{?with_bootstrap:%{__bootstrap}}
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_purl_namespace %{dist_purl_namespace}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
EOF

# use unbranded datadir
install -d -m 0755 %{buildroot}%{_datadir}/basalt-release
ln -s basalt-release %{buildroot}%{_datadir}/redhat-release
install -p -m 0644 %{SOURCE200} %{buildroot}%{_datadir}/basalt-release/

# copy systemd presets
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -d -m 0755 %{buildroot}%{_prefix}/lib/systemd/user-preset
install -p -m 0644 %{SOURCE300} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE301} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE302} %{buildroot}%{_prefix}/lib/systemd/user-preset/

# installing the same file for both system and user presets to set the same behavior for both
install -p -m 0644 %{SOURCE303} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -p -m 0644 %{SOURCE303} %{buildroot}%{_prefix}/lib/systemd/user-preset/

# copy sysctl presets
mkdir -p %{buildroot}/%{_prefix}/lib/sysctl.d/
install -m 0644 %{SOURCE304} %{buildroot}/%{_prefix}/lib/sysctl.d/

# Create stub yum repos
mkdir %{buildroot}%{_sysconfdir}/yum.repos.d
touch %{buildroot}%{_sysconfdir}/yum.repos.d/redhat.repo

# Copy secureboot certificates
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/sb-certs/
install -d -m 0755 %{buildroot}%{_datadir}/pki/sb-certs/

# Install aarch64 certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer
install -m 644 %{SOURCE402} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer
install -m 644 %{SOURCE403} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-aarch64.cer


# Install x86_64 certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer
install -m 644 %{SOURCE402} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer
install -m 644 %{SOURCE403} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-x86_64.cer

# Install ppc64le certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer
install -m 644 %{SOURCE402} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-ppc64le.cer

# Install s390x certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-s390x.cer
install -m 644 %{SOURCE401} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-s390x.cer
install -m 644 %{SOURCE404} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-s390x.cer

# Link x86_64 certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-x86_64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-x86_64.cer

# Link aarch64 certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-aarch64.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-aarch64.cer

# Link ppc64le certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-ppc64le.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-ppc64le.cer

# Link s390x certs
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-s390x.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-s390x.cer
ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-uki-virt-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-uki-virt-s390x.cer

# copy yum repos
install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -p -m 0644 %{SOURCE500} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE501} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE502} %{buildroot}%{_sysconfdir}/yum.repos.d/
install -p -m 0644 %{SOURCE503} %{buildroot}%{_sysconfdir}/yum.repos.d/


# dnf variables
install -d -m 0755 %{buildroot}%{_sysconfdir}/dnf/vars
echo "%{major}-stream" > %{buildroot}%{_sysconfdir}/dnf/vars/stream

# copy GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p -m 0644 %{SOURCE600} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

# These variables should be set in the build environment to change rpm names
mkdir -p %{buildroot}%{_sysconfdir}/rpm
%ifarch x86_64_v2
install -p -m 0644 %{SOURCE700}  %{buildroot}%{_sysconfdir}/rpm/
%endif


%files
%license docs/LICENSE
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/basalt-release
%config(noreplace) %{_sysconfdir}/os-release
%config %{_sysconfdir}/system-release-cpe
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%dir %{_sysconfdir}/yum.repos.d
%ghost %{_sysconfdir}/yum.repos.d/redhat.repo
%{_rpmmacrodir}/macros.dist
%{_datadir}/redhat-release
%{_datadir}/basalt-release
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*
%{_prefix}/lib/systemd/user-preset/*
%{_prefix}/lib/sysctl.d/50-redhat.conf

%files -n basalt-sb-certs
# Note to future packagers:
# resetting the symlinks in /etc/pki/sb-certs on upgrade is the intended behavior here
%dir %{_sysconfdir}/pki/sb-certs
%dir %{_datadir}/pki/sb-certs/
%{_sysconfdir}/pki/sb-certs/*.cer
%{_datadir}/pki/sb-certs/*.cer

%files -n basalt-repos
%config(noreplace) %{_sysconfdir}/yum.repos.d/basalt-appstream.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/basalt-baseos.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/basalt-crb.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/basalt-extras-common.repo
%config(noreplace) %{_sysconfdir}/dnf/vars/stream

%files -n basalt-gpg-keys
%{_sysconfdir}/pki/rpm-gpg

%changelog
* Tue Feb 10 2026 Sidney Birkhead <birkheadsidney261@protonmail.com> - 10.1-16
- 10.1 stable
- Initial BasaltOS release
