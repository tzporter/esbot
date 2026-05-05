# Static Analysis — ESBot

## Tools Selected

### Category 1: Linter — Ruff
### Category 2: Security Scanner — Bandit

## Justification

Ruff was chosen as the linter because ESBot is a multi-developer 
Python project with contributors working across frontend , 
backend, and test code. A linter enforces consistent style 
and catches common mistakes like unused imports and redefined names, 
which become increasingly important as the codebase grows across 
multiple team members.

Bandit was chosen as the security scanner because ESBot handles 
several security-sensitive areas: API keys for the Groq LLM service, 
user-supplied chat input passed to an AI model, 
and a PostgreSQL database accessed through FastAPI endpoints. 
Identifying vulnerabilities in these areas early is critical.

## Setup and Configuration

Both tools are configured via `pyproject.toml` in the project root.

```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "W"]
exclude = [".venv", "__pycache__", "migrations"]

[tool.bandit]
exclude_dirs = ["tests", ".venv"]
skips = []
```

Install dependencies:
```bash
pip install ruff bandit
```

## How to Run

**Ruff:**
```bash
ruff check .
```

To auto-fix simple issues:
```bash
ruff check . --fix
```

**Bandit:**
```bash
bandit -r . -x ./tests,./.venv
```

## Results

### Ruff — 127 issues found

The issues fell into these categories:

- **E501 (Line too long):** Most common finding. Many lines in 
  `main.py` and BDD step files exceed the 88-character limit. 
- **F811 (Redefined function name):** Flagged extensively in BDD 
  step files where every step function is named `step_impl`. 
- **F401 (Unused imports):** Several files import modules that are 
  never used, including `UserSession` in `conftest.py` and `Field`, 
  `SQLModel` in `main.py`. 
- **W293/W292 (Whitespace issues):** Blank lines containing spaces 
  and missing newlines at end of file.
- **E401 (Multiple imports on one line):** `import sys, os` in 
  `conftest.py` should be split into two lines.

34 of the 127 issues were automatically fixed using `ruff check . --fix`.

### Bandit — 90 issues found  

All 90 findings were **B101: assert_used** that is Bandit flagging the 
use of `assert` statements across test files. This warning exists 
because Python's `-O` optimization flag strips `assert` statements 
at runtime, which could hide logic errors in production code.

However, all flagged `assert` statements are located inside pytest 
and Behave test files, where `assert` is the correct and intended 
mechanism. This is a well-known false positive when Bandit scans 
test directories. No medium or high severity issues were found.

## Evaluation

### Usefulness

Ruff was immediately useful. The unused import findings in `main.py` 
and `conftest.py` are genuine code quality issues that could cause 
confusion for future developers. The whitespace findings, while minor, 
were easy to fix automatically.

Bandit was less immediately useful for this codebase in its default 
configuration.  

### Noise and False Positives

Ruff's F811 warnings on Behave step files are false positives. The 
`step_impl` naming pattern is a Behave convention, not a real defect. 

Bandit's B101 warnings are entirely false positives in this context. 
Scanning test files for assert usage produces no actionable findings. 
This can be resolved by passing `-x ./tests` to exclude the test 
directory, which is already documented in the run command above.

### Development Impact

Both tools run in under 5 seconds on this codebase, making them 
suitable for local use before committing code. They do not noticeably 
slow down the development process.

Running `ruff check . --fix` automatically resolved 34 issues, 
demonstrating that linting can improve code quality with minimal 
developer effort.

### Pipeline Automation Consideration

Ruff would be a good candidate for CI/CD integration due to its 
speed and low false positive rate on application code. Bandit would 
require additional configuration before pipeline integration to 
avoid generating noise on every run. For this reason, both tools 
are currently documented for local execution only.

Claude AI was used in the development of this document as a form of brainstorming and revising my work. All AI-edited content was thoroughly checked.