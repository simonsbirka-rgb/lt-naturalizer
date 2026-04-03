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
  'pasinerkime į',
  'panagrinėkime',
  'tyrinėti',
  'atskleisti',
  'svarbu pažymėti',
  'verta atkreipti dėmesį',
  'neabejotinai',
  'nuolat besikeičiančiame kraštovaizdyje',
  'šiuolaikiniame skaitmeniniame amžiuje',
  'sparčiai populiarėjant',
  'išlaisvinti potencialą',
  'įgalinti',
  'sužavėti',
  'yra daroma',
  'buvo pastebėta',
  'yra tikimasi',
  'priėmėme sprendimą',
  'vykdyti tobulinimą',
  'įmonės plėtros strategijos įgyvendinimo plano optimizavimas',
];

// ─── Tier 2: Suspicious in Density ──────────────────────
// Normal in isolation, but multiple occurrences signal AI authorship.

const TIER_2 = [
  'besikeičiančiame',
  'kraštovaizdyje',
  'skaitmeniniame',
  'amžiuje',
  'populiarėjant',
  'potencialą',
  'įgalinti',
  'sprendimą',
  'tobulinimą',
  'strategijos',
  'įgyvendinimo',
  'plėtros',
  'optimizavimas',
  'darbą',
  'veiksmą',
  'veiklos',
  'procesą',
  'veiksmą',
];

// ─── Tier 3: Context-Dependent ──────────────────────────
// Common words that only become AI signals at high density or in
// combination with other AI patterns. Flagged when density > 3%.

const TIER_3 = [
  'gerai',
  'geriau',
  'geriausias',
  'puikus',
  'puikiai',
  'puikus',
  'išskirtinis',
  'išskirtinė',
  'svarbus',
  'svarbi',
  'svarbu',
  'reikšmingas',
  'reikšminga',
  'reikšmingai',
  'geras',
  'gera',
  'gerai',
  'labai',
  'tikrai',
  'tikrai',
  'tikrai',
];

// ─── AI Phrases (Tier 3+) ───────────────────────────────
// Multi-word phrases that strongly signal AI authorship.
// Each has a regex pattern and a severity weight.

