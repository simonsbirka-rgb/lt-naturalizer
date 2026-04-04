/**
 * patterns.js — AI writing pattern detection engine.
 *
 * 24 pattern detectors organized into 5 categories, with a registry
 * that supports dynamic add/remove and custom word lists.
 *
 * Architecture:
 *   - Each pattern is an object with id, name, category, description,
 *     weight (1-5), and a detect(text) function
 *   - detect() returns [{ match, index, line, column, suggestion, confidence }]
 *   - The registry holds all patterns and provides query methods
 *   - Vocabulary is sourced from vocabulary.js (500+ words/phrases)
 */

const { TIER_1, TIER_2, TIER_3, AI_PHRASES } = require('./vocabulary');
// Stats imported for cross-module analysis when needed
// const { tokenize } = require('./stats');

// ─── Helpers ─────────────────────────────────────────────

/**
 * Find all regex matches with line numbers and columns.
 * Returns [{ match, index, line, column, suggestion, confidence }]
 */
function findMatches(text, regex, suggestion, confidence = 'high') {
  const results = [];
  const lines = text.split('\n');
  let offset = 0;

  for (let lineNum = 0; lineNum < lines.length; lineNum++) {
    const line = lines[lineNum];
    const lineRegex = new RegExp(
      regex.source,
      regex.flags.includes('g') ? regex.flags : `${regex.flags}g`,
    );
    let m;
    while ((m = lineRegex.exec(line)) !== null) {
      results.push({
        match: m[0],
        index: offset + m.index,
        line: lineNum + 1,
        column: m.index + 1,
        suggestion: typeof suggestion === 'function' ? suggestion(m[0]) : suggestion,
        confidence,
      });
    }
    offset += line.length + 1;
  }
  return results;
}

/** Count regex occurrences. */
function countMatches(text, regex) {
  const m = text.match(regex);
  return m ? m.length : 0;
}

/** Word count. */
function wordCount(text) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

// ─── Vocabulary Detection Helpers ────────────────────────

/**
 * Build a case-insensitive word-boundary regex for a word.
 * Escapes special regex chars in the word.
 */
function wordRegex(word) {
  const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  // For multi-word phrases, don't use word boundaries on internal spaces
  if (word.includes(' ')) {
    return new RegExp(`\\b${escaped}\\b`, 'gi');
  }
  return new RegExp(`\\b${escaped}\\b`, 'gi');
}

/**
 * Scan text for words from a tier list. Returns matches with word-specific suggestions.
 */
function scanWordList(text, wordList, suggestionPrefix, confidence = 'high') {
  const results = [];
  for (const word of wordList) {
    const regex = wordRegex(word);
    const matches = findMatches(
      text,
      regex,
      `${suggestionPrefix}: "${word}". Use a simpler, more specific alternative.`,
      confidence,
    );
    results.push(...matches);
  }
  return results;
}

/**
 * Scan text for AI phrases. Returns matches with phrase-specific fixes.
 */
function scanPhrases(text, phrases, tierFilter = null) {
  const results = [];
  for (const { pattern, tier, fix } of phrases) {
    if (tierFilter !== null && tier !== tierFilter) continue;
    const matches = findMatches(
      text,
      pattern,
      fix.startsWith('(') ? fix : `Replace with: ${fix}`,
      tier === 1 ? 'high' : tier === 2 ? 'medium' : 'low',
    );
    results.push(...matches);
  }
  return results;
}

// ─── Pattern Definitions ─────────────────────────────────

