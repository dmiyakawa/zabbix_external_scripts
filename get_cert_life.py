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
import socket
import ssl
import time

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=('A script that checks certificate '
                                                'freshness'))
  parser.add_argument('hostname', type=str, help='hostname for a SSL server')
  parser.add_argument('--port', '-p', help='port', default='443')
  parser.add_argument('--original', '-o', help='show original longevity instead',
                      action='store_true')

  args = parser.parse_args()

  ssl_sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                             ca_certs='/etc/ssl/certs/ca-certificates.crt',
                             cert_reqs=ssl.CERT_REQUIRED)
  ssl_sock.connect((args.hostname, int(args.port)))

  notAfter = ssl.cert_time_to_seconds(ssl_sock.getpeercert()['notAfter'])
  day = 60 * 60 * 24
  if args.original:
    notBefore = ssl.cert_time_to_seconds(ssl_sock.getpeercert()['notBefore'])
    print (int((notAfter - notBefore) / day))
  else:
    t = time.time()
    print(int((notAfter - t) / day))
