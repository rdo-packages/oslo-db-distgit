%global pypi_name oslo.db
%global pkg_name oslo-db

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pkg_name}
Version:        4.6.0
Release:        1%{?dist}
Summary:        OpenStack oslo.db library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%description
The OpenStack Oslo database handling library. Provides database connectivity
to the different backends and helper utils.

%package -n python2-%{pkg_name}
Summary:        OpenStack oslo.db library

%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
# test requirements
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-config
BuildRequires:  python-six
BuildRequires:  python-alembic
BuildRequires:  python-fixtures
BuildRequires:  python-migrate
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  python-oslotest
BuildRequires:  python-oslo-context
BuildRequires:  python-psycopg2

Requires:       MySQL-python
Requires:       python-PyMySQL
Requires:       python-oslo-config >= 2:2.3.0
Requires:       python-oslo-context >= 0.2.0
Requires:       python-oslo-i18n >= 1.5.0
Requires:       python-oslo-utils >= 2.0.0
Requires:       python-alembic >= 0.8.0
Requires:       python-babel
Requires:       python-iso8601
Requires:       python-migrate >= 0.9.6
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 0.9.9
Requires:       python-stevedore >= 1.5.0
Requires:       python-pbr

%description -n python2-%{pkg_name}
The OpenStack Oslo database handling library. Provides database connectivity
to the different backends and helper utils.


%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo database handling library

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python-%{pkg_name}-doc
Documentation for the Oslo database handling library.

%package -n python-%{pkg_name}-tests
Summary:    test subpackage for the Oslo database handling library

Requires:  python-%{pkg_name} = %{version}-%{release}
Requires:  python-oslo-utils
Requires:  python-oslo-config
Requires:  python-six
Requires:  python-alembic
Requires:  python-fixtures
Requires:  python-migrate
Requires:  python-testresources
Requires:  python-testscenarios
Requires:  python-oslotest
Requires:  python-oslo-context
Requires:  python-psycopg2

%description -n python-%{pkg_name}-tests
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
Requires:       python3-oslo-config >= 2:2.3.0
Requires:       python3-oslo-context >= 0.2.0
Requires:       python3-oslo-i18n >= 1.5.0
Requires:       python3-oslo-utils >= 2.0.0
Requires:       python3-alembic >= 0.8.0
Requires:       python3-babel
Requires:       python3-iso8601
Requires:       python3-migrate >= 0.9.6
Requires:       python3-six >= 1.9.0
Requires:       python3-sqlalchemy >= 0.9.9
Requires:       python3-stevedore >= 1.5.0
Requires:       python3-pbr

%description -n python3-%{pkg_name}
The OpenStack Oslo database handling library. Provides database connectivity
to the different backends and helper utils.
%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f requirements.txt

%build
%py2_build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

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

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%files -n python-%{pkg_name}-tests
%{python2_sitelib}/oslo_db/tests

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_db
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_db/tests
%endif

%changelog
* Wed Mar 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 4.6.0-
- Update to 4.6.0

