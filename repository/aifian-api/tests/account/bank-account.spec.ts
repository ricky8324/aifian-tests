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

test.describe('bank account operations', () => {
  test('Get bank list', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.account.bankList);
    expect(response.status()).toBe(200);
  });

  test('Get branch list', async ({ authRequest }) => {
    const response = await authRequest.get(urlPaths.account.branchList, {
      params: { bank_code: '004' },
    });
    expect(response.status()).toBe(200);
  });

  test('Link bank account', async ({ authRequest }) => {
    const preLinkProfile = await authRequest.get(urlPaths.account.v1);

    expect(preLinkProfile.status()).toBe(200);
    const preLinkProfileData = await preLinkProfile.json();
    expect(preLinkProfileData.bank_account).toBe(null);
    expect(preLinkProfileData.bank_branch).toBe(null);
    expect(preLinkProfileData.bank_name).toBe(null);

    const linkResponse = await authRequest.post(urlPaths.account.bankAccount, {
      data: {
        bank_account: '12345678',
        bank_branch: '成功分行',
        bank_name: '臺灣銀行',
        account_name: '貝拉醫生',
      },
    });
    expect(linkResponse.status()).toBe(200);

    const postLinkProfile = await authRequest.get(urlPaths.account.v1);
    expect(postLinkProfile.status()).toBe(200);

    const postLinkProfileData = await postLinkProfile.json();
    expect(postLinkProfileData.bank_account).toBe('12345678');
    expect(postLinkProfileData.bank_branch).toBe('成功分行');
    expect(postLinkProfileData.bank_name).toBe('臺灣銀行');
  });

  test('Change bank account', async ({ authRequest }) => {
    const LinkProfile = await authRequest.get(urlPaths.account.v1);

    expect(LinkProfile.status()).toBe(200);
    const LinkProfileData = await LinkProfile.json();
    expect(LinkProfileData.bank_account).toBe('12345678');
    expect(LinkProfileData.bank_branch).toBe('成功分行');
    expect(LinkProfileData.bank_name).toBe('臺灣銀行');

    const linkResponse = await authRequest.post(urlPaths.account.bankAccount, {
      data: {
        bank_account: '22222222',
        bank_branch: '基隆分行',
        bank_name: '臺灣土地銀行',
        account_name: '貝拉醫生',
      },
    });
    expect(linkResponse.status()).toBe(200);

    const postLinkProfile = await authRequest.get(urlPaths.account.v1);
    expect(postLinkProfile.status()).toBe(200);

    const postLinkProfileData = await postLinkProfile.json();
    expect(postLinkProfileData.bank_account).toBe('22222222');
    expect(postLinkProfileData.bank_branch).toBe('基隆分行');
    expect(postLinkProfileData.bank_name).toBe('臺灣土地銀行');
  });

  test('Delete bank account', async ({ authRequest }) => {
    const deleteResponse = await authRequest.post(
      urlPaths.account.deleteBankAccount,
    );
    expect(deleteResponse.status()).toBe(200);
    
    const postDeleteProfile = await authRequest.get(urlPaths.account.v1);
    expect(postDeleteProfile.status()).toBe(200);

    const postDeleteProfileData = await postDeleteProfile.json();
    expect(postDeleteProfileData.bank_account).toBe(null);
    expect(postDeleteProfileData.bank_branch).toBe(null);
    expect(postDeleteProfileData.bank_name).toBe(null);
  });
});
