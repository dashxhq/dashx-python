"""
Execute a flow with the DashX API.

Prompts via CLI for Flow ID, arguments (JSON), and optional scheduledAt.

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
  python -m examples.execute_flow_example
"""
import json
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

    flow_id = input("Flow ID (UUID): ").strip()
    if not flow_id:
        print("Flow ID is required.")
        sys.exit(1)

    while True:
        raw_args = input("Arguments (JSON, e.g. {\"key\": \"value\"}): ").strip()
        if not raw_args:
            print("Arguments are required.")
            continue
        try:
            arguments = json.loads(raw_args)
            break
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}. Try again.")

    raw_scheduled = input("scheduledAt (optional; press Enter to skip): ").strip()
    scheduled_at = raw_scheduled if raw_scheduled else None

    client = DashX()
    result = client.execute_flow(
        flow_id=flow_id,
        arguments=arguments,
        scheduled_at=scheduled_at,
    )
    print("Result:", result)


if __name__ == "__main__":
    main()
