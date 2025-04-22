import importlib.metadata
from .client import DiavgeiaClient

try:
    # Read the version from the installed package metadata
    __version__ = importlib.metadata.version("diavgeia-api")
except importlib.metadata.PackageNotFoundError:
    # Fallback if the package is not installed (e.g., during development)
    __version__ = "0.0.0-dev"  # Or handle as appropriate

__all__ = ["DiavgeiaClient", "__version__"]
