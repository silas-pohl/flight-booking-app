module.exports = {
  parser: '@typescript-eslint/parser', // add the TypeScript parser
  plugins: [
      'svelte3',
      '@typescript-eslint' // add the TypeScript plugin
  ],
  overrides: [ // this stays the same
    {
      files: ['*.svelte'],
      parserOptions: { // add these parser options
          tsconfigRootDir: __dirname,
          project: ['./tsconfig.json'],
          extraFileExtensions: ['.svelte'],
      },
      extends: [ // then, enable whichever type-aware rules you want to use
          'eslint:recommended',
          'plugin:@typescript-eslint/recommended',
          'plugin:@typescript-eslint/recommended-requiring-type-checking'
      ],
      processor: 'svelte3/svelte3',
      rules: {
        "no-useless-escape": "off",
        "no-undef": "off",
        "@typescript-eslint/no-inferrable-types": "off",
        "@typescript-eslint/no-unsafe-argument": "off",
        "@typescript-eslint/no-unsafe-member-access": "off"
      },
    }
  ],
  settings: {
    'svelte3/typescript': () => require('typescript'), // pass the TypeScript package to the Svelte plugin
  }
};