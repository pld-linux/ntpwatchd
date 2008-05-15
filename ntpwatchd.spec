Summary:	Small CAMK ntp client
Name:		ntpwatchd
Version:	0.1
Release:	1
License:	GPL/BSD/Perl/Apache
Group:		Daemons
URL:		http://users.camk.edu.pl/ntpwatchd
# http://users.camk.edu.pl/chris/ntpwatchd/ntpwatchd-0.1-3kl.src.rpm
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	d84a9eb88030db9879cee75bebdda7d0
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-libexec.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Very simple SNTP daemon

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
ln -s %{_includedir}/sys/timex.h
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,%{_sbindir}}
cp ntpwatchd ntpwatchd.pl $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ntpwatchd
%service ntpwatchd restart "ntpwatchd daemon"

%preun
if [ "$1" = "0" ]; then
	%service ntpwatchd stop
	/sbin/chkconfig --del ntpwatchd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/ntpwatchd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
