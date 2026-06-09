# Local Verification

run the following commands from the repository root to verify the build locally within the Docker container:

```shell
# Run tests
docker compose run --rm backend pytest
docker compose run --rm backend behave features/

# Run linters
docker compose run --rm backend ruff check .
docker compose run --rm backend bandit -r . -x ./tests,./.venv,./features
```