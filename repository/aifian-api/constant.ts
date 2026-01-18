import path from 'path';

export const urlPaths = {
  auth: {
    signIn: '/v2/auth/sign-in',
    refreshToken: '/v2/auth/refresh',
    signOut: '/v2/auth/sign-out',
    register: '/v2/auth',
    challenge: '/v2/auth/challenge',
    setPassword: '/v3/auth/password',
    requestResetPassword: '/v2/auth/reset',
    verifyResetPassword: '/v2/auth/reset/verify',
    resetPassword: '/v2/auth/reset/password',
  },
  exchangeRates: '/v1/exchange-rates',
  announcements: '/v1/announcements',
  account: {
    v1: '/v2/account',
    sendEmailOTP: '/v2/account/emails',
    verifyEmailOTP: '/v1/account/emails/verify',
    bankList: '/v1/account/bank-account/bank-list',
    branchList: '/v1/account/bank-account/branch-list',
    bankAccount: '/v1/account/bank-account',
    deleteBankAccount: '/v1/account/bank-account/delete',
    deleteAccountCheck: '/v2/account/deletion/check',
    deleteAccountOTP: '/v1/account/deletion/otp',
    deleteAccountOTPVerify: '/v1/account/deletion/otp/verify',
    createAccountDeletion: '/v1/account/deletion',
    accountDeletionCancel: '/v1/account/deletion/cancel',
    accountNameChange: '/v1/account/name-change',
  },
  config: '/v1/config',
  kyc: {
    getState: '/v1/kyc/state',
    start: '/v1/kyc/start',
    submit: '/v1/kyc/submit',
  },
  referrals: {
    enterReferrals: '/v1/referrals',
  },
  lottery: '/v2/lottery',
  products: '/v1/products',
  nonces: {
    v2: {
      create: '/v2/nonces',
    },
  },
  graph: {
    asset: {
      total: '/v1/graph/asset/total',
      individual: '/v1/graph/asset/individual',
    },
    product: '/v1/graph/product',
  },
  portfolio: {
    asset: {
      totalInfo: '/v1/portfolio/asset/total-info',
      individualInfo: '/v1/portfolio/asset/individual-info',
      detail: '/v1/portfolio/asset',
    },
    summary: '/v1/portfolio',
    product: {
      latestInfo: '/v1/portfolio/product/latest-info',
    },
  },
  product: {
    transaction: {
      completed: '/v1/products/transactions/completed',
      processing: '/v1/products/transactions/processing',
      detail: '/v1/products/transactions/detail',
    },
  },
  rewards: {
    v1: {
      info: '/v1/rewards',
    },
  },
  event: {
    eventCards: '/v1/events',
  },
};

export const legacyUrlPaths = {
  members: {
    profile: '/members/profile',
  },
};

export const aifianUrlPaths = {
  order: {
    compute: '/api/orders/compute',
    fullDiscountCreate: '/api/orders/reward-points',
  },
};

// Member ID and their corresponding auth info
export const userRole = {
  // Refresh Token
  214680: {
    mobile: '+886912137582',
    password: 'Bella098',
  },
  // SIT SignIn & SignOut
  214446: {
    mobile: '+886900752481',
    password: 'Bella010',
  },
  214692: {
    mobile: '+886978725961',
    password: 'AIFIAN123',
  },
  // SIT SignIn with deleted account
  215476: {
    mobile: '+886900010139',
    password: 'Bella139',
  },
  // SIT Bank Account
  214450: {
    mobile: '+886900752464',
    password: 'Bella013',
  },
  // SIT Lottery
  214919: {
    mobile: '+886900752640',
    password: 'Bella015',
  },
  // SIT Resell and Cancel
  214457: {
    mobile: '+886900752647',
    password: 'Bella020',
  },
  // SIT Portfolio with Liquor
  214490: {
    mobile: '+886900753594',
    password: 'Bella044',
  },
  // SIT Portfolio with Liquor
  214953: {
    mobile: '+886900753054',
    password: 'Bella022',
  },
  // forget password
  215464: {
    email: 'product_qa+138@aifian.com',
    mobile: '+886900010138',
    password: 'Bella138$',
  },
  // get reward info
  217168: {
    mobile: '+886900010156',
    password: 'Bella156$',
  },
  // SIT Account had withdraw process
  214666: {
    mobile: '+886900753254',
    password: 'Bella031$',
  },
};

export const userAgent = 'aifian/6.0.0 iPhone14,4 iOS/17.1.2';

export const authFilePath = path.resolve(
  __dirname,
  'playwright/.auth',
  'auth.json',
);

// Staging will use this OTP for all test cases.
export const stagingMobileOTP = '123456';
export const stagingEmailOTP = '123456';

// Wrong OTP for test cases.
export const wrongEmailOTP = '112233';
export const wrongMobileOTP = '112233';
