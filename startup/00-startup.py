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

import nslsii
#import ucal
#from ucal.startup import *
#from ucal.plans.alignment import load_saved_manipulator_calibration
#from bluesky.callbacks import LiveTable
from bluesky_queueserver import is_re_worker_active

from nbs_bl.configuration import load_and_configure_everything

load_and_configure_everything()

nslsii.configure_base(get_ipython().user_ns, "ucal", bec=False, publish_documents_with_kafka=True)

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



# sd SupplementalData preprocessor is automatically loaded and
# subscribed to RunEngine by nslsii.configure_base
#sd.baseline.append(eslit)

# Fix LiveTable display
#LiveTable._FMT_MAP["number"] = "g"
