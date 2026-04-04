# Lithuanian vs English Grammar Research: Aspect System

## Research Objective

Comprehensive analysis of Lithuanian vs English aspect systems, identifying all grammatical divergences that create "AI accent" in generated text.

## Lithuanian Aspect System

### Perfective/Imperfective Pairs
- **Perfective**: Completed, bounded actions
- **Imperfective**: Ongoing, unbounded actions
- **Formation**: Morphological distinction through prefixes/suffixes

### Prefix-Based Perfectives
- **Common prefixes**: at-, iš-, per-, pra-, prie-, su-, už-, ž-, po-, prieš
- **Function**: Mark perfective aspect
- **Example**: skaityti (imperfective) → perskaityti (perfective)

### Aspectual Meaning
- **Perfective**: Completed action, result achieved
- **Imperfective**: Ongoing action, process focus
- **No tense dependency**: Aspectual distinction independent of tense

### Key Characteristics
- **Morphological aspect**: Prefixes mark aspectual distinction
- **Aspectual pairs**: Most verbs have perfective/imperfective counterparts
- **Aspectual meaning**: Perfective = completed, imperfective = ongoing

## English vs Lithuanian Divergence

### No Direct Mapping
- **English**: Simple vs progressive aspect distinction
- **Lithuanian**: Perfective vs imperfective morphological distinction
- **AI Error Pattern**: Incorrect aspectual pairing of verbs

### Prefix Confusion
- **English**: No prefix-based aspect system
- **Lithuanian**: Prefixes mark perfective aspect
- **AI Error Pattern**: Wrong or missing aspectual prefixes

### Aspectual Meaning
- **English**: Progressive = ongoing, simple = habitual/generic
- **Lithuanian**: Perfective = completed, imperfective = ongoing
- **AI Error Pattern**: Confusion between aspectual meanings

## AI Translation Errors

### Aspectual Mismatch
```
English: "She read the book" (completed action)
AI Lithuanian: "Ji skaito knygą" (imperfective)
Natural Lithuanian: "Ji perskaito knygą" (perfective with prefix)
```

### Prefix Errors
```
English: "He was writing a letter" (ongoing)
AI Lithuanian: "Jis rašė laišką" (past imperfective)
Natural Lithuanian: "Jis rašė laišką" (correct), but context-dependent
```

### Aspectual Meaning Confusion
```
English: "I have read the book"
AI Lithuanian: "Aš perskaičiau knygą" (perfective)
Natural Lithuanian: "Aš esu perskaitęs knygą" (compound perfective)
```

## Detection Rules

### Perfective Prefix Patterns
```regex
\b(at|ap|į|iš|per|pra|prie|su|už|ž|po|prieš)\w+\b
```

### Imperfective Base Patterns
```regex
\b(ne|be|nedidelis|nedidelė)\w+\b
```

### Aspectual Pair Confusion
```regex
\b(skaičiu|skaito|perskaityti)\b
```

### Prefix Missing Errors
```regex
\b(rašo|rašė|parašyta|parašė)\b
```

## Natural Alternatives

### Perfective for Completed Actions
```
English: "She read the book" (completed)
AI: "Ji skaito knygą" (imperfective)
Natural: "Ji perskaito knygą" (perfective)
```

### Imperfective for Ongoing Actions
```
English: "He was writing" (ongoing)
AI: "Jis ra\u0161\u0117" (past imperfective)
Natural: "Jis ra\u0161\u0117" (correct), context-dependent
```

### Compound Forms for Perfect Meaning
```
English: "I have read the book"
AI: "A\u0161 perskai\u010diau knyg\u0105"
Natural: "A\u0161 esu perskait\u0119s knyg\u0105"
```

## Source-Backed Analysis

### Academic References
- **De Gruyter Brill**: "The Perfective present in Lithuanian" - Anna Daugavet
- **Baltistica**: "Aspectual pairs in Lithuanian" - Ema Geniu\u0161ien\u0117
- **Cambridge Core**: "Verbal aspect in Baltic languages" - Peter Arkadiev

### Key Research Findings
- Lithuanian aspect system is primarily morphological through prefixes
- Perfective/imperfective distinction is independent of tense
- No direct English equivalent - English aspect is tense-based

## Implementation Notes

This research will directly inform the `lt-naturalizer` detection engine by:
- Identifying aspectual pair confusion patterns
- Detecting prefix-based aspect errors
- Recognizing aspectual meaning confusion
- Providing source-based validation for pattern weights
- Creating comprehensive detection rule sets

## Validation Approach

1. Cross-reference multiple academic sources
2. Verify patterns against native speaker corpora
3. Test detection rules against actual AI-generated text samples
4. Consult with Lithuanian linguistics experts if available