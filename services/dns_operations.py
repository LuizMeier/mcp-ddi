"""
DNS operations module
"""

from client.infoblox_client import InfobloxClient

class DNSOperationsService:
    """
    DNS operations service
    """

    def __init__(self, client: InfobloxClient):
        self.client = client

    async def list_zones(self):
        """List all DNS zones"""
        data = await self.client.get_zones()
        return [
            {"fqdn": z.fqdn, "view": z.view, "ref": z.ref}
            for z in data
        ]

    async def list_records(self, zone: str):
        """List all DNS records in a zone"""
        data = await self.client.get_records(zone)
        return [
            {"name": r.name, "ipv4addr": r.ipv4addr, "ref": r.ref}
            for r in data
        ]

    async def list_grid_members(self):
        """List all grid members"""
        data = await self.client.get_grid_members()
        return [
            {"host_name": m.host_name, "ref": m.ref}
            for m in data
        ]
