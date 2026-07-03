#!/usr/bin/env python3
import os
import sys


def load_env_file(path="/home/hermes/.hermes/.env"):
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    except FileNotFoundError:
        pass


load_env_file()
sys.path.insert(0, "/home/hermes/homelab-plugin")

from mcp.server.fastmcp import FastMCP
from providers.operations.tools import register as register_operations

mcp = FastMCP("homelab")
register_operations(mcp)

if __name__ == "__main__":
    mcp.run()
