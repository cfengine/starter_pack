from cf_remote.remote import get_info, print_info, install_host
from cf_remote.packages import Releases
from cf_remote.utils import canonify, pretty, user_error


def info(hosts, users=None):
    assert hosts
    for host in hosts:
        data = get_info(host, users)
        print_info(data)


def install(hub, clients, bootstrap, config):
    assert hub or clients
    directory = None
    if config and "directory" in config:
        directory = config["directory"]
    if hub:
        install_host(hub, config, True, directory)
    for host in clients:
        install_host(host, config, False, directory)


def packages(config, tags=None):
    releases = Releases()
    if not tags:
        print(releases)
        return
    release = releases.default
    print("Using {}:".format(release))
    artifacts = release.find(tags)

    if len(artifacts) == 0:
        print("No suitable packages found")
    else:
        for artifact in artifacts:
            print(artifact)
