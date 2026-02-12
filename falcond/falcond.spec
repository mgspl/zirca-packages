%global _include_minidebuginfo 0
%global debug_package %{nil}

Name:           falcond
Version:        1.2.3
Release:        %autorelease
Summary:        Advanced Linux Gaming Performance Daemon

License:        MIT
URL:            https://git.pika-os.com/general-packages/%{name}
Source0:        https://github.com/PikaOS-Linux/falcond/archive/refs/tags/v%{version}.tar.gz

ExclusiveArch:	x86_64

BuildRequires:  zig >= 0.14.0
BuildRequires:  systemd-rpm-macros

Recommends:	%{name}-profiles
Recommends:	%{name}-gui
Requires:	%{name}-profiles
Requires:	%{name}-gui
Requires:	scx-scheds

Provides:       group(falcond)

%description
falcond is a powerful system daemon designed to automatically optimize your Linux gaming experience. It intelligently manages system resources and performance settings on a per-game basis, eliminating the need to manually configure settings for each game.

%prep

%autosetup -n %{name}

%build

%install
cd %{name}
mkdir -p %{buildroot}%{_unitdir}/
install -Dm644 debian/%{name}.service %{buildroot}%{_unitdir}
DESTDIR="%{buildroot}" \
zig build \
    -Doptimize=ReleaseFast \
    -Dcpu=x86_64_v3
    
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
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
