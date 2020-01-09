Name:		cpupowerutils
Version:	1.2
Release:	1%{?dist}.1
Summary:	CPU power management utilities	
Group:		System Environment/Base
License:	GPLv2
URL:		http://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tools/power
Source0:	cpupowerutils-g650a37f.tar.bz2 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	pciutils-devel, kernel-headers >= 2.6.32-376
ExclusiveArch:	%{ix86} x86_64 ppc ppc64
Conflicts:	cpufrequtils
%description
cpupowerutils is a suite of tools designed to manage power states on
appropriately enabled cpus

%package devel
Summary:        Header files for development of cpu power utilities
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Conflicts:	cpufrequtils-devel

Patch0: cpupowerutils-cpupower-m-remove.patch
Patch1: cpupowerutils-energy-perf-policy-usage.patch
Patch2: cpupowerutils-energy-perf-policy-rootcheck.patch
Patch3: cpupowerutils-cpufreq-bench-nonroot-output-crash.patch
Patch4: cpupowerutils-cpupower-version.patch
Patch5: cpupowerutils-turbostat-update1.patch
Patch6: cpupowerutils-haswell-c8_c9_c10.patch
Patch7: cpupowerutils-turbostat-energystatus.patch
Patch8: cpupowerutils-turbostat-rapl-fix.patch

%description devel
Header files and libraries to enable development of cpupower utities

%prep
%setup -q -n power 
%patch0 -p1
%patch1 -p1
%patch2 -p1 
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
make -C cpupower
%ifarch %{ix86} x86_64
make -C x86/turbostat/
make -C x86/x86_energy_perf_policy
%endif

%install
make DESTDIR=$RPM_BUILD_ROOT mandir=/usr/share/man libdir=%{_libdir} -C cpupower install
%ifarch %{ix86} x86_64
install -D -m 0755 x86/turbostat/turbostat $RPM_BUILD_ROOT/usr/bin/turbostat
install -D -m 0644 x86/turbostat/turbostat.8 $RPM_BUILD_ROOT%{_mandir}/man8/turbostat.8
install -D -m 0755 x86/x86_energy_perf_policy/x86_energy_perf_policy $RPM_BUILD_ROOT/usr/bin/x86_energy_perf_policy
install -D -m 0644 x86/x86_energy_perf_policy/x86_energy_perf_policy.8 $RPM_BUILD_ROOT%{_mandir}/man8/x86_energy_perf_policy.8
%endif
rm -rf $RPM_BUILD_ROOT/usr/share/locale

%clean
rm -rf %{buildroot}

%files 
%config /etc/cpufreq-bench.conf
%doc /usr/share/doc/packages/cpupower
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man1/*
%ifarch %{ix86} x86_64
%{_mandir}/man8/*
%endif
%{_libdir}/libcpupower.so.0
%{_libdir}/libcpupower.so.0.0.0

%files devel
%{_includedir}/*
%{_libdir}/libcpupower.so

%changelog
* Tue Apr 22 2014 Neil Horman <nhorman@redhat.com> 1.2-1.1
- Fixed wildcatpass error message (bz 1056310)
- Fixed rapl register reads (bz 1080631
- Enalbed haswell power states (bz 1008033)

* Mon Apr 29 2013 Neil Horman <nhorman@redhat.com> 1.2-1
- Updated to latest upstream version

* Fri Mar 01 2013 Neil Horman <nhorman@redhat.com> 1.1-3
- Fixed cpupower version output (bz 914787)

* Fri Feb 22 2013 Neil Horman <nhorman@redhat.com> 1.1-2
- Removed set -m option from cpupower (bz 914623)
- Added man pages for turbostat & perf policy (bz 886225)
- Improved perf_poilcy usage (bz 886228)
- Added check for root on energy_perf_poilcy (bz 886227)
- Fixed crash when running cpufreq-bench as non-root (bz 886226)

* Thu Nov 08 2012 Neil Horman <nhorman@redhat.com> 1.1-1
- Version bump to fix stupid release typo (bz 697418)

* Thu Nov 08 2012 Neil Horman <nhorman@redhat.com> 1-5
- Fixed a minor typo (bz 697418)

* Thu Nov 08 2012 Neil Horman <nhorman@redhat.com> 1-4
- update spec to use Conflicts rather than Obsoletes (bz 697418)

* Tue Oct 09 2012 Neil Horman <nhorman@redhat.com> 1-3
- Update spec to fix some other typos/etc (bz 697418)

* Tue Oct 09 2012 Neil Horman <nhorman@redhat.com> 1-2
- Updated obsoletes fields in spec file (bz 697418)

* Mon Jun 25 2012 Neil Horman <nhorman@tuxdriver.com> 1-1 
- Initial build
