const js = require('@eslint/js');
module.exports = [
  js.configs.recommended,
  {
    files: ['src/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'commonjs',
      globals: {
        require: 'readonly',
        module: 'readonly',
        process: 'readonly',
        console: 'readonly',
        __dirname: 'readonly'
      },
    },
    rules: {
      'no-unused-vars': 'warn',
    },
  },
  {
    files: ['tests/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        describe: 'readonly',
        it: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        beforeAll: 'readonly',
        afterAll: 'readonly',
        require: 'readonly',
        console: 'readonly',
        __dirname: 'readonly',
        performance: 'readonly'
      },
    },
    rules: {
      'no-unused-vars': 'warn',
    },
  },
  { ignores: ['node_modules/', 'dist/'] },
];
