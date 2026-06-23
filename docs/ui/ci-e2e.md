# E2E CI Pipeline Design

## Trigger Conditions

The pipeline is configured in `.github/workflows/e2e.yml` and triggers whenever code is pushed to the repository, a pull request is opened or updated, or the workflow is triggered manually from the GitHub Actions UI.

## Environment Setup

The pipeline sets up both the backend and frontend before executing tests. Both use python. However node is needed to install cypress and run the tests. 

### Backend Startup
1. The pipeline installs Python dependencies (`pip install -r requirements.txt`).
2. It starts the FastAPI backend using `uvicorn main:app --host 0.0.0.0 --port 8000 &`.
3. The environment variable `LLM_PROVIDER` is set to `mock`. This ensures that all E2E tests run against a deterministic response from the backend rather than hitting the real Groq API. This avoids network latency, rate limits, and non-deterministic text outputs. It also avoids the need to provide an API key to GitHub.

### Frontend Startup
1. The pipeline installs Streamlit dependencies (`pip install -r requirements.txt`).
2. It starts the frontend using `streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &`.
3. The pipeline uses the `wait-on` npm package to poll `http-get://127.0.0.1:8000/` and `http-get://127.0.0.1:8501/` to ensure both servers are fully initialized and responding before test execution begins.

## Testing Framework

**Framework:** Cypress

We chose cypress for reasons detailed in `docs/ui/e2e-setup.md`.

## Artifact Management

If any E2E test fails during the CI run, the workflow uses `actions/upload-artifact@v4` to preserve critical debugging information. Screenshots are automatically captured at the exact moment of failure. These are uploaded to GitHub Actions artifacts under the name `cypress-screenshots`. Cypress records video of the entire test run, providing full context of what led to the failure. These are uploaded as `cypress-videos`.

## Trade-offs

- **Runtime:** Starting both a Python backend and a Python frontend in the same GitHub Actions runner takes a minute or two. Using a mock backend mitigates some of this time by eliminating API call latency.
- **Flakiness:** While the mock LLM removes non-determinism from the AI responses, browser tests are inherently susceptible to timing-related flakiness. We rely on Cypress's automatic waiting and `wait-on` to reduce this risk.
- **Resource Cost:** Running full browser E2E tests takes more processing than unit or API tests. However, the value of catching critical user-facing errors outweighs the cost.

## Evidence of Green Run

*[Insert screenshot or link to a successful GitHub Actions run here after pushing to the repository.]*



**This file was generated with the help of AI. All AI-generated content was thoroughly reviewed and edited by a human**