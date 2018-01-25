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

def run_command(command):
    if dry_run:
        print(command)
        return
    print("Running: {}".format(command))
    r = os.system(command)
    if r != 0:
        print("Command:   {}".format(command))
        print("Exit code: {}".format(r))
        sys.exit(r)

def perform_step(step, repo, source, warnings, build_folder=None):
    tmp_cmd = ""
    command = None
    if isinstance(step, list):
        args = step[1:]
        step = step[0]
    if step == "checkout":
        tmp_cmd = "git checkout {}".format(args[0])
    elif step == "fetch":
        tmp_cmd = "git fetch --all"
    elif step == "rebase":
        tmp_cmd = "git rebase {}".format(args[0])
    elif step == "rsync":
        build_folder = args[0]
        command = "mkdir -p {dst} && rsync -r {root}/{repo} {dst}".format(root=source, repo=repo, dst=args[0])
    elif step == "clean":
        tmp_cmd = "make clean"
    elif step == "autogen":
        tmp_cmd = "./autogen.sh --enable-debug"
        if repo == "nova":
            tmp_cmd = "./autogen.sh --enable-debug --with-postgresql-hub=/usr"
    elif step == "make":
        tmp_cmd = "make -j2"
        if warnings:
            tmp_cmd = "make -j2 CFLAGS=-Werror" # TODO: Default to this
    elif step == "install":
        tmp_cmd = "make -j2 install"
    else:
        raise NotImplementedError()
    if not command:
        if build_folder:
            source = build_folder
        command = "cd {source} && cd {repo} && {tmp_cmd}".format(source=source,
                                                             repo=repo,
                                                             tmp_cmd=tmp_cmd)
    run_command(command)
    return build_folder

def build(steps, repos, source, warnings):
    build_folder = None
    for step in steps:
        for repo in repos:
            build_folder = perform_step(step,repo,source,warnings,build_folder)

def get_steps(args):
    steps = []
    build = args.build or args.build_all
    if args.steps:
        steps += args.steps
    if args.checkout:
        steps.append(["checkout", args.checkout])
    if args.fetch:
        steps.append("fetch")
    if args.rebase:
        steps.append(["rebase", args.rebase])
    if args.rsync:
        steps.append(["rsync", args.rsync])
    if args.clean:
        steps.append("clean")
    if args.autogen or build:
        steps.append("autogen")
    if args.make or build:
        steps.append("make")
    if args.install:
        steps.append("install")
    if not steps:
        user_error("No build steps specified, see --help")
    return steps

def get_repos(args):
    repos = []
    _all = args.build_all or args.all_repos
    if args.repos and not _all:
        repos += args.repos
    if args.core or _all:
        repos.append("core")
    if args.masterfiles or _all:
        repos.append("masterfiles")
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
    ap.add_argument("--build-all", help="Equiv: --build --all-repos", action="store_true")
    ap.add_argument("--all-repos", help="Equiv: --core --masterfiles --enterprise --nova", action="store_true")
    ap.add_argument("--build",     help="Equiv: --autogen --make", action="store_true")

    # STEPS:
    ap.add_argument("--checkout", help="Switch git branch", type=str)
    ap.add_argument("--fetch",    help="Run fetch step",    action="store_true")
    ap.add_argument("--rebase",   help="Rebase git branch", type=str)
    ap.add_argument("--rsync",    help="Rsync and run remaining commands in specified directory",   type=str)
    ap.add_argument("--clean",    help="Run clean step",    action="store_true")
    ap.add_argument("--autogen",  help="Run autogen step",  action="store_true")
    ap.add_argument("--make",     help="Run make step",     action="store_true")
    ap.add_argument("--install",  help="Run install step",  action="store_true")
    ap.add_argument("--steps",    help="Steps (commands) to run", nargs="+")

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
    ap.add_argument("--warnings", help="WIP: -Werror", action="store_true")

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
    build(steps, repos, args.source, args.warnings)
