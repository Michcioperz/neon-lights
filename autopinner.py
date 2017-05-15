#!/usr/bin/python3
#you can run this in cron
#probably should
#on some server
import subprocess
from pprint import pprint

def resolve_ipns(addr):
    return subprocess.check_output(['ipfs', 'name', 'resolve', addr], universal_newlines=True)[6:].strip()

def cat_ipfs(addr):
    return subprocess.check_output(['ipfs', 'cat', addr], universal_newlines=True).strip()

def understand_msg(content):
    header_section, message = content.split('\n\n', 1)
    headers = dict([header.split(': ', 1) for header in header_section.strip().split('\n')])
    return (headers, message)

def fetch_all():
    with open('following') as f:
        following = f.read().strip().split('\n')
    addresses = [resolve_ipns(follow) for follow in following]
    while len(addresses):
        address = addresses.pop()
        subprocess.check_output(['ipfs', 'pin', 'add', address], universal_newlines=True)
        msg = understand_msg(cat_ipfs(address))
        if 'Previous' in msg[0]:
            addresses.append(msg[0]['Previous'])

if __name__ == '__main__':
    fetch_all()
