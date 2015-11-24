Name:           DiffusionKurtosisFit
Version:        0.1.1
Release:        1%{?dist}
Summary:        Code to reconstruct the Diffusion Kurtosis Tensor from Diffusion Weighted MRI

License:        BSD
URL:            https://github.com/clwyatt/DiffusionKurtosisFit
Source0:        https://github.com/clwyatt/DiffusionKurtosisFit/archive/v%{version}/%{name}-%{version}.tar.gz

Provides:       dkifit%{?_isa} = %{version}-%{release}
# It contains vul from vxl slightly modified
# * added vul_arg<vcl_list<vcl_strin>> support
# * changed -? to -h
# https://github.com/clwyatt/DiffusionKurtosisFit/issues/1
Provides:       bundled(vxl) = 1.14

BuildRequires:  cmake gcc-c++
BuildRequires:  InsightToolkit-devel
BuildRequires:  vxl-devel

%description
%{summary}.

%prep
%autosetup

# link to system vcl
sed -i \
  -e "s/itkvcl/vcl/" \
  -e "/ADD_LIBRARY/s/vul /vul STATIC /" \
  Utilities/vul/CMakeLists.txt

rm -rf build/
mkdir build/

%build
pushd build/
  export ITK_DIR=%{_libdir}/cmake/InsightToolkit/
  %cmake ../
  %make_build
popd

%install
pushd build/
  mkdir -p %{buildroot}%{_bindir}/
  install -p -m0755 bin/* %{buildroot}%{_bindir}/
popd

%check
pushd build/
  ctest -VV
popd

%files
%license LICENSE.txt
%doc Documentation
%{_bindir}/dkifit
%{_bindir}/dkiscalars
%{_bindir}/dtiscalars

%changelog
* Tue Nov 24 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.1.1-1
- Initial package
