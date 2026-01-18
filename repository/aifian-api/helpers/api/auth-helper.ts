import { APIRequestContext, expect } from '@playwright/test';
import { urlPaths, userAgent } from 'repository/aifian-api/constant';
import { SignInResult } from 'repository/aifian-api/types';
import { TokenManager } from 'repository/aifian-api/utils/token-manager';

export class AuthHelper {
  constructor(
    private readonly request: APIRequestContext,
    private readonly tokenManager: TokenManager,
  ) {}

  async signIn({ mobile, password }: { mobile: string; password: string }) {
    const response = await this.request.post(urlPaths.auth.signIn, {
      data: { mobile, password },
    });
    expect(response.status()).toBe(200);
    const data = (await response.json()) as SignInResult;

    this.tokenManager.set(mobile, data);
    return data;
  }

  async refreshToken(mobile: string) {
    const response = await this.request.post(urlPaths.auth.refreshToken, {
      data: {
        mobile,
        refresh_token: this.tokenManager.get(mobile)?.refresh_token,
      },
    });
    expect(response.status()).toBe(200);
    const data = (await response.json()) as SignInResult;
    const newTokens = {
      ...this.tokenManager.get(mobile),
      ...data,
    };
    this.tokenManager.set(mobile, newTokens);
    return data;
  }

  async getNonceV2(mobile: string, type: string) {
    const response = await this.request.post(urlPaths.nonces.v2.create, {
      headers: {
        'user-agent': userAgent,
        Authorization: this.tokenManager.get(mobile)?.access_token || '',
      },
      data: {
        type,
      },
    });
    expect(response.status()).toBe(200);
    const data = (await response.json()) as { nonce: string };
    const original = this.tokenManager.get(mobile);
    if (!original) {
      throw new Error('User not signed in');
    }

    return data.nonce;
  }
  async signOut(mobile: string) {
    const response = await this.request.post(urlPaths.auth.signOut, {
      headers: {
        Authorization: this.tokenManager.get(mobile)?.access_token || '',
      },
    });
    expect(response.status()).toBe(200);
    this.tokenManager.delete(mobile);
  }
}
