from providers.docker import client as docker

def register(mcp):
    @mcp.tool()
    def docker_ps():
        """List Docker containers."""
        return docker.ps()

    @mcp.tool()
    def docker_stats():
        """Return Docker container resource usage."""
        return docker.stats()

    @mcp.tool()
    def docker_images():
        """List Docker images."""
        return docker.images()

    @mcp.tool()
    def docker_info():
        """Return Docker daemon info."""
        return docker.info()

    @mcp.tool()
    def docker_logs(container: str, tail: int = 100):
        """Return Docker container logs."""
        return docker.logs(container, tail)

    @mcp.tool()
    def docker_restart(container: str):
        """Restart Docker container."""
        return docker.restart(container)

    @mcp.tool()
    def docker_start(container: str):
        """Start Docker container."""
        return docker.start(container)

    @mcp.tool()
    def docker_stop(container: str):
        """Stop Docker container."""
        return docker.stop(container)

    @mcp.tool()
    def docker_compose_ls():
        """List Docker Compose projects."""
        return docker.compose_ls()

    @mcp.tool()
    def docker_inspect(container: str):
        """Inspect Docker container."""
        return docker.inspect(container)

    @mcp.tool()
    def docker_exec(container: str, command: str):
        """Execute command inside Docker container."""
        return docker.exec(container, command)

    @mcp.tool()
    def docker_pull(image: str):
        """Pull Docker image."""
        return docker.pull(image)

    @mcp.tool()
    def docker_remove(container: str):
        """Remove Docker container."""
        return docker.remove(container)

    @mcp.tool()
    def docker_networks():
        """List Docker networks."""
        return docker.networks()

    @mcp.tool()
    def docker_volumes():
        """List Docker volumes."""
        return docker.volumes()

