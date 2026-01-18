import { userAgent } from '../constant';
import { GetFixtureType } from '../types';
import { getConfigToken } from '../utils/config-token';

type BaseRequestFixture = GetFixtureType<'request'>;

export const baseRequestFixture: BaseRequestFixture = async (
  { playwright },
  use,
) => {
  const requestContext = await playwright.request.newContext({
    extraHTTPHeaders: {
      'user-agent': userAgent,
      'Content-Type': 'application/json',
      'x-aifian-token': getConfigToken(),
    },
  });
  await use(requestContext);
  await requestContext.dispose();
};
