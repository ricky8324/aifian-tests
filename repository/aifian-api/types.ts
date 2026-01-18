import {
  APIRequestContext,
  Fixtures,
  PlaywrightTestArgs,
  PlaywrightTestOptions,
  PlaywrightWorkerArgs,
  PlaywrightWorkerOptions,
} from '@playwright/test';

export enum KYCProgress {
  EMAIL = 'EMAIL',
  REFERRAL = 'REFERRAL',
  KYC = 'KYC',
}

export type SignInResult = {
  external_id: string;
  status: string;
  access_token: string;
  refresh_token: string;
  is_restricted: boolean;
  scheduledDeletionAt: string;
};

export enum HttpResponseEnum {
  INTERNAL_ERROR = 500,
  SUCCESS = 200,
  UNAUTHORIZED = 401,
  BAD_REQUEST = 400,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
}

export enum Currency {
  USD = 'USD',
  TWD = 'TWD',
  JPY = 'JPY',
}

export type GetFixtureType<T extends keyof any> = Fixtures<
  { [K in T]: APIRequestContext },
  object,
  PlaywrightTestArgs & PlaywrightTestOptions,
  PlaywrightWorkerArgs & PlaywrightWorkerOptions
>[T];
