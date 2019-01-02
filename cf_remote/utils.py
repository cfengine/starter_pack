import os
import sys
import json
from collections import OrderedDict
from cf_remote import log
from datetime import datetime


def cf_remote_dir(string=None):
    path = os.path.expanduser("~/.cfengine/cf-remote")
    if string:
        path += string
    return path


def is_in_past(date):
    now = datetime.now()
    date = datetime.strptime(date, "%Y-%m-%d")
    return now > date


def canonify(string):
    legal = "abcdefghijklmnopqrstuvwxyz0123456789-_"
    string = string.strip()
    string = string.lower()
    string = string.replace(".", "_")
    string = string.replace(" ", "_")
    results = []
    for c in string:
        if c in legal:
            results.append(c)
    return "".join(results)


def file_extension(path):
    index = path.rfind(".")
    return path[index + 1:]


def file_name(path):
    index = path.rfind("/")
    return path[index + 1:]


def user_error(msg):
    sys.exit("cf-remote: " + msg)


def mkdir(path):
    if not os.path.exists(path):
        log.info("Creating directory: {}".format(path))
        os.makedirs(path)
    else:
        log.debug("Directory already exists: {}".format(path))


def ls(path):
    return os.listdir(path)


def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


def save_file(path, data):
    mkdir("/".join(path.split("/")[0:-1]))
    with open(path, "w") as f:
        f.write(data)


def pretty(data):
    return json.dumps(data, indent=2)


def package_path():
    above_dir = os.path.dirname(__file__)
    return os.path.abspath(above_dir)


def above_package_path():
    path = package_path() + "/../"
    return os.path.abspath(path)


def read_json(path):
    try:
        with open(path, "r") as f:
            return json.loads(f.read(), object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        return None


def write_json(path, data):
    data = pretty(data)
    return save_file(path, data)


def os_release(inp):
    if not inp:
        log.debug("Cannot parse os-release file (empty)")
        return None
    d = OrderedDict()
    for line in inp.split("\n"):
        line = line.strip()
        if "=" not in line:
            continue
        split = line.index("=")
        assert line[split] == "="
        key = line[0:split]
        assert "=" not in key
        value = line[split + 1:]
        if (len(value) > 1 and value[0] == value[-1] and value[0] in ["'", '"']):
            value = value[1:-1]
        d[key] = value
    return d


def column_print(data):
    width = 0
    for key in data:
        if len(key) > width:
            width = len(key)

    for key, value in data.items():
        fill = " " * (width - len(key))
        print("{}{} : {}".format(key, fill, value))


def pretty(data):
    return json.dumps(data, indent=2)


def download_packages(path):
    pass


def find_packages(path, extension=None, arch=None, os=None, hub=False):
    download_packages(path)
    packages = ls(path)
    if extension:
        packages = filter(lambda p: p.endswith(extension), packages)
    if arch:
        if arch == "32":
            packages = filter(lambda p: "64" not in p, packages)
        else:
            packages = filter(lambda p: arch in p, packages)
    if hub:
        packages = filter(lambda p: "hub" in p, packages)
    else:
        packages = filter(lambda p: "hub" not in p, packages)
    return list(packages)
