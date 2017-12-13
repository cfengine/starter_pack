#!/usr/bin/env python3
"""CFEngine Enterprise build script - for humans"""

import sys
import os
import argparse
import logging

log = logging.getLogger(__name__)

dry_run = False

def user_error(msg):
    log.error(msg)
    sys.exit(1)

def run_cmd(cmd):
    if dry_run:
        print(cmd)
        return
    print("Running: {}".format(cmd))
    r = os.system(cmd)
    if r != 0:
        print("Command:   {}".format(cmd))
        print("Exit code: {}".format(r))
        sys.exit(r)

def perform_step(step, repo, source):
    command = ""
    if step == "autogen":
        command = "./autogen.sh --enable-debug"
        if repo == "nova":
            command = "./autogen.sh --enable-debug --with-postgresql-hub=/usr"
    elif step == "make":
        command = "make -j2"
    elif step == "install":
        command = "make -j2 install"
    else:
        raise NotImplementedError()

    cmd = "cd {source} && cd {repo} && {command}".format(source=source,
                                                         repo=repo,
                                                         command=command)
    if step == "install" and repo == "nova":
        log.info("Skipping: {}".format(cmd))
    else:
        run_cmd(cmd)

def build(steps, repos, source):
    for repo in repos:
        for step in steps:
            perform_step(step,repo,source)

def get_steps(args):
    steps = []
    _all = args.all or args.all_steps
    if args.steps and not _all:
        steps += args.steps
    if args.autogen or _all:
        steps.append("autogen")
    if args.make or _all:
        steps.append("make")
    if args.install or _all:
        steps.append("install")
    if not steps:
        user_error("No build steps specified")
    return steps

def get_repos(args):
    repos = []
    _all = args.all or args.all_repos
    if args.repos and not _all:
        repos += args.repos
    if args.core or _all:
        repos.append("core")
    if args.masterfiless or _all:
        repos.append("masterfiless")
    if args.enterprise or _all:
        repos.append("enterprise")
    if args.nova or _all:
        repos.append("nova")
    if not repos:
        user_error("No repos specified")
    return repos

def get_args():
    ap = argparse.ArgumentParser(description="Developer script for building CFEngine enterprise",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    build_local_path  = os.path.abspath(__file__)
    buildscripts_path = os.path.dirname(build_local_path)
    cfengine_path     = os.path.dirname(buildscripts_path)

    # ALL:
    ap.add_argument("--all", "-a", help="Run all steps on all repos",       action="store_true")
    ap.add_argument("--all-repos", help="Run specified steps on all repos", action="store_true")
    ap.add_argument("--all-steps", help="Run all steps on specified repos", action="store_true")

    # STEPS:
    ap.add_argument("--autogen", help="Run autogen step", action="store_true")
    ap.add_argument("--make",    help="Run make step",    action="store_true")
    ap.add_argument("--install", help="Run install step", action="store_true")
    ap.add_argument("--steps",   help="Steps (commands) to run", nargs="+")

    # REPOS:
    ap.add_argument("--core",        help="Add core to --repos",        action="store_true")
    ap.add_argument("--masterfiles", help="Add masterfiles to --repos", action="store_true")
    ap.add_argument("--enterprise",  help="Add enterprise to --repos",  action="store_true")
    ap.add_argument("--nova",        help="Add nova to --repos",        action="store_true")
    ap.add_argument("--repos",       help="Repositories to run commands in", nargs="+")

    # SOURCE:
    ap.add_argument("--source", "-d", help="Where to look for CFEngine sources", type=str, default=cfengine_path)

    # LOGGING:
    ap.add_argument("--info",    help="Sets python loglevel to info",  action="store_true")
    ap.add_argument("--verbose", help="Sets python loglevel to debug", action="store_true")

    # BUILD TYPE:
    ap.add_argument("--debug",   help="Build in debug mode",   action="store_true")
    ap.add_argument("--release", help="Build in release mode", action="store_true")

    # MISC:
    ap.add_argument("--dry-run", help="Show commands to be run", action="store_true")

    args = ap.parse_args()

    if args.dry_run:
        global dry_run
        dry_run = True
        print("\nThese commands would run if you didn't specify --dry-run:")

    if args.info:
        log.setLevel(logging.INFO)
    if args.verbose:
        log.setLevel(logging.DEBUG)

    args.source = os.path.abspath(args.source)

    if not args.release and not args.debug:
        args.debug = True

    return args

if __name__ == "__main__":
    log.setLevel(logging.WARNING)
    args = get_args()
    steps, repos = get_steps(args), get_repos(args)
    build(steps, repos, args.source)
