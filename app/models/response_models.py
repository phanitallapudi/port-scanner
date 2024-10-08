from pydantic import BaseModel
from typing import List

class OpenPort(BaseModel):
    port: int
    service: str

class ScanResponse(BaseModel):
    ip: str
    open_ports: List[OpenPort] = []
    message: str = "Open ports found"
