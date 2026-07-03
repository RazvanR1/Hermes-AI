from providers.truenas import client as truenas

def register(mcp):
    @mcp.tool()
    def truenas_system_info():
        """Return TrueNAS system information."""
        return truenas.system_info()

    @mcp.tool()
    def truenas_pools():
        """Return TrueNAS pool status."""
        return truenas.pools()

    @mcp.tool()
    def truenas_disks():
        """Return TrueNAS disks."""
        return truenas.disks()

    @mcp.tool()
    def truenas_datasets():
        """Return TrueNAS datasets."""
        return truenas.datasets()

    @mcp.tool()
    def truenas_shares_smb():
        """Return TrueNAS SMB shares."""
        return truenas.shares_smb()

    @mcp.tool()
    def truenas_alerts():
        """Return TrueNAS alerts."""
        return truenas.alerts()

    @mcp.tool()
    def truenas_smart_tests():
        """Return TrueNAS SMART test configuration."""
        return truenas.smart_tests()

    @mcp.tool()
    def truenas_scrub_tasks():
        """Return TrueNAS scrub tasks."""
        return truenas.scrub_tasks()

    @mcp.tool()
    def truenas_snapshots():
        """Return TrueNAS ZFS snapshots."""
        return truenas.snapshots()

    @mcp.tool()
    def truenas_health():
        """Return a combined TrueNAS health report with system, pools, alerts and disks."""
        return truenas.health()
