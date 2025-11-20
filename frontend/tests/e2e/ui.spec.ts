import { test, expect } from '@playwright/test';

test.describe('Stream-View UI', () => {
  test('page loads with correct layout', async ({ page }) => {
    await page.goto('/');

    // Check that the page title is present
    await expect(page).toHaveTitle(/Stream/i);
  });

  test('header displays Realitech logo and title', async ({ page }) => {
    await page.goto('/');

    // Check for header elements
    const header = page.locator('header');
    await expect(header).toBeVisible();

    // Check for Realitech logo
    const logo = page.locator('img[alt*="Realitech" i]');
    await expect(logo).toBeVisible();

    // Check for Stream-View title
    await expect(page.locator('text=Stream-View')).toBeVisible();
  });

  test('URL input and View button are present', async ({ page }) => {
    await page.goto('/');

    // Check for URL input
    const urlInput = page.locator('input[type="text"], input[placeholder*="manifest" i], input[id="stream-url"]');
    await expect(urlInput).toBeVisible();

    // Check for View button
    const viewButton = page.locator('button:has-text("View")');
    await expect(viewButton).toBeVisible();
  });

  test('URL validation works', async ({ page }) => {
    await page.goto('/');

    // Enter invalid URL
    const urlInput = page.locator('input[type="text"], input[id="stream-url"]').first();
    await urlInput.fill('invalid-url');

    // Click View button
    const viewButton = page.locator('button:has-text("View")');
    await viewButton.click();

    // Check for error message
    await expect(page.locator('text=/error|invalid|url/i')).toBeVisible({ timeout: 5000 });
  });

  test('loading state shows during analysis', async ({ page }) => {
    await page.goto('/');

    // Enter a valid URL format
    const urlInput = page.locator('input[type="text"], input[id="stream-url"]').first();
    await urlInput.fill('https://example.com/stream.m3u8');

    // Click View button
    const viewButton = page.locator('button:has-text("View")');
    await viewButton.click();

    // Check for loading indicator (spinner or "Analyzing..." text)
    await expect(page.locator('text=/analyzing|loading/i, svg.animate-spin')).toBeVisible({ timeout: 2000 });
  });

  test('form elements are accessible', async ({ page }) => {
    await page.goto('/');

    // Check that input has a label
    const urlInput = page.locator('input[id="stream-url"]');
    const label = page.locator('label[for="stream-url"]');
    await expect(label).toBeVisible();

    // Check button is keyboard accessible
    const viewButton = page.locator('button:has-text("View")');
    await viewButton.focus();
    await expect(viewButton).toBeFocused();
  });

  test('responsive design works', async ({ page }) => {
    // Test desktop size
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.goto('/');
    await expect(page.locator('header')).toBeVisible();

    // Test tablet size
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('input')).toBeVisible();
  });
});

test.describe('Error Handling', () => {
  test('error messages display correctly', async ({ page }) => {
    await page.goto('/');

    // Enter invalid URL
    const urlInput = page.locator('input[type="text"]').first();
    await urlInput.fill('not-a-url');

    // Click View
    await page.locator('button:has-text("View")').click();

    // Verify error message appears
    const errorMessage = page.locator('[class*="error" i], [class*="red" i]').filter({ hasText: /error|invalid|check/i });
    await expect(errorMessage.first()).toBeVisible({ timeout: 5000 });
  });
});

test.describe('Accessibility', () => {
  test('proper heading hierarchy', async ({ page }) => {
    await page.goto('/');

    // Check for h1
    const h1 = page.locator('h1');
    await expect(h1).toBeVisible();
  });

  test('keyboard navigation works', async ({ page }) => {
    await page.goto('/');

    // Tab through elements
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');

    // Should be able to focus on button
    const viewButton = page.locator('button:has-text("View")');
    await expect(viewButton).toBeFocused();
  });
});
