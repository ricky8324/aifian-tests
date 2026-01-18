import { APIRequestContext, test as base, expect } from '@playwright/test';
import {
  stagingEmailOTP,
  stagingMobileOTP,
  urlPaths,
  userAgent,
} from 'repository/aifian-api/constant';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';
import { getConfigToken } from 'repository/aifian-api/utils/config-token';

let newAccount;
const STAGING_OTP_CODE = '123456';

const test = base.extend<{
  request: APIRequestContext;
}>({
  request: baseRequestFixture,
});

test.describe('Account Registration and Deletion', () => {
  test('Register and Delete account successfully', async ({
    request,
    playwright,
  }) => {
    let isRegistrationSuccess = false;
    let responseChallengeCode = undefined;
    for (
      let retryTimes = 3;
      retryTimes > 0 && !isRegistrationSuccess;
      retryTimes--
    ) {
      newAccount = generateFakeAccount();

      await test.step('Register with mobile and Get challenge code', async () => {
        const requestBody = {
          mobile: newAccount.mobile,
        };
        const response = await request.post(urlPaths.auth.register, {
          data: requestBody,
        });
        expect(response.status()).toBe(200);
      });

      await test.step('Confirm challenge code successfully', async () => {
        const requestBody = {
          mobile: newAccount.mobile,
          code: stagingMobileOTP,
        };
        const response = await request.post(urlPaths.auth.challenge, {
          data: requestBody,
        });
        const responseData = await response.json();

        // if false: meaning this fake mobile number has already exist and need to generate a new one
        if (responseData.errno !== 'USER_EXISTS') {
          expect(responseData.confirmation_code).not.toBeUndefined();
          responseChallengeCode = responseData.confirmation_code;
          expect(response.status()).toBe(200);
          isRegistrationSuccess = true;
        }
      });
    }

    expect(
      isRegistrationSuccess,
      'Max retry attempts reached. Registration failed.',
    ).toBe(true);

    let setPasswordResponse;
    await test.step('Set password successfully and will get access token', async () => {
      const requestBody = {
        mobile: newAccount.mobile,
        confirmation_code: responseChallengeCode,
        password: newAccount.password,
      };
      const response = await request.post(urlPaths.auth.setPassword, {
        data: requestBody,
      });
      setPasswordResponse = await response.json();
      expect(response.status()).toBe(200);
    });

    const authRequest = await playwright.request.newContext({
      extraHTTPHeaders: {
        'user-agent': userAgent,
        'x-aifian-token': getConfigToken(),
        Authorization: setPasswordResponse.access_token || '',
      },
    });

    await test.step('Enter referrals', async () => {
      const requestBody = {
        aifian_id: 'annnnny_',
      };
      const response = await authRequest.post(
        urlPaths.referrals.enterReferrals,
        {
          data: requestBody,
        },
      );

      expect(response.status()).toBe(200);
    });

    await test.step('Send email OTP', async () => {
      const requestBody = {
        email: newAccount.email,
      };
      const response = await authRequest.post(urlPaths.account.sendEmailOTP, {
        data: requestBody,
      });
      expect(response.status()).toBe(200);
    });

    await test.step('Verify email OTP successfully', async () => {
      const requestBody = {
        code: stagingEmailOTP,
      };
      const response = await authRequest.post(urlPaths.account.verifyEmailOTP, {
        data: requestBody,
      });

      expect(response.status()).toBe(200);
    });

    await test.step('Should fail when verifying OTP again', async () => {
      const requestBody = {
        code: stagingEmailOTP,
      };
      const response = await authRequest.post(urlPaths.account.verifyEmailOTP, {
        data: requestBody,
      });

      expect(response.status()).toBe(400);
      const data = await response.json();
      expect(data.errno).toBe('INVALID_OTP_CODE');
    });

    await test.step('Member status should be "registered" before Persona KYC passed', async () => {
      const response = await authRequest.post(urlPaths.auth.signIn, {
        data: {
          mobile: newAccount.mobile,
          password: newAccount.password,
        },
      });

      expect(response.status()).toBe(200);
      const data = await response.json();
      expect(data.status).toBe('registered');
    });

    await test.step('User should be able to request account deletion', async () => {
      const deleteAccountCheckResponse = await authRequest.get(
        urlPaths.account.deleteAccountCheck,
      );
      expect(deleteAccountCheckResponse.status()).toBe(200);

      const deleteAccountCheckData = await deleteAccountCheckResponse.json();
      expect(deleteAccountCheckData.reasons).toEqual([]);

      const deleteAccountOTPResponse = await authRequest.post(
        urlPaths.account.deleteAccountOTP,
        {
          data: {
            contact_value: newAccount.mobile,
          },
        },
      );
      expect(deleteAccountOTPResponse.status()).toBe(200);

      const deleteAccountOTPVerifyResponse = await authRequest.post(
        urlPaths.account.deleteAccountOTPVerify,
        {
          data: {
            code: STAGING_OTP_CODE,
          },
        },
      );
      expect(deleteAccountOTPVerifyResponse.status()).toBe(200);
      const deleteAccountOTPVerifyData =
        await deleteAccountOTPVerifyResponse.json();
      expect(deleteAccountOTPVerifyData.reward_points).toEqual(0);

      const createAccountDeletionResponse = await authRequest.post(
        urlPaths.account.createAccountDeletion,
        {
          data: { reason: 'NOT_NEEDED' },
        },
      );
      expect(createAccountDeletionResponse.status()).toBe(200);
      const createAccountDeletionData =
        await createAccountDeletionResponse.json();
      expect(typeof createAccountDeletionData.scheduled_deletion_at).toBe(
        'string',
      );

      const signInResponse = await request.post(urlPaths.auth.signIn, {
        data: {
          mobile: newAccount.mobile,
          password: newAccount.password,
        },
      });
      expect(signInResponse.status()).toBe(200);
      const signInData = await signInResponse.json();
      expect(typeof signInData.scheduled_deletion_at).toBe('string');
    });

    await test.step('User should be able to cancel the account deletion', async () => {
      const accountDeletionCancelResponse = await authRequest.post(
        urlPaths.account.accountDeletionCancel,
      );
      expect(accountDeletionCancelResponse.status()).toBe(200);

      const signInResponse = await request.post(urlPaths.auth.signIn, {
        data: {
          mobile: newAccount.mobile,
          password: newAccount.password,
        },
      });
      expect(signInResponse.status()).toBe(200);
      const signInData = await signInResponse.json();
      expect(signInData.scheduled_deletion_at).toBe(null);
    });

    await test.step('User should be able to request account deletion again after cancel', async () => {
      const deleteAccountCheckResponse = await authRequest.get(
        urlPaths.account.deleteAccountCheck,
      );
      expect(deleteAccountCheckResponse.status()).toBe(200);

      const deleteAccountCheckData = await deleteAccountCheckResponse.json();
      expect(deleteAccountCheckData.reasons).toEqual([]);

      const deleteAccountOTPResponse = await authRequest.post(
        urlPaths.account.deleteAccountOTP,
        {
          data: {
            contact_value: newAccount.mobile,
          },
        },
      );
      expect(deleteAccountOTPResponse.status()).toBe(200);

      const deleteAccountOTPVerifyResponse = await authRequest.post(
        urlPaths.account.deleteAccountOTPVerify,
        {
          data: {
            code: STAGING_OTP_CODE,
          },
        },
      );
      expect(deleteAccountOTPVerifyResponse.status()).toBe(200);
      const deleteAccountOTPVerifyData =
        await deleteAccountOTPVerifyResponse.json();
      expect(deleteAccountOTPVerifyData.reward_points).toEqual(0);

      const createAccountDeletionResponse = await authRequest.post(
        urlPaths.account.createAccountDeletion,
        {
          data: { reason: 'NOT_NEEDED' },
        },
      );
      expect(createAccountDeletionResponse.status()).toBe(200);
      const createAccountDeletionData =
        await createAccountDeletionResponse.json();
      expect(typeof createAccountDeletionData.scheduled_deletion_at).toBe(
        'string',
      );

      const signInResponse = await request.post(urlPaths.auth.signIn, {
        data: {
          mobile: newAccount.mobile,
          password: newAccount.password,
        },
      });
      expect(signInResponse.status()).toBe(200);
      const signInData = await signInResponse.json();
      expect(typeof signInData.scheduled_deletion_at).toBe('string');
    });
  });
});

function generateFakeAccount() {
  const newMobile = generateFakeMobileNumber('+886', '999'); // 0999 為工程測試使用
  return {
    mobile: newMobile,
    password: 'Abcdef1!',
    email: 'integ-test+' + newMobile.replace(/^\+886/, '0') + '@aifian.com',
  };
}

function generateFakeMobileNumber(countryCode: string, fakePrefix: string) {
  // Generate a random 6-digit number
  const randomMobileNumber = Math.floor(Math.random() * 1000000)
    .toString()
    .padStart(6, '0');
  // Concatenate components to form the complete fake mobile number
  const completeFakeMobileNumber = `${countryCode}${fakePrefix}${randomMobileNumber}`;
  return completeFakeMobileNumber;
}
