import ipaddress
import math
from typing import List
from calculator.models import IPDetails, SubnetRow, SubnetDivisionResult

class NetworkEngine:
    @staticmethod
    def get_ipv4_class(ip: ipaddress.IPv4Address) -> str:
        first_octet = int(ip) >> 24
        if 0 <= first_octet <= 127:
            return "Class A"
        elif 128 <= first_octet <= 191:
            return "Class B"
        elif 192 <= first_octet <= 223:
            return "Class C"
        elif 224 <= first_octet <= 239:
            return "Class D (Multicast)"
        else:
            return "Class E (Experimental)"

    @staticmethod
    def get_ipv4_binary(ip: ipaddress.IPv4Address) -> str:
        return ".".join(f"{octet:08b}" for octet in ip.packed)

    @staticmethod
    def get_ipv6_binary(ip: ipaddress.IPv6Address) -> str:
        groups = [f"{int.from_bytes(ip.packed[i:i+2], 'big'):016b}" for i in range(0, 16, 2)]
        return ":".join(groups)

    @classmethod
    def calculate_ip_details(cls, ip_str: str, cidr: int) -> IPDetails:
        iface = ipaddress.ip_interface(f"{ip_str}/{cidr}")
        ip = iface.ip
        net = iface.network

        ip_version = ip.version
        address_str = str(ip)
        netmask_str = str(net.netmask)
        wildcard_str = str(net.hostmask)
        network_address_str = str(net.network_address)
        total_addresses = net.num_addresses

        is_ipv4_mapped = False
        if ip_version == 6:
            is_ipv4_mapped = ip.ipv4_mapped is not None
            broadcast_address_str = "N/A"
            address_class = "N/A"
            binary_repr = cls.get_ipv6_binary(ip)
            decimal_repr = int(ip)
            hex_repr = f"0x{decimal_repr:032x}"
            reverse_dns = ip.reverse_pointer

            if cidr == 128:
                first_usable = str(net.network_address)
                last_usable = str(net.network_address)
                usable_hosts = 1
            elif cidr == 127:
                first_usable = str(net.network_address)
                last_usable = str(net.network_address + 1)
                usable_hosts = 2
            else:
                first_usable = str(net.network_address)
                last_usable = str(net.network_address + total_addresses - 1)
                usable_hosts = total_addresses

            network_range = f"{net.network_address} - {net.network_address + total_addresses - 1}"
            host_range = f"{first_usable} - {last_usable}"
        else:
            broadcast_address_str = str(net.broadcast_address)
            address_class = cls.get_ipv4_class(ip)
            binary_repr = cls.get_ipv4_binary(ip)
            decimal_repr = int(ip)
            hex_repr = f"0x{decimal_repr:08x}"
            reverse_dns = ip.reverse_pointer

            if cidr == 32:
                first_usable = str(net.network_address)
                last_usable = str(net.network_address)
                usable_hosts = 1
            elif cidr == 31:
                first_usable = str(net.network_address)
                last_usable = str(net.broadcast_address)
                usable_hosts = 2
            else:
                first_usable = str(net.network_address + 1)
                last_usable = str(net.broadcast_address - 1)
                usable_hosts = total_addresses - 2

            network_range = f"{net.network_address} - {net.broadcast_address}"
            host_range = f"{first_usable} - {last_usable}"

        ip_type = "Public"
        if ip.is_private:
            ip_type = "Private"
        elif ip.is_loopback:
            ip_type = "Loopback"
        elif ip.is_multicast:
            ip_type = "Multicast"
        elif ip.is_link_local:
            ip_type = "Link-Local"
        elif ip.is_reserved:
            ip_type = "Reserved"

        return IPDetails(
            ip_version=ip_version,
            address=address_str,
            cidr=cidr,
            netmask=netmask_str,
            wildcard=wildcard_str,
            network_address=network_address_str,
            broadcast_address=broadcast_address_str,
            first_usable=first_usable,
            last_usable=last_usable,
            total_addresses=total_addresses,
            usable_hosts=usable_hosts,
            address_class=address_class,
            binary_repr=binary_repr,
            decimal_repr=decimal_repr,
            hex_repr=hex_repr,
            reverse_dns=reverse_dns,
            network_range=network_range,
            host_range=host_range,
            ip_type=ip_type,
            is_private=ip.is_private,
            is_loopback=ip.is_loopback,
            is_multicast=ip.is_multicast,
            is_link_local=ip.is_link_local,
            is_reserved=ip.is_reserved,
            is_ipv4_mapped=is_ipv4_mapped
        )

    @classmethod
    def divide_by_subnet_count(cls, parent_ip: str, parent_cidr: int, count: int) -> SubnetDivisionResult:
        if count <= 0:
            raise ValueError("Subnet count must be greater than zero")
        
        prefix_delta = math.ceil(math.log2(count))
        new_cidr = parent_cidr + prefix_delta
        
        iface = ipaddress.ip_interface(f"{parent_ip}/{parent_cidr}")
        ip_version = iface.ip.version
        max_cidr = 32 if ip_version == 4 else 128
        
        if new_cidr > max_cidr:
            raise ValueError(f"Requested subnet count requires CIDR /{new_cidr}, which exceeds maximum /{max_cidr}")

        parent_net = iface.network
        subnets_list = list(parent_net.subnets(new_prefix=new_cidr))[:count]
        
        rows = []
        for i, sub in enumerate(subnets_list):
            total = sub.num_addresses
            if ip_version == 4:
                if new_cidr == 32:
                    usable_range = f"{sub.network_address}"
                    broadcast = str(sub.network_address)
                    usable = 1
                elif new_cidr == 31:
                    usable_range = f"{sub.network_address} - {sub.broadcast_address}"
                    broadcast = str(sub.broadcast_address)
                    usable = 2
                else:
                    usable_range = f"{sub.network_address + 1} - {sub.broadcast_address - 1}"
                    broadcast = str(sub.broadcast_address)
                    usable = total - 2
            else:
                broadcast = "N/A"
                if new_cidr == 128:
                    usable_range = f"{sub.network_address}"
                    usable = 1
                elif new_cidr == 127:
                    usable_range = f"{sub.network_address} - {sub.network_address + 1}"
                    usable = 2
                else:
                    usable_range = f"{sub.network_address} - {sub.network_address + total - 1}"
                    usable = total

            rows.append(SubnetRow(
                index=i + 1,
                network_address=str(sub.network_address),
                netmask=str(sub.netmask),
                cidr=new_cidr,
                usable_range=usable_range,
                broadcast_address=broadcast,
                total_hosts=total,
                usable_hosts=usable
            ))

        return SubnetDivisionResult(
            parent_network=str(parent_net.network_address),
            parent_cidr=parent_cidr,
            subnets=rows
        )

    @classmethod
    def divide_by_host_count(cls, parent_ip: str, parent_cidr: int, host_count: int) -> SubnetDivisionResult:
        if host_count <= 0:
            raise ValueError("Host count must be greater than zero")

        iface = ipaddress.ip_interface(f"{parent_ip}/{parent_cidr}")
        ip_version = iface.ip.version
        
        if ip_version == 4:
            needed_addresses = host_count + 2
            if host_count == 1:
                new_cidr = 32
            elif host_count == 2:
                new_cidr = 31
            else:
                new_cidr = 32 - math.ceil(math.log2(needed_addresses))
        else:
            new_cidr = 128 - math.ceil(math.log2(host_count))

        if new_cidr < parent_cidr:
            raise ValueError(f"Requested host count requires CIDR /{new_cidr}, which is larger than parent network CIDR /{parent_cidr}")

        parent_net = iface.network
        subnets_list = list(parent_net.subnets(new_prefix=new_cidr))
        
        rows = []
        for i, sub in enumerate(subnets_list):
            total = sub.num_addresses
            if ip_version == 4:
                if new_cidr == 32:
                    usable_range = f"{sub.network_address}"
                    broadcast = str(sub.network_address)
                    usable = 1
                elif new_cidr == 31:
                    usable_range = f"{sub.network_address} - {sub.broadcast_address}"
                    broadcast = str(sub.broadcast_address)
                    usable = 2
                else:
                    usable_range = f"{sub.network_address + 1} - {sub.broadcast_address - 1}"
                    broadcast = str(sub.broadcast_address)
                    usable = total - 2
            else:
                broadcast = "N/A"
                if new_cidr == 128:
                    usable_range = f"{sub.network_address}"
                    usable = 1
                elif new_cidr == 127:
                    usable_range = f"{sub.network_address} - {sub.network_address + 1}"
                    usable = 2
                else:
                    usable_range = f"{sub.network_address} - {sub.network_address + total - 1}"
                    usable = total

            rows.append(SubnetRow(
                index=i + 1,
                network_address=str(sub.network_address),
                netmask=str(sub.netmask),
                cidr=new_cidr,
                usable_range=usable_range,
                broadcast_address=broadcast,
                total_hosts=total,
                usable_hosts=usable
            ))

        return SubnetDivisionResult(
            parent_network=str(parent_net.network_address),
            parent_cidr=parent_cidr,
            subnets=rows
        )
