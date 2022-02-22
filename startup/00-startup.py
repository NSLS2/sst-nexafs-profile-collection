import nslsii
import ucal_common as ucal
from ucal_common.startup import *
from ucal_common.run_engine import setup_run_engine
from bluesky import RunEngine

RE = RunEngine(call_returns_result=True)
RE = setup_run_engine(RE)
nslsii.configure_base(get_ipython().user_ns, "ucal")