const patterns = [
  // ── LITHUANIAN AI PATTERNS (1-6) ──────────────────────────────

  {
    id: 1,
    name: 'Lexical calques',
    category: 'content',
    description:
      'Literal translations of English idioms that sound unnatural in Lithuanian.',
    weight: 5,
    detect(text) {
      const results = [];
      
      // Delve/Explore family
      results.push(...findMatches(text, /pasinerkime į/gi, 'Replace with: pažiūrėkime', 'high'));
      results.push(...findMatches(text, /panagrinėkime/gi, 'Replace with: pažiūrėk', 'high'));
      results.push(...findMatches(text, /tyrinėti/gi, 'Replace with: pažvelgti', 'high'));
      results.push(...findMatches(text, /atskleisti/gi, 'Replace with: parodyti', 'high'));
      
      // Crucial/Important family
      results.push(...findMatches(text, /svarbu pažymėti/gi, 'Remove — just state the fact', 'high'));
      results.push(...findMatches(text, /verta atkreipti dėmesį/gi, 'Remove — just state the fact', 'high'));
      results.push(...findMatches(text, /neabejotinai/gi, 'Replace with: tikrai', 'high'));
      
      // "In today's world" clichés
      results.push(...findMatches(text, /nuolat besikeičiančiame kraštovaizdyje/gi, 'Replace with: dabar', 'high'));
      results.push(...findMatches(text, /šiuolaikiniame skaitmeniniame amžiuje/gi, 'Replace with: dabar', 'high'));
      
      // Melodramatic verbs
      results.push(...findMatches(text, /išlaisvinti potencialą/gi, 'Replace with: padėti geriau', 'high'));
      results.push(...findMatches(text, /įgalinti/gi, 'Replace with: padėti', 'high'));
      
      return results;
    },
  },

  {
    id: 2,
    name: 'SVO Tyranny',
    category: 'language',
    description:
      'Strict Subject-Verb-Object word order ignoring natural Lithuanian word order flexibility.',
    weight: 4,
    detect(text) {
      const results = [];
      
      // Unnecessary pronoun usage (Lithuanian drops pronouns since verb endings indicate subject)
      results.push(...findMatches(text, /Mes turime suprasti, kad/gi, 'Remove "Mes" — use: Turime suprasti, kad', 'high'));
      results.push(...findMatches(text, /Jis mano, kad/gi, 'Remove "Jis" — use: Mano, kad', 'high'));
      results.push(...findMatches(text, /Ji sako, kad/gi, 'Remove "Ji" — use: Sako, kad', 'high'));
      
      return results;
    },
  },

  {
    id: 3,
    name: 'Passive voice overload',
    category: 'language',
    description:
      'AI translates English passive voice directly into Lithuanian passive participles instead of using natural reflexive verbs or active voice.',
    weight: 4,
    detect(text) {
      const results = [];
      
      results.push(...findMatches(text, /yra daroma/gi, 'Replace with: darosi', 'high'));
      results.push(...findMatches(text, /buvo pastebėta/gi, 'Replace with: pastebima', 'high'));
      results.push(...findMatches(text, /yra tikimasi/gi, 'Replace with: tikimasi', 'high'));
      
      return results;
    },
  },

  {
    id: 4,
    name: 'Nominalization (Daiktavardėjimas)',
    category: 'language',
    description:
      'AI turns actions into nouns. Instead of verbs, it uses noun phrases like "priėmėme sprendimą" instead of "mes nusprendėme".',
    weight: 4,
    detect(text) {
      const results = [];
      
      results.push(...findMatches(text, /priėmėme sprendimą/gi, 'Replace with: mes nusprendėme', 'high'));
      results.push(...findMatches(text, /vykdyti tobulinimą/gi, 'Replace with: tobulinti', 'high'));
      
      return results;
    },
  },

  {
    id: 5,
    name: 'Genitive chains',
    category: 'language',
    description:
      'Stacking nouns in the genitive case (kilmininkas) creating bureaucratic, unnatural sentences.',
    weight: 3,
    detect(text) {
      // Match 3+ consecutive words ending in common Lithuanian genitive suffixes
      // Extended suffix set: -o, -io, -ių, -os, -umo, -ymo, -stės, -ijos, -tybės, -tavimo
      const genitiveChain = /(?:\S+(?:o|io|i\u0173|os|umo|ymo|st\u0117s|ijos|tyb\u0117s|tavimo|es)\s+){2,}\S+(?:o|io|i\u0173|os|umo|ymo|st\u0117s|ijos|tyb\u0117s|tavimo|es)\b/gi;
      return findMatches(text, genitiveChain, 'Rewrite using verbs instead of stacked genitive nouns (kilminink\u0173 virtin\u0117)', 'high');
    },
  },

  {
    id: 6,
    name: 'Lack of particles (Dalelytės)',
    category: 'style',
    description:
      'AI generated text is almost entirely devoid of natural Lithuanian particles like juk, gi, vis dėlto, bene, turbūt.',
    weight: 3,
    detect(text) {
      const particles = ['juk', 'gi', 'vis dėlto', 'bene', 'turbūt', 'gal', 'na'];
      const particleCount = particles.reduce((count, p) => {
        const regex = new RegExp(`(?:^|\\s)${p}(?:\\s|$|[.,;!?:])`, 'gi');
        return count + countMatches(text, regex);
      }, 0);
      
      const words = wordCount(text);
      if (words > 50 && particleCount === 0) {
        return [{
          match: 'No particles found',
          index: 0,
          line: 1,
          column: 1,
          suggestion: 'Add natural Lithuanian particles (juk, gi, turbūt, etc.) to make text sound more human',
          confidence: 'medium',
        }];
      }
      return [];
    },
  },

  // ── LANGUAGE PATTERNS (7-12) ────────────────────────────

  {
    id: 7,
    name: 'AI vocabulary',
    category: 'language',
    description:
      'Words and phrases that appear far more frequently in AI-generated Lithuanian text.',
    weight: 5,
    detect(text) {
      const results = [];
      const words = wordCount(text);

      // Tier 1: always flag
      results.push(...scanWordList(text, TIER_1, 'Tier 1 AI word', 'high'));

      // Tier 2: flag if 2+ tier-2 words appear
      const tier2Matches = scanWordList(text, TIER_2, 'Tier 2 AI word', 'medium');
      if (tier2Matches.length >= 2) {
        results.push(...tier2Matches);
      }

      // Tier 3: flag only at high density (>3% of words are tier-3)
      if (words > 50) {
        const tier3Count = TIER_3.reduce((count, word) => {
          const regex = wordRegex(word);
          return count + countMatches(text, regex);
        }, 0);
        const density = tier3Count / words;
        if (density > 0.03) {
          results.push(...scanWordList(text, TIER_3, 'Tier 3 AI word (high density)', 'low'));
        }
      }

      // AI phrases
      results.push(...scanPhrases(text, AI_PHRASES));

      return results;
    },
  },

  // ── STYLE PATTERNS (13-18) ──────────────────────────────

  {
    id: 13,
    name: 'Em dash overuse',
    category: 'style',
    description: 'LLMs overuse em dashes (—) as a crutch for punchy writing.',
    weight: 2,
    detect(text) {
      const emDashes = text.match(/—/g) || [];
      const words = wordCount(text);
      const ratio = words > 0 ? emDashes.length / (words / 100) : 0;

      if (ratio > 1.0 && emDashes.length >= 2) {
        return findMatches(
          text,
          /—/g,
          `High em dash density (${emDashes.length} in ${words} words). Replace most with commas, periods, or parentheses.`,
          'medium',
        );
      }
      return [];
    },
  },

  {
    id: 14,
    name: 'Boldface overuse',
    category: 'style',
    description:
      'Mechanical emphasis of phrases in bold. AI uses **bold** as a highlighting crutch.',
    weight: 2,
    detect(text) {
      const boldMatches = text.match(/\*\*[^*]+\*\*/g) || [];
      if (boldMatches.length >= 3) {
        return findMatches(
          text,
          /\*\*[^*]+\*\*/g,
          'Excessive boldface. Remove emphasis — let the writing carry the weight.',
          'medium',
        );
      }
      return [];
    },
  },

  {
    id: 15,
    name: 'Inline-header lists',
    category: 'style',
    description: 'Lists where each item starts with a bolded header followed by a colon.',
    weight: 3,
    detect(text) {
      const inlineHeaders = /^[*-]\s+\*\*[^*]+:\*\*\s/gm;
      const matches = text.match(inlineHeaders) || [];
      if (matches.length >= 2) {
        return findMatches(
          text,
          inlineHeaders,
          'Inline-header list pattern. Convert to a paragraph or use a simpler list.',
          'high',
        );
      }
      return [];
    },
  },

  {
    id: 16,
    name: 'Title Case headings',
    category: 'style',
    description: 'Capitalizing Every Main Word In Headings. AI chatbots default to this.',
    weight: 1,
    detect(text) {
      const headingRegex = /^#{1,6}\s+(.+)$/gm;
      const results = [];
      let m;
      while ((m = headingRegex.exec(text)) !== null) {
        const heading = m[1].trim();
        const hWords = heading.split(/\s+/);
        if (hWords.length >= 3) {
          const skipWords =
            /^(I|AI|API|CLI|URL|HTML|CSS|JS|TS|NPM|NYC|USA|UK|EU|LLM|GPT|SaaS|IoT|CEO|CTO|VP|PR|HR|IT|UI|UX)\b/;
          const capitalizedCount = hWords.filter(
            (w) => /^[A-Z]/.test(w) && !skipWords.test(w),
          ).length;
          if (capitalizedCount / hWords.length > 0.7) {
            const lineNum = text.substring(0, m.index).split('\n').length;
            results.push({
              match: m[0],
              index: m.index,
              line: lineNum,
              column: 1,
              suggestion:
                'Use sentence case for headings (only capitalize first word and proper nouns).',
              confidence: 'medium',
            });
          }
        }
      }
      return results;
    },
  },

  {
    id: 17,
    name: 'Emoji overuse',
    category: 'style',
    description: 'Decorating headings or bullet points with emojis in professional/technical text.',
    weight: 2,
    detect(text) {
      const emojiCount = countMatches(text, /[\u{1F300}-\u{1F9FF}\u{2600}-\u{27BF}]/gu);
      if (emojiCount >= 3) {
        return findMatches(
          text,
          /[\u{1F300}-\u{1F9FF}\u{2600}-\u{27BF}\u{2300}-\u{23FF}\u{2B50}]/gu,
          'Remove emoji decoration from professional text.',
          'high',
        );
      }
      return [];
    },
  },

  {
    id: 18,
    name: 'Curly quotes',
    category: 'style',
    description:
      'ChatGPT uses Unicode curly quotes (\u201C\u201D\u2018\u2019) instead of straight quotes.',
    weight: 1,
    detect(text) {
      return findMatches(
        text,
        /[\u201C\u201D\u2018\u2019]/g,
        'Replace curly quotes with straight quotes.',
        'high',
      );
    },
  },

  // ── NEW LITHUANIAN PATTERNS (25-30) ──────────────────
  // Patterns 19-24 removed (English-only chatbot/filler patterns)

  {
    id: 25,
    name: 'Indirect mood misuse',
    category: 'language',
    description:
      'Using indicative after reporting verbs instead of evidential (netiesioginė nuosaka).',
    weight: 4,
    detect(text) {
      const results = [];
      const re = /\b(?:sako|sak\u0117|ra\u0161o|ra\u0161\u0117|teigia|teig\u0117|prane\u0161a|prane\u0161\u0117)\b/gi;
      let m;
      while ((m = re.exec(text)) !== null) {
        const after = text.substring(m.index, m.index + 120);
        if (/\bkad\b[^.]{0,50}?\b(?:buvo|buvome)\b/.test(after) && !/\b\w+(?:\u0117s|\u0119s)\b/.test(after.substring(0, after.indexOf('buvo') > -1 ? after.indexOf('buvo') : 40))) {
          results.push({
            match: m[0] + '...buvo',
            index: m.index, line: 0, column: 0,
            suggestion: 'Naudok netiesiogin\u0119 nuosak\u0105: vietoj "kad jis buvo" sakyk "kad jis b\u016bt\u0173 buv\u0119s"',
            confidence: 'medium',
          });
        }
      }
      return results;
    },
  },

  {
    id: 26,
    name: 'Aspect confusion',
    category: 'language',
    description:
      'Imperfective verbs used where perfective prefix required.',
    weight: 3,
    detect(text) {
      const cues = ['vis\u0105', 'visi\u0161kai', 'pabaig\u0117', 'u\u017ebaig\u0117', 'i\u0161 karto', 'per valand', 'per met', 'baig\u0117'];
      const stems = ['skaito', 'skaityti', 'daryti', 'mokosi', 'ra\u0161o', 'dirba', 'tvarko', 'kuria'];
      const results = [];
      const words = text.split(/\s+/);
      for (let i = 0; i < words.length; i++) {
        const w = words[i].toLowerCase().replace(/[^\w\u0119\u0161\u016b\u017e\u0105\u010d\u0117\u012f\u016b]/g, '');
        if (cues.some(c => c.includes(w) || w.includes(c))) {
          for (let j = i + 1; j <= Math.min(i + 10, words.length - 1); j++) {
            const v = words[j].toLowerCase().replace(/[^\w\u0119\u0161\u016b\u017e\u0105\u010d\u0117\u012f\u016b]/g, '');
            if (stems.some(s => v === s || v.startsWith(s))) {
              const px = v.includes('skait') ? 'perskait\u0117' : v.includes('dar') ? 'padar\u0117' : v.includes('ra\u0161') ? 'para\u0161\u0117' : 'perf.';
              results.push({ match: v, suggestion: 'Aspektas: vietoj "' + v + '" naudok perfektyv\u0105 (pvz., ' + px + ')', confidence: 'low' });
            }
          }
        }
      }
      return results;
    },
  },

  {
    id: 27,
    name: 'Article hallucination',
    category: 'language',
    description:
      'Using "vienas" as indefinite article like English "a/an".',
    weight: 3,
    detect(text) {
      return findMatches(text, /\bvienas\s+\w+(?:\s+(?:yra|buvo|bus|turi|tur\u0117jo))?\b/gi, 'Pa\u0161alink "vienas" nebent rei\u0161kia skai\u010di\u0173 "one". LT neturi artikli\u0173.', 'medium');
    },
  },

  {
    id: 28,
    name: 'Preposition overuse',
    category: 'language',
    description:
      'Prepositions (apie, d\u0117l, per, su) where case suffix alone would suffice.',
    weight: 2,
    detect(text) {
      return findMatches(text, /\b(?:apie|d\u0117l|per|su)\s+\w+/gi, 'Ar prielinksnis b\u016btinas? Da\u017enai u\u017etinka linksnis.', 'low');
    },
  },

  {
    id: 29,
    name: 'Word order rigidity',
    category: 'style',
    description:
      'Strict SVO without topicalization. LT naturally varies word order.',
    weight: 2,
    detect(text) {
      const sents = text.split(/(?<=[.!?])\s+/);
      let svo = 0, fronted = 0;
      for (const s of sents) {
        const fw = s.toLowerCase().split(/\s+/).slice(0, 2);
        if (['a\u0161', 'tu', 'mes', 'j\u016bs', 'jis', 'ji', 'jie', 'jos'].includes(fw[0]) && fw[1] && /(ti|o|a|a|e|y)$/.test(fw[1])) svo++;
        if (/^(vakar|ryte|vakare|namie|mieste|\u0161iandien|rytoj|anksti)\b/i.test(s)) fronted++;
      }
      if (sents.length >= 3 && (svo / sents.length) > 0.6 && fronted === 0) {
        return [{ match: 'SVO standumas', suggestion: 'Keisk \u017eod\u017ei\u0173 tvark\u0105: LT da\u017enai keliamos aplinkyb\u0117s ("Vakar a\u0161" vietoj "A\u0161 vakar")', confidence: 'low' }];
      }
      return [];
    },
  },

  {
    id: 30,
    name: 'Register mixing',
    category: 'style',
    description:
      'Formal bureaucratic terms mixed with informal particles in same paragraph.',
    weight: 2,
    detect(text) {
      const paras = text.split(/\n\s*\n/);
      const results = [];
      for (let i = 0; i < paras.length; i++) {
        const p = paras[i].toLowerCase();
        const formal = ['optimizavimas', 'efektyvinimas', 'strategija', 'implementavimas', 'platforma', 'ekosistema', 'proces\u0173', 'veiklos', 'tobulinimas', 'savitarna'].some(w => p.includes(w));
        const informal = /\b(?:gi|juk|d\u0117lto|bene|turb\u016bt|gal|na)\b/.test(p);
        if (formal && informal) {
          results.push({ match: 'registro mai\u0161ymas', suggestion: 'Laikykit\u0117s vieno registro: formalas ARBA neformalus pastraipoje.', confidence: 'low' });
        }
      }
      return results;
    },
  },
];

