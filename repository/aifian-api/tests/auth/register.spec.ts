import { urlPaths } from '../../constant';
import { createAuthRequestFixture } from '../../fixtures/auth-request';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();

const test = base.extend<{
  request: APIRequestContext;
  authRequest: APIRequestContext;
}>({
  request: baseRequestFixture,
  authRequest: createAuthRequestFixture('', tokenManager),
});

function generateFakeMobileNumber(): string {
  const countryCode = '+886';
  const fakePrefix = '900';
  const randomMobileNumber = Math.floor(Math.random() * 1000000)
    .toString()
    .padStart(6, '0');
  return countryCode + fakePrefix + randomMobileNumber;
}

test.describe('register flow', () => {
  const password = 'Abcdef1!';
  const fakeMobile = generateFakeMobileNumber();

  test('successfully register using a mobile number', async ({ request }) => {
    // Register
    const registerResponse = await request.post(urlPaths.auth.register, {
      data: { mobile: fakeMobile },
    });
    expect(registerResponse.status()).toBe(200);

    // Validate OTP
    const validateOtpResponse = await request.post(urlPaths.auth.challenge, {
      data: { mobile: fakeMobile, code: '123456' },
    });
    expect(validateOtpResponse.status()).toBe(200);
    const { confirmation_code } = await validateOtpResponse.json();

    // Set Password
    const setPasswordResponse = await request.post(urlPaths.auth.setPassword, {
      data: { mobile: fakeMobile, confirmation_code, password },
    });
    const data = await setPasswordResponse.json();

    expect(setPasswordResponse.status()).toBe(200);
    expect(data.status).toBe('registered');
    expect(data.access_token).toBeTruthy();
    expect(data.refresh_token).toBeTruthy();
    expect(data.external_id).toBeTruthy();
  });
});
