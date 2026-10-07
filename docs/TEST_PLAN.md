# Test Plan: OWASP Juice Shop (web + API)

## 1. Scope
| In scope | Out of scope |
|---|---|
| Login / registration | Payment gateway integrations |
| Product search & listing | Load / stress testing |
| Basket (add, update, quantity rules) | Mobile layouts |
| Access control (admin pages, other users' data) | |
| API contracts (schema, status codes, auth) | |

## 2. Approach
- **UI (Playwright, Page Object Model)**: critical user journeys.
- **API (Pytest + requests + jsonschema)**: contracts, auth handling, boundary values, negative cases.
- **Security checks**: injection, IDOR, broken access control, data exposure. These matter for a security product like Osto.
- Every test creates its own user, so tests are independent and can run in parallel.

## 3. Priority
| Priority | Meaning | Run when |
|---|---|---|
| P0 | Blocks release (auth, core flow, security) | Every commit (smoke) |
| P1 | Major feature broken, workaround exists | Every build |
| P2 | Edge case / cosmetic | Nightly |

## 4. Entry / exit criteria
- **Entry:** app reachable on :3000; test data API working.
- **Exit:** 100% of P0 passing *or* every P0 failure linked to a logged defect; no open Critical defect without a triage decision.

## 5. Defect workflow
New → Triaged (severity/priority) → In Progress → Fixed → **Retest (regression test)** → Closed / Reopened.
Known open defects are kept in the suite as `xfail(strict=True)`. When a fix lands, the test XPASSes and fails the build, which reminds you to remove the marker and close the ticket.

## 6. Risks
- Juice Shop is reset on restart, so tests must not rely on persistent data.
- UI selectors can change between versions. Keeping them in page objects means a change only needs fixing in one place.
