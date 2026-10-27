import { Page, expect } from '@playwright/test';

export const USERS = {
  standard: 'standard_user',
  locked: 'locked_out_user',
  problem: 'problem_user',
  password: 'secret_sauce', // published on the login page of the demo site
};

export async function login(page: Page, user = USERS.standard, pass = USERS.password) {
  await page.goto('/');
  await page.locator('[data-test="username"]').fill(user);
  await page.locator('[data-test="password"]').fill(pass);
  await page.locator('[data-test="login-button"]').click();
}

export async function loginAsStandard(page: Page) {
  await login(page);
  await expect(page).toHaveURL(/inventory\.html/);
}

export async function prices(page: Page): Promise<number[]> {
  const texts = await page.locator('[data-test="inventory-item-price"]').allTextContents();
  return texts.map((t) => parseFloat(t.replace('$', '')));
}

export async function names(page: Page): Promise<string[]> {
  return page.locator('[data-test="inventory-item-name"]').allTextContents();
}
