# RPM spec file for Cisco AnyConnect VPN client

The section on system requirements for Linux in the [AnyConnect release notes][1] indicates that the only Red Hat distribution validated by Cisco is Red Hat Enterprise Linux 5 Desktop and that the software "reportedly runs on 64-bit Linux, although we do not support it."

However, running `rpmbuild -ba anyconnect.spec` on the spec file in this repo results in an RPM that is known to work on x86_64 versions of both CentOS 6 and Fedora 16.  Before building, one must download the anyconnect-predeploy-linux tarballs from Cisco and place them in `~/rpmbuild/SOURCES` or equivalent.

[1]: http://www.cisco.com/en/US/docs/security/vpn_client/anyconnect/anyconnect30/release/notes/anyconnect30rn.html#wp949967

---

For more discussion about this RPM, please see:

* Announcing a spec file for Cisco AnyConnect VPN client - http://lists.repoforge.org/pipermail/users/2012-February/022723.html
* 64-bit anyconnect on linux - problems with libraries - Cisco Support Community - https://supportforums.cisco.com/message/3566916#3566916
* ha! finally! i have a working centos6 cisco anyconnect vpn rpm! \o/ - http://irclog.perlgeek.de/crimsonfu/2012-02-13#i_5143886
* nice! some guy just emailed me an RPM spec - https://plus.google.com/107770072576338242009/posts/Jr6nX8jYMVh
* Getting the Cisco AnyConnect VPN Client to work on CentOS 6 x86_64 - http://people.fas.harvard.edu/~pdurbin/blog/2011/09/15/getting-the-cisco-anyconnect-vpn-client-to-work-on-centos-6-x86_64.html

---

You might also consider http://openvpn.net/index.php/open-source.html
