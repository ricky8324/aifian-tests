import { urlPaths, userRole } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { AuthHelper } from '../../helpers/api/auth-helper';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const user = userRole[217168];

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

test('should get reward information', async ({ authRequest }) => {
  // Get reward information
  const response = await authRequest.get(`${urlPaths.rewards.v1.info}`);
  expect(response.status()).toBe(200);
  const rewardInfo = await response.json();
  expect(rewardInfo.cur_reward_points).toBeDefined();
  expect(rewardInfo.has_interaction).toBeDefined();
  expect(rewardInfo.total_earned).toBeDefined();
  expect(rewardInfo.rewards).toBeDefined();
  expect(rewardInfo.estimated_value).toBeDefined();
});
