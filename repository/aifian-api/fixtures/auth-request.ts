import { userAgent } from '../constant';
import { GetFixtureType } from '../types';
import { getConfigToken } from '../utils/config-token';
import { TokenManager } from '../utils/token-manager';

type AuthRequestFixture = GetFixtureType<'authRequest'>;

export const createAuthRequestFixture =
  (mobile: string, tokenManager: TokenManager): AuthRequestFixture =>
  async ({ playwright }, use) => {
    const authContext = await playwright.request.newContext({
      extraHTTPHeaders: {
        'user-agent': userAgent,
        'x-aifian-token': getConfigToken(),
        Authorization: tokenManager.get(mobile)?.access_token || '',
      },
    });

    await use(authContext);
    await authContext.dispose();
  };
