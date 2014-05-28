import sys
import os
import requests

sys.path.insert(0, os.path.join(os.environ["CSK_HOME"], "legato", "lib"))

from cskconfig import config
from cskpipeline import data

# the following settings will be found in /etc/cato/legato.yaml
cfg = config.get_plugin_conf("buildbot")
URL = cfg.get("url")


def print_request_error(msg, url, error):
    """Will print a custom error message, url and requests error"""

    print("%s\n%s\n%s" % (msg, url, error))


def issue_request(url):
    """Used to issue get requests for Buildbot."""

    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.Timeout as e:
        m = "Timeout attempting to access Buildbot server. Check address, port, " \
            "protocol and any firewall settings"
        print_request_error(m, url, e)
        raise Exception(e)
    except requests.exceptions.TooManyRedirects as e:
        m = "Too many redirect requests attempting to access the Buildbot server."
        print_request_error(m, url, e)
        raise Exception(e)
    except requests.exceptions.HTTPError as e:
        m = "HTTP error, connection established but the Buildbot server " \
            "responded with an http error code. Possibly wrong builder or build number"
        print_request_error(m, url, e)
        raise Exception(e)
    except requests.exceptions.ConnectionError as e:
        m = "Connection error attemtping to communicate with Buildbot server. " \
            "Check http or https, server address and port"
        print_request_error(m, url, e)
        raise Exception(e)
    except requests.exceptions.RequestException as e:
        m = "Exception attempting to access Buildbot server."
        print_request_error(m, url, e)
        raise Exception(e)

    # we made it this far, the response should be json
    return r.json()


def get_build_info(step, args):
    """Will retrieve the buildbot build information in json format and will
       store the json in the release candidate data document.
       This plugin requires that the build number and builder name be
       passed as arguments in the pipeline."""

    # args is a dictionary that is defined in the pipeline document,
    # or more specifically on the stage, step.
    builder = args.get("builder")
    build_number = args.get("build_number")

    # test the arguments, if either is empty, return False
    # either False or an Exception will cause the pipeline to stop and error

    if not builder or not len(builder):
        print("Buildbot plugin builder parameter is required")
        return False
    if not build_number or not len(build_number):
        print("Buildbot plugin build_number parameter is required")
        return False

    url = "%s/json/builders/%s/builds/%s" % (URL, builder, build_number)

    j = issue_request(url)

    # now we need to store the json retrieved from Buildbot in the release candidate
    # data store. 
    step.update_data({"buildbot": j})
    print j

    # everything worked as expected
    return True
