import { APIRequestContext, test as base, expect } from '@playwright/test';
import {
  stagingEmailOTP,
  stagingMobileOTP,
  urlPaths,
  userAgent,
  userRole,
  wrongEmailOTP,
  wrongMobileOTP,
} from 'repository/aifian-api/constant';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { AuthHelper } from 'repository/aifian-api/helpers/api/auth-helper';
import { HttpResponseEnum } from 'repository/aifian-api/types';
import { getConfigToken } from 'repository/aifian-api/utils/config-token';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

const tokenManager = new TokenManager();
const existingAccount: { email: string; mobile: string; password: string } =
  userRole[215464];

const test = base.extend<{
  request: APIRequestContext;
}>({
  request: baseRequestFixture,
});

test.describe('Forgot Account and Reset Password', () => {
  test('Request Reset Password', async ({ request, playwright }) => {
    const { email, mobile, password: originalPassword } = existingAccount;
    const resetPassword = `${originalPassword}!`;
    let resetPasswordOTPCode: string;

    const authRequest: APIRequestContext = await playwright.request.newContext({
      extraHTTPHeaders: {
        'user-agent': userAgent,
        'x-aifian-token': getConfigToken(),
        Authorization: tokenManager.get(email)?.access_token || '',
      },
    });
    // Case 1-1: 透過 Email 重設密碼
    await test.step('Request Reset Password through email', async () => {
      const response = await request.post(urlPaths.auth.requestResetPassword, {
        data: { username: email },
      });

      expect(response.status()).toBe(HttpResponseEnum.SUCCESS);
    });

    // Case 1-2: 驗證是否收到 OTP
    await test.step('Should fail when verifying wrong OTP', async () => {
      const wrongOTPResponse = await request.post(
        urlPaths.auth.verifyResetPassword,
        {
          data: { username: email, code: wrongEmailOTP },
        },
      );

      expect(wrongOTPResponse.status()).toBe(HttpResponseEnum.BAD_REQUEST);
    });

    await test.step('Verify OTP successfully', async () => {
      const otpResponse = await request.post(
        urlPaths.auth.verifyResetPassword,
        {
          data: { username: email, code: stagingEmailOTP },
        },
      );
      const { code } = await otpResponse.json();
      resetPasswordOTPCode = code;

      expect(otpResponse.status()).toBe(HttpResponseEnum.SUCCESS);
    });

    // Case 1-3: 重設密碼
    await test.step('Reset password successfully', async () => {
      const resetPasswordResponse = await request.post(
        urlPaths.auth.resetPassword,
        {
          data: {
            username: email,
            code: resetPasswordOTPCode,
            password: resetPassword,
          },
        },
      );

      expect(resetPasswordResponse.status()).toBe(HttpResponseEnum.SUCCESS);
    });

    // Case 1-4: 驗證重設密碼後可以成功登入
    await test.step('Should be logged in successfully', async () => {
      const authHelper = new AuthHelper(authRequest, tokenManager);
      await authHelper.signIn({
        mobile: existingAccount.mobile,
        password: resetPassword,
      });

      await authHelper.signOut(existingAccount.mobile);
    });

    // Case 2-1: 透過手機重設密碼
    await test.step('Request Reset Password through mobile', async () => {
      const response2 = await request.post(urlPaths.auth.requestResetPassword, {
        data: { username: mobile },
      });

      expect(response2.status()).toBe(HttpResponseEnum.SUCCESS);
    });

    // Case 2-2: 驗證是否收到 OTP
    await test.step('Should fail when verifying wrong OTP', async () => {
      const wrongOTPResponse2 = await request.post(
        urlPaths.auth.verifyResetPassword,
        {
          data: { username: mobile, code: wrongMobileOTP },
        },
      );

      expect(wrongOTPResponse2.status()).toBe(HttpResponseEnum.BAD_REQUEST);
    });

    await test.step('Verify OTP successfully', async () => {
      const otpResponse2 = await request.post(
        urlPaths.auth.verifyResetPassword,
        {
          data: { username: mobile, code: stagingMobileOTP },
        },
      );
      const { code } = await otpResponse2.json();
      resetPasswordOTPCode = code;

      expect(otpResponse2.status()).toBe(HttpResponseEnum.SUCCESS);
    });

    // Case 2-3: 重設密碼
    await test.step('Reset password successfully', async () => {
      const resetPasswordResponse2 = await request.post(
        urlPaths.auth.resetPassword,
        {
          data: {
            username: mobile,
            code: resetPasswordOTPCode,
            password: originalPassword,
          },
        },
      );

      expect(resetPasswordResponse2.status()).toBe(HttpResponseEnum.SUCCESS);
    });

    // Case 2-4: 驗證重設密碼後可以成功登入
    await test.step('Should be logged in successfully', async () => {
      const authHelper = new AuthHelper(authRequest, tokenManager);
      await authHelper.signIn({
        mobile: existingAccount.mobile,
        password: originalPassword,
      });

      await authHelper.signOut(existingAccount.mobile);
    });
  });
});
