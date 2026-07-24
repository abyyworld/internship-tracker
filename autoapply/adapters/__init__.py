from .ashby import AshbyAdapter
from .greenhouse import GreenhouseAdapter
from .lever import LeverAdapter


def get_adapter(ats: str):
    adapters = {
        "greenhouse": GreenhouseAdapter,
        "lever": LeverAdapter,
        "ashby": AshbyAdapter,
    }
    try:
        return adapters[ats]()
    except KeyError as exc:
        raise ValueError(f"Unsupported ATS for browser automation: {ats}") from exc
