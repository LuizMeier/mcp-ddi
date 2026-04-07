"""Infoblox WAPI client module."""
import httpx
from config import WAPI_URL, WAPI_USER, WAPI_PASS, WAPI_VERIFY_SSL
from models import Zone, DNSRecord, GridMember

class InfobloxClient:
    """Simple client for Infoblox WAPI interactions."""

    def __init__(self):
        """Initialize the InfobloxClient with connection parameters."""
        self.base_url = WAPI_URL.rstrip("/")
        self.auth = (WAPI_USER, WAPI_PASS)
        self.headers = {"Accept": "application/json"}
        self.verify_ssl = WAPI_VERIFY_SSL

    async def get_zones(self):
        """Retrieve all authoritative DNS zones."""
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            resp = await client.get(
                f"{self.base_url}/zone_auth?",
                auth=self.auth,
                headers=self.headers  # pylint: disable=line-too-long
            )
            resp.raise_for_status()
            data = resp.json()
            # Convert list of dictionaries to list of Zone objects
            # The API returns: [{"_ref": "...", "fqdn": "...", "view": "..."}, ...]
            return [Zone(**zone_data) for zone_data in data]

    async def get_records(self, zone: str, record_type: str = "a"):
        """Retrieve records from a specific zone."""

        if not zone:
            # Get all records across all zones if no specific zone is provided
            endpoint = f"{self.base_url}/allRecords"
        else:
            endpoint = f"{self.base_url}/record:{record_type}"

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            resp = await client.get(
                endpoint,
                params={"zone": zone},
                auth=self.auth,
                headers=self.headers
            )
            resp.raise_for_status()
            data = resp.json()
            # Convert list of dictionaries to list of DNSRecord objects
            return [DNSRecord(**record_data) for record_data in data]

    async def search_a_records_by_ip(self, ip: str, zone: str | None = None):
        """Search A records by IPv4 address."""
        params = {"ipv4addr": ip}
        if zone:
            params["zone"] = zone

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            resp = await client.get(
                f"{self.base_url}/record:a",
                params=params,
                auth=self.auth,
                headers=self.headers
            )
            resp.raise_for_status()
            data = resp.json()
            return [DNSRecord(**record_data) for record_data in data]

    async def search_a_records_by_name(self, name: str, zone: str | None = None):
        """Search A records by host name or FQDN."""
        params = {"name": name}
        if zone:
            params["zone"] = zone

        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            resp = await client.get(
                f"{self.base_url}/record:a",
                params=params,
                auth=self.auth,
                headers=self.headers
            )
            resp.raise_for_status()
            data = resp.json()
            return [DNSRecord(**record_data) for record_data in data]

    async def get_grid_members(self):
        """Retrieve all Grid Members and their statuses."""
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            params = {"_return_fields": "host_name,config_addr_type,host_name,platform,service_type_configuration,vip_setting,service_status"}
            resp = await client.get(
                f"{self.base_url}/member",
                auth=self.auth,
                headers=self.headers,
                params=params
                )
            resp.raise_for_status()
            data = resp.json()
            # Convert list of dictionaries to list of GridMember objects
            return [GridMember(**member_data) for member_data in data]
