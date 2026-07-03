from providers.homelab import client

def register(mcp):
    @mcp.tool()
    def homelab_health():
        """Return overall health of Proxmox, Docker, Home Assistant and TrueNAS."""
        return client.health()

    @mcp.tool()
    def homelab_health_summary():
        """Return compact overall homelab health summary."""
        return client.health_summary()

    @mcp.tool()
    def homelab_auto_fix():
        """Safely attempt automatic fixes for common homelab issues."""
        return client.auto_fix()
