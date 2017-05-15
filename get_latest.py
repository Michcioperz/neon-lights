#!/usr/bin/env python3
import argparse, subprocess, tqdm
from pprint import pprint

def resolve_ipns(addr):
    return subprocess.check_output(['./ipfs', 'name', 'resolve', addr], universal_newlines=True)[6:].strip()

def cat_ipfs(addr):
    return subprocess.check_output(['./ipfs', 'cat', addr], universal_newlines=True).strip()

def understand_msg(content):
    header_section, message = content.split('\n\n', 1)
    headers = dict([header.split(': ', 1) for header in header_section.strip().split('\n')])
    return (headers, message)

def fetch_all():
    with open('following') as f:
        following = f.read().strip().split('\n')
    addresses = [resolve_ipns(follow) for follow in tqdm.tqdm(following, unit='user')]
    messages = []
    t = tqdm.tqdm(total=len(addresses), unit='statuses')
    while len(addresses):
        address = addresses.pop()
        t.update()
        msg = understand_msg(cat_ipfs(address))
        messages.append(msg)
        if 'Previous' in msg[0]:
            t.total += 1
            t.refresh()
            addresses.append(msg[0]['Previous'])
    return sorted(messages, key=lambda x: x[0]['Date-Time'])

if __name__ == '__main__':
    pprint(fetch_all())
