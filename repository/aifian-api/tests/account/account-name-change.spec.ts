import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[214450];

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

test.describe('name change operations', () => {
  test('OCR error option', async ({ authRequest }) => {
    const response = await authRequest.post(urlPaths.account.accountNameChange, {
      data: {
        name_last: "醫生",
        name_first: "貝拉",
        reason: "OCR_ERROR",
      },
    });
    expect(response.status()).toBe(200);
    const responseID = await response.json();
    expect(typeof responseID.id).toBe('string');
  });

 test('Legal change option', async ({ authRequest }) => {
    const response = await authRequest.post(urlPaths.account.accountNameChange, {
      data: {
        name_last: "醫生",
        name_first: "貝拉",
        reason: "LEGAL_CHANGE",
      },
    });
    expect(response.status()).toBe(200);
    const responseID = await response.json();
    expect(typeof responseID.id).toBe('string');
  });

  test('Name no change', async ({ authRequest }) => {
    const response = await authRequest.post(urlPaths.account.accountNameChange, {
      data: {
        name_last: "貝拉醫生",
        name_first: "",
        reason: "LEGAL_CHANGE",
      },
    });
    expect(response.status()).toBe(400);
    const responseError = await response.json();
    expect(responseError.errno).toBe('SAME_AS_CURRENT');
  });
});