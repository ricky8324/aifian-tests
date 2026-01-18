import { SignInResult } from '../types';

export class TokenManager extends Map<string, SignInResult> {
  get [Symbol.toStringTag]() {
    return this.constructor.name;
  }
}
