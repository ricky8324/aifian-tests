import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[214446];

const test = base.extend<{
  request: APIRequestContext;
  authRequest: APIRequestContext;
}>({
  request: baseRequestFixture,
  authRequest: createAuthRequestFixture(user.mobile, tokenManager),
});

test.describe.configure({ mode: 'serial' });

test.describe('sign out', () => {
  let authHelper: AuthHelper;

  test.beforeAll(async ({ request }) => {
    authHelper = new AuthHelper(request, tokenManager);
    await authHelper.signIn(user);
  });

  test('Sign out and verify API access', async ({ authRequest }) => {
    // Test API access before sign out
    const announcementsResponse = await authRequest.get(urlPaths.announcements);
    expect(announcementsResponse.status()).toBe(200);

    // Sign out
    const signOutResponse = await authRequest.post(urlPaths.auth.signOut);
    expect(signOutResponse.status()).toBe(200);
  });
});
