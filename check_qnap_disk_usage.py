#!/usr/bin/python2.7
#
#   Copyright 2013 Daisuke Miyakawa (d.miyakawa@gmail.com)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
A script that checks remaining disk space of QNAP NAS storage in percent.
Tested with QNAP TS-219P II.

SNMP will be used, so netsnmp library should be installed on the host.
(In Debian, "libsnmp-python" will be what you probably want)

QNAP returns string forms of free/total disk spaces with its private
MIB information, which aren't easy for Zabbix to parse.

This script translates those values (e.g. '1.78 TB') into numerical
ones (e.g. 1780000), and then calculate usage rate that is easy
to handle in Zabbix (e.g. 78.80).
"""

import argparse
import netsnmp
import re

_r = re.compile('(\d+(?:\.\d+))\s+(TB|GB|KB)')

"""Convert strings provided by QNAP (NAS) to integer form
e.g. 1.79 TB -> 1866465 (unit: KB)

"""
def _convert_to_numeric(org_val):
    m = _r.match(org_val)
    if m:
        unit = m.group(2)
        if unit == 'EB':
            mul = 1000 * 1000 * 1000 * 1000
        elif unit == 'PB':
            mul = 1000 * 1000 * 1000
        elif unit == 'TB':
            mul = 1000 * 1000
        elif unit == 'GB':
            mul = 1000
        else:
            mul = 1
            pass
        return int(float(m.group(1)) * mul)
    else:
        return -1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('A script that checks'
                                                  ' remaining disk space of'
                                                  ' QNAP NAS storage in percent.'))
    parser.add_argument('hostname', type=str,
                        help='QNAP hostname ready for SNMP access')
    parser.add_argument('-c', '--community', type=str, default='public',
                        help='SNMP community to be used')
    parser.add_argument('-v', '--version', type=str, default='2c',
                        help='SNMP version to be used (1, 2c, 3)')
    args = parser.parse_args()

    if args.version == '2c':
        version = 2
    else:
        version = int(args.version)
        pass

    oid_total_storage = netsnmp.Varbind('enterprises.24681.1.2.17.1.4.1')
    oid_free_storage = netsnmp.Varbind('enterprises.24681.1.2.17.1.5.1')
    session = netsnmp.Session(Version=version,
                              DestHost=args.hostname,
                              Community=args.community)
    result = session.get(netsnmp.VarList(oid_total_storage, oid_free_storage))
    total = _convert_to_numeric(result[0])
    free = _convert_to_numeric(result[1])

    print(float(free)/total * 100)

