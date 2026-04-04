# CLI Argument Parser Review

## Issue
The current implementation of `--format=json` in `src/cli.js` only checks for exact string matching:
`args.includes('--format=json')`

## Vulnerabilities & Deficiencies
1. **Space Separation:** Fails if the user passes `--format json` (the POSIX standard).
2. **Case Sensitivity:** Fails if the user passes `--format=JSON`.
3. **No Validation:** Does not validate if the value provided after `--format` is actually valid.
4. **Short Flags:** Lacks support for `-f json`.

## Required Rewrite (For Jules)
Refactor the parsing loop in `src/cli.js` to iterate over `args` and properly evaluate the next token when `--format` is detected. Example logic to implement:

```javascript
for (let i = 0; i < args.length; i++) {
  const arg = args[i].toLowerCase();
  if (arg === '--format' || arg === '-f') {
    if (args[i + 1]?.toLowerCase() === 'json') flags.json = true;
  } else if (arg.startsWith('--format=')) {
    if (arg.split('=')[1] === 'json') flags.json = true;
  }
}
```
