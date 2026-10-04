"""Config constants for the Hue Lights Sync provider."""

from __future__ import annotations

from typing import Final

CONF_BRIDGE_HOST: Final[str] = "bridge_host"
CONF_BRIDGE_ID: Final[str] = "bridge_id"
CONF_ACTION_PAIR: Final[str] = "pair"
CONF_USERNAME: Final[str] = "hue_username"
CONF_CLIENTKEY: Final[str] = "hue_clientkey"
CONF_BRIGHTNESS: Final[str] = "brightness"
CONF_COLOR_MODE: Final[str] = "color_mode"
CONF_COLOR_VIVIDNESS: Final[str] = "color_vividness"
CONF_PALETTE_SCHEME: Final[str] = "palette_scheme"
CONF_HUE_LATENCY_MS: Final[str] = "hue_latency_ms"

# Visualization modes; first entry is the default. Used to build the config
# options and to migrate away orphaned stored values from older versions.
COLOR_MODES: Final[tuple[str, ...]] = ("smooth", "ambient", "flashing", "energetic")
DEFAULT_COLOR_MODE: Final[str] = COLOR_MODES[0]

# Palette schemes; first entry is the default. "artwork" cycles the album art's
# own colors, every other scheme generates the palette (see the analyzer).
PALETTE_SCHEMES: Final[tuple[str, ...]] = (
    "artwork",
    "triadic",
    "tetradic",
    "complementary",
    "analogous",
    "fixed",
)
DEFAULT_PALETTE_SCHEME: Final[str] = PALETTE_SCHEMES[0]

DEFAULT_BRIGHTNESS: Final[int] = 100

# Mid-scale, because the vividness setting is symmetric around the look the
# provider rendered before it existed.
DEFAULT_COLOR_VIVIDNESS: Final[int] = 50

DEFAULT_HUE_LATENCY_MS: Final[int] = 20

HUE_MDNS_TYPE: Final[str] = "_hue._tcp.local."

# The devicetype registered with the Hue bridge during pairing. Shown in the
# Hue app's list of linked apps; keeps Music Assistant's identity on (re)pair.
HUE_DEVICE_TYPE: Final[str] = "music_assistant#hue_entertainment"

# ---- Spectrum config requested from the Sendspin visualizer ----

# 17 mel bins over 20-20kHz: enough resolution to map distinct bands to lights
# while keeping the per-frame payload small (bin ~10 ≈ 3.5kHz is the musical
# ceiling, see _CHANNEL_BIN_MAX in the analyzer).
SPECTRUM_BINS: Final[int] = 17
SPECTRUM_SCALE: Final = "mel"
SPECTRUM_F_MIN: Final[int] = 20
SPECTRUM_F_MAX: Final[int] = 20000
