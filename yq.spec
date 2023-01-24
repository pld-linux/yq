%define		vendor_ver	4.30.8

Summary:	Command-line YAML, JSON, XML, CSV and properties processor
Name:		yq
Version:	4.30.8
Release:	1
License:	MIT
Group:		Applications/Text
Source0:	https://github.com/mikefarah/yq/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	78ccc739a27454c9564019a3a0515906
Source1:	%{name}-vendor-%{vendor_ver}.tar.xz
# Source1-md5:	00401f6d57414f386cea4893efabdfa9
URL:		https://mikefarah.gitbook.io/yq/
BuildRequires:	golang >= 1.19
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
A lightweight and portable command-line YAML, JSON and XML processor.
yq uses jq like syntax but works with yaml files as well as json, xml,
properties, csv and tsv. It doesn't yet support everything jq does -
but it does support the most common operations and functions, and more
is being added continuously.

%package -n bash-completion-yq
Summary:	Bash completion for yq command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-yq
Bash completion for yq command line.

%package -n fish-completion-yq
Summary:	fish-completion for yq
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-yq
fish-completion for yq.

%package -n zsh-completion-yq
Summary:	ZSH completion for yq command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-yq
ZSH completion for yq command line.

%prep
%setup -q -a1
%{__mv} %{name}-%{vendor_ver}/vendor .

%build
%__go build -v -mod=vendor -o target/yq

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{bash_compdir},%{fish_compdir},%{zsh_compdir}}

cp -p target/yq $RPM_BUILD_ROOT%{_bindir}/yq

./target/yq shell-completion bash > $RPM_BUILD_ROOT%{bash_compdir}/yq
./target/yq shell-completion fish > $RPM_BUILD_ROOT%{fish_compdir}/yq.fish
./target/yq shell-completion zsh > $RPM_BUILD_ROOT%{zsh_compdir}/_yq

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md README.md
%attr(755,root,root) %{_bindir}/yq

%files -n bash-completion-yq
%defattr(644,root,root,755)
%{bash_compdir}/yq

%files -n fish-completion-yq
%defattr(644,root,root,755)
%{fish_compdir}/yq.fish

%files -n zsh-completion-yq
%defattr(644,root,root,755)
%{zsh_compdir}/_yq
