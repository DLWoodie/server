"""
Tests for the Hue Lights Sync settings readers and their translations.

Brightness, vividness and latency all accept 0 as a valid value (the config
entries declare ranges of 0-100, 0-100 and 0-3000), so the readers must fall
back to the default only when nothing is configured. That same fallback is
what an install saved before a setting existed reads, so adding a setting
needs no migration of stored config.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import pytest
from music_assistant_models.config_entries import ConfigEntry, ConfigValueType, ProviderConfig
from music_assistant_models.enums import ConfigEntryType, ProviderType

from music_assistant.providers.hue_entertainment import constants as hue_constants
from music_assistant.providers.hue_entertainment.constants import (
    CONF_BRIGHTNESS,
    CONF_COLOR_MODE,
    CONF_COLOR_VIVIDNESS,
    CONF_HUE_LATENCY_MS,
    DEFAULT_BRIGHTNESS,
    DEFAULT_COLOR_MODE,
    DEFAULT_COLOR_VIVIDNESS,
    DEFAULT_HUE_LATENCY_MS,
)
from music_assistant.providers.hue_entertainment.provider import HueEntertainmentProvider
from music_assistant.providers.hue_entertainment.settings import (
    get_brightness,
    get_color_mode,
    get_color_vividness,
    get_hue_latency_ms,
)

# the provider's strings live next to its constants module
_STRINGS_PATH = Path(hue_constants.__file__).resolve().parent / "strings.json"


def _config(**values: ConfigValueType) -> ProviderConfig:
    """Build a ProviderConfig holding only the given settings."""
    entries = {}
    for key, value in values.items():
        entry = ConfigEntry(key=key, type=ConfigEntryType.STRING)
        entry.value = value
        entries[key] = entry
    return ProviderConfig(
        type=ProviderType.PLUGIN,
        domain="hue_entertainment",
        instance_id="hue_entertainment--test",
        values=entries,
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0, 0), (50, 50), (100, 100), ("75", 75), (62.5, 62)],
    ids=["zero", "mid", "max", "string", "float"],
)
def test_get_brightness(value: ConfigValueType, expected: int) -> None:
    """Brightness is read as-is, including 0."""
    assert get_brightness(_config(**{CONF_BRIGHTNESS: value})) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0, 0), (120, 120), ("250", 250)],
    ids=["zero", "mid", "string"],
)
def test_get_hue_latency_ms(value: ConfigValueType, expected: int) -> None:
    """Latency is read as-is, including 0."""
    assert get_hue_latency_ms(_config(**{CONF_HUE_LATENCY_MS: value})) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0, 0), (50, 50), (100, 100), ("80", 80), (62.5, 62)],
    ids=["zero", "default", "max", "string", "float"],
)
def test_get_color_vividness(value: ConfigValueType, expected: int) -> None:
    """Vividness is read as-is, including 0."""
    assert get_color_vividness(_config(**{CONF_COLOR_VIVIDNESS: value})) == expected


def test_get_color_mode() -> None:
    """Colour mode is read as-is."""
    assert get_color_mode(_config(**{CONF_COLOR_MODE: "ambient"})) == "ambient"


@pytest.mark.parametrize(
    ("reader", "default"),
    [
        (get_brightness, DEFAULT_BRIGHTNESS),
        (get_hue_latency_ms, DEFAULT_HUE_LATENCY_MS),
        (get_color_mode, DEFAULT_COLOR_MODE),
        (get_color_vividness, DEFAULT_COLOR_VIVIDNESS),
    ],
    ids=["brightness", "latency", "color_mode", "color_vividness"],
)
def test_unset_setting_falls_back_to_default(
    reader: Callable[[ProviderConfig], int | str], default: int | str
) -> None:
    """An unconfigured setting yields the default."""
    assert reader(_config()) == default


async def test_every_setting_is_translated() -> None:
    """Each settings entry has its label and description in strings.json."""
    strings = json.loads(_STRINGS_PATH.read_text(encoding="utf-8"))["config_entries"]
    provider = HueEntertainmentProvider.__new__(HueEntertainmentProvider)
    for entry in await provider.get_config_entries():
        assert {"label", "description"} <= strings[entry.key].keys()
