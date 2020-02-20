# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%global pypi_name oslo.db
%global pkg_name oslo-db

# guard for rhosp obsoletes
%global rhosp 0

%global common_desc \
The OpenStack Oslo database handling library. Provides database connectivity \
to the different backends and helper utils.

Name:           python-%{pkg_name}
Version:        5.0.2
Release:        2%{?dist}
Summary:        OpenStack oslo.db library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{pkg_name}
Summary:        OpenStack oslo.db library

%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

%if 0%{rhosp} == 1
Obsoletes: python-%{pkg_name}-tests < %{version}-%{release}
Obsoletes: python2-%{pkg_name}-tests < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
# test requirements
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-context
# Required to compile translation files
BuildRequires:  python%{pyver}-babel
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-migrate
BuildRequires:  python-alembic
BuildRequires:  python-psycopg2
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
%else
BuildRequires:  python%{pyver}-migrate
BuildRequires:  python%{pyver}-alembic
BuildRequires:  python%{pyver}-psycopg2
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-testscenarios
%endif

Requires:       python%{pyver}-PyMySQL
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-sqlalchemy >= 1.0.10
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-debtcollector >= 1.2.0
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-alembic >= 0.9.6
Requires:       python-migrate >= 0.11.0
%else
Requires:       python%{pyver}-alembic >= 0.9.6
Requires:       python%{pyver}-migrate >= 0.11.0
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo database handling library

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{pkg_name}-doc
%{common_desc}

Documentation for the Oslo database handling library.
%endif

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    test subpackage for the Oslo database handling library

Requires:  python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires:  python%{pyver}-oslo-utils
Requires:  python%{pyver}-oslo-config
Requires:  python%{pyver}-six
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-oslotest
# Handle python2 exception
%if %{pyver} == 2
Requires:  python-alembic
Requires:  python-migrate
Requires:  python-psycopg2
Requires:  python-testresources
Requires:  python-testscenarios
%else
Requires:  python%{pyver}-alembic
Requires:  python%{pyver}-migrate
Requires:  python%{pyver}-psycopg2
Requires:  python%{pyver}-testresources
Requires:  python%{pyver}-testscenarios
%endif

%description -n python%{pyver}-%{pkg_name}-tests
%{common_desc}

Test subpackage for the Oslo database handling library.

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
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_db/locale

%install
%{pyver_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_db/locale/*/LC_*/oslo_db*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_db/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_db/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_db --all-name

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{pkg_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/oslo_db
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_db/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_db/tests

%files -n python-%{pkg_name}-lang -f oslo_db.lang
%license LICENSE

%changelog
* Thu Oct 03 2019 Joel Capitao <jcapitao@redhat.com> 5.0.2-2
- Removed python2 subpackages in no el7 distros

* Wed Sep 18 2019 RDO <dev@lists.rdoproject.org> 5.0.2-1
- Update to 5.0.2

