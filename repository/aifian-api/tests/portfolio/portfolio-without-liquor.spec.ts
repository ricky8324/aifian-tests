import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[214953];

const test = base.extend<{
  request: APIRequestContext;
  authRequest: APIRequestContext;
}>({
  request: baseRequestFixture,
  authRequest: createAuthRequestFixture(user.mobile, tokenManager),
});

test.beforeAll(async ({ request }) => {
  const authHelper = new AuthHelper(request, tokenManager);
  await authHelper.signIn(user);
});

test.afterAll(async ({ authRequest }) => {
  const authHelper = new AuthHelper(authRequest, tokenManager);
  await authHelper.signOut(user.mobile);
});

test.describe('Portfolio without liquor', () => {
  test('Total asset chart', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.graph.asset.total, {
      params: {
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Total asset value and return rate', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.portfolio.asset.totalInfo, {
      params: {
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Partial information on liquor appreciation homepage', async ({
    authRequest,
  }) => {
    const response = await authRequest.get(urlPaths.portfolio.asset.totalInfo, {
      params: {
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Partial information on liquor detail page', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.portfolio.asset.totalInfo, {
      params: {
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Price trend information on liquor detail page', async ({
    authRequest,
  }) => {
    const response = await authRequest.get(urlPaths.portfolio.asset.totalInfo, {
      params: {
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Price trend chart on liquor detail page', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.portfolio.asset.totalInfo, {
      params: {
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);
  });
});
