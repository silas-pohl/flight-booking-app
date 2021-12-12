module.exports = {
  parser: '@typescript-eslint/parser',
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended', 'plugin:@typescript-eslint/recommended-requiring-type-checking'],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    tsconfigRootDir: __dirname,
    project: ['./tsconfig.json'],
    extraFileExtensions: ['.svelte'],
  },
  env: {
    es6: true,
    browser: true,
  },
  overrides: [
    {
      files: ['*.svelte'],
      processor: 'svelte3/svelte3',
      rules: { 'no-undef': 'off' },
    },
  ],
  settings: {
    'svelte3/typescript': require('typescript'),
  },
  plugins: ['svelte3', '@typescript-eslint'],
  ignorePatterns: ['node_modules', 'public/build', '.eslintrc.js', 'prettier.config.js', 'rollup.config.js', 'svelte.config.js'],
};
