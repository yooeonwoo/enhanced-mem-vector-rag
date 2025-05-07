#!/usr/bin/env python
"""Entry point for running the EMVR UI.

This script is a simple wrapper around the Chainlit UI.
"""

import argparse
import logging
import sys

from emvr.ui.run import run_chainlit

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main() -> int:
    """Run the UI."""
    parser = argparse.ArgumentParser(description="Run the EMVR UI")
    parser.add_argument(
        "--host", default="localhost",
        help="Host to bind to (default: localhost)",
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Port to bind to (default: 8000)",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Run in debug mode",
    )

    args = parser.parse_args()

    try:
        run_chainlit(
            host=args.host,
            port=args.port,
            debug=args.debug,
        )
    except KeyboardInterrupt:
        logger.info("UI stopped by user")
    except Exception:
        logger.exception("Error running UI")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
