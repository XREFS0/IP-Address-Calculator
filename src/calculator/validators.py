import ipaddress
from typing import Tuple, Optional, Union

class InputValidator:
    @staticmethod
    def parse_mask_to_cidr(mask_str: str, ip_version: int) -> Tuple[Optional[int], Optional[str]]:
        mask_str = mask_str.strip()
        if not mask_str:
            return None, "Mask is empty"

        if mask_str.startswith("/"):
            mask_str = mask_str[1:]

        if mask_str.isdigit():
            val = int(mask_str)
            max_cidr = 32 if ip_version == 4 else 128
            if 0 <= val <= max_cidr:
                return val, None
            return None, f"Prefix length must be between 0 and {max_cidr}"

        if ip_version == 4:
            try:
                netmask = ipaddress.IPv4Address(mask_str)
                net = ipaddress.IPv4Network(f"0.0.0.0/{netmask}", strict=False)
                return net.prefixlen, None
            except Exception:
                pass

            try:
                wildcard = ipaddress.IPv4Address(mask_str)
                inverted_bytes = bytes(255 - b for b in wildcard.packed)
                netmask = ipaddress.IPv4Address(inverted_bytes)
                net = ipaddress.IPv4Network(f"0.0.0.0/{netmask}", strict=False)
                return net.prefixlen, None
            except Exception:
                pass

            return None, "Invalid IPv4 netmask or wildcard mask"
        else:
            try:
                netmask = ipaddress.IPv6Address(mask_str)
                net = ipaddress.IPv6Network(f"::/{netmask}", strict=False)
                return net.prefixlen, None
            except Exception:
                pass

            return None, "Invalid IPv6 netmask"

    @classmethod
    def validate_and_parse(cls, ip_str: str, mask_str: str, ip_version: int) -> Tuple[bool, Optional[str], Optional[int], Optional[str]]:
        ip_str = ip_str.strip()
        if not ip_str:
            return False, None, None, "IP Address is empty"

        if "/" in ip_str:
            parts = ip_str.split("/", 1)
            ip_str = parts[0].strip()
            mask_str = parts[1].strip()

        try:
            if ip_version == 4:
                ip = ipaddress.IPv4Address(ip_str)
            else:
                ip = ipaddress.IPv6Address(ip_str)
        except Exception:
            return False, None, None, f"Invalid IPv{ip_version} address format"

        cidr, err = cls.parse_mask_to_cidr(mask_str, ip_version)
        if err:
            return False, None, None, err

        return True, str(ip), cidr, None
