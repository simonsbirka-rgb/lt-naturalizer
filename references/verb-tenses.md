# Lithuanian vs English Grammar Research: Verb Tense Systems

## Research Objective

Comprehensive analysis of Lithuanian vs English verb tense systems, identifying all grammatical divergences that create "AI accent" in generated text.

## Lithuanian System

### Main Tenses
- **Present (einamasis laikas)**: dirbu (I work)
- **Past (būtasis laikas)**: dirbau (I worked)
- **Future (būsimasis laikas)**: dirbsiu (I will work)
- **Inchoative (prasidėtinė būtimoji forma)**: pradėjau dirbti (I began to work)

### Key Characteristics
- **No progressive tenses**: Lithuanian lacks continuous/progressive forms like English "is running"
- **Compound tenses**: Formed with būti + participle (e.g., "buvo skaitęs" - had read)
- **Aspectual pairs**: Perfective vs imperfective distinction is morphological, not tense-based

## English vs Lithuanian Divergence

### Progressive Mismatch
- **English**: is running, was running, will be running
- **Lithuanian**: NO direct equivalent - uses simple present/past/future
- **AI Error Pattern**: Incorrect application of English progressive patterns

### Perfect Form Confusion
- **English**: have run, had run, will have run
- **Lithuanian**: Compound forms with būti + participle, but semantic mapping imperfect
- **AI Error Pattern**: Incorrect mapping of English perfect tenses to Lithuanian compound forms

### Inchoative Uniqueness
- **English**: No dedicated inchoative tense
- **Lithuanian**: Prasidėtinė būtimoji forma for beginning actions
- **AI Error Pattern**: Failure to recognize and use inchoative forms

## AI Translation Errors

### Progressive Overuse
```
English: "She is running every morning"
AI Lithuanian: "Ji yra bėga kiekvieną rytą" (incorrect progressive)
Natural Lithuanian: "Ji bėga kiekvieną rytą" (simple present)
```

### Perfect Form Confusion
```
English: "He has been studying for hours"
AI Lithuanian: "Jis buvo mokosi valandų" (incorrect perfect progressive)
Natural Lithuanian: "Jis mokosi jau valandas" (present perfective)
```

### Inchoative Misuse
```
English: "She started working"
AI Lithuanian: "Ji pradėjo darbuotis" (incorrect inchoative)
Natural Lithuanian: "Ji pradėjo dirbti" (correct inchoative form)
```

## Detection Rules

### Progressive Tense Patterns
```regex
\b(is|am|are|was|were|will be|would be) \w+ing\b
```

### Perfect Tense Patterns
```regex
\b(have|has|had) \w+ed\b
\b(will have|would have) \w+ed\b
```

### Inchoative Patterns
```regex
\b(pradėjo|prasidėjo|pradėjo būti) \w+\b
```

## Natural Alternatives

### Simple Present for Habitual Actions
```
English: "She runs every morning"
AI: "Ji yra bėga kiekvieną rytą"
Natural: "Ji bėga kiekvieną rytą"
```

### Simple Past for Completed Actions
```
English: "He read the book"
AI: "Jis buvo skaitęs knygą"
Natural: "Jis perskaito knygą"
```

### Compound Tenses for Perfect Meaning
```
English: "I have finished"
AI: "Aš baigiau"
Natural: "Aš esu baigęs"
```

## Source-Backed Analysis

### Academic References
- **De Gruyter Brill**: "The Tense System of Lithuanian" - Nijolė Sližienė
- **Cambridge Core**: "Case and word order in Lithuanian" - Milena Šereikaitė
- **Baltistica**: "Grammatical evidentiality in Lithuanian" - Björn Wiemer

### Key Research Findings
- Lithuanian has only 4 main tenses vs English 12+ tense-aspect combinations
- Progressive tenses are a Germanic language feature absent in Lithuanian
- Aspectual distinction (perfective/imperfective) is morphological, not tense-based

## Implementation Notes

This research will directly inform the `lt-naturalizer` detection engine by:
- Identifying progressive tense overuse patterns
- Detecting incorrect perfect form mappings
- Recognizing inchoative form misuse
- Providing source-based validation for pattern weights
- Creating comprehensive detection rule sets

## Validation Approach

1. Cross-reference multiple academic sources
2. Verify patterns against native speaker corpora
3. Test detection rules against actual AI-generated text samples
4. Consult with Lithuanian linguistics experts if available