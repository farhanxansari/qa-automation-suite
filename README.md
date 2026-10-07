# QA Automation Suite: Web, API & Security Testing

![QA Regression](https://github.com/farhanxansari/qa-automation-suite/actions/workflows/qa.yml/badge.svg)

End-to-end QA of [OWASP Juice Shop](https://github.com/juice-shop/juice-shop), a realistic e-commerce web app with real defects, using **Playwright (Python)**, **Pytest**, **REST API contract tests**, and a **Jira-style defect workflow** run in CI on every push.

**Result:** 23 test cases (25 executions with parametrisation): 16 pass, **9 fail on 7 real defects** (SQL-injection auth bypass, DOM XSS, IDOR, broken access control, negative basket quantity, data exposure, missing validation). Each defect has a bug report and a regression test.

## Structure
```
pages/          Page Object Model (Playwright)
tests/ui/       Browser tests: login, search, admin access
tests/api/      API tests: auth, products, basket, access control
schemas/        JSON Schemas for API contract checks
utils/          API client, test-data factory, schema helper
docs/           Test plan, test-case sheet, bug reports, bug template
.github/        CI: P0 smoke + full regression + HTML report artifact
```

## Run locally
```bash
# 1. Start the app under test
docker run -d -p 3000:3000 bkimminich/juice-shop

# 2. Install
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# 3. Run
pytest                          # everything
pytest -m p0                    # smoke (release blockers only)
pytest -m "api and security"    # security API checks
pytest --headed -m ui           # watch the browser
pytest --html=reports/report.html --self-contained-html
```

## How known bugs are handled
Open defects stay in the suite as `@pytest.mark.xfail(reason="BUG-00X: ...", strict=True)`.
- The build stays green while the bug is known and tracked.
- When a fix lands, the test XPASSes and **fails the build**, which forces someone to verify the fix, remove the marker, and close the ticket. This is how the regression verification step of STLC is enforced.

## STLC mapping
| Phase | Artifact |
|---|---|
| Test planning | `docs/TEST_PLAN.md` |
| Test case design | `docs/TEST_CASES.md` |
| Execution | `pytest` + CI (`.github/workflows/qa.yml`) |
| Defect logging | `docs/bugs/` (mirrored in Jira) |
| Regression | `xfail(strict=True)` + CI on every push |
