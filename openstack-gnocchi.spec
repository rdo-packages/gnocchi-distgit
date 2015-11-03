%global pypi_name gnocchi
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-gnocchi
Version:	1.3.0
Release:	1%{?dist}
Summary:        Gnocchi is a API to store metrics and index resources

License:	APL 2.0
URL:		http://github.com/openstack/gnocchi
Source0:	https://pypi.python.org/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        %{pypi_name}.conf.sample
Source2:        %{pypi_name}.logrotate
Source10:       %{name}-api.service
Source11:       %{name}-metricd.service
Source12:       %{name}-statsd.service
BuildArch:      noarch

BuildRequires:	python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-pbr
BuildRequires:  python2-devel


%description
HTTP API to store metrics and index resources.

%package -n     python-gnocchi
Summary:        OpenStack gnocchi python libraries

Requires:       numpy
Requires:       python-flask
Requires:       python-futures
Requires:	python-jinja2
Requires:       python-keystonemiddleware
Requires:	python-msgpack
Requires:       python-oslo-config
Requires:       python-oslo-db
Requires:       python-oslo-log
Requires:       python-oslo-policy
Requires:       python-oslo-sphinx
Requires:       python-oslo-serialization
Requires:       python-oslo-utils
Requires:       python-pandas
Requires:       python-pecan
Requires:       python-pytimeparse
Requires:       python-retrying
Requires:       python-requests
Requires:       python-swiftclient
Requires:	python-six
Requires:	python-sqlalchemy
Requires:       python-sqlalchemy-utils
Requires:	python-stevedore
Requires:	python-sysv_ipc
Requires:       python-tooz
Requires:	python-trollius
Requires:	python-voluptuous
Requires:	python-werkzeug
Requires:       pytz
Requires:	PyYAML


%description -n   python-gnocchi
OpenStack gnocchi provides API to store metrics from OpenStack components
and index resources.

This package contains the gnocchi python library.


%package        api

Summary:        OpenStack gnocchi api

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-flask
Requires:       python-jinja2
Requires:       python-keystonemiddleware
Requires:       python-oslo-db
Requires:       python-oslo-policy
Requires:       python-oslo-utils
Requires:       python-oslo-serialization
Requires:       python-pecan
Requires:       python-pytimeparse
Requires:       python-requests
Requires:       python-six
Requires:	python-sqlalchemy
Requires:       python-sqlalchemy-utils
Requires:       python-stevedore
Requires:       python-tooz
Requires:       python-voluptuous
Requires:       python-werkzeug
Requires:       PyYAML

%description api
OpenStack gnocchi provides API to store metrics from OpenStack components
and index resources.

This package contains the gnocchi API service.

%package        carbonara

Summary:        OpenStack gnocchi carbonara

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-futures
Requires:       python-msgpack
Requires:       python-oslo-utils
Requires:       python-pandas
Requires:       python-retrying
Requires:       python-swiftclient
Requires:       python-tooz

%description carbonara
OpenStack gnocchi provides API to store metrics from OpenStack
components and index resources.

This package contains the gnocchi carbonara backend including swift,ceph and
file service.


%package        common
Summary:        Components common to all OpenStackk gnocchi services

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-oslo-log
Requires:       python-oslo-utils
Requires:       python-trollius
Requires:       python-six

%description    common
OpenStack gnocchi provides services to measure and
collect metrics from OpenStack components.


%package        indexer-sqlalchemy

Summary:        OpenStack gnocchi indexer sqlalchemy driver

Requires:       python-gnocchi = %{version}-%{release}

Requires:       python-oslo-db
Requires:       python-oslo-utils
Requires:       python-sqlalchemy
Requires:       python-swiftclient
Requires:       python-stevedore
Requires:       pytz

%description indexer-sqlalchemy
OpenStack gnocchi provides API to store metrics from OpenStack
components and index resources.

This package contains the gnocchi indexer with sqlalchemy driver.


%package        metricd

Summary:        OpenStack gnocchi metricd daemon

Requires:       %{name}-common = %{version}-%{release}

%description metricd
OpenStack gnocchi provides API to store metrics from OpenStack
components and index resources.

This package contains the gnocchi metricd daemon


%package        statsd

Summary:        OpenStack gnocchi statsd daemon

Requires:       %{name}-common = %{version}-%{release}

%description statsd
OpenStack gnocchi provides API to store metrics from OpenStack
components and index resources.

This package contains the gnocchi statsd daemon

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack gnocchi

Requires:         python-gnocchi = %{version}-%{release}

%description      doc
OpenStack gnocchi provides services to measure and
collect metrics from OpenStack components.

This package contains documentation files for gnocchi.
%endif


%prep
%setup -q -n gnocchi-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find gnocchi -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build

%{__python2} setup.py build

install -p -D -m 640 %{SOURCE1} etc/gnocchi/gnocchi.conf.sample

%install

%{__python2} setup.py install --skip-build --root %{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/gnocchi/
mkdir -p %{buildroot}/%{_var}/log/%{name}

install -p -D -m 640 etc/gnocchi/gnocchi.conf.sample %{buildroot}%{_sysconfdir}/gnocchi/gnocchi.conf

#TODO(prad): build the docs at run time, once the we get rid of postgres setup dependency

# Configuration
cp -R etc/gnocchi/policy.json %{buildroot}/%{_sysconfdir}/gnocchi

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/gnocchi
install -d -m 755 %{buildroot}%{_sharedstatedir}/gnocchi/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/gnocchi

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install systemd unit services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-metricd.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-statsd.service


%pre common
getent group gnocchi >/dev/null || groupadd -r gnocchi --gid 166
if ! getent passwd gnocchi >/dev/null; then
  # Id reservation request: https://bugzilla.redhat.com/923891
  useradd -u 166 -r -g gnocchi -G gnocchi,nobody -d %{_sharedstatedir}/gnocchi -s /sbin/nologin -c "OpenStack gnocchi Daemons" gnocchi
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

%files -n python-gnocchi
%{python2_sitelib}/gnocchi
%{python2_sitelib}/gnocchi-*.egg-info

%files api
%defattr(-,root,root,-)
%{_bindir}/gnocchi-api
%{_unitdir}/%{name}-api.service

%files carbonara
%{_bindir}/carbonara-create
%{_bindir}/carbonara-dump
%{_bindir}/carbonara-update

%files common
%dir %{_sysconfdir}/gnocchi
%config(noreplace) %attr(-, root, gnocchi) %{_sysconfdir}/gnocchi/policy.json
%config(noreplace) %attr(-, root, gnocchi) %{_sysconfdir}/gnocchi/gnocchi.conf
%config(noreplace) %attr(-, root, gnocchi) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0755, gnocchi, root)  %{_localstatedir}/log/gnocchi

%defattr(-, gnocchi, gnocchi, -)
%dir %{_sharedstatedir}/gnocchi
%dir %{_sharedstatedir}/gnocchi/tmp


%files indexer-sqlalchemy
%{_bindir}/gnocchi-dbsync

%files metricd
%{_bindir}/gnocchi-metricd
%{_unitdir}/%{name}-metricd.service

%files statsd
%{_bindir}/gnocchi-statsd
%{_unitdir}/%{name}-statsd.service

%if 0%{?with_doc}
%files doc
%doc doc/source/
%endif


%changelog
* Tue Nov 03 2015 Alan Pevec <apevec@redhat.com> - 1.3.0-1
- Update to 1.3.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 27 2015 Pradeep Kilambi <pkilambi@redhat.com> 1.0.0-1
- initial package release
