# aifian-tests

## Getting Started

This will help you understand the structure of the aifian-tests and how to start development. It's recommend to finish our introduction doc on notion for Playwright and this repo. [notion doc](https://www.notion.so/aifianapp/Playwright-intro-67b9193707cb492b8cf11c44f6f90128#e2be4c942dcb48f6ac2e0c6b76bdce0b)

## Local Environment Setup

1. Install project dependency

   ```typescript
   yarn install
   ```

2. Install Playwright dependency

   Before using Playwright, we need to install browser binary to enable Playwright run on different environment.

   ```typescript
   sudo npx playwright install --with-deps
   ```

3. Setup .env file

   Copy the .env.example file to .env and update the variables with your specific values. Those variables are used to configure emulation environment which will be used in emu:webview script.

## Project Structure

The project is a Playwright application. The codebase is organized into several directories:

```text
.
├── README.md
├── eslint.config.mjs
├── package.json
├── playwright-report
│   └── index.html
├── repository
│   └── aifian-api
│       ├── constant.ts
│       ├── fixtures
│       │   └── auth-request.ts
│       ├── helpers
│       │   ├── pages
│       │   └── api
│       ├── playwright
│       │   └── .auth
│       │       └── auth.json
│       ├── playwright.config.ts
│       ├── tests
│       │   └── auth
│       │       ├── auth.setup.ts
│       │       └── refresh-token-sign-in.spec.ts
│       └── utils
└── test-results
```

- `package.json`: Contains scripts related to starting tests. To run tests for a specific repo, use `yarn test:{TARGET_REPO}`. To run only the critical path tests that would be executed in production, use `yarn test:{TARGET_REPO}:prod`. (Production env is not setup yet, currently this command only run critical path test on staging)
- `playwright-report`: The report generated after tests are completed is stored here.
- `test-results`: Records the results of the most recent test run.
- `repository`: All tests are placed here. They are organized into different directories according to different projects (such as aifian-api, aifian-async, etc.). The directory structure under each repository should follow these guidelines:
  - `environment`: Staging and Prod env will store here. Currently we only use .env.staging
  - `constant.ts`: A file to store constant variables and export environment variables.
  - `fixtures`: A directory to place custom fixtures.
  - `helpers`: A directory for custom page models or helper classes. API helper classes are placed under the `api` directory. Page objects are placed under `pages`.
    Page object models are a design pattern that uses a page object to represent a part of our web application. An e-commerce web application might have a home page, a listings page, and a checkout page. Each of these can be represented by page object models.
  - `playwright.config.ts`: Stores the playwright test configuration for each repository. When running integration tests, each repository will read its own settings.
  - `playwright/.auth`: Used to store shared browser contexts. Refer to https://playwright.dev/docs/auth
  - `tests`: Stores all tests, organized into different module directories based on business logic. Within these module directories are files for different processes. For example, the directory structure `tests/auth/refresh-token-sign-in.spec.ts` represents the module name 'auth' and the process to be tested 'refresh-token-sign-in.spec.ts'.
  - `utils`: Contains shared tools other than page objects and API helpers.

## Local Development

- Leverage [trace viewer](https://playwright.dev/docs/trace-viewer-intro)

  Trace viewer is a GUI tool which show the recored test with interactive window. We can see the snapshot between each steps and go back or forward through each action of your test and visually see what was happening during each action.

- Use Playwright extension on VSCode

  The Playwright VSCode plugin allows us to easily run individual tests or a select group of tests. During test execution, by adjusting settings, we can invoke the headed mode which opens the browser, or call up the trace viewer.

  [Playwright extension](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright)

- Use UI Mode on local development

  Open UI Mode by running `npx playwright test --ui`.

  UI Mode is a powerful tool which let us trace the whole test lifecycle. It’s a interactive trace viewer with additional tools. Run and debug test with watchable and interactive human friendly GUI.

## Resources

For more detailed information on the technologies and frameworks used in this project, refer to the following documentation:

1. **Playwright**:

   - Aifian notion: [Aifian Playwright Intro](https://www.notion.so/aifianapp/Playwright-intro-67b9193707cb492b8cf11c44f6f90128#19825ce25065479e8c893bce5df17b2e)
   - Official Documentation: [Playwright Docs](https://playwright.dev/docs/intro)

2. **Test automation university**

   - Official Website: [Test automation university](https://testautomationu.applitools.com/)
