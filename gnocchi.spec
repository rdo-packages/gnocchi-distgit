%global pypi_name gnocchi
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service gnocchi

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           %{service}
Version:        XXX
Release:        XXX
Summary:        Gnocchi is a API to store metrics and index resources

License:        ASL 2.0
URL:            http://github.com/gnocchixyz/%{service}
Source0:        https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        %{pypi_name}-dist.conf
Source2:        %{pypi_name}.logrotate
Source10:       %{name}-api.service
Source11:       %{name}-metricd.service
Source12:       %{name}-statsd.service
BuildArch:      noarch

BuildRequires:  python3-setuptools >= 30.3
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-sphinx
BuildRequires:  python3-devel
BuildRequires:  systemd
BuildRequires:  python3-tenacity >= 4.6.0
BuildRequires:  openstack-macros

%description
HTTP API to store metrics and index resources.

%package -n     python3-%{service}
Summary:        %{service} python libraries
%{?python_provide:%python_provide python3-%{service}}

Requires:       python3-numpy >= 1.9.0
Requires:       python3-daiquiri
Requires:       python3-iso8601
Requires:       python3-jinja2
Requires:       python3-keystonemiddleware >= 4.0.0
Requires:       python3-lz4 >= 0.9.0
Requires:       python3-monotonic
Requires:       python3-msgpack
Requires:       python3-oslo-config >= 2:3.22.0
Requires:       python3-oslo-db >= 4.29.0
Requires:       python3-oslo-middleware >= 3.22.0
Requires:       python3-oslo-policy >= 0.3.0
Requires:       python3-pecan >= 0.9
Requires:       python3-requests
Requires:       python3-swiftclient >= 3.1.0
Requires:       python3-six
Requires:       python3-sqlalchemy
Requires:       python3-stevedore
Requires:       python3-tooz >= 1.62
Requires:       python3-trollius
Requires:       python3-tenacity >= 4.6.0
Requires:       python3-ujson
Requires:       python3-voluptuous >= 0.8.10
Requires:       python3-werkzeug
Requires:       python3-pytz
Requires:       python3-webob >= 1.4.1
Requires:       python3-alembic
Requires:       python3-prettytable
Requires:       python3-cotyledon >= 1.5.0
Requires:       python3-jsonpatch
Requires:       python3-cachetools
Requires:       python3-pyparsing >= 2.2.0

Requires:       python3-paste
Requires:       python3-paste-deploy
Requires:       python3-pytimeparse >= 1.1.5
Requires:       python3-sqlalchemy-utils
Requires:       python3-sysv_ipc
Requires:       python3-PyYAML
Requires:       python3-psycopg2

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

# Config file generation
BuildRequires:    python3-daiquiri
BuildRequires:    python3-jsonpatch
BuildRequires:    python3-oslo-config >= 2:3.22.0
BuildRequires:    python3-oslo-concurrency
BuildRequires:    python3-oslo-db
BuildRequires:    python3-oslo-log
BuildRequires:    python3-oslo-messaging
BuildRequires:    python3-oslo-policy
BuildRequires:    python3-oslo-reports
BuildRequires:    python3-oslo-service
BuildRequires:    python3-lz4 >= 0.9.0
BuildRequires:    python3-numpy
BuildRequires:    python3-pecan >= 0.9
BuildRequires:    python3-tooz >= 1.62
BuildRequires:    python3-ujson
BuildRequires:    python3-werkzeug
BuildRequires:    python3-gnocchiclient >= 2.1.0

BuildRequires:    python3-pytimeparse >= 1.1.5

Requires:       python3-%{service} = %{version}-%{release}

Provides:         openstack-%{service}-common = %{version}-%{release}
Obsoletes:        openstack-%{service}-common < 4.1.3

Obsoletes:        openstack-%{service}-carbonara

# openstack-gnocchi-indexer-sqlalchemy is removed and merged into common
Provides:         openstack-%{service}-indexer-sqlalchemy = %{version}-%{release}
Obsoletes:        openstack-%{service}-indexer-sqlalchemy < 4.1.3

# Obsolete old openstack-gnocchi packages

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
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       python3-%{service} = %{version}-%{release}
Requires:       python3-gabbi >= 1.30.0

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

find . \( -name .gitignore -o -name .placeholder \) -delete
find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# (amoralej) Remove upper limit created upstream to fix issue with Ubuntu Focal
sed -i 's/oslo.policy>=0.3.0.*/oslo.policy>=0.3.0/' setup.cfg

%py_req_cleanup


%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=%{service}/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

%{py3_build}

# Programmatically update defaults in sample config
# which is installed at /etc/gnocchi/gnocchi.conf
# TODO: Make this more robust
# Note it only edits the first occurrence, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" %{service}/%{service}.conf
done < %{SOURCE1}

%install

%{py3_install}

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/
mkdir -p %{buildroot}/%{_var}/log/%{name}

install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 %{service}/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

#TODO(prad): build the docs at run time, once the we get rid of postgres setup dependency

# Configuration
cp -R %{service}/rest/api-paste.ini %{buildroot}/%{_sysconfdir}/%{service}
cp -R %{service}/rest/policy.json %{buildroot}/%{_sysconfdir}/%{service}
cp -R %{service}/rest/policy.yaml %{buildroot}/%{_sysconfdir}/%{service}

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
  useradd -r -g %{service} -G %{service},nobody -d %{_sharedstatedir}/%{service} -s /sbin/nologin -c "%{service} Daemons" %{service}
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

%files -n python3-%{service}
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info

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
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/policy.json
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/policy.yaml
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
