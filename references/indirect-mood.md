# Lithuanian vs English Grammar Research: Indirect Mood

## Research Objective

Comprehensive analysis of Lithuanian vs English indirect mood systems, identifying all grammatical divergences that create "AI accent" in generated text.

## Lithuanian Evidential System

### Grammatical Evidentiality
- **Unique feature**: Lithuanian is one of few Indo-European languages with grammatical evidentiality
- **Formation**: past active participle + būti
- **Function**: Marks information as second-hand or uncertain

### Indirect Mood Formation
```
Present: serga → sergęs
Past: sirgo → sirgęs
Future: sirgs → sirgsiės
```

### Semantic Function
- **Direct speech**: "Jis sako: "Mano tėvas serga""
- **Indirect speech**: "Jis sako, kad jo tėvas sergęs"
- **Meaning**: Marks information as reported, not directly witnessed

### Key Characteristics
- **Participle-based**: Formed with past active participle
- **Semantic marking**: Indicates evidential status
- **No English equivalent**: English lacks grammatical evidential marking

## English vs Lithuanian Divergence

### Evidential Gap
- **English**: No grammatical evidential marking
- **Lithuanian**: Grammatical evidentiality system
- **AI Error Pattern**: Loss of evidential distinction when defaulting to indicative

### Semantic Loss
- **English**: Relies on context/adverbs for evidential meaning
- **Lithuanian**: Grammatical marking of evidential status
- **AI Error Pattern**: Failure to mark reported information

### Mood Confusion
- **English**: Subjunctive for hypotheticals, not evidentiality
- **Lithuanian**: Distinct indirect mood for evidentiality
- **AI Error Pattern**: Confusion between evidential and hypothetical meanings

## AI Translation Errors

### Evidential Collapse
```
English: "They say he was at home"
AI Lithuanian: "Jie sako, kad jis buvo namie" (indicative mood)
Natural Lithuanian: "Jie sako, kad jis būtů namie" (indirect mood)
```

### Semantic Ambiguity
```
English: "According to reports, the building collapsed"
AI Lithuanian: "Pagal pranešimus, pastatas sudužo" (indicative)
Natural Lithuanian: "Pagal pranešimus, pastatas būtů sudužęs" (indirect)
```

### Hypothetical Confusion
```
English: "If he was at home"
AI Lithuanian: "Jei jis būtů namie" (incorrectly uses indirect mood)
Natural Lithuanian: "Jei jis buvo namie" (correct indicative for hypothetical)
```

## Detection Rules

### Indirect Mood Patterns
```regex
\b(buvo|esą|bus) \w+ęs\b
\b(buvo|esą|bus) \w+usi\b
\b(buvo|esą|bus) \w+ę\b
```

### Evidential Context Patterns
```regex
\b(sako|praneša|rašo|rašė|pasakė|teigia) \w+\b
```

### Indicative vs Indirect Confusion
```regex
\b(Jei|Jeigu|Kuomet) \w+\b
```

## Natural Alternatives

### Indirect Mood for Reported Information
```
English: "They say he was at home"
AI: "Jie sako, kad jis buvo namie"
Natural: "Jie sako, kad jis būtů namie"
```

### Indicative for Direct Knowledge
```
English: "I saw he was at home"
AI: "Aš matau, kad jis būtů namie"
Natural: "Aš matau, kad jis buvo namie"
```

### Conditional for Hypotheticals
```
English: "If he was at home"
AI: "Jei jis būtů namie"
Natural: "Jei jis buvo namie"
```

## Source-Backed Analysis

### Academic References
- **Baltistica**: "Grammatical evidentiality in Lithuanian" - Björn Wiemer
- **Cambridge Core**: "Evidentiality in Lithuanian" - Claire Gronemeyer
- **De Gruyter Brill**: "The Lithuanian Participles: Their System and Functions" - Antanas Klimas

### Key Research Findings
- Lithuanian is one of few Indo-European languages with grammatical evidentiality
- Evidential mood is formed with past active participle + būti
- No direct English equivalent - English relies on context/adverbs

## Implementation Notes

This research will directly inform the `lt-naturalizer` detection engine by:
- Identifying evidential mood collapse patterns
- Detecting semantic ambiguity in reported information
- Recognizing conditional vs evidential confusion
- Providing source-based validation for pattern weights
- Creating comprehensive detection rule sets

## Validation Approach

1. Cross-reference multiple academic sources
2. Verify patterns against native speaker corpora
3. Test detection rules against actual AI-generated text samples
4. Consult with Lithuanian linguistics experts if available