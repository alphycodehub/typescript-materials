# QA Report: Swag Labs Demo Store

> **Portfolio project.** Tested against https://www.saucedemo.com, a public demo site
> built by Sauce Labs for testing practice. Not a client engagement.

**Tester:** Alphonce
**Date executed:** ____ / ____ / 2026
**Browser / OS:** ______________________ (e.g. Chromium via Playwright, Windows 11)
**Build tested:** Live site on the date above

## 1. Test objective
Verify that the core shopper journey on the demo store (login, browse and sort products,
manage the cart, check out, log out) works as a user would expect, and that invalid input
is handled with clear error messages.

## 2. Scope
**In scope:** login and validation, product list sorting, cart add/remove, checkout form
validation, checkout completion, logout, access control on the product page.
**Out of scope:** performance, security testing, accessibility audit, mobile layouts,
payment (the demo has none).

## 3. Approach
Automated checks with Playwright (`tests/saucedemo.spec.ts`) plus a short manual
exploratory pass. Failures capture a screenshot automatically; save any you cite under `evidence/`.

## 4. Test cases and results
Fill the **Result** column from the Playwright HTML report (`npm run report`). Use
Pass / Fail / Blocked only. Leave "Not run" for anything you did not execute.

| ID | Test case | Expected result | Result | Notes / evidence |
|---|---|---|---|---|
| TC-01 | Valid login (standard_user) | Product page opens, 6 products shown | Not run | |
| TC-02 | Wrong password | Error says username and password do not match | Not run | |
| TC-03 | Locked-out user | Error says the user is locked out | Not run | |
| TC-04 | Empty username | "Username is required" | Not run | |
| TC-05 | Empty password | "Password is required" | Not run | |
| TC-06 | Open /inventory.html without logging in | Access blocked with an error | Not run | |
| TC-07 | Sort price low to high | Prices ascending | Not run | |
| TC-08 | Sort name Z to A | Names descending | Not run | |
| TC-09 | Add then remove an item | Cart badge shows 1, then disappears | Not run | |
| TC-10 | Item still in cart on cart page | Correct item listed | Not run | |
| TC-11 | Checkout with first name blank | "First Name is required" | Not run | |
| TC-12 | Complete a purchase | Confirmation message shown | Not run | |
| TC-13 | Logout | Returns to login page | Not run | |
| TC-14 | problem_user: product images | Each product has its own image | Not run | |

**Summary:** __ run, __ passed, __ failed.

## 5. Defects found
Only list what you actually observed and reproduced. If nothing failed, write:
"No defects found in the scoped areas during this test run." Do not invent one.

### DEF-01: <short title>
- **Related test:** TC-__
- **Severity:** Low / Medium / High
- **Steps to reproduce:**
  1. ...
  2. ...
  3. ...
- **Expected result:** ...
- **Actual result:** ...
- **Evidence:** `evidence/def-01.png`
- **Environment:** browser, OS, date

## 6. Conclusion
<2-3 sentences: what was covered, what the results show, what you would test next.>
