"""Data models for Infoblox MCP Connector."""
from typing import Optional
from pydantic import BaseModel

class Zone(BaseModel):
    """Model for an authoritative DNS zone."""
    fqdn: str
    view: str
    _ref: str

class DNSRecord(BaseModel):
    """Model for a DNS A record."""
    name: str
    ipv4addr: str
    zone: Optional[str]
    _ref: str

class GridMember(BaseModel):
    """Model for a Grid Member."""
    host_name: str
    ipv4_address: str
    status: Optional[str]
    _ref: str

class Breed(BaseModel):
    """Model for a Dog Breed."""
    id: int
    type: str
