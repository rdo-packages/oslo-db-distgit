%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%global pypi_name oslo.db
%global pkg_name oslo-db

%if 0%{?fedora} >= 24
%global with_python3 1
%endif
# guard for rhosp obsoletes
%global rhosp 0

%global common_desc \
The OpenStack Oslo database handling library. Provides database connectivity \
to the different backends and helper utils.

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack oslo.db library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{pkg_name}
Summary:        OpenStack oslo.db library

%{?python_provide:%python_provide python2-%{pkg_name}}

%if 0%{rhosp} == 1
Obsoletes: python-%{pkg_name}-tests < %{version}-%{release}
Obsoletes: python2-%{pkg_name}-tests < %{version}-%{release}
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
# test requirements
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-oslo-config
BuildRequires:  python2-six
BuildRequires:  python2-fixtures
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-context
# Required to compile translation files
BuildRequires:  python2-babel
%if 0%{?fedora} > 0
BuildRequires:  python2-migrate
BuildRequires:  python2-alembic
BuildRequires:  python2-psycopg2
BuildRequires:  python2-testresources
BuildRequires:  python2-testscenarios
%else
BuildRequires:  python-migrate
BuildRequires:  python-alembic
BuildRequires:  python-psycopg2
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
%endif

Requires:       MySQL-python
Requires:       python2-PyMySQL
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-six >= 1.10.0
Requires:       python2-sqlalchemy >= 1.0.10
Requires:       python2-stevedore >= 1.20.0
Requires:       python2-pbr
Requires:       python2-debtcollector >= 1.2.0
%if 0%{?fedora} > 0
Requires:       python2-alembic >= 0.9.6
Requires:       python2-migrate >= 0.11.0
%else
Requires:       python-alembic >= 0.9.6
Requires:       python-migrate >= 0.11.0
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo database handling library

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{pkg_name}-doc
%{common_desc}

Documentation for the Oslo database handling library.
%endif

%package -n python2-%{pkg_name}-tests
Summary:    test subpackage for the Oslo database handling library
%{?python_provide:%python_provide python2-%{pkg_name}-tests}

Requires:  python2-%{pkg_name} = %{version}-%{release}
Requires:  python2-oslo-utils
Requires:  python2-oslo-config
Requires:  python2-six
Requires:  python2-fixtures
Requires:  python2-oslotest
%if 0%{?fedora} > 0
Requires:  python2-alembic
Requires:  python2-migrate
Requires:  python2-psycopg2
Requires:  python2-testresources
Requires:  python2-testscenarios
%else
Requires:  python-alembic
Requires:  python-migrate
Requires:  python-psycopg2
Requires:  python-testresources
Requires:  python-testscenarios
%endif

%description -n python2-%{pkg_name}-tests
%{common_desc}

Test subpackage for the Oslo database handling library.

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.db library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# test requirements
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-config
BuildRequires:  python3-six
BuildRequires:  python3-alembic
BuildRequires:  python3-fixtures
BuildRequires:  python3-migrate
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-context
BuildRequires:  python3-psycopg2

Requires:       MySQL-python3
Requires:       python3-PyMySQL
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-alembic >= 0.9.6
Requires:       python3-migrate >= 0.11.0
Requires:       python3-six >= 1.10.0
Requires:       python3-sqlalchemy >= 1.0.10
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-pbr
Requires:       python3-debtcollector >= 1.2.0
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%package -n python3-%{pkg_name}-tests
Summary:    test subpackage for the Oslo database handling library
%{?python_provide:%python_provide python2-%{pkg_name}-tests}

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-oslo-utils
Requires:  python3-oslo-config
Requires:  python3-six
Requires:  python3-fixtures
Requires:  python3-oslotest
Requires:  python3-alembic
Requires:  python3-migrate
Requires:  python3-psycopg2
Requires:  python3-testresources
Requires:  python3-testscenarios

%description -n python3-%{pkg_name}-tests
%{common_desc}

Test subpackage for the Oslo database handling library.
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo db library

%description -n python-%{pkg_name}-lang
%{common_desc}

Translation files for Oslo db library

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_db/locale

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_db/locale/*/LC_*/oslo_db*po
rm -f %{buildroot}%{python2_sitelib}/oslo_db/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_db/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_db/locale
%endif

# Find language files
%find_lang oslo_db --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_db
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_db/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_db/tests

%files -n python-%{pkg_name}-lang -f oslo_db.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_db
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_db/tests

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_db/tests
%endif

%changelog
