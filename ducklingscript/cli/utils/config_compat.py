
from typing import Any


def verify_compat(
    config: Any,
):
    if not hasattr(config, "config_version"):
        ...

    return config