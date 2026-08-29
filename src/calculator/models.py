from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IPDetails:
    ip_version: int
    address: str
    cidr: int
    netmask: str
    wildcard: str
    network_address: str
    broadcast_address: str
    first_usable: str
    last_usable: str
    total_addresses: int
    usable_hosts: int
    address_class: str
    binary_repr: str
    decimal_repr: int
    hex_repr: str
    reverse_dns: str
    network_range: str
    host_range: str
    ip_type: str
    is_private: bool
    is_loopback: bool
    is_multicast: bool
    is_link_local: bool
    is_reserved: bool
    is_ipv4_mapped: bool = False

@dataclass
class SubnetRow:
    index: int
    network_address: str
    netmask: str
    cidr: int
    usable_range: str
    broadcast_address: str
    total_hosts: int
    usable_hosts: int

@dataclass
class SubnetDivisionResult:
    parent_network: str
    parent_cidr: int
    subnets: List[SubnetRow]

@dataclass
class HistoryItem:
    timestamp: str
    ip_address: str
    cidr: int
    ip_version: int
    network_address: str
