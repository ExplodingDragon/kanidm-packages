Name:           kanidm
Version:        1.1.0
Release:        1%{?dist}
Summary:        a simple and secure identity management platform, which provides services to allow other systems and application to authenticate against.

License:        MPL-2.0
URL:            https://github.com/kanidm/kanidm
Source0:        kanidm-v%{version}-alpha.11.tar.gz

BuildRequires:  systemd-devel sqlite-devel openssl-devel pam-devel

%description
Kanidm is a simple and secure identity management platform,
which provides services to allow other systems and application to authenticate against.
The project aims for the highest levels of reliability, security and ease of use.

%prep
%setup -q -D -n %{name}-%{version}-alpha.11


%build
export KANIDM_BUILD_PROFILE="release_suse_x86_64"
cargo build --locked --release --target-dir target

%install

# Client
%{__install} -Dm0644 LICENSE.md %{buildroot}/%{_defaultlicensedir}/%{name}-client-%{version}/COPYING
%{__install} -Dm0644 LICENSE.md %{buildroot}/%{_defaultlicensedir}/%{name}-server-%{version}/COPYING
%{__install} -Dm0644 LICENSE.md %{buildroot}/%{_defaultlicensedir}/%{name}-unixd-clients-%{version}/COPYING
%{__install} -Dm644 examples/config %{buildroot}/etc/kanidm/config
%{__install} -Dm755 target/release/kanidm %{buildroot}/usr/bin/kanidm
%{__install} -Dm644 target/release/build/completions/_kanidm %{buildroot}/usr/share/zsh/site-functions/_kanidm
%{__install} -Dm644 target/release/build/completions/kanidm.bash %{buildroot}/usr/share/bash-completion/completions/kanidm.sh

#Server
%{__install} -Dm644 examples/server.toml %{buildroot}/etc/kanidm/server.toml
%{__install} -Dm644 platform/opensuse/kanidmd.service %{buildroot}/usr/lib/systemd/system/kanidmd.service
%{__install} -Dm755 target/release/kanidmd %{buildroot}/usr/bin/kanidmd
%{__install} -Dm644 target/release/build/completions/_kanidmd %{buildroot}/usr/share/zsh/site-functions/_kanidmd
%{__install} -Dm644 target/release/build/completions/kanidmd.bash %{buildroot}/usr/share/bash-completion/completions/kanidmd.sh
%{__install} -dv %{buildroot}/usr/share/kanidm/ui/
cp -r kanidmd_web_ui/pkg %{buildroot}/usr/share/kanidm/ui/

#unixd-clients
%{__install} -Dm644 examples/unixd %{buildroot}/etc/kanidm/unixd
%{__install} -Dm644 platform/opensuse/kanidm-unixd.service "%{buildroot}/usr/lib/systemd/system/kanidm-unixd.service"
%{__install} -Dm644 platform/opensuse/kanidm-unixd-tasks.service "%{buildroot}/usr/lib/systemd/system/kanidm-unixd-tasks.service"

%{__install} -Dm755 target/release/libnss_kanidm.so "%{buildroot}/usr/lib/libnss_kanidm.so.2"
%{__install} -Dm755 target/release/libpam_kanidm.so "%{buildroot}/usr/lib/security/pam_kanidm.so"

%{__install} -Dm755 target/release/kanidm_cache_clear "%{buildroot}/usr/bin/kanidm_cache_clear"
%{__install} -Dm755 target/release/kanidm_cache_invalidate "%{buildroot}/usr/bin/kanidm_cache_invalidate"
%{__install} -Dm755 target/release/kanidm_ssh_authorizedkeys "%{buildroot}/usr/bin/kanidm_ssh_authorizedkeys"
%{__install} -Dm755 target/release/kanidm_ssh_authorizedkeys_direct "%{buildroot}/usr/bin/kanidm_ssh_authorizedkeys_direct"
%{__install} -Dm755 target/release/kanidm_unixd "%{buildroot}/usr/bin/kanidm_unixd"
%{__install} -Dm755 target/release/kanidm_unixd_status "%{buildroot}/usr/bin/kanidm_unixd_status"
%{__install} -Dm755 target/release/kanidm_unixd_tasks "%{buildroot}/usr/bin/kanidm_unixd_tasks"

%{__install} -Dm644 target/release/build/completions/_kanidm_ssh_authorizedkeys_direct "%{buildroot}/usr/share/zsh/site-functions/_kanidm_ssh_authorizedkeys_direct"
%{__install} -Dm644 target/release/build/completions/_kanidm_cache_clear "%{buildroot}/usr/share/zsh/site-functions/_kanidm_cache_clear"
%{__install} -Dm644 target/release/build/completions/_kanidm_cache_invalidate "%{buildroot}/usr/share/zsh/site-functions/_kanidm_cache_invalidate"
%{__install} -Dm644 target/release/build/completions/_kanidm_ssh_authorizedkeys "%{buildroot}/usr/share/zsh/site-functions/_kanidm_ssh_authorizedkeys"
%{__install} -Dm644 target/release/build/completions/_kanidm_unixd_status "%{buildroot}/usr/share/zsh/site-functions/_kanidm_unixd_status"

