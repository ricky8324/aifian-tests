import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import {
  liquorBuyTransactionSchema,
  liquorClaimTransactionSchema,
  liquorResellTransactionSchema,
} from '../../schema';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[214457];

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

test.describe('Transaction APIs in product detail page', () => {
  test('Get completed transaction history', async ({ authRequest }) => {
    const response = await authRequest.get(
      urlPaths.product.transaction.completed,
      {
        params: {
          product_id: 'WHI001',
          is_detail_page: true,
        },
      },
    );

    expect(response.status()).toBe(200);
    expect((await response.json()).records.length).toBeLessThanOrEqual(3);
  });

  test('Get completed transaction history in product transaction page', async ({
    authRequest,
  }) => {
    const response = await authRequest.get(
      urlPaths.product.transaction.completed,
      {
        params: {
          product_id: 'WHI001',
        },
      },
    );
    const responseJson = await response.json();

    expect(response.status()).toBe(200);
    expect(responseJson.records.length).toBeLessThanOrEqual(10);
    expect(responseJson.cursor).toBeDefined();

    // Get next page with cursor
    const response2 = await authRequest.get(
      urlPaths.product.transaction.completed,
      {
        params: {
          product_id: 'WHI001',
          cursor: responseJson.cursor,
        },
      },
    );
    const response2Json = await response2.json();

    expect(response2.status()).toBe(200);
    expect(response2Json.records.length).toBeLessThanOrEqual(10);

    // Verify second page records are older than first page
    const firstPageLastTime = new Date(
      responseJson.records[responseJson.records.length - 1].created_at,
    ).getTime();
    const secondPageFirstTime = new Date(
      response2Json.records[0].created_at,
    ).getTime();
    expect(secondPageFirstTime).toBeLessThan(firstPageLastTime);
  });

  test('Get completed transaction history with falsy product_id returns 400', async ({
    authRequest,
  }) => {
    // Test with empty string
    const responseEmptyString = await authRequest.get(
      urlPaths.product.transaction.completed,
      {
        params: {
          product_id: '',
        },
      },
    );
    expect(responseEmptyString.status()).toBe(400);

    // Test with undefined
    const responseUndefined = await authRequest.get(
      urlPaths.product.transaction.completed,
      {
        params: {
          product_id: 'undefined',
        },
      },
    );
    expect(responseUndefined.status()).toBe(400);

    // Test with null
    const responseNull = await authRequest.get(
      urlPaths.product.transaction.completed,
      {
        params: {
          product_id: 'null',
        },
      },
    );
    expect(responseNull.status()).toBe(400);
  });

  test('Get processing transaction history', async ({ authRequest }) => {
    const response = await authRequest.get(
      urlPaths.product.transaction.processing,
      {
        params: {
          product_id: 'WHI001',
        },
      },
    );
    const responseJson = await response.json();

    expect(response.status()).toBe(200);
    expect(responseJson.records).toBeDefined();
    expect(Array.isArray(responseJson.records)).toBe(true);
    // Verify record structure if there are any processing transactions
    // if (responseJson.records.length > 0) {
    //   const record = responseJson.records[0];
    //   expect(record).toHaveProperty('created_at');
    //   expect(record).toHaveProperty('status');
    //   expect(record.status).toBe('processing');
    // }
  });

  test('Get processing transaction history with falsy product_id returns 400', async ({
    authRequest,
  }) => {
    // Test with empty string
    const responseEmptyString = await authRequest.get(
      urlPaths.product.transaction.processing,
      {
        params: {
          product_id: '',
        },
      },
    );
    expect(responseEmptyString.status()).toBe(400);

    // Test with undefined
    const responseUndefined = await authRequest.get(
      urlPaths.product.transaction.processing,
      {
        params: {
          product_id: 'undefined',
        },
      },
    );
    expect(responseUndefined.status()).toBe(400);

    // Test with null
    const responseNull = await authRequest.get(
      urlPaths.product.transaction.processing,
      {
        params: {
          product_id: 'null',
        },
      },
    );
    expect(responseNull.status()).toBe(400);
  });

  test('Get transaction detail returns correct fields', async ({
    authRequest,
  }) => {
    // Test buy transaction
    const buyResponse = await authRequest.get(
      urlPaths.product.transaction.detail,
      {
        params: { id: 'ee9d6f44-1891-4a4f-906e-c6b2c37f28b5' },
      },
    );
    expect(buyResponse.status()).toBe(200);
    const buyData = await buyResponse.json();
    expect(() => liquorBuyTransactionSchema.parse(buyData)).not.toThrow();

    // Test resell transaction
    const resellResponse = await authRequest.get(
      urlPaths.product.transaction.detail,
      {
        params: { id: '68cdca07-4705-445e-b7d4-e017b93c4009' },
      },
    );
    expect(resellResponse.status()).toBe(200);
    const resellData = await resellResponse.json();
    expect(() => liquorResellTransactionSchema.parse(resellData)).not.toThrow();

    // Test claim transaction
    const claimResponse = await authRequest.get(
      urlPaths.product.transaction.detail,
      {
        params: { id: '501da093-2d55-4578-88e7-c5a80a89a905' },
      },
    );
    expect(claimResponse.status()).toBe(200);
    const claimData = await claimResponse.json();
    expect(() => liquorClaimTransactionSchema.parse(claimData)).not.toThrow();
  });

  test('Get transaction detail with non-existent ID returns 404', async ({
    authRequest,
  }) => {
    const response = await authRequest.get(
      urlPaths.product.transaction.detail,
      {
        params: {
          id: 'non-existent-id',
        },
      },
    );
    expect(response.status()).toBe(404);
  });

  test('Get transaction detail without transaction_id returns 400', async ({
    authRequest,
  }) => {
    const response = await authRequest.get(urlPaths.product.transaction.detail);
    expect(response.status()).toBe(400);
  });
});
