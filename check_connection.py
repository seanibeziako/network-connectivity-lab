#!/usr/bin/env python3
"""Resolve one host and test a single TCP port, using only the standard library."""
import argparse
import ipaddress
import socket
import sys


def check_connection(host, port, timeout=3.0):
    """Return a report; TCP timeouts do not bound the system DNS resolver."""
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        return {"host": host, "port": port, "addresses": [], "connected": False,
                "error": f"DNS lookup failed: {exc}"}
    addresses = sorted({entry[4][0] for entry in infos}, key=lambda x: (ipaddress.ip_address(x).version, x))
    try:
        with socket.create_connection((host, port), timeout=timeout) as connection:
            peer = connection.getpeername()
            return {"host": host, "port": port, "addresses": addresses,
                    "connected": True, "peer": peer[0]}
    except OSError as exc:
        return {"host": host, "port": port, "addresses": addresses,
                "connected": False, "error": f"TCP connection failed: {exc}"}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Resolve one host and test one TCP port.')
    parser.add_argument('host', help='Hostname or IP address you are authorized to test')
    parser.add_argument('port', type=int, help='TCP port from 1 to 65535')
    parser.add_argument('--timeout', type=float, default=3.0, help='TCP connection timeout in seconds')
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error('port must be between 1 and 65535')
    if not 0 < args.timeout <= 60:
        parser.error('timeout must be greater than 0 and at most 60 seconds')
    result = check_connection(args.host, args.port, args.timeout)
    print(f"Host: {result['host']}  Port: {result['port']}")
    print('Resolved addresses: ' + (', '.join(result['addresses']) or 'none'))
    if result['connected']:
        print(f"TCP: connected to {result['peer']}")
        return 0
    print(result['error'], file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
