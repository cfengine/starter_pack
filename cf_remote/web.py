import requests
from cf_remote.utils import write_json, read_json, file_name, cf_remote_dir
from cf_remote import log


def get_json(url):
    filename = cf_remote_dir("/json/" + file_name(url))
    local_data = read_json(filename)
    if local_data:
        log.info("Using cached data for {}".format(url))
        return local_data
    r = requests.get(url)
    assert r.status_code >= 200 and r.status_code < 300
    data = r.json()

    write_json(filename, data)

    return data
