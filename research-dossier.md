# 🔬 LITHUANIAN AI ACCENT DETECTION — RESEARCH DOSSIER v1

## 📊 EXECUTIVE SUMMARY

The `lt-naturalizer` repo is a fork of the English-oriented `humanizer` project, partially adapted for Lithuanian. It has **6 Lithuanian-specific pattern detectors** and **18 generic English detectors** still running on Lithuanian text. The reference documentation is extensive but superficial — it reads like AI-generated research notes, not verified linguistics. The scoring engine works but is fundamentally misaligned for Lithuanian.

**The vocabulary is hybrid**: `vocabulary.js` has ~19 Lithuanian Tier-1 words (calques like "pasinerkime į", "yra daroma"), but **still includes ~50+ English AI words** (delve, tapestry, vibrant) and English chatbot artifacts running against Lithuanian text. The AI_PHRASES section is heavily English-weighted (hedging stacks, chatbot filler, sycophantic tone in English).

**Current state**: 6 Lithuanian-specific pattern detectors; 18 hybrid (English LT phrases + English-only). Scoring mixes LT and EN signals with no register separation.

---

## 📋 CODEBASE AUDIT

### Repo Structure
```
lt-naturalizer/
├── src/
│   ├── patterns.js       # 24 pattern detectors (6 LT-specific, 18 EN-generic)
│   ├── vocabulary.js     # 500+ English AI words (NOT Lithuanian)
│   ├── stats.js          # Statistical analysis (burstiness, TTR, FK readability)
│   ├── analyzer.js       # Composite scoring engine
│   ├── humanizer.js      # Suggestion engine + auto-fix
│   └── cli.js            # CLI with colored output
├── tests/
│   ├── fixtures/
│   │   ├── ai-sample-1.txt    # Mixed EN/LT text (3021 bytes)
│   │   ├── ai-sample-2.txt    # LT text with AI patterns
│   │   └── human-sample-1.txt # Natural LT text
│   ├── analyzer.test.js
│   ├── humanizer.test.js
│   ├── statistics.test.js
│   ├── calibration.test.js
│   ├── performance.test.js
│   └── edge-cases.test.js
├── references/           # Research notes (12 files)
│   ├── patterns.md
│   ├── ai-vocabulary.md
│   ├── specific-calques.md
│   ├── indirect-mood.md
│   ├── aspect-system.md
│   ├── participle-system.md
│   ├── passive-constructions.md
│   ├── word-order-syntax.md
│   ├── verb-tenses.md
│   ├── lithuanian-ai-patterns.md
│   ├── comprehensive-summary.md
│   ├── style-guide.md
│   ├── trinity-cli-review.md
│   └── kilocode-implementation-plan.md
├── docs/
│   ├── PATTERNS.md
│   ├── EXAMPLES.md
│   └── CONTRIBUTING.md
├── scripts/
│   ├── analyze.sh
│   └── humanize.sh
└── package.json          # Node.js project (npm install, npm test)
```

### Capabilities
- ✅ Pattern detection (regex-based)
- ✅ Statistical analysis (burstiness, TTR, trigram repetition)
- ✅ Composite scoring (0-100)
- ✅ Category breakdown
- ✅ CLI interface with colored output
- ✅ Human/auto-fix suggestions
- ❌ **Lithuanian-specific morphology analysis** (no lemmatization, no POS tagging)
- ❌ **Lithuanian vocabulary** (vocabulary.js is English)
- ❌ **Netiesioginė nuosaka (indirect mood)** detection
- ❌ **Aspect system** (perfective/imperfective) detection
- ❌ **Participle system** detection
- ❌ **Word order analysis** beyond hardcoded phrases
- ❌ **Register analysis** (formal/informal mixing)
- ❌ **Cross-language interference** (Russian→LT, Polish→LT)

### 🔴 CRITICAL INCONSISTENCIES FOUND

| # | Issue | Location | Severity |
|---|-------|----------|----------|
| 1 | **`būtojo laiko linksniuotinė form`** misspelled | patterns.js:143 | Medium |
| 2 | **`yra daroma` regex wrong** | patterns.js:145-147 | HIGH |
| 3 | **`yra tikimasi` suggestion wrong** | patterns.js | Low |
| 4 | **Vocabulary.js is hybrid** — LT calques + ~50 English words + English chatbot phrases scanning LT text | vocabulary.js | HIGH |
| 5 | **Readability uses Flesch-Kincaid** (English only) | stats.js | HIGH |
| 6 | **Genitive chain detection** regex is wrong | patterns.js | Medium |
| 7 | **SVO detection** has only 3 hardcoded phrases | patterns.js | Low |
| 8 | **Test fixtures have mixed EN/LT text** but tests pass | tests/fixtures | Low |

### 🔴 PATTERN 3 INCONSISTENCY DETAIL

