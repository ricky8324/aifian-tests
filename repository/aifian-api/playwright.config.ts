import { userAgent } from './constant';
import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';
import path from 'path';

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */

const envFileName = process.env.ENV === 'prod' ? '.env.prod' : '.env.staging';

dotenv.config({
  path: path.resolve(__dirname, 'environment', envFileName),
});

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: './tests',
  /* Prevent parallel execution */
  fullyParallel: false,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /*
   *  Github host standard runner has 2 cores
   *  https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#standard-github-hosted-runners-for--private-repositories
   * But we set 1 to avoid the test case failed due to the parallel execution
   */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  /* reporter: 'html', */
  reporter: [
    ['list'],
    [
      'playwright-qase-reporter',
      {
        debug: true,
        testops: {
          mode: 'testops',
          api: {
            token: "46d80b5b502c91c52628552849220c0ad1c468bc7d28759bdb49005d4b434680",
          },
          project: "API",
          uploadAttachments: true,
          run: {
            complete: true,
          },
        },
      },
    ],
  ],
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: process.env.AIFIAN_API_ENDPOINT,
    extraHTTPHeaders: {
      'Content-Type': 'application/json',
      'user-agent': userAgent,
    },
    // video: 'retain-on-failure',
    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: process.env.CI ? 'retain-on-failure' : 'on',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'setup',
      testMatch: /global\.setup\.ts/,
    },
    {
      name: 'Mobile Chrome',
      use: {
        ...devices['Pixel 5'],
      },
      dependencies: ['setup'],
    },
    {
      name: 'Mobile Safari',
      use: {
        ...devices['iPhone 12'],
      },
      dependencies: ['setup'],
    },
  ],
});
