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

class ServiceStatus(BaseModel):
    """Model for service status."""
    description: Optional[str] = None
    service: str
    status: str

class VipSetting(BaseModel):
    """Model for VIP settings."""
    address: str
    dscp: int
    gateway: str
    primary: bool
    subnet_mask: str
    use_dscp: bool

class GridMember(BaseModel):
    """Model for a Grid Member."""
    host_name: str
    config_addr_type: Optional[str]
    ref: str = Field(alias="_ref")
    platform: Optional[str]
    service_type_configuration: Optional[str]
    vip_setting: Optional[VipSetting]
    service_status: list[ServiceStatus] = Field(default_factory=list)
    # Allow using 'ref' instead of '_ref' when creating instances
    model_config = ConfigDict(populate_by_name=True)
