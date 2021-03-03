_DEFAULTS = {
    "red":   "\033[31m",
    "green": "\033[32m",
    "blue":  "\033[34m",
    "bold":  "\033[1m",
    "close": "\033[0m",
}

_COLORS = {
    "red":   _DEFAULTS["red"],
    "green": _DEFAULTS["green"],
    "blue":  _DEFAULTS["blue"],
    "bold":  _DEFAULTS["bold"],
    "close": _DEFAULTS["close"],
}


def disable() -> None:
    _COLORS["red"]   = ""
    _COLORS["green"] = ""
    _COLORS["blue"]  = ""
    _COLORS["bold"]  = ""
    _COLORS["close"] = ""


def enable() -> None:
    _COLORS["red"]   = _DEFAULTS["red"]
    _COLORS["green"] = _DEFAULTS["green"]
    _COLORS["blue"]  = _DEFAULTS["blue"]
    _COLORS["bold"]  = _DEFAULTS["bold"]
    _COLORS["close"] = _DEFAULTS["close"]


def green(s: str) -> str:
    return _COLORS["green"] + s + _COLORS["close"]


def red(s: str) -> str:
    return _COLORS["red"] + s + _COLORS["close"]


def blue(s: str) -> str:
    return _COLORS["blue"] + s + _COLORS["close"]


def bold(s: str) -> str:
    return _COLORS["bold"] + s + _COLORS["close"]
