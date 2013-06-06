#!/usr/bin/python3
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

import argparse
import urllib.request
import re

_tr72w_status_path = 'B/CrrntData/cData.txt'
_r_t = re.compile('^cTemperature1=(\d+(?:\.\d+)?)\D+$', flags=re.MULTILINE)
_r_h = re.compile('^cHumidity=(\d+(?:\.\d+)?)\D+$', flags=re.MULTILINE)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A script that checks TR-72W status.')
    parser.add_argument('hostname', type=str, help='hostname for TR-72W')
    parser.add_argument('--type', '-t', type=str, default='t',
                        help='What kind of parameter do you want.'
                        ' t: temperature, h: humidity.')
    args = parser.parse_args()
    url = 'http://%s/%s' % (args.hostname, _tr72w_status_path)
    lines = urllib.request.urlopen(url).read().decode('utf-8')
    if args.type == 'h':
        m = _r_h.search(lines)
    else:
        m = _r_t.search(lines)
        pass
    if m:
        print(m.group(1))
    pass
