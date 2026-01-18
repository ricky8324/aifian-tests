import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[214919];

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

test.describe('lottery prediction operations', () => {
  test('Get lottery participation information', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.lottery);
    expect(response.status()).toBe(200);
  });

  test('Create a new lottery entry', async ({ authRequest }) => {
    const createResponse = await authRequest.post(urlPaths.lottery, {
      data: { code: '1219' },
    });

    expect([201, 400].includes(createResponse.status())).toBeTruthy();

    const getResponse = await authRequest.get(urlPaths.lottery);
    expect(getResponse.status()).toBe(200);
    const responseData = await getResponse.json();
    expect(responseData.code).toBe('1219');
  });
});
