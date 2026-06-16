# Exercise 10.4 — ESBot API Performance Report

## 1. Tool chosen and rationale

**[Locust](https://locust.io/) 2.44.3** was selected for the performance tests.

- **Python-native** — fits the ESBot backend stack; the load scenario lives in a
  single `locustfile.py` alongside the project.
- **Code-as-tests** — request flows are expressed as plain Python, easy to
  version and review.
- **Headless + reports** — runs from the CLI with `--headless` and emits HTML
  dashboards (`smoke.html`, `load.html`, `stress.html`) and CSV summaries for
  reproducible numbers.

Per the exercise guidance, only the **non-LLM endpoints** are exercised
(`/health`, session create/list, message history) so results are deterministic
and reproducible without a live AI inference engine.

## 2. Test environment

| Item | Value |
|------|-------|
| Hardware | Intel Core i5-1135G7 @ 2.40 GHz, 8 logical cores, 8 GB RAM |
| OS | Pop!_OS 24.04 LTS (Linux 6.17) |
| Runtime | Python 3.12.3 |
| Backend | FastAPI + Uvicorn, **single worker** (`--workers 1`) |
| Database | SQLite file (`DATABASE_URL=sqlite:////tmp/esbot_perf.db`), fresh before run |
| LLM provider | **Mock** (`LLM_PROVIDER=mock`) — deterministic, no network |
| Load generator | Locust 2.44.3, same host as backend (loopback `127.0.0.1:8000`) |

> Note: load generator and backend run on the **same machine**, so absolute
> throughput is bounded by shared CPU. Latency figures remain representative for
> relative comparison across the three profiles.

### How the runs were produced

```bash
# 1. Start the backend (mock LLM, fresh DB, single worker)
cd backend
LLM_PROVIDER=mock DATABASE_URL="sqlite:////tmp/esbot_perf.db" \
  python -m uvicorn main:app --host 127.0.0.1 --port 8000 --workers 1

# 2. Run each profile (from docs/api/performance/)
python -m locust -f locustfile.py --headless -u 2   -r 2 -t 30s    --host http://127.0.0.1:8000 --html smoke.html  --csv smoke
python -m locust -f locustfile.py --headless -u 50  -r 1 -t 4m     --host http://127.0.0.1:8000 --html load.html   --csv load
python -m locust -f locustfile.py --headless -u 300 -r 2 -t 3m30s  --host http://127.0.0.1:8000 --html stress.html --csv stress
```

## 3. Results

### Non-functional requirement (NFR)

> **Load:** up to 50 concurrent users · **Response time:** 2–5 s under normal load

### Aggregated results per profile

| Profile | VUs | Requests | Errors | Avg | p90 | p95 | p99 | Max | Throughput |
|---------|----:|---------:|:------:|----:|----:|----:|----:|----:|-----------:|
| Smoke   |   2 |      192 | 0 (0.00%) | 5.3 ms | 7 ms  | 11 ms | 14 ms | 24 ms  | 6.7 req/s   |
| Load    |  50 |   35 055 | 0 (0.00%) | 5.4 ms | 9 ms  | 11 ms | 15 ms | 65 ms  | 146 req/s   |
| Stress  | 300 |  131 572 | 0 (0.00%) | 7.4 ms | 14 ms | 23 ms | 55 ms | 231 ms | 629 req/s   |

(Latency values in **milliseconds**; NFR comparisons are against the
2 000 ms / 5 000 ms targets.)

### Per-endpoint breakdown — Load profile (50 VUs)

| Endpoint | Requests | Errors | Avg | p95 | Max |
|----------|---------:|:------:|----:|----:|----:|
| `GET /health` | 15 943 | 0 | 3 ms | 6 ms | 27 ms |
| `GET /sessions` | 9 577 | 0 | 5 ms | 10 ms | 42 ms |
| `GET /sessions/{id}/messages` | 6 401 | 0 | 6 ms | 12 ms | 41 ms |
| `POST /sessions` | 3 211 | 0 | 10 ms | 16 ms | 64 ms |

### Pass criteria check

| Profile | Criterion | Result |
|---------|-----------|:------:|
| Smoke  | all 2xx, 0 errors, response time < 1 s | ✅ (max 24 ms) |
| Load   | p95 ≤ 2 s, error rate < 1% | ✅ (p95 11 ms, 0% errors) |
| Stress | find degradation point (error rate > 5%) | ⚠️ not reached at 300 VUs (0% errors) |

## 4. Interpretation

**Does the backend meet the NFR under the load test?** Yes — comfortably. At the
target of 50 concurrent users the 95th-percentile response time was **11 ms**,
roughly **180× faster** than the 2 000 ms NFR ceiling, with a **0% error rate**
over 35 000 requests. The NFR is met with a very large margin.

**At what point does it degrade in the stress test?** No breaking point was
reached. Even at **300 concurrent users** the API returned **zero errors** and a
p99 of **55 ms**. Latency scaled gracefully — p99 grew from 15 ms (50 VUs) to
55 ms (300 VUs) — but never approached the 5% error threshold or any
NFR-relevant latency. Observed throughput on this single-worker setup peaked at
roughly **630–960 req/s**.

The tested endpoints are lightweight (a health constant and simple SQLite
lookups) and the LLM is mocked, so each request is CPU/IO-light. Under more
extreme load the limiting factor would be the **single Uvicorn worker**
(one process, GIL-bound) and the **SQLite write lock**, not the application logic.

## 5. Observations & recommendations

1. **Scale out workers for real concurrency headroom.** The tests ran with a
   single Uvicorn worker. Running multiple workers (`uvicorn --workers N` or
   Gunicorn + Uvicorn workers) behind a reverse proxy would parallelize
   request handling across cores and raise the observed ~600–960 req/s ceiling.

2. **Move off SQLite for write-heavy load.** SQLite serializes writes with a
   database-level lock. `POST /sessions` was already the slowest endpoint
   (avg 10 ms vs 3 ms for `/health`); under heavier write load this becomes the
   first bottleneck. Migrating to PostgreSQL with a connection pool would improve
   write concurrency.

3. **Re-run the stress test from a separate host** to remove load-generator /
   backend CPU contention and locate the true breaking point — on a single
   8-core machine, generator and server compete for the same cores above ~300 VUs.
