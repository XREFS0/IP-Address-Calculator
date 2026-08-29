import pytest
from calculator.engine import NetworkEngine
from calculator.validators import InputValidator

def test_valid_ipv4_calculation():
    details = NetworkEngine.calculate_ip_details("192.168.1.10", 24)
    assert details.ip_version == 4
    assert details.address == "192.168.1.10"
    assert details.cidr == 24
    assert details.netmask == "255.255.255.0"
    assert details.wildcard == "0.0.0.255"
    assert details.network_address == "192.168.1.0"
    assert details.broadcast_address == "192.168.1.255"
    assert details.first_usable == "192.168.1.1"
    assert details.last_usable == "192.168.1.254"
    assert details.total_addresses == 256
    assert details.usable_hosts == 254
    assert details.address_class == "Class C"
    assert details.ip_type == "Private"
    assert details.is_private is True
    assert details.is_loopback is False
    assert details.is_multicast is False
    assert details.is_link_local is False
    assert details.is_reserved is False
    assert details.binary_repr == "11000000.10101000.00000001.00001010"

def test_ipv4_edge_cases():
    details_32 = NetworkEngine.calculate_ip_details("10.0.0.1", 32)
    assert details_32.total_addresses == 1
    assert details_32.usable_hosts == 1
    assert details_32.first_usable == "10.0.0.1"
    assert details_32.last_usable == "10.0.0.1"

    details_31 = NetworkEngine.calculate_ip_details("10.0.0.2", 31)
    assert details_31.total_addresses == 2
    assert details_31.usable_hosts == 2
    assert details_31.first_usable == "10.0.0.2"
    assert details_31.last_usable == "10.0.0.3"

def test_valid_ipv6_calculation():
    details = NetworkEngine.calculate_ip_details("2001:db8::1", 64)
    assert details.ip_version == 6
    assert details.address == "2001:db8::1"
    assert details.cidr == 64
    assert details.netmask == "ffff:ffff:ffff:ffff::"
    assert details.wildcard == "::ffff:ffff:ffff:ffff"
    assert details.network_address == "2001:db8::"
    assert details.broadcast_address == "N/A"
    assert details.total_addresses == 18446744073709551616
    assert details.usable_hosts == 18446744073709551616
    assert details.address_class == "N/A"
    assert details.ip_type == "Private"
    assert details.is_private is True

def test_ipv6_edge_cases():
    details_128 = NetworkEngine.calculate_ip_details("::1", 128)
    assert details_128.total_addresses == 1
    assert details_128.usable_hosts == 1
    assert details_128.is_loopback is True

    details_127 = NetworkEngine.calculate_ip_details("2001:db8::", 127)
    assert details_127.total_addresses == 2
    assert details_127.usable_hosts == 2

def test_validators():
    is_valid, ip, cidr, err = InputValidator.validate_and_parse("192.168.1.1/24", "", 4)
    assert is_valid is True
    assert ip == "192.168.1.1"
    assert cidr == 24
    assert err is None

    is_valid, ip, cidr, err = InputValidator.validate_and_parse(" 192.168.1.1   ", "255.255.255.0", 4)
    assert is_valid is True
    assert ip == "192.168.1.1"
    assert cidr == 24
    assert err is None

    is_valid, ip, cidr, err = InputValidator.validate_and_parse("garbage", "24", 4)
    assert is_valid is False
    assert err is not None

def test_subnetting_division():
    res = NetworkEngine.divide_by_subnet_count("192.168.1.0", 24, 4)
    assert len(res.subnets) == 4
    for sub in res.subnets:
        assert sub.cidr == 26
        assert sub.total_hosts == 64
        assert sub.usable_hosts == 62

    res_hosts = NetworkEngine.divide_by_host_count("192.168.1.0", 24, 50)
    assert len(res_hosts.subnets) == 4
    for sub in res_hosts.subnets:
        assert sub.cidr == 26
