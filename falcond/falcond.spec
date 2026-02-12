%global _include_minidebuginfo 0

Name:           falcond
Version:        1.2.3
Release:        3%{?dist}
Summary:        Advanced Linux Gaming Performance Daemon
License:        MIT
URL:            https://git.pika-os.com/general-packages/falcond
Source0:        https://github.com/PikaOS-Linux/falcond/archive/refs/tags/v%{version}.tar.gz
BuildRequires:  systemd-rpm-macros
BuildRequires:  zig >= 0.15.2
BuildRequires:  zig-rpm-macros
Requires:       %{name}-profiles
Requires:       (scx-scheds or scx-scheds-nightly)
Suggests:       %{name}-gui
Conflicts:      gamemode
Provides:       group(falcond)

%description
falcond is a powerful system daemon designed to automatically optimize your Linux gaming experience.
It intelligently manages system resources and performance settings on a per-game basis.
This eliminates the need to manually configure settings for each game.


%description
falcond is a powerful system daemon designed to automatically optimize your Linux gaming experience. It intelligently manages system resources and performance settings on a per-game basis, eliminating the need to manually configure settings for each game.

%prep
%autosetup -n %{name}/%{name}

%build

%install
install -Dm644 debian/%{name}.service -t %{buildroot}%{_unitdir}
# When DNF supports microarchitectures the fallback option for -c can be used here instead
DESTDIR="%{buildroot}" \
%{zig_build_target -r fast -cx86_64_v3 -s} 

%pre
# Create falcond group if it doesn't exist
getent group 'falcond' >/dev/null || groupadd -f -r 'falcond' || :

# Root must be a member of the group
usermod -aG 'falcond' root || :

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc ../README.md
%license ../LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service


%changelog
%autochangelog
