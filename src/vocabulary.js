/**
 * vocabulary.js — Comprehensive AI vocabulary database.
 *
 * 500+ words and phrases organized into detection tiers based on how strongly
 * they signal AI-generated text. Sourced from:
 *   - Wikipedia:Signs of AI writing (WikiProject AI Cleanup)
 *   - Copyleaks stylistic fingerprint research (arxiv 2503.01659v1)
 *   - godofprompt.ai comprehensive AI word analysis
 *   - Real-world pattern observation across ChatGPT, Claude, Gemini, Llama
 *
 * Tiers:
 *   1 — Dead giveaways. Almost never appear in natural human writing at these frequencies.
 *   2 — Suspicious when clustered. Fine alone, damning in groups.
 *   3 — Context-dependent. Only flagged when density exceeds threshold.
 */

// ─── Tier 1: Dead Giveaways ─────────────────────────────
// Lithuanian calques and AI overused words that appear 5-20x more often in AI text than human text.

const TIER_1 = [
  "pasinerkime",
  "panagrinėkime",
  "apžvelkime",
  "atskleidžia",
  "svarbu pažymėti",
  "verta atkreipti dėmesį",
  "neabejotinai",
  "besikeičiančiame kraštovaizdyje",
  "skaitmeniniame amžiuje",
  "sparčiai tobulėjant",
  "išlaisvinti potencialą",
  "įgalina",
  "sužavėti",
  "yra daroma",
  "buvo pastebėta",
  "yra tikimasi",
  "priėmėme sprendimą",
  "vykdyti tobulinimą",
  "kraštovaizdis",
  "skaitmeninis",
  "paradigmos",
  "holistinis",
  "inovatyvus",
  "dinamiškas",
  "nepaprastas",
  "įtraukiantis",
  "vizionieriškas",
  "transformuojantis",
];

// ─── Tier 2: Suspicious in Density ──────────────────────
// Normal in isolation, but multiple occurrences signal AI authorship.

const TIER_2 = [
  "visapusiškas",
  "sistemiškas",
  "optimizuoti",
  "integruoti",
  "inovacija",
  "tvarus",
  "efektyvus",
  "išplėsti",
  "įgyvendinti",
  "skatinti",
  "fasilituoti",
  "niuansuotas",
  "proaktyvus",
];

// ─── Tier 3: Context-Dependent ──────────────────────────
// Common words that only become AI signals at high density or in
// combination with other AI patterns. Flagged when density > 3%.

const TIER_3 = [
  "puikus",
  "išskirtinis",
  "svarbus",
  "reikšmingas",
  "unikaliai",
  "efektyviai",
  "veiksmingai",
  "potencialiai",
  "atitinkamai",
  "akivaizdžiai",
];

// ─── AI Phrases (Tier 3+) ───────────────────────────────
// Multi-word phrases that strongly signal AI authorship.
// Each has a regex pattern and a severity weight.

const AI_PHRASES = [
  // Calques from English
  {
    pattern: /pasinerkime į/gi,
    tier: 1,
    fix: "pažiūrėkime",
  },
  { pattern: /panagrinėkime/gi, tier: 1, fix: "pažiūrėk" },
  { pattern: /tyrinėti/gi, tier: 1, fix: "pažvelgti" },
  { pattern: /atskleisti/gi, tier: 1, fix: "parodyti" },
  { pattern: /svarbu pažymėti/gi, tier: 1, fix: "tiek — tiesiog pasakyk" },
  { pattern: /verta atkreipti dėmesį/gi, tier: 1, fix: "tiesiog pasakyk" },
  { pattern: /neabejotinai/gi, tier: 1, fix: "tikrai" },

  // SVO tyranny patterns
  {
    pattern: /Mes turime suprasti, kad/gi,
    tier: 1,
    fix: "Turime suprasti, kad",
  },
  { pattern: /Jis mano, kad/gi, tier: 1, fix: "Mano, kad" },
  { pattern: /Ji sako, kad/gi, tier: 1, fix: "Sako, kad" },

  // Passive voice patterns
  { pattern: /yra daroma/gi, tier: 1, fix: "darosi" },
  { pattern: /buvo pastebėta/gi, tier: 1, fix: "pastebima" },
  { pattern: /yra tikimasi/gi, tier: 1, fix: "tikimasi" },

  // Nominalization patterns
  { pattern: /priėmėme sprendimą/gi, tier: 1, fix: "mes nusprendėme" },
  { pattern: /vykdyti tobulinimą/gi, tier: 1, fix: "tobulinti" },

  // Cliché phrases
  {
    pattern: /nuolat besikeičiančiame kraštovaizdyje/gi,
    tier: 1,
    fix: "dabar",
  },
  { pattern: /šiuolaikiniame skaitmeniniame amžiuje/gi, tier: 1, fix: "dabar" },
  { pattern: /išlaisvinti potencialą/gi, tier: 1, fix: "padėti geriau" },
  { pattern: /įgalinti/gi, tier: 1, fix: "padėti" },

  // ── Lithuanian: Hedging stacks ──────────────────
  { pattern: /\bgalėtų potencialiai\b/gi, tier: 1, fix: "galėtų" },
  { pattern: /\bgalbūt įmanoma\b/gi, tier: 1, fix: "galbūt" },

  // ── Lithuanian: Chatbot filler ──────────────────
  { pattern: /\bTikiuosi, kad tai padės\b/gi, tier: 1, fix: "(pašalinti)" },
  { pattern: /\bLeiskite žinoti, jei\b/gi, tier: 1, fix: "(pašalinti)" },
  { pattern: /\bAr norėtumėte, kad\b/gi, tier: 1, fix: "(pašalinti)" },
  { pattern: /\bNedvejokite\b/gi, tier: 1, fix: "(pašalinti)" },
  {
    pattern: /\bDžiaugiuosi galėdamas padėti\b/gi,
    tier: 1,
    fix: "(pašalinti)",
  },
  {
    pattern:
      /\b(?:Štai|Čia yra) (?:išsami|trumpa|greita)? ?(?:apžvalga|santrauka|sąrašas|gidas|paaiškinimas)\b/gi,
    tier: 1,
    fix: "(pašalinti — pradėkite nuo turinio)",
  },

  // ── Lithuanian: Sycophantic ─────────────────────
  { pattern: /\bPuikus klausimas\b/gi, tier: 1, fix: "(pašalinti)" },
  { pattern: /\bPuikus pastebėjimas\b/gi, tier: 1, fix: "(pašalinti)" },
  {
    pattern: /\bJūs visiškai teisus\b/gi,
    tier: 1,
    fix: "(pašalinti arba adresuoti esmę)",
  },

  // ── Lithuanian: Cutoff disclaimers ──────────────
  {
    pattern: /\bremiantis (?:mano|naujausiomis) žiniomis\b/gi,
    tier: 1,
    fix: "(pašalinti)",
  },
  {
    pattern: /\bnors (?:konkrečių )?detalių trūksta\b/gi,
    tier: 1,
    fix: "(pašalinti)",
  },

  // ── Lithuanian: Generic conclusions ─────────────
  {
    pattern: /\bateitis atrodo šviesi\b/gi,
    tier: 1,
    fix: "(baigti konkrečiu faktu)",
  },
  {
    pattern: /\blaukia įdomūs laikai\b/gi,
    tier: 1,
    fix: "(baigti konkrečiu faktu)",
  },
  {
    pattern: /\btik laikas parodys\b/gi,
    tier: 1,
    fix: "(baigti tuo, ką iš tikrųjų žinote)",
  },
  {
    pattern: /\bgalimybės yra neribotos\b/gi,
    tier: 1,
    fix: "(būkite konkretus apie galimybes)",
  },

  // ── Lithuanian: Formulaic filler ────────────────
  { pattern: /\bdėl to fakto, kad\b/gi, tier: 1, fix: "nes" },
  { pattern: /\bšiuo laiko momentu\b/gi, tier: 1, fix: "dabar" },
  { pattern: /\btuo atveju, jei\b/gi, tier: 1, fix: "jei" },
  { pattern: /\bturi galimybę\b/gi, tier: 1, fix: "gali" },
  { pattern: /\bsu tikslu\b/gi, tier: 1, fix: "kad" },
  { pattern: /\batsižvelgiant į tai, kad\b/gi, tier: 1, fix: "nes" },
  { pattern: /\bvisų pirma\b/gi, tier: 2, fix: "pirmiausia" },
  {
    pattern: /\bpaskutinis, bet ne prasčiausias\b/gi,
    tier: 2,
    fix: "galiausiai",
  },
  { pattern: /\bgali būti sakoma\b/gi, tier: 2, fix: "(tiesiog sakyti)" },
  { pattern: /\bkalbant apie\b/gi, tier: 2, fix: "dėl" },
];

// ─── Function Words ─────────────────────────────────────
// Function words make up ~0.04% of vocabulary but 50%+ of usage.
// Their distribution differs measurably between AI and human text.
// These are the Lithuanian function words tracked for stylometric analysis.

const FUNCTION_WORDS = [
  "ir",
  "o",
  "bet",
  "taip",
  "ne",
  "ar",
  "kad",
  "jei",
  "kol",
  "nes",
  "nors",
  "kai",
  "kuomet",
  "kur",
  "kurie",
  "kuris",
  "kurios",
  "kuri",
  "jo",
  "jos",
  "jų",
  "jam",
  "jai",
  "jiems",
  "joms",
  "jis",
  "ji",
  "jie",
  "jos",
  "aš",
  "tu",
  "mes",
  "jūs",
  "man",
  "tau",
  "mums",
  "jums",
  "mane",
  "tave",
  "mus",
  "jus",
  "į",
  "iš",
  "su",
  "ant",
  "po",
  "prie",
  "tarp",
  "per",
  "apie",
  "iki",
  "nuo",
  "už",
  "už",
  "be",
  "apie",
  "dėl",
  "tam",
  "tai",
  "tada",
  "tada",
  "dabar",
  "visada",
  "dažnai",
  "kartais",
  "niekada",
  "visai",
  "tik",
  "tikrai",
  "tikrai",
  "gerai",
  "blogai",
  "labai",
  "gana",
  "per",
  "pakankamai",
  "daug",
  "mažai",
  "truputį",
  "viską",
  "viskas",
  "nieko",
  "kažkas",
  "kas",
  "ką",
  "kodėl",
  "kodėl",
  "kaip",
  "kiek",
  "kur",
  "kur",
];

// ─── Exports ─────────────────────────────────────────────

module.exports = {
  TIER_1,
  TIER_2,
  TIER_3,
  AI_PHRASES,
  FUNCTION_WORDS,
};
