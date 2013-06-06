# About this repo

Contains a few "external scripts" for Zabbix.

This doesn't care any enviromental dependency things.
Linux, Python and some more will be implicitly required.

All scripts are licensed under Apache License 2.0.

## check_tr72w.py

TR72W is a temperature & humidity data logger that allows external
servers to fetch such info. This script checks those info and
send them back to the (Zabbix) server.

## check_qnap_disk_usage.py

This script checks remaining disk space of QNAP NAS storage in percent.
Tested with QNAP TS-219P II.

Python's netsnmp library should be installed on the (Zabbix) server.
(In Debian, "libsnmp-python" will be what you probably want)

QNAP returns string forms of free/total disk spaces with its private
MIB information, which aren't easy for Zabbix to parse.

This script translates those values (e.g. '1.78 TB') into numerical
ones (e.g. 1780000), and then calculate usage rate that is easy
to handle in Zabbix (e.g. 78.80).

## check_cert_status.py

This script connects to a given ssl server and check the cert's
freshness (by seeing 'notBefore/notAfter' section).

Two values will be returned:

* The first one tells remaining days of life (in days)
* The second one tells a specified longevity (in days == notAfter - notBefore)

