import { test, expect } from '@playwright/test';
import { ctbcWebhookEndpoint } from 'repository/aifian-async/constant';

test('ctbc webhook should return status code 200', async ({ request }) => {
  if (!ctbcWebhookEndpoint) {
    throw new Error('CTBC_WEBHOOK_ENDPOINT is not defined');
  }

  const response = await request.post(ctbcWebhookEndpoint, {
    headers: {
      'user-agent': 'aifian-health-check',
    },
  });
  expect(response.status()).toBe(200);
});
