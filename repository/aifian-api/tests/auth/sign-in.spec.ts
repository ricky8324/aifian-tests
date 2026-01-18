import { urlPaths, userRole } from '../../constant';
import { APIRequestContext, test as base, expect } from '@playwright/test';
import { baseRequestFixture } from 'repository/aifian-api/fixtures/base-request';

const test = base.extend<{
  request: APIRequestContext;
}>({
  request: baseRequestFixture,
});

test.describe('sign-in test', () => {
  test('should return valid data for the correct username and password', async ({
    request,
  }) => {
    const res = await request.post(urlPaths.auth.signIn, {
      data: {
        mobile: userRole[214692].mobile,
        password: userRole[214692].password,
      },
    });

    expect(res.status()).toBe(200);

    const responseData = await res.json();
    expect(responseData.external_id).toBe(
      'dcc19209-32af-4412-a09f-33e2fd788be3',
    );
    expect(responseData.status).toBe('verified');
    expect(typeof responseData.access_token).toBe('string');
    expect(typeof responseData.refresh_token).toBe('string');
  });

  test('should return status code 400 and correct errno for the incorrect password', async ({
    request,
  }) => {
    const res = await request.post(urlPaths.auth.signIn, {
      data: {
        mobile: userRole[214692].mobile,
        password: 'incorrect_password',
      },
    });

    expect(res.status()).toBe(400);

    const responseData = await res.json();
    expect(responseData.errno).toBe('NOT_AUTHENTICATED');
  });

  test('should return status code 400 and correct errno for users who have the account deleted application', async ({
    request,
  }) => {
    const res = await request.post(urlPaths.auth.signIn, {
      data: userRole[215476],
    });

    expect(res.status()).toBe(400);

    const responseData = await res.json();
    expect(responseData.errno).toBe('USER_IN_ACCOUNT_DELETE_PROCESSING');
  });
});
