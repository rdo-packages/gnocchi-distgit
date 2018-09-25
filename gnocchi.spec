# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
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

BuildRequires:  python%{pyver}-setuptools >= 30.3
BuildRequires:  python%{pyver}-setuptools_scm
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-devel
BuildRequires:  systemd
BuildRequires:  python%{pyver}-tenacity >= 4.6.0
BuildRequires:  openstack-macros

%description
HTTP API to store metrics and index resources.

%package -n     python%{pyver}-%{service}
Summary:        %{service} python libraries
%{?python_provide:%python_provide python%{pyver}-%{service}}

Requires:       python%{pyver}-numpy >= 1.9.0
Requires:       python%{pyver}-daiquiri
Requires:       python%{pyver}-iso8601
Requires:       python%{pyver}-jinja2
Requires:       python%{pyver}-keystonemiddleware >= 4.0.0
Requires:       python%{pyver}-lz4 >= 0.9.0
Requires:       python%{pyver}-monotonic
Requires:       python%{pyver}-msgpack
Requires:       python%{pyver}-oslo-config >= 2:3.22.0
Requires:       python%{pyver}-oslo-db >= 4.29.0
Requires:       python%{pyver}-oslo-middleware >= 3.22.0
Requires:       python%{pyver}-oslo-policy >= 0.3.0
Requires:       python%{pyver}-pecan >= 0.9
Requires:       python%{pyver}-requests
Requires:       python%{pyver}-swiftclient >= 3.1.0
Requires:       python%{pyver}-six
Requires:       python%{pyver}-sqlalchemy
Requires:       python%{pyver}-stevedore
Requires:       python%{pyver}-tooz >= 1.38
Requires:       python%{pyver}-trollius
Requires:       python%{pyver}-tenacity >= 4.6.0
Requires:       python%{pyver}-ujson
Requires:       python%{pyver}-voluptuous >= 0.8.10
Requires:       python%{pyver}-werkzeug
Requires:       python%{pyver}-pytz
Requires:       python%{pyver}-webob >= 1.4.1
Requires:       python%{pyver}-alembic
Requires:       python%{pyver}-prettytable
Requires:       python%{pyver}-cotyledon >= 1.5.0
Requires:       python%{pyver}-jsonpatch
Requires:       python%{pyver}-cachetools
Requires:       python%{pyver}-pyparsing

# Handle python2 exception
%if %{pyver} == 2
Requires:       python-futures
Requires:       python-paste
Requires:       python-paste-deploy
Requires:       python-pytimeparse >= 1.1.5
Requires:       python-sqlalchemy-utils
Requires:       python-sysv_ipc
Requires:       PyYAML
Requires:       python-psycopg2
%else
Requires:       python%{pyver}-paste
Requires:       python%{pyver}-paste-deploy
Requires:       python%{pyver}-pytimeparse >= 1.1.5
Requires:       python%{pyver}-sqlalchemy-utils
Requires:       python%{pyver}-sysv_ipc
Requires:       python%{pyver}-PyYAML
Requires:       python%{pyver}-psycopg2
%endif

%description -n   python%{pyver}-%{service}
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
BuildRequires:    python%{pyver}-daiquiri
BuildRequires:    python%{pyver}-jsonpatch
BuildRequires:    python%{pyver}-oslo-config >= 2:3.22.0
BuildRequires:    python%{pyver}-oslo-concurrency
BuildRequires:    python%{pyver}-oslo-db
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-messaging
BuildRequires:    python%{pyver}-oslo-policy
BuildRequires:    python%{pyver}-oslo-reports
BuildRequires:    python%{pyver}-oslo-service
BuildRequires:    python%{pyver}-lz4 >= 0.9.0
BuildRequires:    python%{pyver}-pandas >= 0.18.0
BuildRequires:    python%{pyver}-pecan >= 0.9
BuildRequires:    python%{pyver}-tooz
BuildRequires:    python%{pyver}-ujson
BuildRequires:    python%{pyver}-werkzeug
BuildRequires:    python%{pyver}-gnocchiclient >= 2.1.0

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-pytimeparse >= 1.1.5
%else
BuildRequires:    python%{pyver}-pytimeparse >= 1.1.5
%endif

Requires:       python%{pyver}-%{service} = %{version}-%{release}

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

%package -n python%{pyver}-%{service}-tests
Summary:        Gnocchi tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}
Requires:       python%{pyver}-%{service} = %{version}-%{release}
Requires:       python%{pyver}-gabbi >= 1.30.0

%description -n python%{pyver}-%{service}-tests
This package contains the Gnocchi test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{service}

Requires:         python%{pyver}-%{service} = %{version}-%{release}

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

%py_req_cleanup


%build
# Generate config file
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=%{service}/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

%{pyver_build}

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

%{pyver_install}

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/
mkdir -p %{buildroot}/%{_var}/log/%{name}

install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 %{service}/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

#TODO(prad): build the docs at run time, once the we get rid of postgres setup dependency

# Configuration
cp -R %{service}/rest/policy.json %{buildroot}/%{_sysconfdir}/%{service}

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

%files -n python%{pyver}-%{service}
%{pyver_sitelib}/%{service}
%{pyver_sitelib}/%{service}-*.egg-info
%exclude %{pyver_sitelib}/%{service}/tests

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/tests

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
%dir %{_sysconfdir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/policy.json
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
