"""
DNS operations module
"""

import re
from ipaddress import ip_address
from client.infoblox_client import InfobloxClient

class DNSOperationsService:
    """
    DNS operations service
    """

    def __init__(self, client: InfobloxClient):
        self.client = client

    def detect_query_type(self, query: str) -> str:
        """Detect the type of data based on its format."""
        value = query.strip()

        try:
            ip_address(value)
            return "ip"
        except ValueError:
            pass

        if re.fullmatch(r"[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+\.?", value):
            return "fqdn"

        if re.fullmatch(r"[A-Za-z0-9-]+", value):
            return "host"

        return "unknown"

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

    async def search_dns_record(self, query: str, zone: str | None = None):
        """Search for a specific DNS A record by IP, host name, or FQDN."""
        query_type = self.detect_query_type(query)

        if query_type == "ip":
            data = await self.client.search_a_records_by_ip(query, zone)
        elif query_type == "fqdn":
            data = await self.client.search_a_records_by_name(query, zone)
        elif query_type == "host":
            if not zone:
                raise ValueError("Zone must be provided when searching by host name.")
            data = await self.client.search_a_records_by_name(query, zone)
        else:
            raise ValueError(
                "Unsupported query type. Please provide a valid IP address, FQDN, or host name."
            )

        return [
            {"name": r.name, "ipv4addr": r.ipv4addr, "zone": r.zone, "ref": r.ref}
            for r in data
        ]

    async def check_ip_usage(self, ip: str):
        """Check if an IP address is in use"""

        # Validate that it's a valid IP address
        query_type = self.detect_query_type(ip)

        # Only proceed if it's an IP address
        if query_type != "ip":
            raise ValueError("Invalid IP address format.")

        # Search for A records by the IP address
        results = await self.client.search_a_records_by_ip(ip)

        # Determine usage status based on the number of records found
        if len(results) == 0:
            status =  "unused"
        elif len(results) == 1:
            status =  "in_use"
        else:
            status =  "shared"

        return {
            "status": status,
            "results": [
                {"name": r.name, "ipv4addr": r.ipv4addr, "zone": r.zone, "ref": r.ref}
                for r in results
            ]
        }

    async def get_zone_summary(self, zone: str):
        """Get a summary of DNS A records in a zone."""
        records = await self.client.get_records(zone)

        results = [
            {"name": r.name, "ipv4addr": r.ipv4addr, "zone": r.zone, "ref": r.ref}
            for r in records
        ]

        summary = {
            "zone": zone,
            "total_records": len(results),
            "total_unique_ips": len({record["ipv4addr"] for record in results}),
            "sample_records": results[:5]
        }

        return summary
