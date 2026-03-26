"""
DNS operations module
"""

import re
from ipaddress import ip_address
from client.infoblox_client import InfobloxClient
from models import GridMember

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
            {"host_name": m.host_name,
             "ref": m.ref}
            for m in data
        ]

    def _summarize_member_services(self, member: GridMember) -> dict:
        """Summarize the service status of a grid member."""

        # Define critical services
        critical_services = {"DNS", "DHCP"}

        service_summary = {}
        for service in member.service_status:
            service_summary[service.service] = {
                "status": service.status if service.status else "UNKNOWN",
                "description": service.description
            }

        # Determine node status based on critical services
        if all(service_summary.get(s, {}).get("status") == "WORKING" for s in critical_services):
            node_status = "healthy"
        elif any(service_summary.get(s, {}).get("status") != "WORKING" for s in critical_services):
            node_status = "degraded"
        else:
            node_status = "unknown"

        return {
            "host_name": member.host_name,
            "ref": member.ref,
            "platform": member.platform,
            "service_type_configuration": member.service_type_configuration,
            "vip_setting": member.vip_setting.dict() if member.vip_setting else None,
            "service_status_summary": service_summary,
            "member_status": node_status
        }

    async def get_grid_status(self):
        """Get the status of all grid members, including VIP settings and service status."""
        members = await self.client.get_grid_members()

        # Define a structure to hold the results of each member's status
        results = []

        # Define critical services that impact overall node health
        critical_services = {"DNS", "DHCP"}

        # Summarize the status of each member based on its service status and VIP settings
        for member in members:
            response = self._summarize_member_services(member)
            this_member = {
                "host_name": response["host_name"],
                "platform": response["platform"],
                "vip_address": response["vip_setting"]["address"] if response["vip_setting"] else None,
                "member_status": response["member_status"],
                "critical_services": {service: details for service, details in response["service_status_summary"].items() if service in critical_services},
                "service_counts": {
                    "WORKING": sum(1 for s in response["service_status_summary"].values() if s.get("status") == "WORKING"),
                    "INACTIVE": sum(1 for s in response["service_status_summary"].values() if s.get("status") == "INACTIVE"),
                    "UNKNOWN": sum(1 for s in response["service_status_summary"].values() if s.get("status") == "UNKNOWN")
                },
                "ref": response["ref"]
            }

            # Append the summarized member status to the results list
            results.append(this_member)

        # Create a summary of the overall grid status based on the member statuses
        summary = {
            "total_members": len(results),
            "healthy_members": sum(1 for m in results if m["member_status"] == "healthy"),
            "degraded_members": sum(1 for m in results if m["member_status"] == "degraded"),
            "unknown_status_members": sum(1 for m in results if m["member_status"] == "unknown")
        }

        return {
            "members": results,
            "summary": summary
            }


    async def get_dns_overview(self):
        """Check and inform a panorama of the DNS service, including zones, records, and grid member statuses."""

        # Get statuses of zones and all grid members, including VIP settings and service status
        grid_status = await self.get_grid_status()
        zones = await self.list_zones()

        if grid_status["summary"]["degraded_members"] > 0:
            overall_status = "degraded"
        elif len(zones) > 0:
            overall_status = "healthy"
        else:
            overall_status = "unknown"

        summary = {
            "overall_status": "healthy" if grid_status["summary"]["degraded_members"] == 0 else "degraded",
            "total_zones": len(zones),
            "total_grid_members": grid_status["summary"]["total_members"],
            "healthy_grid_members": grid_status["summary"]["healthy_members"],
            "degraded_grid_members": grid_status["summary"]["degraded_members"],
            "unknown_status_grid_members": grid_status["summary"]["unknown_status_members"]
        }

        results = {
            "zones": zones[:5],  # Include a sample of zones
            "grid": grid_status["summary"],
        }

        # Generate a user-friendly message based on the overall status
        if overall_status == "healthy":
            message = "DNS overview generated successfully. Environment appears healthy."
        elif overall_status == "degraded":
            message = "DNS overview generated successfully. Some grid members require attention."
        else:
            message = "DNS overview generated successfully, but the environment status could not be fully determined."

        return {
            "overall_status": overall_status,
            "summary": summary,
            "results": results,
            "message": message
        }



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
