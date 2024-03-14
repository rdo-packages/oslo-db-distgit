%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order pifpaf
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc 1
%global pypi_name oslo.db
%global pkg_name oslo-db

# guard for rhosp obsoletes
%global rhosp 0

%global common_desc \
The OpenStack Oslo database handling library. Provides database connectivity \
to the different backends and helper utils.

Name:           python-%{pkg_name}
Version:        15.0.0
Release:        1%{?dist}
Summary:        OpenStack oslo.db library

License:        Apache-2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.db library


%if 0%{rhosp} == 1
Obsoletes: python-%{pkg_name}-tests < %{version}-%{release}
%endif

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires:       python-%{pkg_name}-lang = %{version}-%{release}
Requires:       python-%{pkg_name}+mysql = %{version}-%{release}

# pynacl is not defined upstream, so we have to keep the requires explicitly.
# More information in https://review.rdoproject.org/r/c/openstack/oslo-db-distgit/+/29883
%if 0%{?rhosp} == 0
Requires:       python3-pynacl
%endif

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo database handling library

%description -n python-%{pkg_name}-doc
%{common_desc}

Documentation for the Oslo database handling library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    test subpackage for the Oslo database handling library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-oslo-utils
Requires:  python3-oslo-config
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

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo db library

%description -n python-%{pkg_name}-lang
%{common_desc}

Translation files for Oslo db library

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/doc8/d' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_doc}
# generate html docs
PYTHONPATH="%{buildroot}/%{python3_sitelib}"
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_db/locale --domain oslo_db


# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_db/locale/*/LC_*/oslo_db*po
rm -f %{buildroot}%{python3_sitelib}/oslo_db/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_db/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_db --all-name

%check
%tox -e %{default_toxenv}

%pyproject_extras_subpkg -n python3-%{pkg_name} mysql

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_db
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/oslo_db/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_db/tests

%files -n python-%{pkg_name}-lang -f oslo_db.lang
%license LICENSE

%changelog
* Thu Mar 14 2024 RDO <dev@lists.rdoproject.org> 15.0.0-1
- Update to 15.0.0