// ─── Pattern Registry ────────────────────────────────────

class PatternRegistry {
  constructor() {
    this._patterns = [...patterns];
    this._customWords = { tier1: [], tier2: [], tier3: [] };
  }

  /** Get all patterns. */
  all() {
    return this._patterns;
  }

  /** Get pattern by ID. */
  get(id) {
    return this._patterns.find((p) => p.id === id);
  }

  /** Get patterns by category. */
  byCategory(category) {
    return this._patterns.filter((p) => p.category === category);
  }

  /** Add a custom pattern. */
  add(pattern) {
    if (!pattern.id || !pattern.name || !pattern.detect) {
      throw new Error('Pattern must have id, name, and detect function');
    }
    this._patterns.push(pattern);
  }

  /** Remove a pattern by ID. */
  remove(id) {
    this._patterns = this._patterns.filter((p) => p.id !== id);
  }

  /** Add custom words to a tier. */
  addWords(tier, words) {
    const key = `tier${tier}`;
    if (!this._customWords[key]) throw new Error(`Invalid tier: ${tier}`);
    this._customWords[key].push(...words);
  }

  /** Get full vocabulary for a tier (built-in + custom). */
  getVocabulary(tier) {
    const builtIn = tier === 1 ? TIER_1 : tier === 2 ? TIER_2 : TIER_3;
    return [...builtIn, ...(this._customWords[`tier${tier}`] || [])];
  }

  /** List all pattern IDs and names. */
  list() {
    return this._patterns.map((p) => ({
      id: p.id,
      name: p.name,
      category: p.category,
      weight: p.weight,
    }));
  }

  /** Get categories. */
  categories() {
    return [...new Set(this._patterns.map((p) => p.category))];
  }
}

// Singleton registry
const registry = new PatternRegistry();

// ─── Exports ─────────────────────────────────────────────

module.exports = {
  patterns,
  registry,
  PatternRegistry,
  findMatches,
  countMatches,
  wordCount,
  scanWordList,
  scanPhrases,
  // Re-export vocabulary for backward compat
  TIER_1,
  TIER_2,
  TIER_3,
  AI_PHRASES,
};
