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

from nbs_bl.configuration import load_and_configure_everything
from nbs_bl.beamline import GLOBAL_BEAMLINE



load_and_configure_everything()


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