const AI_PHRASES = [
  // Calques from English
  {
    pattern: /pasinerkime į/gi,
    tier: 1,
    fix: 'pažiūrėkime',
  },
  { pattern: /panagrinėkime/gi, tier: 1, fix: 'pažiūrėk' },
  { pattern: /tyrinėti/gi, tier: 1, fix: 'pažvelgti' },
  { pattern: /atskleisti/gi, tier: 1, fix: 'parodyti' },
  { pattern: /svarbu pažymėti/gi, tier: 1, fix: 'tiek — tiesiog pasakyk' },
  { pattern: /verta atkreipti dėmesį/gi, tier: 1, fix: 'tiesiog pasakyk' },
  { pattern: /neabejotinai/gi, tier: 1, fix: 'tikrai' },
  
  // SVO tyranny patterns
  { pattern: /Mes turime suprasti, kad/gi, tier: 1, fix: 'Turime suprasti, kad' },
  { pattern: /Jis mano, kad/gi, tier: 1, fix: 'Mano, kad' },
  { pattern: /Ji sako, kad/gi, tier: 1, fix: 'Sako, kad' },
  
  // Passive voice patterns
  { pattern: /yra daroma/gi, tier: 1, fix: 'darosi' },
  { pattern: /buvo pastebėta/gi, tier: 1, fix: 'pastebima' },
  { pattern: /yra tikimasi/gi, tier: 1, fix: 'tikimasi' },
  
  // Nominalization patterns
  { pattern: /priėmėme sprendimą/gi, tier: 1, fix: 'mes nusprendėme' },
  { pattern: /vykdyti tobulinimą/gi, tier: 1, fix: 'tobulinti' },
  
  // Cliché phrases
  { pattern: /nuolat besikeičiančiame kraštovaizdyje/gi, tier: 1, fix: 'dabar' },
  { pattern: /šiuolaikiniame skaitmeniniame amžiuje/gi, tier: 1, fix: 'dabar' },
  { pattern: /išlaisvinti potencialą/gi, tier: 1, fix: 'padėti geriau' },
  { pattern: /įgalinti/gi, tier: 1, fix: 'padėti' },

  // ── Language-agnostic: Hedging stacks ──────────────────
  { pattern: /\bcould potentially\b/gi, tier: 1, fix: 'could / might' },
  { pattern: /\bmight possibly\b/gi, tier: 1, fix: 'might' },
  { pattern: /\bcould possibly\b/gi, tier: 1, fix: 'could' },
  { pattern: /\bperhaps potentially\b/gi, tier: 1, fix: 'perhaps / maybe' },
  { pattern: /\bmay potentially\b/gi, tier: 1, fix: 'may' },
  { pattern: /\bcould conceivably\b/gi, tier: 1, fix: 'could' },

  // ── Language-agnostic: Chatbot filler ──────────────────
  { pattern: /\bI hope this helps\b/gi, tier: 1, fix: '(remove)' },
  { pattern: /\blet me know if (you|there)\b/gi, tier: 1, fix: '(remove)' },
  { pattern: /\bwould you like me to\b/gi, tier: 1, fix: '(remove)' },
  { pattern: /\bfeel free to\b/gi, tier: 1, fix: '(remove)' },
  { pattern: /\bdon'?t hesitate to\b/gi, tier: 1, fix: '(remove)' },
  { pattern: /\bhappy to help\b/gi, tier: 1, fix: '(remove)' },
  {
    pattern:
      /\bhere is (a |an |the )?(comprehensive |brief |quick )?(overview|summary|breakdown|list|guide|explanation|look)\b/gi,
    tier: 1,
    fix: '(remove — start with the content)',
  },
  { pattern: /\bI'?d be happy to\b/gi, tier: 1, fix: '(remove)' },
  { pattern: /\bis there anything else\b/gi, tier: 1, fix: '(remove)' },

  // ── Language-agnostic: Sycophantic ─────────────────────
  { pattern: /\bgreat question\b/gi, tier: 1, fix: '(remove)' },
  { pattern: /\bexcellent (question|point|observation)\b/gi, tier: 1, fix: '(remove)' },
  {
    pattern:
      /\bthat'?s a (great|excellent|wonderful|fantastic|good|insightful|thoughtful) (question|point|observation)\b/gi,
    tier: 1,
    fix: '(remove)',
  },
  { pattern: /\byou'?re absolutely right\b/gi, tier: 1, fix: '(remove or address the substance)' },
  {
    pattern: /\byou raise a (great|good|excellent|valid|important) point\b/gi,
    tier: 1,
    fix: '(remove or address the substance)',
  },

  // ── Language-agnostic: Cutoff disclaimers ──────────────
  {
    pattern: /\bas of (my|this) (last|latest|most recent) (training|update|knowledge)\b/gi,
    tier: 1,
    fix: '(remove)',
  },
  {
    pattern: /\bwhile (specific )?details are (limited|scarce|not available)\b/gi,
    tier: 1,
    fix: '(remove)',
  },
  {
    pattern: /\bbased on (available|my|current) (information|knowledge|understanding|data)\b/gi,
    tier: 1,
    fix: '(remove)',
  },
  { pattern: /\bup to my (last )?training\b/gi, tier: 1, fix: '(remove)' },

  // ── Language-agnostic: Generic conclusions ─────────────
  {
    pattern: /\bthe future (looks|is|remains) bright\b/gi,
    tier: 1,
    fix: '(end with a specific fact or plan)',
  },
  {
    pattern: /\bexciting times (lie|lay|are) ahead\b/gi,
    tier: 1,
    fix: '(end with a specific fact or plan)',
  },
  {
    pattern: /\bcontinue (this|their|our|the) journey\b/gi,
    tier: 1,
    fix: '(be specific about what happens next)',
  },
  {
    pattern: /\bjourney toward(s)? (excellence|success|greatness)\b/gi,
    tier: 1,
    fix: '(be specific)',
  },
  { pattern: /\bstep in the right direction\b/gi, tier: 1, fix: '(be specific about the outcome)' },
  { pattern: /\bonly time will tell\b/gi, tier: 1, fix: '(end with what you actually know)' },
  {
    pattern: /\bthe possibilities are (endless|limitless|infinite)\b/gi,
    tier: 1,
    fix: "(be specific about what's possible)",
  },
  {
    pattern: /\bpoised for (growth|success|greatness|expansion)\b/gi,
    tier: 1,
    fix: '(cite evidence or remove)',
  },
  { pattern: /\bwatch this space\b/gi, tier: 2, fix: '(end with something concrete)' },
  { pattern: /\bstay tuned\b/gi, tier: 2, fix: '(end with something concrete)' },
  { pattern: /\bremains to be seen\b/gi, tier: 2, fix: '(state what you do know)' },

  // ── Language-agnostic: Formulaic filler ────────────────
  { pattern: /\bin order to\b/gi, tier: 2, fix: 'to' },
  { pattern: /\bdue to the fact that\b/gi, tier: 1, fix: 'because' },
  { pattern: /\bat this point in time\b/gi, tier: 1, fix: 'now' },
  { pattern: /\bin the event that\b/gi, tier: 1, fix: 'if' },
  { pattern: /\bhas the ability to\b/gi, tier: 1, fix: 'can' },
  { pattern: /\bfor the purpose of\b/gi, tier: 1, fix: 'to / for' },
  { pattern: /\bin light of the fact that\b/gi, tier: 1, fix: 'because / since' },
  { pattern: /\bfirst and foremost\b/gi, tier: 2, fix: 'first' },
  { pattern: /\blast but not least\b/gi, tier: 2, fix: 'finally' },
  { pattern: /\bat the end of the day\b/gi, tier: 2, fix: '(remove or be specific)' },
  { pattern: /\bwhen it comes to\b/gi, tier: 2, fix: 'for / regarding' },
  { pattern: /\bthe fact of the matter is\b/gi, tier: 1, fix: '(remove — just state it)' },
  { pattern: /\bin terms of\b/gi, tier: 3, fix: 'for / about / regarding' },
  { pattern: /\bat its core\b/gi, tier: 2, fix: '(remove or be specific)' },
  {
    pattern: /\bit goes without saying\b/gi,
    tier: 2,
    fix: "(if it goes without saying, don't say it)",
  },
  { pattern: /\bneedless to say\b/gi, tier: 2, fix: "(if needless to say, don't say it)" },
];

// ─── Function Words ─────────────────────────────────────
// Function words make up ~0.04% of vocabulary but 50%+ of usage.
// Their distribution differs measurably between AI and human text.
// These are the Lithuanian function words tracked for stylometric analysis.

const FUNCTION_WORDS = [
  'ir',
  'o',
  'bet',
  'taip',
  'ne',
  'ar',
  'kad',
  'jei',
  'kol',
  'nes',
  'nors',
  'kai',
  'kuomet',
  'kur',
  'kurie',
  'kuris',
  'kurios',
  'kuri',
  'jo',
  'jos',
  'jų',
  'jam',
  'jai',
  'jiems',
  'joms',
  'jis',
  'ji',
  'jie',
  'jos',
  'aš',
  'tu',
  'mes',
  'jūs',
  'man',
  'tau',
  'mums',
  'jums',
  'mane',
  'tave',
  'mus',
  'jus',
  'į',
  'iš',
  'su',
  'ant',
  'po',
  'prie',
  'tarp',
  'per',
  'apie',
  'iki',
  'nuo',
  'už',
  'už',
  'be',
  'apie',
  'dėl',
  'tam',
  'tai',
  'tada',
  'tada',
  'dabar',
  'visada',
  'dažnai',
  'kartais',
  'niekada',
  'visai',
  'tik',
  'tikrai',
  'tikrai',
  'gerai',
  'blogai',
  'labai',
  'gana',
  'per',
  'pakankamai',
  'daug',
  'mažai',
  'truputį',
  'viską',
  'viskas',
  'nieko',
  'kažkas',
  'kas',
  'ką',
  'kodėl',
  'kodėl',
  'kaip',
  'kiek',
  'kur',
  'kur',
];

// ─── Exports ─────────────────────────────────────────────

module.exports = {
  TIER_1,
  TIER_2,
  TIER_3,
  AI_PHRASES,
  FUNCTION_WORDS,
};
