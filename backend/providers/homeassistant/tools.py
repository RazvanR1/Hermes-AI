from providers.homeassistant import client as ha

def register(mcp):
    @mcp.tool()
    def homeassistant_status():
        """Return Home Assistant API status."""
        return ha.status()

    @mcp.tool()
    def homeassistant_config():
        """Return Home Assistant configuration info."""
        return ha.config()

    @mcp.tool()
    def homeassistant_entities():
        """Return all Home Assistant entity states."""
        return ha.states()

    @mcp.tool()
    def homeassistant_state(entity_id: str):
        """Return one Home Assistant entity state."""
        return ha.state(entity_id)

    @mcp.tool()
    def homeassistant_services():
        """Return Home Assistant available services."""
        return ha.services()

    @mcp.tool()
    def homeassistant_events():
        """Return Home Assistant event types."""
        return ha.events()

    @mcp.tool()
    def homeassistant_call_service(domain: str, service: str, data: dict = {}):
        """Call any Home Assistant service."""
        return ha.call_service(domain, service, data)

    @mcp.tool()
    def homeassistant_light_on(entity_id: str):
        """Turn on a light."""
        return ha.call_service(
            "light",
            "turn_on",
            {"entity_id": entity_id},
        )

    @mcp.tool()
    def homeassistant_light_off(entity_id: str):
        """Turn off a light."""
        return ha.call_service(
            "light",
            "turn_off",
            {"entity_id": entity_id},
        )

    @mcp.tool()
    def homeassistant_switch_on(entity_id: str):
        """Turn on a switch."""
        return ha.call_service(
            "switch",
            "turn_on",
            {"entity_id": entity_id},
        )

    @mcp.tool()
    def homeassistant_switch_off(entity_id: str):
        """Turn off a switch."""
        return ha.call_service(
            "switch",
            "turn_off",
            {"entity_id": entity_id},
        )

    @mcp.tool()
    def homeassistant_climate_temperature(entity_id: str, temperature: float):
        """Set climate target temperature."""
        return ha.call_service(
            "climate",
            "set_temperature",
            {
                "entity_id": entity_id,
                "temperature": temperature,
            },
        )

    @mcp.tool()
    def homeassistant_climate_mode(entity_id: str, hvac_mode: str):
        """Set climate HVAC mode."""
        return ha.call_service(
            "climate",
            "set_hvac_mode",
            {
                "entity_id": entity_id,
                "hvac_mode": hvac_mode,
            },
        )

    @mcp.tool()
    def homeassistant_climate_fan_mode(entity_id: str, fan_mode: str):
        """Set climate fan mode."""
        return ha.climate_fan_mode(entity_id, fan_mode)

    @mcp.tool()
    def homeassistant_climate_preset_mode(entity_id: str, preset_mode: str):
        """Set climate preset mode."""
        return ha.climate_preset_mode(entity_id, preset_mode)

    @mcp.tool()
    def homeassistant_climate_swing_mode(entity_id: str, swing_mode: str):
        """Set climate swing mode."""
        return ha.climate_swing_mode(entity_id, swing_mode)


    @mcp.tool()
    def homeassistant_script_run(entity_id: str):
        """Run a Home Assistant script."""
        return ha.script_run(entity_id)

    @mcp.tool()
    def homeassistant_scene_activate(entity_id: str):
        """Activate a Home Assistant scene."""
        return ha.scene_activate(entity_id)

    @mcp.tool()
    def homeassistant_automation_enable(entity_id: str):
        """Enable a Home Assistant automation."""
        return ha.automation_enable(entity_id)

    @mcp.tool()
    def homeassistant_automation_disable(entity_id: str):
        """Disable a Home Assistant automation."""
        return ha.automation_disable(entity_id)

    @mcp.tool()
    def homeassistant_automation_trigger(entity_id: str):
        """Trigger a Home Assistant automation."""
        return ha.automation_trigger(entity_id)

