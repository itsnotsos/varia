Name:           varia
Version:        2025.1.24
Release:        1%{?dist}
Summary:        A modern GTK4-based download manager
License:        GPL-3.0
URL:            https://github.com/giantpinkrobots/varia
Source0:        https://github.com/giantpinkrobots/varia/archive/refs/tags/v%{version}.tar.gz
Source1:        https://files.pythonhosted.org/packages/source/a/aria2p/aria2p-0.11.0.tar.gz
Source2:        https://files.pythonhosted.org/packages/source/y/yt_dlp/yt_dlp-2023.10.13.tar.gz

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  gettext
BuildRequires:  python3-pip

Requires:       python3
Requires:       gtk4
Requires:       libadwaita
Requires:       aria2
Requires:       ffmpeg

%description
Varia is a simple and efficient download manager built with GTK4 and Libadwaita,
designed to integrate seamlessly with the GNOME desktop environment. It supports
features like pausing and resuming downloads, speed limiting, and browser integration,
leveraging aria2 for file downloads and yt-dlp for video/audio streams.

%prep
%setup -q -n varia-%{version}
cd ..
tar -xzf %{SOURCE1}
tar -xzf %{SOURCE2}

%build
%meson
%meson_build

%install
%meson_install
cd ../aria2p-0.11.0
%py3_install
cd ../yt_dlp-2023.10.13
%py3_install

%files
%{_bindir}/varia.py
%{_datadir}/varia/*
%{_datadir}/applications/io.github.giantpinkrobots.varia.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.giantpinkrobots.varia.svg
%{_datadir}/metainfo/io.github.giantpinkrobots.varia.appdata.xml
%{python3_sitelib}/aria2p*
%{python3_sitelib}/yt_dlp*

%changelog
* Tue Mar 18 2025 Your Name <your.email@example.com> - 0.1.0-1
- Initial RPM release
