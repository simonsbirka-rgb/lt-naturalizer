# Lithuanian vs English Grammar Research: Passive Constructions

## Research Objective

Comprehensive analysis of Lithuanian vs English passive voice systems, identifying all grammatical divergences that create "AI accent" in generated text.

## Lithuanian Passive System

### Two Types of Passive

#### 1. Standard Passive
- **Formation**: passive participle + būti
- **Example**: "Knyga buvo parašyta" (The book was written)
- **Usage**: Limited, Lithuanian prefers active constructions

#### 2. Reflexive Passive
- **Formation**: reflexive verbs with si/siūbu
- **Example**: "Šis darbas atliekamas" (This work is done)
- **Usage**: Common alternative to standard passive

### Neuter Passive Participles
- **Formation**: special neuter forms
- **Example**: "Padaryta klaidų" (Mistakes were made)
- **Usage**: Impersonal constructions, no agent specified

### Key Characteristics
- **Limited passive use**: Lithuanian prefers active voice
- **Reflexive alternatives**: Common substitution for passive
- **Neuter forms**: Unique impersonal constructions

## English vs Lithuanian Divergence

### Passive Overuse
- **English**: Frequent passive voice usage
- **Lithuanian**: Prefers active constructions
- **AI Error Pattern**: Overuse of English-style passive constructions

### Reflexive Alternatives
- **English**: No reflexive passive equivalent
- **Lithuanian**: Reflexive constructions as passive alternatives
- **AI Error Pattern**: Failure to use Lithuanian reflexive passive forms

### Neuter Forms
- **English**: No neuter passive equivalent
- **Lithuanian**: Unique impersonal neuter passive participles
- **AI Error Pattern**: Missing impersonal constructions

## AI Translation Errors

### Standard Passive Overuse
```
English: "The book was written by the author"
AI Lithuanian: "Knyga buvo parašyta autoriaus" (incorrect passive)
Natural Lithuanian: "Autorius parašė knygą" (active construction)
```

### Missing Reflexive Alternatives
```
English: "Mistakes were made"
AI Lithuanian: "Klaidos buvo padarytos" (incorrect passive)
Natural Lithuanian: "Padaryta klaidų" (neuter passive) or "Kas nors padarė klaidas" (reflexive)
```

### Incorrect Agent Construction
```
English: "The window was broken by the wind"
AI Lithuanian: "Langas buvo sulaužytas vėjo" (incorrect agent form)
Natural Lithuanian: "Vėjas sulaužė langą" (active) or "Langas sulaužytas" (agentless)
```

## Detection Rules

### Standard Passive Patterns
```regex
\b(yra|buo|bus) \w+as\b
\b(yra|buo|bus) \w+os\b
\b(yra|buo|bus) \w+us\b
```

### Reflexive Passive Patterns
```regex
\b(si|su) \w+si\b
```

### Neuter Passive Patterns
```regex
\b(yra|buo|bus) \w+ta\b
```

### Agent Construction Errors
```regex
\b(yra|buo|bus) \w+(as|os|us) \w+\b
```

## Natural Alternatives

### Active Voice Preference
```
English: "The report was completed"
AI: "Ataskaita buvo užbaigta"
Natural: "Atliko ataskaitą" or "Ataskaita užbaigta"
```

### Reflexive Passive
```
English: "The work is being done"
AI: "Darbas yra atliekamas"
Natural: "Darbas atliekamas" or "Darbas vykdomas"
```

### Neuter Impersonal
```
English: "Mistakes were made"
AI: "Klaidos buvo padarytos"
Natural: "Padaryta klaidų" or "Kas nors padarė klaidas"
```

## Source-Backed Analysis

### Academic References
- **Lituanus.org**: "The Two Kinds of Passive Voice in Lithuanian" - Antanas Klimas
- **De Gruyter Brill**: "The Lithuanian Participles: Their System and Functions" - Antanas Klimas
- **Cambridge Core**: "Case and word order in Lithuanian" - Milena Šereikaitė

### Key Research Findings
- Lithuanian has two distinct passive systems vs English single passive system
- Reflexive passive is more common in Lithuanian than standard passive
- Neuter passive participles are unique to Lithuanian for impersonal meaning

## Implementation Notes

This research will directly inform the `lt-naturalizer` detection engine by:
- Identifying passive overuse patterns
- Detecting missing reflexive alternatives
- Recognizing neuter impersonal construction errors
- Providing source-based validation for pattern weights
- Creating comprehensive detection rule sets

## Validation Approach

1. Cross-reference multiple academic sources
2. Verify patterns against native speaker corpora
3. Test detection rules against actual AI-generated text samples
4. Consult with Lithuanian linguistics experts if available