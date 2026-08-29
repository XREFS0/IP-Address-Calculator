import json
from calculator.models import IPDetails

class ResultExporter:
    @staticmethod
    def export_to_json(details: IPDetails, filepath: str) -> None:
        data = {
            "ip_version": details.ip_version,
            "address": details.address,
            "cidr": details.cidr,
            "netmask": details.netmask,
            "wildcard": details.wildcard,
            "network_address": details.network_address,
            "broadcast_address": details.broadcast_address,
            "first_usable": details.first_usable,
            "last_usable": details.last_usable,
            "total_addresses": details.total_addresses,
            "usable_hosts": details.usable_hosts,
            "address_class": details.address_class,
            "binary_repr": details.binary_repr,
            "decimal_repr": details.decimal_repr,
            "hex_repr": details.hex_repr,
            "reverse_dns": details.reverse_dns,
            "network_range": details.network_range,
            "host_range": details.host_range,
            "ip_type": details.ip_type,
            "is_private": details.is_private,
            "is_loopback": details.is_loopback,
            "is_multicast": details.is_multicast,
            "is_link_local": details.is_link_local,
            "is_reserved": details.is_reserved,
            "is_ipv4_mapped": details.is_ipv4_mapped
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def export_to_txt(details: IPDetails, filepath: str) -> None:
        lines = [
            "=" * 50,
            "          IP ADDRESS CALCULATION DETAILS",
            "=" * 50,
            f"IP Version:        IPv{details.ip_version}",
            f"IP Address:        {details.address}",
            f"CIDR Prefix:       /{details.cidr}",
            "-" * 50,
            "ADDRESS INFORMATION",
            "-" * 50,
            f"Netmask:           {details.netmask}",
            f"Wildcard Mask:     {details.wildcard}",
            f"Network Address:   {details.network_address}",
            f"Broadcast Address: {details.broadcast_address}",
            f"Address Class:     {details.address_class}",
            "-" * 50,
            "HOST & RANGE INFORMATION",
            "-" * 50,
            f"First Usable Host: {details.first_usable}",
            f"Last Usable Host:  {details.last_usable}",
            f"Total Addresses:   {details.total_addresses}",
            f"Usable Host Count: {details.usable_hosts}",
            f"Network Range:     {details.network_range}",
            f"Host Range:        {details.host_range}",
            "-" * 50,
            "REPRESENTATIONS & ADDITIONAL INFO",
            "-" * 50,
            f"Binary:            {details.binary_repr}",
            f"Decimal:           {details.decimal_repr}",
            f"Hexadecimal:       {details.hex_repr}",
            f"Reverse DNS (PTR): {details.reverse_dns}",
            f"Address Type:      {details.ip_type}",
            f"Is Private:        {details.is_private}",
            f"Is Loopback:       {details.is_loopback}",
            f"Is Multicast:      {details.is_multicast}",
            f"Is Link-Local:     {details.is_link_local}",
            f"Is Reserved:       {details.is_reserved}",
            f"Is IPv4 Mapped:    {details.is_ipv4_mapped}",
            "=" * 50
        ]
        with open(filepath, "w") as f:
            f.write("\n".join(lines) + "\n")
