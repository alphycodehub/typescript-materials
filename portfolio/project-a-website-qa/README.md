# Website QA Report: Swag Labs Demo Store (Portfolio Sample)

Automated Playwright suite and QA report for the public practice site https://www.saucedemo.com.

## Run it
```bash
npm install
npx playwright install chromium
npm test
npm run report     # opens the HTML report with screenshots and traces
```

## Then complete the report
1. Open `QA_REPORT.md`, fill in the date, browser and OS.
2. Copy each result from the HTML report into the table (Pass / Fail).
3. Any test that fails: reproduce it manually before calling it a bug. Check that the
   expected text in my test matches the site's actual wording, since a wrong assertion is a
   test problem, not a site defect. Then write it up as DEF-01 with a screenshot in `evidence/`.
4. No real defects? Say so plainly.
5. Delete the italic guidance lines before publishing.
