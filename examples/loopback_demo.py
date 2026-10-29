#!/usr/bin/env python3
"""Demonstrate a successful and a refused TCP check on local loopback."""
from pathlib import Path
import socket
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_connection import check_connection


def main():
    host = '127.0.0.1'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, 0))
        server.listen(1)
        server.settimeout(3)
        port = server.getsockname()[1]
        accepted = []

        def accept_one():
            try:
                connection, _ = server.accept()
                with connection:
                    accepted.append(True)
            except socket.timeout:
                pass

        thread = threading.Thread(target=accept_one, daemon=True)
        thread.start()
        success = check_connection(host, port, timeout=2)
        thread.join(timeout=4)
        if not success['connected'] or not accepted:
            raise RuntimeError('Local connection test did not succeed')
        print(f"Listening service: connected to {success['peer']}:{port}")

    failure = check_connection(host, port, timeout=2)
    if failure['connected']:
        raise RuntimeError('Port was reused after the test service stopped; try again')
    print(f"Stopped service: {failure['error']}")
    print('Completed: observed one successful and one unsuccessful loopback connection.')


if __name__ == '__main__':
    main()