%{__install} -Dm644 target/release/build/completions/kanidm_ssh_authorizedkeys_direct.bash "%{buildroot}/usr/share/bash-completion/completions/kanidm_ssh_authorizedkeys_direct.sh"
%{__install} -Dm644 target/release/build/completions/kanidm_cache_clear.bash "%{buildroot}/usr/share/bash-completion/completions/kanidm_cache_clear.sh"
%{__install} -Dm644 target/release/build/completions/kanidm_cache_invalidate.bash "%{buildroot}/usr/share/bash-completion/completions/kanidm_cache_invalidate.sh"
%{__install} -Dm644 target/release/build/completions/kanidm_ssh_authorizedkeys.bash "%{buildroot}/usr/share/bash-completion/completions/kanidm_ssh_authorizedkeys.sh"
%{__install} -Dm644 target/release/build/completions/kanidm_unixd_status.bash "%{buildroot}/usr/share/bash-completion/completions/kanidm_unixd_status.sh"


%package client
Summary: kanidm client to interact with kanidm identity management server.
%description client
kanidm client to interact with kanidm identity management server.

%files client
%license %{_defaultlicensedir}/%{name}-client-%{version}/COPYING
%config(noreplace) /etc/kanidm/config
/usr/bin/kanidm
/usr/share/zsh/site-functions/_kanidm
/usr/share/bash-completion/completions/kanidm.sh

%package server
Summary: kanidm server for idendity management, supports RADIUS, ssh key management.
%description server
kanidm server for idendity management, supports RADIUS, ssh key management.

%files server
%config(noreplace) /etc/kanidm/server.toml
%license %{_defaultlicensedir}/%{name}-server-%{version}/COPYING
/usr/bin/kanidmd
/usr/lib/systemd/system/kanidmd.service
/usr/share/zsh/site-functions/_kanidmd
/usr/share/bash-completion/completions/kanidmd.sh
/usr/share/kanidm/ui

%post server
systemctl daemon-reload >/dev/null 2>&1 ||:
systemctl enable kanidmd ||:


%preun server
case $1 in
  0)
  systemctl disable --now kanidmd >/dev/null 2>&1 ||:
  ;;
esac

%package unixd-clients
Summary: kanidm localhost resolver to resolve posix identities to a kanidm instance.
%description unixd-clients
kanidm localhost resolver to resolve posix identities to a kanidm instance.

%files unixd-clients
%config(noreplace) /etc/kanidm/unixd
%license %{_defaultlicensedir}/%{name}-unixd-clients-%{version}/COPYING
/usr/lib/systemd/system/kanidm-unixd.service
/usr/lib/systemd/system/kanidm-unixd-tasks.service
/usr/lib/libnss_kanidm.so.2
/usr/lib/security/pam_kanidm.so
/usr/bin/kanidm_cache_clear
/usr/bin/kanidm_cache_invalidate
/usr/bin/kanidm_ssh_authorizedkeys
/usr/bin/kanidm_ssh_authorizedkeys_direct
/usr/bin/kanidm_unixd
/usr/bin/kanidm_unixd_status
/usr/bin/kanidm_unixd_tasks
/usr/share/zsh/site-functions/_kanidm_ssh_authorizedkeys_direct
/usr/share/zsh/site-functions/_kanidm_cache_clear
/usr/share/zsh/site-functions/_kanidm_cache_invalidate
/usr/share/zsh/site-functions/_kanidm_ssh_authorizedkeys
/usr/share/zsh/site-functions/_kanidm_unixd_status
/usr/share/bash-completion/completions/kanidm_ssh_authorizedkeys_direct.sh
/usr/share/bash-completion/completions/kanidm_cache_clear.sh
/usr/share/bash-completion/completions/kanidm_cache_invalidate.sh
/usr/share/bash-completion/completions/kanidm_ssh_authorizedkeys.sh
/usr/share/bash-completion/completions/kanidm_unixd_status.sh


%post unixd-clients
systemctl daemon-reload >/dev/null 2>&1 ||:

%preun unixd-clients
case $1 in
  0)
  systemctl disable --now kanidm-unixd.service >/dev/null 2>&1 ||:
  systemctl disable --now kanidm-unixd-tasks.service >/dev/null 2>&1 ||:
  ;;
esac

%changelog
* Wed Oct 26 2022 Dragon
- 初始化项目
