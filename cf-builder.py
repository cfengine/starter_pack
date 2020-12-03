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


def run_command(command, on_failure=None):
    if dry_run:
        print(command)
        return
    print("Running: {}".format(command))
    r = os.system(command)
    if r != 0:
        print("Command:   {}".format(command))
        print("Exit code: {}".format(r))
        if on_failure:
            print("Triggered: {}".format(on_failure))
            os.system(on_failure)
        sys.exit(r)


def build_cmd(cd, cmd):
    return "{} && {}".format(cd, cmd) if cmd else None


def perform_step(step, repo, source, warnings, asan, build_folder=None):
    tmp_cmd = ""
    cmd_fail = None
    optarg = None
    if isinstance(step, list):
        args = step[1:]
        step = step[0]
        optarg = args[0]

    autogen = "./autogen.sh -C --enable-debug" + (
        " --with-postgresql-hub=/usr" if repo == "nova" else "")
    cflags = "-Werror -Wall" if warnings else ""
    if asan:
        cflags += " -fsanitize=address"
    ldflags = "-fsanitize=address -static-libasan" if asan else ""

    command_dict = {
        "checkout": "git checkout {}".format(optarg),
        "fetch": "git fetch --all",
        "rebase": "git rebase {}".format(optarg),
        "push": "git push",
        "clean": "git clean -fXd",
        "autogen": autogen,
        "make": f"make -j -l8 CFLAGS='{cflags}' LDFLAGS='{ldflags}'",
        "install": "make -j2 install"
    }

    if step in command_dict:
        tmp_cmd = command_dict[step]
    elif step == "rsync":
        build_folder = args[0]
        run_command(
            "mkdir -p {dst} && rsync -r {root}/{repo} {dst}".format(
                root=source, repo=repo, dst=build_folder))
        return build_folder
    elif step == "test":
        # Don't want warning flags when compiling tests:
        cflags = "-fsanitize=address" if asan else ""
        tmp_cmd = f"cd tests/unit && make check LDFLAGS='{ldflags}' CFLAGS='{cflags}'"
        cmd_fail = "cd tests/unit && cat test-suite.log"
    else:
        raise NotImplementedError()
    if build_folder:
        source = build_folder

    cmd_cd = "cd {src} && cd {repo}".format(src=source, repo=repo)
    command = build_cmd(cmd_cd, tmp_cmd)
    cmd_fail = build_cmd(cmd_cd, cmd_fail)

    run_command(command, cmd_fail)
    return build_folder


def build(steps, repos, source, warnings, asan):
    build_folder = None
    for step in steps:
        for repo in repos:
            build_folder = perform_step(
                step, repo, source, warnings, asan, build_folder)


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
    if args.push:
        steps.append(["push", args.push])
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
    if args.test:
        steps.append("test")
    if not steps:
        user_error("No build steps specified, see --help")
    return steps


def get_repos(args):
    repos = []
    _all = args.build_all or args.all_repos
    if args.repos and not _all:
        repos += args.repos
    if args.libntech:
        repos.append("libntech")
    if args.core or _all:
        repos.append("core")
    if args.masterfiles or _all:
        repos.append("masterfiles")
    if args.enterprise or _all:
        repos.append("enterprise")
    if args.nova or _all:
        repos.append("nova")
    # Buildscripts and documentation are not necessary for normal development:
    if args.buildscripts:
        repos.append("buildscripts")
    if args.documentation:
        repos.append("documentation")
    if args.design_center:
        repos.append("design-center")
    if args.mission_portal:
        repos.append("mission-portal")
    if not repos:
        user_error("No repos specified")
    return repos


def get_args():
    ap = argparse.ArgumentParser(
        description="Developer script for building CFEngine enterprise",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    build_local_path = os.path.abspath(__file__)
    buildscripts_path = os.path.dirname(build_local_path)
    cfengine_path = os.path.dirname(buildscripts_path)

    # ALL:
    ap.add_argument(
        "--build-all", help="Equiv: --build --all-repos", action="store_true")
    ap.add_argument(
        "--all-repos",
        help="Equiv: --libntech --core --masterfiles --enterprise --nova",
        action="store_true")
    ap.add_argument(
        "--build", help="Equiv: --autogen --make", action="store_true")

    # STEPS:
    ap.add_argument("--checkout", help="Switch git branch", type=str)
    ap.add_argument("--fetch", help="Run fetch step", action="store_true")
    ap.add_argument("--rebase", help="Rebase git branch", type=str)
    ap.add_argument("--push", help="Push git branch", action="store_true")
    ap.add_argument("--clean", help="Run clean step", action="store_true")
    ap.add_argument(
        "--rsync",
        help="Rsync and run remaining commands in specified directory",
        type=str)
    ap.add_argument("--autogen", help="Run autogen step", action="store_true")
    ap.add_argument("--make", help="Run make step", action="store_true")
    ap.add_argument("--test", help="Run make check", action="store_true")
    ap.add_argument("--install", help="Run install step", action="store_true")
    ap.add_argument("--steps", help="Steps (commands) to run", nargs="+")

    # REPOS:
    ap.add_argument("--libntech", help="Add libntech to --repos", action="store_true")
    ap.add_argument("--core", help="Add core to --repos", action="store_true")
    ap.add_argument(
        "--masterfiles",
        help="Add masterfiles to --repos",
        action='store_true')
    ap.add_argument(
        "--enterprise", help="Add enterprise to --repos", action="store_true")
    ap.add_argument("--nova", help="Add nova to --repos", action="store_true")
    ap.add_argument(
        "--buildscripts",
        help="Add buildscripts to --repos",
        action="store_true")
    ap.add_argument(
        "--documentation",
        help="Add documentation to --repos",
        action="store_true")
    ap.add_argument(
        "--design-center",
        help="Add design-center to --repos",
        action="store_true")
    ap.add_argument(
        "--mission-portal",
        help="Add mission-portal to --repos",
        action="store_true")
    ap.add_argument(
        "--repos", help="Repositories to run commands in", nargs="+")

    # SOURCE:
    ap.add_argument(
        "--source",
        help="Where to look for CFEngine sources",
        type=str,
        default=cfengine_path)

    # LOGGING:
    ap.add_argument(
        "--info", help="Sets python loglevel to info", action="store_true")
    ap.add_argument(
        "--verbose",
        help="Sets python loglevel to debug",
        action="store_true")

    # BUILD TYPE:
    ap.add_argument(
        "--debug", help="Build in debug mode", action="store_true")
    ap.add_argument(
        "--release", help="Build in release mode", action="store_true")

    # MISC:
    ap.add_argument(
        "--dry-run", help="Show commands to be run", action="store_true")
    ap.add_argument("--warnings", help="Stricter compiler", action="store_true")
    ap.add_argument("--asan", help="AddressSanitizer", action="store_true")

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
    build(steps, repos, args.source, args.warnings, args.asan)
