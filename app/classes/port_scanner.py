import socket
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

# List of common ports
COMMON_PORTS = {
    20: 'FTP (Data)',
    21: 'FTP (Control)',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    3389: 'RDP',
    8080: 'HTTP (Alternate)',
    3306: 'MySQL',
    587: 'SMTP (TLS)',
    995: 'POP3 (SSL)',
    993: 'IMAP (SSL)',
    5900: 'VNC',
}

def scan_port(ip: str, port: int) -> Tuple[int, bool]:
    """Scans a single port and returns its status (open/closed)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Set timeout to 1 second
        result = s.connect_ex((ip, port))
        s.close()
        return port, result == 0
    except Exception:
        return port, False

def scan_ports(ip: str, ports: List[int], max_workers: int = 100) -> List[int]:
    """Scans a given list of ports on the IP address."""
    open_ports = []

    # Use ThreadPoolExecutor for concurrent scanning
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda port: scan_port(ip, port), ports))

    # Gather open ports
    open_ports = [port for port, is_open in results if is_open]

    return open_ports
