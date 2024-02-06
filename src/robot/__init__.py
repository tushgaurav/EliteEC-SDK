from importlib import resources
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

__version__ = "0.0.2"
__all__ = ["Logo", "SDK"]

from .logo import Logo
from .SDK import Robot

_cfg = tomllib.loads(resources.read_text("robot", "config.toml"))
DOWNLOADS = _cfg["website"]["download_url"]
