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
#import ucal
#from ucal.startup import *
#from ucal.plans.alignment import load_saved_manipulator_calibration
#from bluesky.callbacks import LiveTable
from bluesky_queueserver import is_re_worker_active

from nbs_bl.configuration import load_and_configure_everything
from nbs_bl.globalVars import GLOBAL_BEAMLINE
from tiled.client import from_profile
import os


load_and_configure_everything()

# nslsii.configure_base(get_ipython().user_ns, "ucal", bec=False, publish_documents_with_kafka=True)
ipython = get_ipython()

configure_bluesky_logging(ipython=ipython)
    
# IPython logging will be enabled with logstart(...)
configure_ipython_logging(exception_logger=log_exception, ipython=ipython)
    
ipython.run_line_magic("xmode", "minimal")

tiled_writing_client = from_profile("nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_NEXAFS"])['ucal']['raw']

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
        time.sleep(2)
    else:
        raise error

RE.subscribe(post_document)
configure_kafka_publisher(RE, beamline_name="ucal")

if is_re_worker_active():
    RE.waiting_hook = None
    
loadfile = beamline_config.get("loadfile", None)
if loadfile is not None and loadfile != "":
    print("Loading last samples")
    if beamline_config.get("bar", "") == "Standard 4-sided bar":
        load_standard_four_sided_bar(loadfile)
        sampleholder.print_samples()
    RE(load_saved_manipulator_calibration())
print("Loading last saved manipulator calibration")

print("Setting TES Path")
if 'tes' in GLOBAL_BEAMLINE.devices:
    def make_dynamic_path():
        yearstr = RE.md.get('cycle', None)
        datasession = RE.md.get('data_session', None)
        if yearstr is None or datasession is None:
            print("Not enough info to set TES File Path")
            return None
        else:
            path = f"/nsls2/data/sst/proposals/{yearstr}/{datasession}/assets/ucal-1/%Y/%m/%2d"
            return path
    tes._dynamic_path = make_dynamic_path
        

# sd SupplementalData preprocessor is automatically loaded and
# subscribed to RunEngine by nslsii.configure_base
#sd.baseline.append(eslit)

# Fix LiveTable display
#LiveTable._FMT_MAP["number"] = "g"
