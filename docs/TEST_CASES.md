# Test Cases

| ID | Module | Title | Type | Priority | Automated | Status |
|---|---|---|---|---|---|---|
| TC_LOGIN_01 | Login | Valid credentials log the user in | UI | P0 | ✅ | Pass |
| TC_LOGIN_02 | Login | Wrong password shows an error, stays on login | UI | P0 | ✅ | Pass |
| TC_LOGIN_03 | Login | Submit disabled when fields are empty | UI | P1 | ✅ | Pass |
| TC_LOGIN_04 | Login | SQL injection does not bypass login | UI/Security | P0 | ✅ | Fail → BUG-001 |
| TC_SEARCH_01 | Search | Results match the search term | UI | P1 | ✅ | Pass |
| TC_SEARCH_02 | Search | Gibberish shows "No results found" | UI | P2 | ✅ | Pass |
| TC_SEARCH_03 | Search | Search term not executed as HTML (XSS) | UI/Security | P0 | ✅ | Fail → BUG-002 |
| TC_ACCESS_01 | Admin | Normal user cannot open the admin page | UI/Security | P0 | ✅ | Pass |
| TC_API_AUTH_01 | Auth API | Login returns token matching schema | API | P0 | ✅ | Pass |
| TC_API_AUTH_02 | Auth API | Invalid / empty creds → 401 (parametrised) | API | P0 | ✅ | Pass |
| TC_API_AUTH_03 | Auth API | Duplicate email registration → 400 | API | P1 | ✅ | Pass |
| TC_API_AUTH_04 | Auth API | Protected endpoints require a token | API | P0 | ✅ | Pass |
| TC_API_AUTH_05 | Auth API | Tampered JWT rejected | API/Security | P1 | ✅ | Pass |
| TC_API_AUTH_06 | Auth API | SQL injection rejected | API/Security | P0 | ✅ | Fail → BUG-001 |
| TC_API_AUTH_07 | Auth API | Malformed email rejected | API | P2 | ✅ | Fail → BUG-003 |
| TC_API_PROD_01 | Products | Product list matches JSON schema | API | P0 | ✅ | Pass |
| TC_API_PROD_02 | Products | Search filters by term | API | P1 | ✅ | Pass |
| TC_API_PROD_03 | Products | Response time < 2s | API | P2 | ✅ | Pass |
| TC_API_BASKET_01 | Basket | Add item to own basket | API | P0 | ✅ | Pass |
| TC_API_BASKET_02 | Basket | Quantity 0 / -1 rejected (boundary) | API | P1 | ✅ | Fail → BUG-004 |
| TC_API_ACCESS_01 | Access | Cannot read another user's basket (IDOR) | API/Security | P0 | ✅ | Fail → BUG-005 |
| TC_API_ACCESS_02 | Access | Non-admin cannot list all users | API/Security | P0 | ✅ | Fail → BUG-006 |
| TC_API_ACCESS_03 | Access | /ftp not publicly listed | API/Security | P1 | ✅ | Fail → BUG-007 |

**Add these next:** checkout flow, address/payment forms, password reset, product reviews, rate limiting on login, security headers (CSP, X-Frame-Options).
