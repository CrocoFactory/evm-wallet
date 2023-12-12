from typing import Any


class InvalidNetworkInfo(TypeError):
    """Raised when network info doesn't provide valid information"""
    def __init__(self, value: Any):
        super().__init__(f"Network information must be represented as NetworkInfo type or name of a supported "
                         f"network. You provided value: {value}")
