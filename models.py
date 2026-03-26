"""Data models for Infoblox MCP Connector."""
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class Zone(BaseModel):
    """Model for an authoritative DNS zone."""
    fqdn: str
    view: str
    ref: str = Field(alias="_ref")
    # Allow using 'ref' instead of '_ref' when creating instances
    model_config = ConfigDict(populate_by_name=True)

class DNSRecord(BaseModel):
    """Model for a DNS A record."""
    name: str
    ipv4addr: str
    zone: Optional[str]
    ref: str = Field(alias="_ref")
    # Allow using 'ref' instead of '_ref' when creating instances
    model_config = ConfigDict(populate_by_name=True)

class GridMember(BaseModel):
    """Model for a Grid Member."""
    host_name: str
    ipv4_address: str
    status: Optional[str]
    ref: str = Field(alias="_ref")
    # Allow using 'ref' instead of '_ref' when creating instances
    model_config = ConfigDict(populate_by_name=True)
