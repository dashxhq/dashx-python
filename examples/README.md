# DashX Python SDK – Examples

These examples show how to use the DashX client for **identify** and **track**. They talk to the real DashX API, so you need valid credentials and environment variables set.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DASHX_PUBLIC_KEY` | Yes | Your DashX public key |
| `DASHX_PRIVATE_KEY` | Yes | Your DashX private key |
| `DASHX_TARGET_ENVIRONMENT` | Yes | Target environment (e.g. `development`, `production`) |
| `DASHX_BASE_URI` | No | API base URL (default: `https://api.dashx.com/graphql`) |

## How to run

**From the project root** (`dashx-python/`):

1. Set the required variables (replace with your real keys):

   ```bash
   export DASHX_PUBLIC_KEY=your_public_key
   export DASHX_PRIVATE_KEY=your_private_key
   export DASHX_TARGET_ENVIRONMENT=development
   ```

2. Run an example:

   ```bash
   # With the package installed (pip install -e .)
   python -m examples.identify_example
   python -m examples.track_example
   python -m examples.execute_flow_example
   ```

   Or without installing (examples add `src` to `sys.path`):

   ```bash
   PYTHONPATH=src python -m examples.identify_example
   PYTHONPATH=src python -m examples.track_example
   PYTHONPATH=src python -m examples.execute_flow_example
   ```

## Using a `.env` file (optional)

To avoid exporting variables in the shell, you can use a `.env` file in the project root and load it before running. **Do not commit `.env`** (it should be in `.gitignore`).

1. Install `python-dotenv` (optional):

   ```bash
   pip install python-dotenv
   ```

2. Create `.env` in the project root:

   ```
   DASHX_PUBLIC_KEY=your_public_key
   DASHX_PRIVATE_KEY=your_private_key
   DASHX_TARGET_ENVIRONMENT=development
   ```

3. Load and run:

   ```bash
   set -a && source .env && set +a
   python -m examples.identify_example
   ```

   Or add `load_dotenv()` at the top of an example script if you use `python-dotenv` in the examples.

## Examples

- **identify_example.py** – Identify a user by UID (and optional traits) or anonymously.
- **track_example.py** – Track events with or without a user UID and optional event data.
- **execute_flow_example.py** – Execute a flow; prompts for Flow ID, arguments (JSON), and optional scheduledAt.
