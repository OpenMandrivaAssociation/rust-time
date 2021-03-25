%bcond_with check
%global debug_package %{nil}

%global crate time

Name:           rust-%{crate}
Version:        0.1.44
Release:        1
Summary:        Utilities for working with time-related functions in Rust

# Upstream license specification: MIT/Apache-2.0
License:        MIT or ASL 2.0
URL:            https://crates.io/crates/time
Source:         %{crates_source}
# Initial patched metadata
# * No windows/redox
# * Exclude CI files, https://github.com/rust-lang-deprecated/time/pull/170
Patch0:         time-fix-metadata.diff

ExclusiveArch:  %{rust_arches}
%if %{__cargo_skip_build}
BuildArch:      noarch
%endif

BuildRequires:  rust-packaging

%global _description %{expand:
Utilities for working with time-related functions in Rust.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages
which use "%{crate}" crate.

%files          devel
%license LICENSE-MIT LICENSE-APACHE
%doc README.md
%{cargo_registry}/%{crate}-%{version}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages
which use "default" feature of "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{cargo_registry}/%{crate}-%{version}/Cargo.toml

%package     -n %{name}+rustc-serialize-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+rustc-serialize-devel %{_description}

This package contains library source intended for building other packages
which use "rustc-serialize" feature of "%{crate}" crate.

%files       -n %{name}+rustc-serialize-devel
%ghost %{cargo_registry}/%{crate}-%{version}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
sed -i -e '/#!\[.*deny(warnings).*\]/d' src/lib.rs
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif
