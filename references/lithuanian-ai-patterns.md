# The Lithuanian AI Accent: Core Patterns

This document defines the core linguistic patterns that identify AI-generated Lithuanian text. These patterns form the foundation of the `lt-naturalizer` detection engine.

## Pillar 1: Lexical Calques & Semantic Clichés (The "AI Hit List")
AI models rely on literal translations of English idioms (calques) that sound unnatural or overly poetic in Lithuanian.

- **The "Delve/Explore" Family:** *Pasinerkime į, panagrinėkime, tyrinėti, atskleisti.*
- **The "Crucial/Important" Family:** *Svarbu pažymėti, verta atkreipti dėmesį, neabejotinai.*
- **The "In today's world" Clichés:** *Nuolat besikeičiančiame kraštovaizdyje* (literal translation of landscape), *šiuolaikiniame skaitmeniniame amžiuje, sparčiai populiarėjant.*
- **Melodramatic Verbs:** *Išlaisvinti potencialą* (unleash potential), *įgalinti* (empower - heavily overused by AI), *sužavėti.*

## Pillar 2: Syntactic Englishisms (Rigidity vs. Flexibility)
Lithuanian is an inflected language with free word order dictated by "aktualioji skaida" (Functional Sentence Perspective). English is strictly SVO (Subject-Verb-Object).

- **SVO Tyranny:** AI almost exclusively uses Subject-Verb-Object, ignoring the natural Lithuanian tendency to invert order for emphasis or flow. This creates a robotic, staccato rhythm.
- **Passive Voice Overload:** English relies heavily on the passive voice in formal text. AI translates this directly into Lithuanian passive participles (*yra daroma, buvo pastebėta, yra tikimasi*), completely ignoring natural reflexive verbs (*darosi, pastebima, tikimasi*) or active voice.
- **Pronoun Overuse:** Lithuanian drops personal pronouns (*aš, tu, jis*) because the verb ending already indicates the subject. AI often includes them unnecessarily (*Mes turime suprasti, kad...* instead of *Turime suprasti, kad...*), mirroring English.

## Pillar 3: Bureaucratic Register Bleed ("Valdiška kalba" / Nominalization)
LLMs are trained on massive amounts of official documents, EU translations, and Wikipedia. When asked to write a casual blog post, they cannot escape this formal register.

- **Nominalization (Daiktavardėjimas):** AI loves to turn actions into nouns. Instead of saying *"mes nusprendėme"* (we decided), it says *"priėmėme sprendimą"* (we made a decision). Instead of *"tobulinti"*, it uses *"vykdyti tobulinimą"*.
- **Genitive Chains:** Stacking nouns in the genitive case (kilmininkas). E.g., *"Įmonės plėtros strategijos įgyvendinimo plano optimizavimas"* instead of a flowing sentence with verbs.
- **Lack of Particles (Dalelytės):** Natural Lithuanian relies heavily on particles (*juk, gi, vis dėlto, bene, turbūt*) to convey tone, nuance, and flow. AI generated text is almost entirely devoid of them, making it sound sterile.

## Core Mission
**De-Englishing the LLM:** Developing parameters for `lt-naturalizer` to restore native syntactic flexibility, reduce nominalization, and eliminate lexical calques in automated Lithuanian text generation.