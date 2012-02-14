%define debug_package %{nil}

Name:		anyconnect
Version:	3.0.4235
Release:	2%{?dist}
Summary:	Cisco AnyConnect Secure Mobility Client

License:	GPLv2 with exceptions
URL:		http://www.cisco.com/
Source0:	anyconnect-predeploy-linux-%{version}-k9.tar.gz
Source1:	anyconnect-predeploy-linux-64-%{version}-k9.tar.gz

#BuildRequires:		chrpath
BuildRequires:		desktop-file-utils

Requires:		hicolor-icon-theme
Requires:		nspr nss
Requires(post):		/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service


%description
The Cisco AnyConnect Secure Mobility client provides remote
users with secure VPN connections to the Cisco ASA 5500 Series
Adaptive Security Appliance using the Secure Socket Layer (SSL)
protocol and the Datagram TLS (DTLS) protocol. 

%prep
%ifarch %{ix86}
%setup -q
%endif
%ifarch x86_64
%setup -q -T -b 1
%endif

%build
vpn/manifesttool -i vpn vpn/ACManifestVPN.xml

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}/opt/cisco/vpn/bin
mkdir -p %{buildroot}/opt/cisco/anyconnect/{script,profile,pixmaps,l10n,lib}
mkdir -p %{buildroot}/opt/cisco/anyconnect/bin/plugins
mkdir -p %{buildroot}/opt/.cisco/certificates/ca
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/desktop-directories/
mkdir -p %{buildroot}/etc/xdg/menus/applications-merged/
mkdir -p %{buildroot}/usr/local
#mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d

cd vpn

for i in AnyConnectLocalPolicy.xsd OpenSource.html update.txt AnyConnectProfile.xsd VPNManifest.dat; do
	%{__install} -p -m 644 $i %{buildroot}/opt/cisco/anyconnect/
done

for i in libcrypto.so libcurl.so.3.0.0 libssl.so libvpnagentutilities.so libvpnapi.so libvpncommoncrypt.so libvpncommon.so; do
	%{__install} -p -m 755 $i %{buildroot}/opt/cisco/anyconnect/lib/
done



for i in vpn vpnagentd vpndownloader vpnui manifesttool; do
	%{__install} -p -m 755 $i %{buildroot}/opt/cisco/anyconnect/bin/
done

%{__install} -p -m 755 libvpnipsec.so %{buildroot}/opt/cisco/anyconnect/bin/plugins/
%{__install} -p -m 644 AnyConnectProfile.xsd %{buildroot}/opt/cisco/anyconnect/profile/
%{__install} -p -m 644 pixmaps/* %{buildroot}/opt/cisco/anyconnect/pixmaps/

%{__install} -p -m 755 VeriSignClass3PublicPrimaryCertificationAuthority-G5.pem %{buildroot}/opt/.cisco/certificates/ca

ln -sf /opt/cisco/anyconnect/update.txt %{buildroot}/opt/cisco/vpn/update.txt
ln -sf /opt/cisco/anyconnect/bin/manifesttool %{buildroot}/opt/cisco/vpn/manifesttool
ln -sf /opt/cisco/anyconnect/bin/vpndownloader %{buildroot}/opt/cisco/vpn/vpndownloader
ln -sf /opt/cisco/anyconnect/update.txt %{buildroot}/opt/cisco/vpn/update.txt

# Stupid linking:
# strings /opt/cisco/anyconnect/lib/libvpncommoncrypt.so | grep -i firefox
ln -sf %{_libdir}/libnss3.so %{buildroot}/opt/cisco/anyconnect/lib/libnss3.so
ln -sf %{_libdir}/libsmime3.so %{buildroot}/opt/cisco/anyconnect/lib/libsmime3.so
ln -sf /%{_lib}/libplc4.so %{buildroot}/opt/cisco/anyconnect/lib/libplc4.so
ln -sf /%{_lib}/libnspr4.so %{buildroot}/opt/cisco/anyconnect/lib/libnspr4.so
ln -sf /opt/cisco/anyconnect/lib %{buildroot}/usr/local/firefox
ln -sf libcurl.so.3.0.0 %{buildroot}/opt/cisco/anyconnect/lib/libcurl.so.3

cat > %{buildroot}/opt/cisco/vpn/vpndownloader.sh << EOF
ERRVAL=0
/opt/cisco/anyconnect/bin/vpndownloader "$*" || ERRVAL=$?
exit ${ERRVAL}
EOF

#/usr/share/mime/application/x-cisco-vpn-settings.xml

# Menu items
desktop-file-install --dir=%{buildroot}%{_datadir}/applications cisco-anyconnect.desktop
%{__install} -p -m 644 cisco-anyconnect.directory %{buildroot}%{_datadir}/desktop-directories/
%{__install} -p -m 644 cisco-anyconnect.menu %{buildroot}/etc/xdg/menus/applications-merged/

%{__install} -m 755 -D vpnagentd_init %{buildroot}%{_initrddir}/vpnagentd_init

# Fix perms
chmod +s %{buildroot}/opt/cisco/anyconnect/bin/vpnagentd

# Stupid rpath:
# chrpath vpnagentd vpn vpnui
#echo "/opt/cisco/anyconnect/lib/" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/cisco-anyconnect.conf
#chrpath -d %{buildroot}/opt/cisco/anyconnect/bin/vpnagentd \
#	%{buildroot}/opt/cisco/anyconnect/bin/vpn \
#	%{buildroot}/opt/cisco/anyconnect/bin/vpnui

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/sbin/ldconfig
/sbin/chkconfig --add vpnagentd_init

%preun
if [ "$1" = 0 ]; then
	/sbin/service vpnagentd_init stop >/dev/null 2>&1 || :
	/sbin/chkconfig --del vpnagentd_init
fi

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
	/sbin/service vpnagentd_init condrestart >/dev/null 2>&1 || :
	/sbin/ldconfig
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc vpn/license.txt
/opt/cisco/
/opt/.cisco/
%{_datadir}/applications/cisco-anyconnect.desktop
%{_datadir}/desktop-directories/cisco-anyconnect.directory
%{_sysconfdir}/xdg/menus/applications-merged/cisco-anyconnect.menu
#%{_sysconfdir}/ld.so.conf.d/cisco-anyconnect.conf
%{_initrddir}/vpnagentd_init
/usr/local/firefox


%changelog
* Mon Feb 13 2012 Simone Caronni <negativo17@gmail.com> - 3.0.4235-2
- Added missing symlink and desktop-file-utils as BuildRequires.

* Sun Jan 14 2012 Simone Caronni <negativo17@gmail.com> - 3.0.4235-1
- First build.

