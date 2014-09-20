# Created by pyp2rpm-1.1.0b
%global pypi_name oslo.db

Name:           python-oslo-db
Version:        1.0.1
Release:        1%{?dist}
Summary:        OpenStack oslo.db library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr

Requires:       python-oslo-config >= 1:1.4.0.0
Requires:       python-oslo-i18n
Requires:       python-oslo-utils
Requires:       python-alembic >= 0.6.4
Requires:       python-babel
Requires:       python-iso8601
Requires:       python-sqlalchemy >= 0.8.4
Requires:       python-migrate >= 0.9.1
Requires:       python-stevedore >= 0.14


%description
The OpenStack Oslo database handling library. Provides database connectivity
to the different backends and helper utils.
* Documentation: http://docs.openstack.org/developer/oslo.db
* Source: http://git.openstack.org/cgit/openstack/oslo.db
* Bugs: http://bugs.launchpad.net/oslo


%package doc
Summary:    Documentation for the Oslo database handling library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for the Oslo database handling library.


%prep
%setup -q -n %{pypi_name}-%{version}
# Let RPM handle the dependencies
rm -f requirements.txt
# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py


%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%files
%doc README.rst LICENSE
%{python2_sitelib}/oslo
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*-nspkg.pth

%files doc
%doc html LICENSE

%changelog
* Sat Sep 20 2014 Alan Pevec <apevec@redhat.com> - 1.0.1-1
- Update to upstream 1.0.1

* Wed Sep 17 2014 Alan Pevec <apevec@redhat.com> - 0.5.0-1
- Update to upstream 0.5.0

* Thu Sep 11 2014 Alan Pevec <apevec@redhat.com> - 0.4.0-2
- update dependencies

* Wed Aug 20 2014 Alan Pevec <apevec@redhat.com> - 0.4.0-1
- update to 0.4.0

* Wed Aug 06 2014 Alan Pevec <apevec@redhat.com> - 0.3.0-2
- rebuild with original egginfo, pbr cannot regenerate SOURCES.txt without git

* Thu Jul 31 2014 Alan Pevec <apevec@redhat.com> - 0.3.0-1
- Initial package.
