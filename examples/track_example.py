"""
Track an event with the DashX API.

Requires environment variables:
  DASHX_PUBLIC_KEY   - Your DashX public key
  DASHX_PRIVATE_KEY  - Your DashX private key
  DASHX_TARGET_ENVIRONMENT - Target environment (e.g. development, production)

Optional:
  DASHX_BASE_URI     - API base URL (default: https://api.dashx.com/graphql)

Run from project root:
  export DASHX_PUBLIC_KEY=your_public_key
  export DASHX_PRIVATE_KEY=your_private_key
  export DASHX_TARGET_ENVIRONMENT=development
  python -m examples.track_example
"""
import os
import sys

# Allow running from project root without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dashx import DashX


def main():
    public_key = os.environ.get("DASHX_PUBLIC_KEY")
    private_key = os.environ.get("DASHX_PRIVATE_KEY")
    target_env = os.environ.get("DASHX_TARGET_ENVIRONMENT")

    if not all([public_key, private_key, target_env]):
        print(
            "Missing required env vars. Set DASHX_PUBLIC_KEY, DASHX_PRIVATE_KEY, "
            "and DASHX_TARGET_ENVIRONMENT. See script docstring."
        )
        sys.exit(1)

    client = DashX()

    # Track event for a known user
    result = client.track(
        event="purchase",
        uid="example-user-123",
        data={"amount": 99.99, "currency": "USD"},
    )
    print("Track (with uid):", result)

    # Track event anonymously
    result = client.track(event="page_view", data={"path": "/home"})
    print("Track (anonymous):", result)


if __name__ == "__main__":
    main()
