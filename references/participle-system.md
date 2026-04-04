# Lithuanian vs English Grammar Research: Participle System

## Research Objective

Comprehensive analysis of Lithuanian vs English participle systems, identifying all grammatical divergences that create "AI accent" in generated text.

## Lithuanian Participle System

### 4 Active Participles

#### 1. Present Active Participle
- **Formation**: 3rd person + -�s, -anti
- **Example**: dirba → dirb�s, dirbanti
- **Function**: Current action, ongoing

#### 2. Past Active Participle
- **Formation**: 3rd person past + -�s, -usi
- **Example**: dirbo → dirb�s, dirbusi
- **Function**: Completed action, result

#### 3. Future Active Participle
- **Formation**: 2nd person future + -�s, -anti
- **Example**: dirbsi → dirbsi�s, dirbsianti
- **Function**: Future action, intention

#### 4. Adverbial Participle
- **Formation**: special forms in -damas/-dama
- **Example**: dirbti → dirbdamas
- **Function**: Concurrent action, subordinate clause

### 2 Passive Participles

#### 1. Present Passive Participle
- **Formation**: infinitive + -mas, -ma
- **Example**: dirbti → dirbamas, dirbam�
- **Function**: Current passive action

#### 2. Past Passive Participle
- **Formation**: infinitive + -tas, -ta
- **Example**: dirbti → dirbtas, dirbt�
- **Function**: Completed passive action

### Neuter Participles
- **Formation**: special neuter forms
- **Example**: girti → giriamas, girtas
- **Function**: Impersonal constructions

### Key Characteristics
- **13 total participles**: 4 active + 2 passive + neuter + adverbial
- **Participial clauses**: Compact expression of complex ideas
- **Declension**: Most participles decline like adjectives

## English vs Lithuanian Divergence

### Participial Richness
- **English**: 2 participles (present/past)
- **Lithuanian**: 13 participles with various functions
- **AI Error Pattern**: Reduction of complex participial constructions

### Clause Expansion
- **English**: Prefers relative clauses
- **Lithuanian**: Uses participial phrases for compactness
- **AI Error Pattern**: Unnecessary expansion of compact Lithuanian expressions

### Participial Functions
- **English**: Limited participial functions
- **Lithuanian**: Participials as subjects, objects, predicates
- **AI Error Pattern**: Failure to recognize participial functions

## AI Translation Errors

### Participial Simplification
```
English: "Having finished his work, he went home"
AI Lithuanian: "Baig�s darb�, jis nuojo namo" (correct participial)
Natural Lithuanian: "Baig�s darb�, jis nuojo namo" (correct)
```

### Clause Expansion
```
English: "The man who was reading the newspaper"
AI Lithuanian: "�mogus, kuris skait� laikra��t�" (relative clause)
Natural Lithuanian: "Laikra��t� skaitantis �mogus" (participial phrase)
```

### Participial Function Errors
```
English: "The working man"
AI Lithuanian: "Dirban�is �mogus" (incorrect participle form)
Natural Lithuanian: "Dirbantis �mogus" (correct present participle)
```

## Detection Rules

### Active Participle Patterns
```regex
\b(\w+ąs|\w+usi|\w+ęs|\w+ę|\w+ant|\w+us)\b
```

### Passive Participle Patterns
```regex
\b(\w+amas|\w+oma|\w+ytas|\w+yta|\w+simas|\w+sima)\b
```

### Adverbial Participle Patterns
```regex
\b(\w+damas|\w+dama|\w+dami|\w+damos)\b
```

### Participial Clause Expansion
```regex
\b(\w+, kuris|\w+, kuri|\w+, kurių|\w+, kurioms)\b
```

## Natural Alternatives

### Participial Phrases for Compactness
```
English: "The man who was reading the newspaper"
AI: "�mogus, kuris skait� laikra��t�"
Natural: "Laikra��t� skaitantis �mogus"
```

### Participial Subjects
```
English: "The working man"
AI: "Dirban�is �mogus"
Natural: "Dirbantis �mogus"
```

### Participial Objects
```
English: "I saw the man reading the book"
AI: "A\u0161 pama\u010diau \u017emog\u0173, kuris skait\u0117 knyg\u0105"
Natural: "A\u0161 pama\u010diau knyg\u0105 skaitant\u012f \u017emog\u012f"
```

## Source-Backed Analysis

### Academic References
- **Lituanus.org**: "The Lithuanian Participles: Their System and Functions" - Antanas Klimas
- **De Gruyter Brill**: "The Lithuanian Participles: Their System and Functions" - Antanas Klimas
- **Cambridge Core**: "Participle usage in Lithuanian" - Milena \u0160ereikait\u0117

### Key Research Findings
- Lithuanian has 13 participles vs 2-3 in English
- Participial clauses are fundamental to Lithuanian expression
- Participials can function as any part of sentence

## Implementation Notes

This research will directly inform the `lt-naturalizer` detection engine by:
- Identifying participial simplification patterns
- Detecting clause expansion errors
- Recognizing participial function failures
- Providing source-based validation for pattern weights
- Creating comprehensive detection rule sets

## Validation Approach

1. Cross-reference multiple academic sources
2. Verify patterns against native speaker corpora
3. Test detection rules against actual AI-generated text samples
4. Consult with Lithuanian linguistics experts if available