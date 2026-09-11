from .ashby import AshbyAdapter
from .greenhouse import GreenhouseAdapter
from .lever import LeverAdapter
from .workday import WorkdayAdapter


def get_adapter(ats: str):
    adapters = {
        "greenhouse": GreenhouseAdapter,
        "lever": LeverAdapter,
        "ashby": AshbyAdapter,
        "workday": WorkdayAdapter,
    }
    try:
        return adapters[ats]()
    except KeyError as exc:
        raise ValueError(f"Unsupported ATS for browser automation: {ats}") from exc
