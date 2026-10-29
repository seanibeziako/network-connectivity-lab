# Network connectivity troubleshooting lab

A small Python command-line tool for diagnosing two common help-desk checks: whether a hostname resolves and whether a TCP connection can be established to a single port. The tool uses only the Python standard library.

## Skills practiced

- DNS name resolution with `socket.getaddrinfo`.
- TCP connectivity checks with a configurable connection timeout.
- Distinguishing DNS lookup failures from TCP connection failures.
- Recording a troubleshooting result and testing code using a local loopback service.

## Requirements

Python 3.9 or later. No packages or elevated privileges are required. Run checks only against systems and ports you are authorized to access.

## Use

```text
python3 check_connection.py HOST PORT --timeout 3
```

Example: test a local HTTP service only if one is already running:

```text
python3 check_connection.py 127.0.0.1 8000
```

A successful check prints the resolved address and connected peer and returns exit code 0. A DNS or connection failure displays an error and returns exit code 1. Invalid arguments produce exit code 2. The TCP timeout does not limit how long the operating system's DNS resolver takes. A successful TCP connection shows the port accepted a connection; it does not establish that the application is functioning correctly or that the service is secure.

## Run automated checks

```text
python3 -m unittest discover -s tests -v
```

The tests start a temporary TCP listener on loopback and exercise DNS failure, a refused connection, and invalid input. No public hosts are contacted.

## Suggested exercise

1. Start a local test service: `python3 -m http.server 8000 --bind 127.0.0.1`.
2. Run the tool against `127.0.0.1` port `8000`; record the output.
3. Stop the test service and repeat. Compare the connection failure with the earlier success.
4. Check an invalid hostname and document how the DNS error differs from a TCP error.
5. Record the time, symptoms, checks performed, and actual outcome. Do not include sensitive customer or system details.

## Scope

This is a learning aid, not a network scanner or monitoring system. Results depend on the operating system, DNS configuration, firewall, and target service.

## Additional networking example

The [small-office network example](examples/small-office-network/README.md) includes a Packet Tracer topology, sample configurations, and screenshots. The Python tests do not validate the Packet Tracer lab.
