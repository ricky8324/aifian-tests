import typescriptEslint from "@typescript-eslint/eslint-plugin";
import prettier from "eslint-plugin-prettier";
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    plugins: {
      "@typescript-eslint": typescriptEslint,
      prettier,
    },

    languageOptions: {
      ecmaVersion: 5,
      sourceType: "module",

      parserOptions: {
        project: ["./tsconfig.json"],
        allowImportExportEverywhere: true,
        extraFileExtensions: [".json"],
      },
    },
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      "linebreak-style": ["error", "unix"],
      "one-var": ["error", "never"],
      quotes: ["error", "single"],
      semi: ["error", "always"],
      "no-duplicate-imports": [
        "error",
        {
          includeExports: true,
        },
      ],
      "no-var": "error",
      "prefer-const": "error",
      "array-callback-return": "error",
      "class-methods-use-this": "error",
      "default-case-last": "error",
      "default-param-last": ["error"],
      "dot-notation": "error",
      eqeqeq: ["error", "always"],
      "require-await": "warn",
      "@typescript-eslint/ban-ts-comment": "off",
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-explicit-any": "off",
    },
  },
];
