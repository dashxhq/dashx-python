# dashx-python
DashX Python SDK

## Testing

Install the package in editable mode with dev dependencies, then run pytest from the project root:

```bash
pip install -e ".[dev]"
pytest
```

Tests use **mocked** requests (no real API calls) and set their own env vars via fixtures, so you do **not** need to set `DASHX_PUBLIC_KEY` or `DASHX_PRIVATE_KEY` to run tests.

- Run with verbose output: `pytest -v`
- Run a specific file: `pytest tests/test_client.py`
- Run a specific test: `pytest tests/test_client.py::TestIdentify::test_identify_with_uid_calls_make_request`

## Examples

The `examples/` folder contains scripts that call the **real** DashX API. They require valid credentials via environment variables.

**Required env vars:** `DASHX_PUBLIC_KEY`, `DASHX_PRIVATE_KEY`, `DASHX_TARGET_ENVIRONMENT`  
**Optional:** `DASHX_BASE_URI` (default: `https://api.dashx.com/graphql`)

From the project root:

```bash
export DASHX_PUBLIC_KEY=your_public_key
export DASHX_PRIVATE_KEY=your_private_key
export DASHX_TARGET_ENVIRONMENT=development

python -m examples.identify_example
python -m examples.track_example
```

Or with `PYTHONPATH` if the package isn’t installed: `PYTHONPATH=src python -m examples.identify_example`

See **examples/README.md** for more detail (e.g. using a `.env` file).
