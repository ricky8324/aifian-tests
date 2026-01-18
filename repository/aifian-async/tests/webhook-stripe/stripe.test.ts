import { test, expect } from '@playwright/test';
import { stripeWebhookEndpoint } from 'repository/aifian-async/constant';
test('stripe webhook should return status code 200', async ({ request }) => {
  if (!stripeWebhookEndpoint) {
    throw new Error('STRIPE_WEBHOOK_ENDPOINT is not defined');
  }

  const response = await request.post(stripeWebhookEndpoint, {
    headers: {
      'user-agent': 'aifian-health-check',
    },
  });
  expect(response.status()).toBe(200);
});
