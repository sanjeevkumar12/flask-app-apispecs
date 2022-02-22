import ipaddress

from flask import request


def get_user_ipaddress():
    return (
        request.environ.get("HTTP_X_FORWARDED_FOR")
        if request.environ.get("HTTP_X_FORWARDED_FOR")
        else request.environ["REMOTE_ADDR"]
    )


def get_user_encoded_ip_address() -> int:
    return int(ipaddress.ip_address(get_user_ipaddress()))


def decode_user_ip_address(encode_address: str) -> str:
    return ipaddress.ip_address(encode_address)
