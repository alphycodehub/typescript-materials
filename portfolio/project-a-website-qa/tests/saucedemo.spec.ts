import { test, expect } from '@playwright/test';
import { USERS, login, loginAsStandard, prices, names } from './helper';

// Test IDs (TC-xx) match QA_REPORT.md

test.describe('Login', () => {
  test('TC-01 valid login reaches product page', async ({ page }) => {
    await login(page);
    await expect(page).toHaveURL(/inventory\.html/);
    await expect(page.locator('[data-test="inventory-item"]')).toHaveCount(6);
  });

  test('TC-02 wrong password shows error', async ({ page }) => {
    await login(page, USERS.standard, 'wrong_password');
    await expect(page.locator('[data-test="error"]')).toContainText('do not match');
  });

  test('TC-03 locked out user cannot log in', async ({ page }) => {
    await login(page, USERS.locked);
    await expect(page.locator('[data-test="error"]')).toContainText('locked out');
  });

  test('TC-04 empty username shows required error', async ({ page }) => {
    await page.goto('/');
    await page.locator('[data-test="password"]').fill(USERS.password);
    await page.locator('[data-test="login-button"]').click();
    await expect(page.locator('[data-test="error"]')).toContainText('Username is required');
  });

  test('TC-05 empty password shows required error', async ({ page }) => {
    await page.goto('/');
    await page.locator('[data-test="username"]').fill(USERS.standard);
    await page.locator('[data-test="login-button"]').click();
    await expect(page.locator('[data-test="error"]')).toContainText('Password is required');
  });

  test('TC-06 product page is not reachable without login', async ({ page }) => {
    await page.goto('/inventory.html');
    await expect(page.locator('[data-test="error"]')).toContainText('logged in');
  });
});

test.describe('Products and cart', () => {
  test.beforeEach(async ({ page }) => loginAsStandard(page));

  test('TC-07 sort by price low to high', async ({ page }) => {
    await page.locator('[data-test="product-sort-container"]').selectOption('lohi');
    const p = await prices(page);
    expect(p).toEqual([...p].sort((a, b) => a - b));
  });

  test('TC-08 sort by name Z to A', async ({ page }) => {
    await page.locator('[data-test="product-sort-container"]').selectOption('za');
    const n = await names(page);
    expect(n).toEqual([...n].sort().reverse());
  });

  test('TC-09 add item updates cart badge, remove clears it', async ({ page }) => {
    await page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('1');
    await page.locator('[data-test="remove-sauce-labs-backpack"]').click();
    await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveCount(0);
  });

  test('TC-10 cart keeps item after navigating to cart page', async ({ page }) => {
    await page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click();
    await page.locator('[data-test="shopping-cart-link"]').click();
    const item = page.locator('[data-test="inventory-item-name"]').filter({ hasText: 'Sauce Labs Bike Light' });
    await expect(item).toHaveText('Sauce Labs Bike Light');
  });
});

test.describe('Checkout', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsStandard(page);
    await page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    await page.locator('[data-test="shopping-cart-link"]').click();
    await page.locator('[data-test="checkout"]').click();
  });

  test('TC-11 missing first name shows error', async ({ page }) => {
    await page.locator('[data-test="lastName"]').fill('Doe');
    await page.locator('[data-test="postalCode"]').fill('00100');
    await page.locator('[data-test="continue"]').click();
    await expect(page.locator('[data-test="error"]')).toContainText('First Name is required');
  });

  test('TC-12 complete purchase shows confirmation', async ({ page }) => {
    await page.locator('[data-test="firstName"]').fill('Test');
    await page.locator('[data-test="lastName"]').fill('User');
    await page.locator('[data-test="postalCode"]').fill('00100');
    await page.locator('[data-test="continue"]').click();
    await page.locator('[data-test="finish"]').click();
    await expect(page.locator('[data-test="complete-header"]')).toContainText('Thank you');
  });
});

test.describe('Session', () => {
  test('TC-13 logout returns to login page', async ({ page }) => {
    await loginAsStandard(page);
    await page.locator('#react-burger-menu-btn').click();
    await page.locator('[data-test="logout-sidebar-link"]').click();
    await expect(page.locator('[data-test="login-button"]')).toBeVisible();
  });
});

test.describe('Exploratory: problem_user (the demo site ships intentionally flawed users)', () => {
  test('TC-14 every product image should be different', async ({ page }) => {
    await login(page, USERS.problem);
    const srcs = await page.locator('[data-test="inventory-item"] img').evaluateAll(
      (imgs) => imgs.map((i) => (i as HTMLImageElement).src),
    );
    expect(new Set(srcs).size, 'each product should show its own image').toBe(srcs.length);
  });
});
