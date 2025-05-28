import { test, expect } from '@playwright/test';

test.describe('Infrastructure Setup', () => {
  test('backend health check endpoint should be accessible', async ({ request }) => {
    const response = await request.get('http://localhost:8000/health');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status', 'healthy');
    expect(data).toHaveProperty('database');
  });

  test('frontend should load successfully', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page loads without errors
    await expect(page).toHaveTitle(/Tickets P2P/);
    
    // Check for basic page structure
    await expect(page.locator('body')).toBeVisible();
  });

  test('backend API documentation should be accessible', async ({ request }) => {
    const response = await request.get('http://localhost:8000/docs');
    expect(response.status()).toBe(200);
  });

  test('database connection should be working', async ({ request }) => {
    const response = await request.get('http://localhost:8000/health');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data.database).toBe('connected');
  });
}); 