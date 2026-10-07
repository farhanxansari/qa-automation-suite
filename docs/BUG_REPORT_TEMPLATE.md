# BUG-XXX: <one-line summary: what breaks, where>

| Field | Value |
|---|---|
| Module | Login / Search / Basket / Access Control / API |
| Severity | Critical / High / Medium / Low (impact) |
| Priority | P0 / P1 / P2 (urgency) |
| Environment | Juice Shop vX.Y, Chromium NNN, Ubuntu / Windows |
| Found by test | `tests/...::test_TC_...` |
| Status | Open |

## Steps to reproduce
1.
2.
3.

## Expected result

## Actual result

## Evidence
Screenshot, trace, or request/response (curl).

## Root-cause note (hypothesis)
Example: the email value is concatenated into a raw SQL query instead of being passed as a bound parameter.

## Suggested fix

## Regression test
`tests/...::test_TC_...` (currently `xfail`; remove the marker once fixed)
