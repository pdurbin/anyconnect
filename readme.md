# RPM spec file for Cisco AnyConnect VPN client

The section on system requirements for Linux in the [AnyConnect release notes][1] indicates that the only Red Hat distribution validated by Cisco is Red Hat Enterprise Linux 5 Desktop and that the software "reportedly runs on 64-bit Linux, although we do not support it."

However, running `rpmbuild -ba anyconnect.spec` on the spec file in this repo results in an RPM that is known to work on x86_64 versions of both CentOS 6 and Fedora 16.  Before building, one must download the anyconnect-predeploy-linux tarballs from Cisco and place them in `~/rpmbuild/SOURCES` or equivalent.

[1]: http://www.cisco.com/en/US/docs/security/vpn_client/anyconnect/anyconnect30/release/notes/anyconnect30rn.html#wp949967
