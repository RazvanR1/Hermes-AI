from providers.operations import sysadmin as sysadmin_router


def register(mcp):
    @mcp.tool()
    def sysadmin(request: str = ""):
        """
        Main and ONLY public AI SysAdmin tool for the homelab.

        Use for:
        - server status
        - homelab health
        - problems
        - updates
        - maintenance
        - recommendations
        - safe auto-fix
        - history
        - changes
        - trends
        """
        return sysadmin_router.run(request)