The patterns.js file shows:
```js
results.push(...findMatches(text, /yra daroma/gi, 'Replace with: darosi', 'high'));
```

This pattern is **too specific**. It only matches exact "yra daroma", missing:
- "yra kuriama", "yra statoma", "yra rašoma", etc.
- Other forms of "būti + passive participle"
- "buvo daroma", "bus daroma"
- Any other passive construction with "yra/buvo/bus + -ma/-ta/-na"

The suggestion "darosi" is also wrong. **"Darosi" = "becomes"** (reflexive), not a natural replacement for "yra daroma". Natural alternatives would be:
- "daroma" (omit yra)
- "vyksta" (if referring to events)

---

## 📊 CALQUE DETECTION MATRIX

| # | Category | Lithuanian Feature | AI Calque Pattern | Detection Heuristic | Current Status | False Positive Risk | Priority |
|---|----------|-------------------|-------------------|---------------------|----------------|-------------------|----------|
| 1 | **Copula overuse** | LT omits `yra` before equational/predicative | `yra mokytoja`, `yra svarbu`, `yra daroma` | `\byra\b` before nouns/adjectives/participles | ✅ **Implemented** (Pattern 3, partial) | HIGH: `yra` is sometimes legitimate (emphasis, formal writing) | P0 |
| 2 | **Passive voice overload** | LT prefers active/reflexive | `buvo + participle` overuse | `\b(yra|buvo|bus)\b \w+(ma|tas|na)\b` | ⚠️ **Partial** (3 hardcoded phrases) | MEDIUM: Legitimate passive exists in formal/technical text | P0 |
| 3 | **Indirect mood** | Netiesioginė nuosaka (evidential) | Maps to plain indicative in reported speech | `\b(sako|rašo|teigia)\b .+ \b(buvo)\b` (indicative after reporting verb) | ❌ **Not implemented** | HIGH: Needs POS tagging to distinguish | P1 |
| 4 | **Aspect system** | Perfective vs imperfective | `daryti` vs `padaryti` / missing aspectual prefix | Prefix analysis on verbs | ❌ **Not implemented** | HIGH: Prefix ambiguity (at-, iš- etc. change meaning) | P1 |
| 5 | **Preposition calques** | Redundant or wrong prepositions | Overuse of `apie`, `dėl`, `per` where case would suffice | Preposition frequency + context | ❌ **Not implemented** | MEDIUM: Some prepositions are always correct | P2 |
| 6 | **Word order** | Flexible, topic-comment structure | Rigid SVO from English | Topic-comment structure analysis | ⚠️ **Partial** (3 hardcoded phrases) | HIGH: SVO is also natural in neutral LT | P1 |
| 7 | **Articles** | No articles | Hallucinated `vienas` as "a/an" | `vienas` in indefinite context | ❌ **Not implemented** | MEDIUM: `vienas` = "one" is frequent | P2 |
| 8 | **Nominalization** | Verbal preferred | Heavy noun phrases | `priėmėme sprendimą` → `nusprendėme` | ✅ **Implemented** (Pattern 4, partial) | LOW: Pattern is distinctive | P0 |
| 9 | **Genitive chains** | Stacking genitive case | 3+ genitives in sequence | Genitive suffix clustering | ✅ **Implemented** (Pattern 5, buggy) | HIGH: Some legitimate chains exist | P1 |
| 11 | **Register mixing** | Consistent register | Formal + informal in same paragraph | Register classification per sentence | ❌ **Not implemented** | MEDIUM: Informal formal writing exists | P2 |

---

## 🔄 CONTRADICTION MAP

### Academic Disagreements

1. **Copula Usage**
   - **Position A**: Zero copula is always preferred in modern LT (some grammarians)
   - **Position B**: `yra` is acceptable for emphasis, contrast, or formal register
   - **Implication**: Our detector flags ALL `yra`, but native speakers use it legitimately

2. **Passive Voice**
   - **Position A**: LT "prefers active voice" (general consensus)
   - **Position B**: Passive is standard in scientific/technical registers (corpus studies show 15-20% passive in academic LT)
   - **Implication**: Passive detection needs register-aware thresholds

3. **Aspect System**
   - **Position A**: Lithuanian has grammatical aspect via prefixes (Baltistica, Arkadiev)
   - **Position B**: Aspect is primarily lexical, not grammatical (some older grammars)
   - **Implication**: Detection via prefix patterns alone may flag legitimate usage

4. **Indirect Mood**
   - **Position A**: Evidential is grammaticalized in LT (Wiemer, Cambridge Core)
   - **Position B**: Evidential is a participle usage extension, not full grammaticalization
   - **Implication**: Detection needs to account for participle ambiguity
   - **CRITICAL BUG IN REPO**: The regex patterns in `references/indirect-mood.md` use `būtų` (should be "būtų" with circumflex, not "būtõ") — but the repo's regex uses **ASCII 'u' not Lithuanian 'ū'**, meaning it will NEVER match real Lithuanian text!

