"""
Chainlit application runner for EMVR.

This module provides a function to run the Chainlit UI application.
"""

import logging
import os
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def run_chainlit(
    host: str = "localhost",
    port: int = 8000,
    debug: bool = False,
) -> None:
    """
    Run the Chainlit UI application.

    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Whether to run in debug mode

    """
    try:
        # Get project root directory
        project_root = Path(__file__).parent.parent.parent.resolve()

        # Set environment variables
        env = os.environ.copy()
        env["CHAINLIT_HOST"] = host
        env["CHAINLIT_PORT"] = str(port)

        if debug:
            env["CHAINLIT_DEBUG"] = "true"

        # Determine app path
        app_path = os.path.join(
            project_root, "emvr", "ui", "app.py",
        )

        # Build command
        cmd = [
            "chainlit", "run", app_path,
            "--host", host,
            "--port", str(port),
        ]

        if debug:
            cmd.append("--debug")

        # Run Chainlit
        logger.info("Starting Chainlit UI on %s:%s", host, port)
        subprocess.run(cmd, env=env, cwd=str(project_root), check=False)

    except Exception:
        logger.exception("Error running Chainlit")
        raise


if __name__ == "__main__":
    # When run directly, start the UI
    import argparse

    parser = argparse.ArgumentParser(description="Run EMVR Chainlit UI")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")

    args = parser.parse_args()

    run_chainlit(
        host=args.host,
        port=args.port,
        debug=args.debug,
    )
