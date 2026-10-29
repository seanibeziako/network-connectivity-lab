import socket
import threading
import unittest
from unittest.mock import patch
from check_connection import check_connection, main

class ConnectivityChecks(unittest.TestCase):
    def test_loopback_tcp_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(('127.0.0.1', 0))
            server.listen(1)
            port = server.getsockname()[1]
            accepted = []
            def receive():
                connection, _ = server.accept()
                with connection:
                    accepted.append(True)
            thread = threading.Thread(target=receive, daemon=True)
            thread.start()
            result = check_connection('127.0.0.1', port, 2)
            thread.join(timeout=2)
            self.assertTrue(result['connected'])
            self.assertEqual(result['peer'], '127.0.0.1')
            self.assertTrue(accepted)

    def test_dns_failure_reported(self):
        with patch('socket.getaddrinfo', side_effect=socket.gaierror('no such host')):
            result = check_connection('invalid.example', 443)
        self.assertFalse(result['connected'])
        self.assertIn('DNS lookup failed', result['error'])

    def test_tcp_failure_reported(self):
        info = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', 80))]
        with patch('socket.getaddrinfo', return_value=info), patch('socket.create_connection', side_effect=ConnectionRefusedError('refused')):
            result = check_connection('127.0.0.1', 80)
        self.assertFalse(result['connected'])
        self.assertIn('TCP connection failed', result['error'])
        self.assertEqual(result['addresses'], ['127.0.0.1'])

    def test_invalid_port_rejected(self):
        with self.assertRaises(SystemExit) as error:
            main(['localhost', '0'])
        self.assertEqual(error.exception.code, 2)

if __name__ == '__main__':
    unittest.main()