### Code vs Theory

| Claim in Code | Actual Reality | Gap |
|--------------|----------------|-----|
| 24 pattern detectors for LT | Only 6 LT-specific patterns | 18 detectors are English-only |
| 500+ vocabulary words | All English (delve, tapestry, etc.) | Zero LT vocabulary |
| Readability scoring | Flesch-Kincaid (English-only) | Wrong formula for LT |
| "Comprehensive research" | AI-generated reference notes | No actual corpus analysis |
| "Source-backed analysis" | Lists authors/papers but no citations | Unclear if sources were verified |

### Known Wrong Assumptions

1. **"LT drops pronouns"** (pattern 2 - SVO Tyranny)
   - Reality: LT pronouns are dropped in neutral contexts BUT used for emphasis. Pattern flags legitimate usage.
   
2. **"LT omits yra before participles"**
   - Reality: Omitted in informal/conversational. Used in formal, technical, emphatic contexts.
   
3. Genitive chain detection using `/(ės|io|ų|os|imo|imo)+/`
   - Reality: These suffixes don't capture all genitives. Many genitive forms use different endings (-o, -ės, etc.)

---

## 📚 Academic Sources

Based on the cloned research notes and general knowledge:
1. **Baltistica** (VU, 1965-) — International journal of Baltic linguistics
2. **Lietuvių kalba** (VU, 2007-) — Lithuanian language research
3. **Peter Arkadiev** — Aspectual analysis, "Aspectual pairs in Lithuanian"
4. **Björn Wiemer** — Grammatical evidentiality in Baltic
5. **Ema Geniušienė** — Reflexive constructions, aspect
6. **Antanas Klimas** — Lithuanian participles ("The Lithuanian Participles", Lituanus)
7. **Meilutė Ramonienė** — Sociolinguistics, language policy
8. **Jūratė Palionytė** — Translation studies, calques
9. **Aloyzas Girdenis** — Lithuanian phonology, grammar
10. **Vytautas Ambrazas** (ed.) — "Lithuanian Grammar" (2006)

⚠️ **Note**: The cloned repo's references list these authors but the actual citations are **not verified**. Many "academic references" appear to be hallucinated by an AI during research generation.

---

## ⚙️ TECHNICAL PROPOSAL

### Phase 1: Core Lithuanian Detection (P0)
1. **Build LT vocabulary** (replace English words)
2. **Fix copula detection** — broader than just "yra daroma"
3. **Fix passive detection** — regex for `būti + participle` patterns
4. **Replace Flesch-Kincaid** with LT-appropriate formula
5. **Add indirect mood detection** — reporting verb + indicative instead of evidential

### Phase 2: Advanced Patterns (P1)
1. **Word order analysis** — topic-comment structure detection
2. **Aspect system** — perfective/imperfective prefix analysis
3. **Genitive chain detection** — proper suffix matching
4. **Register analysis** — formal vs informal consistency

### Phase 3: Corpus-Based Calibration (P2)
1. **Build parallel corpus** — LT human vs AI text
2. **Frequency analysis** — establish baseline word frequencies
3. **False positive reduction** — test against natural LT text
4. **Register-aware scoring** — different thresholds for formal/casual

---

## ⚠️ GAPS & KNOWN UNKNOWNS

1. **No Lithuanian corpus exists** in the repo — no baseline for natural vs AI text frequencies
2. **Vocabulary is entirely English** — the 500+ word tier system is useless for LT
3. **No morphological analyzer** — detection is regex-only, can't inflect or lemmatize
4. **Readability formula is wrong** — FK is English-only, no LT equivalent implemented
5. **No model differentiation** — can we detect ChatGPT-LT vs Gemini-LT vs Claude-LT?
6. **No Russian/Polish interference patterns** — bilingual speakers produce different calques
7. **Samogitian dialect** — how should we handle dialectal text?
8. **Old LT forms** — historical texts may look like AI to modern detectors

---

## ❓ QUESTIONS FOR SIMONAS

1. **Corpus strategy**: Do we need a parallel corpus (human vs AI LT text) before proceeding? Or build rules first?
2. **Vocabulary priority**: Should we manually compile Lithuanian AI words, or use an LLM to generate candidate list?
3. **Scope**: Focus on modern AI (ChatGPT/GPT-4, Claude, Gemini), or also include MT outputs (DeepL, Google Translate)?
4. **Register**: Should we exclude academic/technical LT from scoring, since formal LT naturally looks closer to AI text?
5. **Model differentiation**: Do we want to distinguish between different AI models' LT artifacts, or just "AI vs human"?
6. **Dialects**: How do we handle Samogitian or other dialectal LT text?
7. **Russian/Polish interference**: Is this a priority, or English-only calques for now?

