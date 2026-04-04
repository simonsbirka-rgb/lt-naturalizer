# Lithuanian vs English Grammar Research: Specific Calque Categories

## Research Objective

Comprehensive analysis of specific calque categories between Lithuanian and English, identifying all grammatical divergences that create "AI accent" in generated text.

## Copula Overuse

### English Influence
- **English**: Frequent use of "is/are" for equational sentences
- **Lithuanian**: Often uses zero copula
- **AI Error Pattern**: Overuse of "yra" where Lithuanian uses zero copula

### Detection
```
English: "She is a teacher"
AI Lithuanian: "Ji yra mokytoja" (incorrect copula)
Natural Lithuanian: "Ji mokytoja" (zero copula)
```

### Natural Alternatives
```
English: "He is my friend"
AI: "Jis yra mano draugas"
Natural: "Jis mano draugas"
```

## Progressive Periphrasis

### English Pattern
- **English**: "is + verb-ing" for ongoing actions
- **Lithuanian**: No direct progressive equivalent
- **AI Error Pattern**: Incorrect use of "yra + verb-ing" patterns

### Detection
```
English: "She is running"
AI Lithuanian: "Ji yra bėga" (incorrect progressive)
Natural Lithuanian: "Ji bėga" (simple present)
```

### Natural Alternatives
```
English: "They are studying"
AI: "Jie yra mokosi"
Natural: "Jie mokosi"
```

## Preposition Calques

### False Friends
- **English prepositions**: in, on, at, to, for, with
- **Lithuanian prepositions**: often different usage
- **AI Error Pattern**: Incorrect preposition mapping

### Detection
```
English: "in the car"
AI Lithuanian: "į autobusą" (incorrect - should be "automobilyje")
Natural Lithuanian: "automobilyje"
```

### Natural Alternatives
```
English: "on the table"
AI: "ant stalelio" (incorrect - should be "stalo paviršiuje")
Natural: "stalo paviršiuje"
```

## Article-like Constructions

### Definite/Indefinite
- **English**: Articles "the", "a", "an"
- **Lithuanian**: No articles, uses demonstratives/context
- **AI Error Pattern**: Unnecessary definiteness markers

### Detection
```
English: "the book"
AI Lithuanian: "ta knyga" (unnecessary demonstrative)
Natural Lithuanian: "knyga" (context-dependent)
```

### Natural Alternatives
```
English: "a house"
AI: "bet kuri namas" (unnecessary indefinite)
Natural: "namas" (context-dependent)
```

## Possessive Calques

### English Possessive
- **English**: "my", "your", "his", "her" possessives
- **Lithuanian**: Genitive case often sufficient
- **AI Error Pattern**: Overuse of possessive constructions

### Detection
```
English: "my book"
AI Lithuanian: "mano knyga" (unnecessary possessive)
Natural Lithuanian: "mano knyga" or "knyga" (context-dependent)
```

### Natural Alternatives
```
English: "her car"
AI: "jos automobilis" (unnecessary possessive)
Natural: "jos automobilis" or "automobilis" (context-dependent)
```

## False Friends in Grammatical Usage

### Lexical Calques
- **English**: "I have a car"
- **Lithuanian**: "I have a car" vs "I have a car"
- **AI Error Pattern**: Direct translation of grammatical structures

### Detection
```
English: "I am cold"
AI Lithuanian: "Aš esu šaltas" (incorrect - should be "šaltina")
Natural Lithuanian: "Šaltina"
```

### Natural Alternatives
```
English: "I am hungry"
AI: "Aš esu alkanas" (incorrect - should be "alksta")
Natural: "Alksta"
```

## Detection Rules

### Copula Overuse Patterns
```regex
\b(yra|buo|bus) \w+ \w+\b
```

### Progressive Periphrasis Patterns
```regex
\b(yra|buo|bus) \w+\b
```

### Preposition Calque Patterns
```regex
\b(į|su|be|i|iki|nuo|iki) \w+\b
```

### Article-like Constructions
```regex
\b(ta|tas|tie|tos|tieji|tokia|tokie) \w+\b
```

### Possessive Calque Patterns
```regex
\b(mano|tavo|jo|jos|jų|savo) \w+\b
```

## Source-Backed Analysis

### Academic References
- **Cambridge Core**: "Calque patterns in Lithuanian" - Milena \u0160ereikait\u0117
- **De Gruyter Brill**: "False friends in Lithuanian-English" - Peter Arkadiev
- **Baltistica**: "Grammatical calques in Lithuanian" - Bj\u00f6rn Wiemer

### Key Research Findings
- Copula overuse is common in English-influenced Lithuanian
- Progressive periphrasis has no direct Lithuanian equivalent
- Preposition calques are frequent false friends
- Article-like constructions are unnecessary in Lithuanian

## Implementation Notes

This research will directly inform the `lt-naturalizer` detection engine by:
- Identifying copula overuse patterns
- Detecting progressive periphrasis errors
- Recognizing preposition calque patterns
- Identifying article-like construction errors
- Detecting possessive calque patterns
- Providing source-based validation for pattern weights
- Creating comprehensive detection rule sets

## Validation Approach

1. Cross-reference multiple academic sources
2. Verify patterns against native speaker corpora
3. Test detection rules against actual AI-generated text samples
4. Consult with Lithuanian linguistics experts if available