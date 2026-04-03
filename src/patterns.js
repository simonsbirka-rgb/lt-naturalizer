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
      const genitiveChain = /(?:\S+(?:ės|io|ų|os)\s+){2,}\S+(?:ės|io|ų|os|imo|imo)\b/gi;
      return findMatches(text, genitiveChain, 'Rewrite using verbs instead of stacked genitive nouns', 'high');
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

  // ── COMMUNICATION PATTERNS (19-21) ─────────────────────

  {
    id: 19,
    name: 'Chatbot artifacts',
    category: 'communication',
    description:
      'Leftover chatbot phrases: "I hope this helps!", "Let me know if...", "Here is an overview".',
    weight: 5,
    detect(text) {
      return scanPhrases(
        text,
        AI_PHRASES.filter(
          (p) => p.fix === '(remove)' || p.fix === '(remove — start with the content)',
        ),
      );
    },
  },

  {
    id: 20,
    name: 'Cutoff disclaimers',
    category: 'communication',
    description: 'AI knowledge-cutoff disclaimers left in text.',
    weight: 4,
    detect(text) {
      return scanPhrases(
        text,
        AI_PHRASES.filter(
          (p) =>
            p.fix === '(remove)' &&
            (p.pattern.source.includes('training') ||
              p.pattern.source.includes('details are') ||
              p.pattern.source.includes('available')),
        ),
      );
    },
  },

  {
    id: 21,
    name: 'Sycophantic tone',
    category: 'communication',
    description:
      'Overly positive, people-pleasing language: "Great question!", "You\'re absolutely right!".',
    weight: 4,
    detect(text) {
      return scanPhrases(
        text,
        AI_PHRASES.filter(
          (p) =>
            p.fix &&
            (p.fix.includes('(remove)') || p.fix.includes('address the substance')) &&
            (p.pattern.source.includes('question') ||
              p.pattern.source.includes('point') ||
              p.pattern.source.includes('right') ||
              p.pattern.source.includes('observation')),
        ),
      );
    },
  },

  // ── FILLER & HEDGING (22-24) ────────────────────────────

  {
    id: 22,
    name: 'Filler phrases',
    category: 'filler',
    description:
      'Wordy filler that can be shortened: "in order to" → "to", "due to the fact that" → "because".',
    weight: 3,
    detect(text) {
      return scanPhrases(
        text,
        AI_PHRASES.filter(
          (p) =>
            p.fix &&
            !p.fix.startsWith('(') &&
            [
              'to',
              'because',
              'now',
              'if',
              'can',
              'to / for',
              'first',
              'finally',
              'for / regarding',
              'because / since',
            ].includes(p.fix),
        ),
      );
    },
  },

  {
    id: 23,
    name: 'Excessive hedging',
    category: 'filler',
    description: 'Stacking qualifiers: "could potentially possibly", "might arguably perhaps".',
    weight: 3,
    detect(text) {
      return scanPhrases(
        text,
        AI_PHRASES.filter(
          (p) =>
            p.fix &&
            (p.fix.includes('could') ||
              p.fix.includes('might') ||
              p.fix.includes('may') ||
              p.fix.includes('perhaps') ||
              p.fix.includes('maybe')),
        ),
      );
    },
  },

  {
    id: 24,
    name: 'Generic conclusions',
    category: 'filler',
    description: 'Vague upbeat endings: "The future looks bright", "Exciting times lie ahead".',
    weight: 3,
    detect(text) {
      return scanPhrases(
        text,
        AI_PHRASES.filter(
          (p) =>
            p.fix &&
            (p.fix.includes('specific fact') ||
              p.fix.includes('concrete') ||
              p.fix.includes('cite evidence') ||
              p.fix.includes('what you do know') ||
              p.fix.includes('what happens next')),
        ),
      );
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
