%global pypi_name gnocchi
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service gnocchi

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{service}
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

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-pbr
BuildRequires:  python2-devel
BuildRequires:  systemd
BuildRequires:  python-tenacity >= 4.0.0
BuildRequires:  openstack-macros

%description
HTTP API to store metrics and index resources.

%package -n     python-%{service}
Summary:        OpenStack %{service} python libraries

Requires:       numpy >= 1.9.0
Requires:       python-daiquiri
Requires:       python-futures
Requires:       python-iso8601
Requires:       python-jinja2
Requires:       python-keystonemiddleware >= 4.0.0
Requires:       python-lz4 >= 0.9.0
Requires:       python-monotonic
Requires:       python-msgpack
Requires:       python-oslo-config >= 2:3.22.0
Requires:       python-oslo-db >= 4.8.0
Requires:       python-oslo-log >= 2.3.0
Requires:       python-oslo-middleware >= 3.22.0
Requires:       python-oslo-policy >= 0.3.0
Requires:       python-oslo-sphinx >= 2.2.0
Requires:       python-oslo-serialization >= 1.4.0
Requires:       python-oslo-utils >= 3.18.0
Requires:       python-pandas >= 0.18.0
Requires:       python-paste
Requires:       python-paste-deploy
Requires:       python-pbr
Requires:       python-pecan >= 0.9
Requires:       python-pytimeparse >= 1.1.5
Requires:       python-requests
Requires:       python-scipy
Requires:       python-swiftclient >= 3.1.0
Requires:       python-six
Requires:       python-sqlalchemy
Requires:       python-sqlalchemy-utils
Requires:       python-stevedore
Requires:       python-sysv_ipc
Requires:       python-tooz >= 0.30
Requires:       python-trollius
Requires:       python-tenacity >= 4.0.0
Requires:       python-ujson
Requires:       python-voluptuous
Requires:       python-werkzeug
Requires:       pytz
Requires:       PyYAML
Requires:       python-webob >= 1.4.1
Requires:       python-alembic
Requires:       python-psycopg2
Requires:       python-prettytable
Requires:       python-cotyledon >= 1.5.0
Requires:       python-jsonpatch

%description -n   python-%{service}
OpenStack %{service} provides API to store metrics from OpenStack components
and index resources.

This package contains the %{service} python library.


%package        api

Summary:        OpenStack %{service} api

Requires:       %{name}-common = %{version}-%{release}

%description api
OpenStack %{service} provides API to store metrics from OpenStack components
and index resources.

This package contains the %{service} API service.

%package        common
Summary:        Components common to all OpenStack %{service} services

# Config file generation
BuildRequires:    python-daiquiri
BuildRequires:    python-jsonpatch
BuildRequires:    python-oslo-config >= 2:3.22.0
BuildRequires:    python-oslo-concurrency
BuildRequires:    python-oslo-db
BuildRequires:    python-oslo-log
BuildRequires:    python-oslo-messaging
BuildRequires:    python-oslo-policy
BuildRequires:    python-oslo-reports
BuildRequires:    python-oslo-service
BuildRequires:    python-lz4 >= 0.9.0
BuildRequires:    python-pandas >= 0.18.0
BuildRequires:    python-pecan >= 0.9
BuildRequires:    python-pytimeparse >= 1.1.5
BuildRequires:    python-tooz
BuildRequires:    python-ujson
BuildRequires:    python-werkzeug
BuildRequires:    python-gnocchiclient >= 2.1.0

Requires:       python-%{service} = %{version}-%{release}

Obsoletes:        openstack-%{service}-carbonara

# openstack-gnocchi-indexer-sqlalchemy is removed and merged into common
Provides:         openstack-%{service}-indexer-sqlalchemy = %{version}-%{release}
Obsoletes:        openstack-%{service}-indexer-sqlalchemy < %{version}-%{release}

%description    common
OpenStack %{service} provides services to measure and
collect metrics from OpenStack components.

%package        metricd

Summary:        OpenStack %{service} metricd daemon

Requires:       %{name}-common = %{version}-%{release}

%description metricd
OpenStack %{service} provides API to store metrics from OpenStack
components and index resources.

This package contains the %{service} metricd daemon


%package        statsd

Summary:        OpenStack %{service} statsd daemon

Requires:       %{name}-common = %{version}-%{release}

%description statsd
OpenStack %{service} provides API to store metrics from OpenStack
components and index resources.

This package contains the %{service} statsd daemon

%package -n python-%{service}-tests
Summary:        Gnocchi tests
Requires:       python-%{service} = %{version}-%{release}
Requires:       python-gabbi >= 1.30.0

%description -n python-%{service}-tests
This package contains the Gnocchi test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack %{service}

Requires:         python-%{service} = %{version}-%{release}

%description      doc
OpenStack %{service} provides services to measure and
collect metrics from OpenStack components.

This package contains documentation files for %{service}.
%endif


%prep
%setup -q -n %{service}-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%py_req_cleanup


%build

# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=%{service}/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

%{__python2} setup.py build

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

%{__python2} setup.py install --skip-build --root %{buildroot}

# Create fake egg-info for the tempest plugin
%py2_entrypoint %{service} %{service}

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

# Remove all of the conf files that are included in the buildroot/usr/etc dir since we installed them above
rm -f %{buildroot}/usr/etc/%{service}/*

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
if ! getent passwd %{service} >/dev/null; then
  useradd -r -g %{service} -G %{service},nobody -d %{_sharedstatedir}/%{service} -s /sbin/nologin -c "OpenStack %{service} Daemons" %{service}
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

%files -n python-%{service}
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests
%exclude %{python2_sitelib}/%{service}/tempest

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests
%{python2_sitelib}/%{service}_tests.egg-info
%{python2_sitelib}/%{service}/tempest

%files api
%defattr(-,root,root,-)
%{_bindir}/%{service}-api
%{_unitdir}/%{name}-api.service

%files common
%{_bindir}/%{service}-config-generator
%{_bindir}/%{service}-change-sack-size
%{_bindir}/%{service}-upgrade
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

%files statsd
%{_bindir}/%{service}-statsd
%{_unitdir}/%{name}-statsd.service

%if 0%{?with_doc}
%files doc
%doc doc/source/
%endif


%changelog
