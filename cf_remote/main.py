import os
import sys
import argparse

from cf_remote import log
from cf_remote import commands
from cf_remote.utils import package_path, user_error


def get_args():
    ap = argparse.ArgumentParser(
        description="Spooky CFEngine at a distance",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    default_dir = os.path.expanduser("~/.cfengine/packages/")

    # ALL:
    ap.add_argument("--hosts", "-H", help="What hosts to connect to (ssh)", type=str)
    ap.add_argument("--clients", help="Where to install client package", type=str)
    ap.add_argument("--hub", help="Where to install hub package", type=str)
    ap.add_argument("--bootstrap", help="cf-agent --bootstrap argument", type=str)
    ap.add_argument("--directory", "-d", help="Package directory", type=str, default=default_dir)
    ap.add_argument("--log-level", help="Specify detail of logging", type=str, default="WARNING")
    ap.add_argument("command", help="Action to perform", type=str, nargs='?', default="info")
    ap.add_argument("args", help="Arguments", type=str, nargs='*')

    args = ap.parse_args()
    return args


def run_command_with_args(command, args, config):
    if command == "info":
        return commands.info(args.hosts, None)
    if command == "install":
        return commands.install(args.hub, args.clients, args.bootstrap, config)
    if command == "packages":
        return commands.packages(config, args.args)
    user_error("Unknown command: '{}'".format(command))


def validate_command(command, args):
    if command == "install" and args.hosts:
        user_error("Use --clients and --hub instead of --hosts")
    if command == "info" and not args.hosts:
        user_error("Use --hosts to specify remote hosts")


def validate_args(args):
    if args.hosts:
        args.hosts = args.hosts.split(",")
    if args.clients:
        args.clients = args.clients.split(",")
    args.command = args.command.strip()
    if not args.command:
        user_error("Invalid or missing command")
    validate_command(args.command, args)


def main():
    args = get_args()
    validate_args(args)
    if args.log_level:
        log.set_level(args.log_level)

    config = {}
    config["directory"] = args.directory
    run_command_with_args(args.command, args, config)


if __name__ == "__main__":
    main()
