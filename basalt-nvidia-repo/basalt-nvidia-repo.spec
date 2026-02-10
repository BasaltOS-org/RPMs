Name:		basalt-nvidia-repo
Summary:	BasaltOS NVIDIA driver repository configuration
Version:	%{?rhel}
Release:	1%{?dist}
License:	GPL-2.0-only
URL:		https://basaltdev.tech/
ExclusiveArch:  x86_64 %{x86_64} %{arm64}
Source1:	nvidia-cuda.repo

Requires:       epel-release
Requires(post): epel-release
Provides:	basalt-nvidia-repo = %{version}
Conflicts:	epel-nvidia


%description
DNF configuration for BasaltOS NVIDIA driver repository


%prep
%ifarch x86_64_v2
sed -i "s/\$basearch/x86_64_v2/g" %{SOURCE0}
sed -i '/^mirrorlist=/ s|$|?arch=x86_64_v2|g' %{SOURCE0}
%endif
%ifarch aarch64
sed -i "s/\$basearch/sbsa/g" %{SOURCE1}
%endif

%if %{?rhel} == 9
sed -i "s/\$gpgkey/D42D0685.pub/g" %{SOURCE1}
%endif
%if %{?rhel} == 10
sed -i "s/\$gpgkey/CDF6BA43.pub/g" %{SOURCE1}
%endif

%install
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d/nvidia-cuda.repo


%post
if [ -x /usr/bin/crb ]; then
  /usr/bin/crb enable
fi


%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/nvidia-cuda.repo

%changelog

* Sat Feb 7 2026 Sidney Birkhead <birkheadsidney261@protonmail.com> - %{?rhel}-1
- First commit!!!!
