# Created by pyp2rpm-1.1.0b
%global pypi_name oslo.db

Name:           python-oslo-db
Version:        2.6.0
Release:        4%{?dist}
Summary:        OpenStack oslo.db library

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr

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
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-config
BuildRequires:  python-six
BuildRequires:  python-alembic
BuildRequires:  python-fixtures
BuildRequires:  python-migrate
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios

%description doc
Documentation for the Oslo database handling library.


%prep
%setup -q -n %{pypi_name}-%{version}

# Let RPM handle the dependencies
rm -f requirements.txt


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
%{python2_sitelib}/oslo_db
%{python2_sitelib}/*.egg-info

%files doc
%doc html LICENSE

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Alan Pevec <alan.pevec@redhat.com> 2.6.0-3
- Add python-PyMySQL to requirements (Javier Pena)

* Mon Nov 09 2015 Alan Pevec <alan.pevec@redhat.com> 2.6.0-2
- Add MySQL-python dependency (Ihar Hrachyshka)

* Thu Sep 17 2015 Alan Pevec <alan.pevec@redhat.com> 2.6.0-1
- Update to upstream 2.6.0

* Thu Sep 03 2015 Alan Pevec <alan.pevec@redhat.com> 2.4.1-1
- Update to upstream 2.4.1

* Mon Aug 17 2015 Alan Pevec <alan.pevec@redhat.com> 2.3.0-1
- Update to upstream 2.3.0

* Tue Jul 07 2015 Alan Pevec <alan.pevec@redhat.com> 1.7.2-1
- Update to upstream 1.7.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Alan Pevec <alan.pevec@redhat.com> 1.7.1-1
- Update to 1.7.1

* Tue Oct 07 2014 Alan Pevec <alan.pevec@redhat.com> 1.0.2-2
- keep trying to connect to the database on startup rhbz#1144181

* Thu Oct 02 2014 Alan Pevec <alan.pevec@redhat.com> 1.0.2-1
- Update to upstream 1.0.2

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
