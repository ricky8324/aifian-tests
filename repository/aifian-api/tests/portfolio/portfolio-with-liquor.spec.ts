import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import { portfolioSummarySchema } from '../../schema';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { Currency } from 'repository/aifian-api/types';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[214490];

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

test.describe('Portfolio APIs with liquor', () => {
  const VALID_CURRENCIES = [Currency.TWD, Currency.USD] as const;

  test('Get total asset graph', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.graph.asset.total, {
      params: {},
    });

    // Test 304 Not Modified response
    const response2 = await authRequest.get(urlPaths.graph.asset.total, {
      headers: {
        'If-None-Match': response.headers().etag,
      },
      params: {},
    });
    expect(response2.status()).toBe(304);
  });

  test('Get total asset value and return rate', async ({ authRequest }) => {
    const response = await authRequest.get(
      urlPaths.portfolio.asset.totalInfo,
      {},
    );
    expect(response.status()).toBe(200);
  });

  test('Get portfolio summary with valid currencies', async ({
    authRequest,
  }) => {
    for (const currency of VALID_CURRENCIES) {
      const response = await authRequest.get(urlPaths.portfolio.summary, {
        params: { currency },
      });
      expect(response.status(), `Currency ${currency} should be valid`).toBe(
        200,
      );
      const data = await response.json();
      expect(() => portfolioSummarySchema.parse(data)).not.toThrow();
    }
  });

  test('Get liquor product detail', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.portfolio.asset.detail, {
      params: {
        product_id: 'WHI001',
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);
  });

  test('Get liquor product detail with non-existent product ID returns 400', async ({
    authRequest,
  }) => {
    const response = await authRequest.get(urlPaths.portfolio.asset.detail, {
      params: {
        product_id: 'NONEXISTENT',
      },
    });
    expect(response.status()).toBe(400);
  });

  test('Get liquor product detail without required params returns 400', async ({
    authRequest,
  }) => {
    // Test missing product_id
    const responseWithoutProductId = await authRequest.get(
      urlPaths.portfolio.asset.detail,
      { params: {} },
    );
    expect(responseWithoutProductId.status()).toBe(400);

    // Test missing both params
    const responseWithoutParams = await authRequest.get(
      urlPaths.portfolio.asset.detail,
    );
    expect(responseWithoutParams.status()).toBe(400);
  });

  test('Get liquor product current value info', async ({ authRequest }) => {
    const response = await authRequest.get(
      urlPaths.portfolio.asset.individualInfo,
      {
        params: {
          product_id: 'WHI001',
          currency: 'TWD',
        },
      },
    );
    expect(response.status()).toBe(200);
  });

  test('Get liquor product price trend info', async ({ authRequest }) => {
    const response = await authRequest.get(
      urlPaths.portfolio.product.latestInfo,
      {
        params: {
          product_id: 'WHI001',
          currency: 'TWD',
        },
      },
    );
    expect(response.status()).toBe(200);
  });

  test('Get liquor product current value graph', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.graph.asset.individual, {
      params: {
        product_id: 'WHI001',
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);

    // Test 304 Not Modified response
    const response2 = await authRequest.get(urlPaths.graph.asset.individual, {
      params: {
        product_id: 'WHI001',
        currency: 'TWD',
      },
      headers: {
        'If-None-Match': response.headers().etag,
      },
    });
    expect(response2.status()).toBe(304);
  });

  test('Get liquor product price trend graph', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.graph.product, {
      params: {
        product_id: 'WHI001',
        currency: 'TWD',
      },
    });
    expect(response.status()).toBe(200);

    // Test 304 Not Modified response
    const response2 = await authRequest.get(urlPaths.graph.product, {
      params: {
        product_id: 'WHI001',
        currency: 'TWD',
      },
      headers: {
        'If-None-Match': response.headers().etag,
      },
    });
    expect(response2.status()).toBe(304);
  });
});
