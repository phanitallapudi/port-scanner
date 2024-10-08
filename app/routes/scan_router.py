from fastapi import APIRouter, Query
from typing import Optional, List

from app.models.response_models import ScanResponse, OpenPort
from app.classes.port_scanner import scan_ports, COMMON_PORTS

# Create router instance
router = APIRouter()

@router.get("/scan/", response_model=ScanResponse)
async def scan(
    ip: str,
    all_ports: bool = Query(False, description="Scan all ports (1-65535) if True, else scan common ports."),
    start_port: int = Query(1, description="Start port (if scanning all ports)"),
    end_port: int = Query(65535, description="End port (if scanning all ports)"),
    custom_ports: Optional[List[int]] = Query(None, description="List of custom ports to scan")
):
    """Scans the specified IP address for open ports."""
    
    if custom_ports:
        ports_to_scan = custom_ports
    elif all_ports:
        ports_to_scan = list(range(start_port, end_port + 1))
    else:
        # Scan only the most common ports
        ports_to_scan = list(COMMON_PORTS.keys())

    open_ports = scan_ports(ip, ports_to_scan)

    result = [OpenPort(port=port, service=COMMON_PORTS.get(port, 'Unknown Service')) for port in open_ports]

    if not result:
        return {"ip": ip, "message": "No open ports found."}
    return {"ip": ip, "open_ports": result}
