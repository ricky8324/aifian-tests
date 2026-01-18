import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { AuthHelper } from 'repository/aifian-api/helpers/api/auth-helper';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();

const test = base.extend<{
  request: APIRequestContext;
  authRequest: APIRequestContext;
}>({
  request: baseRequestFixture,
  authRequest: createAuthRequestFixture(userRole[214680].mobile, tokenManager),
});

test.describe('refresh token', () => {
  test.beforeAll(async ({ request }) => {
    const authHelper = new AuthHelper(request, tokenManager);
    await authHelper.signIn(userRole[214680]);
  });
  test('should return valid data for the correct username and refresh token', async ({
    request,
    authRequest,
  }) => {
    const authHelper = new AuthHelper(request, tokenManager);
    const responseData = await authHelper.refreshToken(userRole[214680].mobile);

    expect(responseData.external_id).toBe(
      'c66ffb13-2e83-4197-aa94-22b32d18b1bc',
    );
    expect(responseData.status).toBe('verified');
    expect(typeof responseData.access_token).toBe('string');
    expect(typeof responseData.refresh_token).toBe('string');

    const exchangeRatesResponse = await authRequest.get(
      urlPaths.exchangeRates,
      {
        params: { base: 'USD', quote: 'TWD' },
      },
    );
    expect(exchangeRatesResponse.status()).toBe(200);
  });
});
