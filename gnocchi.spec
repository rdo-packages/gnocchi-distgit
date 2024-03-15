%global pypi_name gnocchi
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service gnocchi

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           %{service}
Version:        XXX
Release:        XXX
Summary:        Gnocchi is a API to store metrics and index resources

License:        Apache-2.0
URL:            http://github.com/gnocchixyz/%{service}
Source0:        https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        %{pypi_name}-dist.conf
Source2:        %{pypi_name}.logrotate
Source10:       %{name}-api.service
Source11:       %{name}-metricd.service
Source12:       %{name}-statsd.service
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  systemd
BuildRequires:  openstack-macros

%description
HTTP API to store metrics and index resources.

%package -n     python3-%{service}
Summary:        %{service} python libraries

Requires:       python3-%{service}+keystone = %{version}-%{release}
Requires:       python3-%{service}+mysql = %{version}-%{release}
Requires:       python3-%{service}+postgresql = %{version}-%{release}
Requires:       python3-%{service}+swift = %{version}-%{release}

%description -n   python3-%{service}
%{service} provides API to store metrics from components
and index resources.

This package contains the %{service} python library.


%package        api

Summary:        %{service} api

Requires:       %{name}-common = %{version}-%{release}
Obsoletes:      openstack-%{service}-api < 4.1.3
Provides:       openstack-%{service}-api = %{version}-%{release}

%description api
%{service} provides API to store metrics from components
and index resources.

This package contains the %{service} API service.

%package        common
Summary:        Components common to all %{service} services

Requires:       python3-%{service} = %{version}-%{release}

Provides:         openstack-%{service}-common = %{version}-%{release}
Obsoletes:        openstack-%{service}-common < 4.1.3

%description    common
%{service} provides services to measure and
collect metrics from components.

%package        metricd

Summary:        %{service} metricd daemon

Requires:       %{name}-common = %{version}-%{release}

Obsoletes:      openstack-%{service}-metricd < 4.1.3
Provides:       openstack-%{service}-metricd = %{version}-%{release}

%description metricd
%{service} provides API to store metrics from OpenStack
components and index resources.

This package contains the %{service} metricd daemon


%package        statsd

Summary:        %{service} statsd daemon

Requires:       %{name}-common = %{version}-%{release}

Obsoletes:      openstack-%{service}-statsd < 4.1.3
Provides:       openstack-%{service}-statsd = %{version}-%{release}

%description statsd
%{service} provides API to store metrics from OpenStack
components and index resources.

This package contains the %{service} statsd daemon

%package -n python3-%{service}-tests
Summary:        Gnocchi tests
Requires:       python3-%{service} = %{version}-%{release}
Requires:       python3-gabbi >= 1.30.0

BuildRequires:  python3-gabbi
BuildRequires:  python3-stestr

%description -n python3-%{service}-tests
This package contains the Gnocchi test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{service}

Requires:         python3-%{service} = %{version}-%{release}

Provides:         openstack-%{service}-doc = %{version}-%{release}
Obsoletes:        openstack-%{service}-doc < 4.1.3

%description      doc
%{service} provides services to measure and
collect metrics from components.

This package contains documentation files for %{service}.
%endif


%prep
%setup -q -n %{service}-%{upstream_version}

echo "graft gnocchi" >> MANIFEST.in

find . \( -name .gitignore -o -name .placeholder \) -delete
find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Automatic BR generation
%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

# Generate config file
PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslo-config-generator --config-file=%{service}/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

# Programmatically update defaults in sample config
# which is installed at /etc/gnocchi/gnocchi.conf
# TODO: Make this more robust
# Note it only edits the first occurrence, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" %{service}/%{service}.conf
done < %{SOURCE1}

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/
mkdir -p %{buildroot}/%{_var}/log/%{name}

install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 %{service}/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

#TODO(prad): build the docs at run time, once the we get rid of postgres setup dependency

# Configuration
cp -R %{service}/rest/api-paste.ini %{buildroot}/%{_sysconfdir}/%{service}

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install systemd unit services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-metricd.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-statsd.service

# Backward compatibility unit services
ln -sf %{_unitdir}/%{name}-api.service %{buildroot}%{_unitdir}/openstack-%{name}-api.service
ln -sf %{_unitdir}/%{name}-metricd.service %{buildroot}%{_unitdir}/openstack-%{name}-metricd.service
ln -sf %{_unitdir}/%{name}-statsd.service %{buildroot}%{_unitdir}/openstack-%{name}-statsd.service

# Remove all of the conf files that are included in the buildroot/usr/etc dir since we installed them above
rm -f %{buildroot}/usr/etc/%{service}/*

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
if ! getent passwd %{service} >/dev/null; then
  useradd -r -g %{service} -G %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin -c "%{service} Daemons" %{service}
fi
exit 0

%post -n %{name}-api
%systemd_post %{name}-api.service

%preun -n %{name}-api
%systemd_preun %{name}-api.service

%post -n %{name}-metricd
%systemd_post %{name}-metricd.service

%preun -n %{name}-metricd
%systemd_preun %{name}-metricd.service

%post -n %{name}-statsd
%systemd_post %{name}-statsd.service

%preun -n %{name}-statsd
%systemd_preun %{name}-statsd.service

%pyproject_extras_subpkg -n python3-%{service} keystone mysql postgresql swift

%files -n python3-%{service}
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.dist-info

%files -n python3-%{service}-tests
%license LICENSE

%files api
%defattr(-,root,root,-)
%{_bindir}/%{service}-api
%{_unitdir}/%{name}-api.service
%{_unitdir}/openstack-%{name}-api.service

%files common
%{_bindir}/%{service}-config-generator
%{_bindir}/%{service}-change-sack-size
%{_bindir}/%{service}-upgrade
%{_bindir}/%{service}-injector
%{_bindir}/%{service}-amqpd
%dir %{_sysconfdir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0750, %{service}, root)  %{_localstatedir}/log/%{service}

%defattr(-, %{service}, %{service}, -)
%dir %{_sharedstatedir}/%{service}
%dir %{_sharedstatedir}/%{service}/tmp

%files metricd
%{_bindir}/%{service}-metricd
%{_unitdir}/%{name}-metricd.service
%{_unitdir}/openstack-%{name}-metricd.service

%files statsd
%{_bindir}/%{service}-statsd
%{_unitdir}/%{name}-statsd.service
%{_unitdir}/openstack-%{name}-statsd.service

%if 0%{?with_doc}
%files doc
%doc doc/source/
%endif

%changelog

