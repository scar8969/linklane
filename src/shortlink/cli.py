from .short.links import create

import argparse

def cmd_create(args):
    link = create(args.url, args.slug, args.expiry, args.password)
    print(f"https://s.me/{link.slug}")

def main():
    p = argparse.ArgumentParser(prog="short")
    sub = p.add_subparsers(dest="cmd")
    c = sub.add_parser("create"); c.add_argument("url")
    c.add_argument("--slug", default=""); c.add_argument("--expiry", default=""); c.add_argument("--password", default="")
    args = p.parse_args()
    if args.cmd == "create":
        return cmd_create(args)
    p.print_help()
    return 1
