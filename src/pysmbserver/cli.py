#!/usr/bin/env python

import argparse

from pysmbserver import logger
from pysmbserver.smbserver import SimpleSMBServer

def main():
    parser = argparse.ArgumentParser(add_help = True, description = "This script will launch a SMB Server and add a "
                                        "share specified as an argument. Usually, you need to be root in order to bind to port 445. "
                                        "For optional authentication, it is possible to specify username and password or the NTLM hash. "
                                        "Example: smbserver.py -comment 'My share' TMP /tmp")

    parser.add_argument('shareName', action='store', help='name of the share to add')
    parser.add_argument('sharePath', action='store', help='path of the share to add')
    parser.add_argument('-comment', action='store', default='', help='share\'s comment to display when asked for shares')
    parser.add_argument('-username', action="store", help='Username to authenticate clients')
    parser.add_argument('-password', action="store", nargs='?', const=None, help='Password for the Username')
    parser.add_argument('-hashes', action="store", metavar = "LMHASH:NTHASH", help='NTLM hashes for the Username, format is LMHASH:NTHASH')
    parser.add_argument('-ts', action='store_true', help='Adds timestamp to every logging output')
    parser.add_argument('-debug', action='store_true', help='Turn DEBUG output ON')
    parser.add_argument('-ip', '--interface-address', action='store', default=argparse.SUPPRESS, help='ip address of listening interface ("0.0.0.0" or "::" if omitted)')
    parser.add_argument('-port', action='store', default='445', help='TCP port for listening incoming connections (default 445)')
    parser.add_argument('-dropssp', action='store_true', default=False, help='Disable NTLM ESS/SSP during negotiation')
    parser.add_argument('-6','--ipv6', action='store_true',help='Listen on IPv6')
    parser.add_argument('-smb2support', action='store_true', default=False, help='SMB2 Support (experimental!)')
    parser.add_argument('-outputfile', action='store', default=None, help='Output file to log smbserver output messages')

    options = parser.parse_args()

    logger.init(options.ts, options.debug)

    if 'interface_address' not in options:
        options.interface_address = '::' if options.ipv6 else '0.0.0.0'

    server = SimpleSMBServer(listenAddress=options.interface_address, listenPort=int(options.port), ipv6=options.ipv6)

    if options.outputfile:
        server.setLogFile(options.outputfile)

    server.addShare(options.shareName, options.sharePath, options.comment)
    server.setSMB2Support(options.smb2support)
    server.setDropSSP(options.dropssp)

    if options.username is not None:
        server.addCredential(options.username, password=options.password, hashes=options.hashes)

    server.start()

if __name__ == '__main__':
    main()