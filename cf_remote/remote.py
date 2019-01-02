#!/usr/bin/env python3
import sys
from collections import OrderedDict

import fabric
from paramiko.ssh_exception import AuthenticationException
from invoke.exceptions import UnexpectedExit

from cf_remote.utils import os_release, column_print, pretty, mkdir, find_packages
from cf_remote import log


def ssh_cmd(c, cmd):
    try:
        log.debug("Running over SSH: '{}'".format(cmd))
        result = c.run(cmd, hide=True)
        return result.stdout.strip()
    except UnexpectedExit:
        return None


def ssh_sudo(c, cmd):
    try:
        log.debug("Running(sudo) over SSH: '{}'".format(cmd))
        result = c.sudo(cmd, hide=True)
        return result.stdout.strip()
    except UnexpectedExit:
        return None


def print_info(data):
    log.debug("JSON data from host info: \n" + pretty(data))
    output = OrderedDict()
    print()
    print(data["ssh"])
    os_release = data["os_release"]
    os = like = None
    if os_release:
        if "ID" in os_release:
            os = os_release["ID"]
        if "ID_LIKE" in os_release:
            like = os_release["ID_LIKE"]
    if not os:
        os = data["uname"]
    if os and like:
        output["OS"] = "{} ({})".format(os, like)
    elif os:
        output["OS"] = "{}".format(os)
    else:
        output["OS"] = "Unknown"

    if "arch" in data:
        output["Architecture"] = data["arch"]

    agent_version = data["agent_version"]
    if agent_version:
        output["CFEngine"] = agent_version
    else:
        output["CFEngine"] = "Not installed"

    binaries = []
    if "bin" in data:
        for key in data["bin"]:
            binaries.append(key)
    if binaries:
        output["Binaries"] = ", ".join(binaries)

    column_print(output)
    print()


def connect(host, users=None):
    if "@" in host:
        parts = host.split("@")
        assert len(parts) == 2
        host = parts[1]
        if not users:
            users = [parts[0]]
    if not users:
        users = ["ubuntu", "centos", "vagrant", "root"]
    c = None
    for user in users:
        try:
            c = fabric.Connection(host=host, user=user)
            c.ssh_user = user
            c.ssh_host = host
            c.run("whoami", hide=True)
            return c
        except AuthenticationException:
            continue
    sys.exit("Could not ssh into {}".format(host))


def get_info(host, users=None):
    c = connect(host, users)
    user, host = c.ssh_user, c.ssh_host
    data = OrderedDict()
    data["ssh_user"] = user
    data["ssh_host"] = host
    data["ssh"] = "{}@{}".format(user, host)
    data["whoami"] = ssh_cmd(c, "whoami")
    data["uname"] = ssh_cmd(c, "uname")
    data["arch"] = ssh_cmd(c, "uname -m")
    data["os_release"] = os_release(ssh_cmd(c, "cat /etc/os-release"))
    data["agent_location"] = ssh_cmd(c, "which cf-agent")
    agent_version = ssh_cmd(c, "cf-agent --version")
    if agent_version:
        agent_version = agent_version.split()[2]
    data["agent_version"] = agent_version
    data["dpkg_location"] = ssh_cmd(c, "which dpkg")
    data["bin"] = {}
    for bin in ["dpkg", "rpm", "yum", "apt", "pkg"]:
        path = ssh_cmd(c, "which {}".format(bin))
        if path:
            data["bin"][bin] = path
    return data


def scp(file, remote, c=None):
    if not c:
        c = connect(remote)
    c.put(file)


def install_package(host, pkg, data):
    print("Installing '{}' on '{}'".format(pkg, host))
    c = connect(host)
    if ".deb" in pkg:
        ssh_sudo(c, "dpkg -i {}".format(pkg))
    else:
        ssh_sudo(c, "rpm -i {}".format(pkg))


def install_host(host, config=None, hub=False, directory=None):
    if not directory:
        directory = "./tmp"
    data = get_info(host)
    print_info(data)
    mkdir(directory)
    arch = "64" if "64" in data["arch"] else "32"
    extension = None
    if "dpkg" in data["bin"]:
        extension = ".deb"
    elif "rpm" in data["bin"]:
        extension = ".rpm"
    else:
        raise ValueError

    local_packages = find_packages(directory, extension=extension, arch=arch, hub=hub)
    assert (len(local_packages) > 0)
    pkg = local_packages[0]
    host = data["ssh"]
    print("Copying '{}' to '{}'".format(pkg, host))
    scp(directory + "/" + pkg, host)
    install_package(host, pkg, data)
    data = get_info(host)
    if data["agent_version"] and len(data["agent_version"]) > 0:
        print("CFEngine {} was successfully installed on {}".format(data["agent_version"], host))
    else:
        print("Installation failed!")
        sys.exit(1)
