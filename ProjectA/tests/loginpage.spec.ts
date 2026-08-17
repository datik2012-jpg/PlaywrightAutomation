import { test, expect } from '@playwright/test';

test('app is available', async ({ page }) => {
  const response = await page.goto('/');

  expect(response).not.toBeNull();
  expect(response?.status()).toBe(200);
});

test('login with valid credentials', async ({ page }) => {
  await page.goto('/');

  await page.getByLabel('Email').fill('danitest@mail.com');
  await page.getByLabel('Password').fill('1234567');
  await page.getByRole('button', { name: 'Log In' }).click();

  await expect(page).toHaveURL('/courts.html');
  await expect(page.getByRole('heading', { name: 'Available courts' })).toBeVisible();
});

test('login using element IDs', async ({ page }) => {
  await page.goto('/');

  await page.locator('#email').fill('danitest@mail.com');
  await page.locator('#password').fill('1234567');
  await page.locator('#login-button').click();

  await expect(page).toHaveURL('/courts.html');
});

test('login using accessible roles', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible();
  await page.getByLabel('Email').fill('danitest@mail.com');
  await page.getByLabel('Password').fill('1234567');
  await page.getByRole('button', { name: 'Log In' }).click();

  await expect(page).toHaveURL('/courts.html');
  await expect(page.getByRole('button', { name: 'Book' })).toHaveCount(2);
});

test('shows available courts after login', async ({ page }) => {
  await page.goto('/');
  await page.getByLabel('Email').fill('danitest@mail.com');
  await page.getByLabel('Password').fill('1234567');
  await page.getByRole('button', { name: 'Log In' }).click();

  const courtA = page.getByRole('article', { name: 'Court A' });
  const courtB = page.getByRole('article', { name: 'Court B' });

  await expect(courtA).toContainText('Available');
  await expect(courtA).toContainText('18:00');
  await expect(courtA.getByRole('button', { name: 'Book' })).toBeVisible();
  await expect(courtB).toContainText('Available');
  await expect(courtB).toContainText('18:00');
  await expect(courtB.getByRole('button', { name: 'Book' })).toBeVisible();
});
