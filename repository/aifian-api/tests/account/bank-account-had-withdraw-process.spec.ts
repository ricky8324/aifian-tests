import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[214666];

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

test.describe('account had withdraw processing', () => {
  test('Account had withdraw processing, change bank account', async ({ authRequest }) => {
    const LinkProfile = await authRequest.get(urlPaths.account.v1);

    expect(LinkProfile.status()).toBe(200);

    const linkResponse = await authRequest.post(urlPaths.account.bankAccount, {
      data: {
        bank_account: '33333333',
        bank_branch: '台中分行',
        bank_name: '元大銀行',
        account_name: '貝拉醫生',
      },
    });
    expect(linkResponse.status()).toBe(400);
  });

  test('Account had withdraw processing, delete bank account', async ({ authRequest }) => {
    const deleteResponse = await authRequest.post(
      urlPaths.account.deleteBankAccount,
    );
    expect(deleteResponse.status()).toBe(400);
  });
});