"""
Tests for how the Hue bridge hands the playback settings to its analyzer.

A bridge builds its analyzer from the provider config when it starts, and the
manager fans a live settings change out to every bridge, so both paths have
to carry each analyzer setting through.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock

from hue_entertainment import LightChannel

from music_assistant.providers.hue_entertainment.analyzer import HueAudioAnalyzer
from music_assistant.providers.hue_entertainment.bridge import (
    HueEntertainmentBridge,
    HueEntertainmentBridgeManager,
)
from music_assistant.providers.hue_entertainment.constants import (
    CONF_BRIGHTNESS,
    CONF_COLOR_MODE,
    CONF_COLOR_VIVIDNESS,
)

if TYPE_CHECKING:
    from music_assistant_models.config_entries import ConfigValueType


def _make_bridge(values: dict[str, ConfigValueType]) -> HueEntertainmentBridge:
    """Build a bridge for a one-light area whose provider config holds ``values``."""
    provider = MagicMock()
    provider.config.get_value.side_effect = values.get
    area = MagicMock()
    area.id = "area-1"
    area.name = "Living room"
    area.channels = [LightChannel(channel_id=0, service_id="svc_0", name="Light 0")]
    return HueEntertainmentBridge(provider, area, MagicMock())


def _assert_analyzer_settings(analyzer: HueAudioAnalyzer | None) -> None:
    """Assert ``analyzer`` runs on ambient, brightness 40 and vividness 100."""
    assert analyzer is not None
    assert analyzer._color_mode == "ambient"
    assert analyzer._brightness == 0.4
    assert analyzer._saturation == HueAudioAnalyzer([], vividness=100)._saturation


async def test_start_builds_the_analyzer_from_the_config() -> None:
    """Every analyzer setting is read from the provider config at start."""
    bridge = _make_bridge(
        {
            CONF_COLOR_MODE: "ambient",
            CONF_BRIGHTNESS: 40,
            CONF_COLOR_VIVIDNESS: 100,
        }
    )
    await bridge.start()
    _assert_analyzer_settings(bridge._analyzer)


def test_live_settings_reach_every_bridge_analyzer() -> None:
    """The manager's fan-out carries every analyzer setting to a running bridge."""
    bridge = _make_bridge({})
    bridge._analyzer = HueAudioAnalyzer(bridge.area.channels)
    manager = HueEntertainmentBridgeManager(bridge.provider)
    manager._bridges[bridge.area.id] = bridge
    manager.update_settings(color_mode="ambient", brightness=40, vividness=100)
    _assert_analyzer_settings(bridge._analyzer)
