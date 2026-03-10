"""Infoblox WAPI client module."""
import httpx
from config import WAPI_URL, WAPI_USER, WAPI_PASS
from models import Zone, DNSRecord, GridMember

class InfobloxClient:
    """Simple client for Infoblox WAPI interactions."""

    def __init__(self):
        """Initialize the InfobloxClient with connection parameters."""
        self.base_url = WAPI_URL.rstrip("/")
        self.auth = (WAPI_USER, WAPI_PASS)
        self.headers = {"Accept": "application/json"}

    async def get_zones(self):
        """Retrieve all authoritative DNS zones."""
        async with httpx.AsyncClient(verify=False) as client:
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

    async def get_records(self, zone: str):
        """Retrieve all A records in a specific zone."""
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(
                f"{self.base_url}/record:a",  # Pode adaptar para record:cname, record:ptr etc.
                params={"zone": zone},
                auth=self.auth,
                headers=self.headers
            )
            resp.raise_for_status()
            data = resp.json()
            # Convert list of dictionaries to list of DNSRecord objects
            return [DNSRecord(**record_data) for record_data in data]

    async def get_grid_members(self):
        """Retrieve all Grid Members and their statuses."""
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(f"{self.base_url}/member", auth=self.auth, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            # Convert list of dictionaries to list of GridMember objects
            return [GridMember(**member_data) for member_data in data]

    async def get_breeds(self):
        """Retrieve all Breeds."""
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get("https://dogapi.dog/api/v2/breeds")
            resp.raise_for_status()
            return resp.json()
