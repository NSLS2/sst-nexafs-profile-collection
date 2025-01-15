#import sys
#from pathlib import Path

"""
paths = [
    path
    for path in Path(
        "/nsls2/data/sst/ucal/shared/config/bluesky/collection_packages"
    ).glob("*")
    if path.is_dir()
]
for path in paths:
    sys.path.append(str(path))
"""

from nslsii import configure_kafka_publisher, configure_bluesky_logging, configure_ipython_logging
from nslsii.common.ipynb.logutils import log_exception
from bluesky.plan_stubs import mv as _mv, mvr as _mvr

#from ucal.startup import *
#from ucal.plans.alignment import load_saved_manipulator_calibration
#from bluesky.callbacks import LiveTable
from bluesky_queueserver import is_re_worker_active

from nbs_bl.configuration import load_and_configure_everything
from nbs_bl.beamline import GLOBAL_BEAMLINE
from tiled.client import from_profile
import time as ttime
import os


load_and_configure_everything()

# nslsii.configure_base(get_ipython().user_ns, "ucal", bec=False, publish_documents_with_kafka=True)
ipython = get_ipython()

configure_bluesky_logging(ipython=ipython)
    
# IPython logging will be enabled with logstart(...)
configure_ipython_logging(exception_logger=log_exception, ipython=ipython)
    
ipython.run_line_magic("xmode", "minimal")

tiled_writing_client = from_profile("nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_NEXAFS"])['ucal']['raw']
#c = tiled_reading_client = from_profile("nsls2")["ucal"]["raw"]

# check the current logged in + active user
def whoami():
    try:
        print(f"\nLogged in to Tiled as: {c.context.whoami()['identities'][0]['id']}\n")
    except TypeError as e:
        print("Not authenticated with Tiled! Please login...")


# whoami()


# logout of Tiled and clear the cached default identities (username)
def logout():
    c = getattr(GLOBAL_BEAMLINE, "tiled_reading_client", None)
    if c is not None:
        c.logout(clear_default=True)


# login to Tiled using the specified username
# this version automatically logs-out the existing user when called
def login():
    c = getattr(GLOBAL_BEAMLINE, "tiled_reading_client", None)
    if c is None:
        c = from_profile("nsls2")["ucal"]["raw"]
        GLOBAL_BEAMLINE.tiled_reading_client = c
    beamline_username = input("Please enter your username: ")
    beamline_unauthenticated = (
        c.context.api_key is None and c.context.http_client.auth is None
    )
    if not beamline_unauthenticated:
        beamline_current_user = c.context.whoami()["identities"][0]["id"]
        if beamline_username != beamline_current_user:
            logout()

    c.login(username=beamline_username)

    print(f"Logged in to Tiled as {beamline_username}!")


def post_document(name, doc):
    ATTEMPTS = 20
    error = None
    for attempt in range(ATTEMPTS):
        try:
            tiled_writing_client.post_document(name, doc)
        except Exception as e:
            print(f"Document saving failure: {e!r}")
            error = e
        else:
            break
        ttime.sleep(2)
    else:
        raise error

RE.subscribe(post_document)
configure_kafka_publisher(RE, beamline_name="ucal")

if is_re_worker_active():
    RE.waiting_hook = None

""" Need to update with new manipulator stuff
loadfile = beamline_config.get("loadfile", None)
if loadfile is not None and loadfile != "":
    print("Loading last samples")
    if beamline_config.get("bar", "") == "Standard 4-sided bar":
        load_standard_four_sided_bar(loadfile)
        sampleholder.print_samples()
    RE(load_saved_manipulator_calibration())
print("Loading last saved manipulator calibration")
"""

# A bug in bluesky 1.13 causes QueueServer validation to fail
# for mv and mvr due to an unserializable type annotation (NamedMovable)
# Redefine without type annotation to fix temporarily
def mv(*args, group=None, **kwargs):
    yield from _mv(*args, group=group, **kwargs)

def mvr(*args, group=None, **kwargs):
    yield from _mvr(*args, group=group, **kwargs)

move = mv


print("Setting TES Path")
if 'tes' in GLOBAL_BEAMLINE.devices:
    def make_dynamic_path():
        yearstr = RE.md.get('cycle', None)
        datasession = RE.md.get('data_session', None)
        is_commissioning = "commissioning" in RE.md.get('proposal', {}).get("type", "").lower()
        if yearstr is None or datasession is None:
            print("Not enough info to set TES File Path")
            return None
        elif is_commissioning:
            #path_dated_subdir = ttime.strftime("%Y/%m/%d", ttime.localtime())
            #path = f"/nsls2/data/sst/proposals/{yearstr}/{datasession}/assets/ucal-1/{path_dated_subdir}"
            path = f"/nsls2/data/sst/proposals/commissioning/{datasession}/assets/ucal-1/%Y/%m/%2d"
            return path
        else:
            path = f"/nsls2/data/sst/proposals/{yearstr}/{datasession}/assets/ucal-1/%Y/%m/%2d"
            return path
    tes._dynamic_path = make_dynamic_path
        

# sd SupplementalData preprocessor is automatically loaded and
# subscribed to RunEngine by nslsii.configure_base
#sd.baseline.append(eslit)

# Fix LiveTable display
#LiveTable._FMT_MAP["number"] = "g"
