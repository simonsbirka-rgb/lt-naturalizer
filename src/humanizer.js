/**
 * humanizer.js — Humanization engine.
 *
 * Takes analysis results and produces actionable rewrite suggestions.
 * Includes both:
 *   - autoFix: safe mechanical transforms (curly quotes, filler phrases, chatbot artifacts)
 *   - humanize: full suggestion report with prioritized guidance
 *
 * Humanization techniques based on 2025 research:
 *   - Sentence length variation (mix short with long)
 *   - Burstiness injection (fragments, questions, varied rhythm)
 *   - Concrete specificity (replace vague with numbers/names/dates)
 *   - First-person injection (where appropriate)
 *   - Opinion injection (humans have preferences, AI is neutral)
 */

const { analyze } = require("./analyzer");

// ─── Automatic Fixes ─────────────────────────────────────

/**
 * Apply safe, mechanical fixes that don't require judgment.
 * Only transforms where the "right" answer is unambiguous.
 *
 * @param {string} text — Input text
 * @returns {{ text: string, fixes: string[] }}
 */
function autoFix(text) {
  let result = text;
  const fixes = [];

  // Curly quotes → straight quotes
  if (/[\u201C\u201D]/.test(result)) {
    result = result.replace(/[\u201C\u201D]/g, '"');
    fixes.push("Replaced curly double quotes with straight quotes");
  }
  if (/[\u2018\u2019]/.test(result)) {
    result = result.replace(/[\u2018\u2019]/g, "'");
    fixes.push("Replaced curly single quotes with straight quotes");
  }

  // Filler phrase replacements (unambiguous) - Lithuanian
  const safeFills = [
    {
      from: /pasinerkime į/gi,
      to: "pažiūrėkime",
      label: '"pasinerkime į" → "pažiūrėkime"',
    },
    {
      from: /panagrinėkime/gi,
      to: "pažiūrėk",
      label: '"panagrinėkime" → "pažiūrėk"',
    },
    {
      from: /neabejotinai/gi,
      to: "tikrai",
      label: '"neabejotinai" → "tikrai"',
    },
    {
      from: /nuolat besikeičiančiame kraštovaizdyje/gi,
      to: "dabar",
      label: '"nuolat besikeičiančiame kraštovaizdyje" → "dabar"',
    },
    {
      from: /šiuolaikiniame skaitmeniniame amžiuje/gi,
      to: "dabar",
      label: '"šiuolaikiniame skaitmeniniame amžiuje" → "dabar"',
    },
    {
      from: /išlaisvinti potencialą/gi,
      to: "padėti geriau",
      label: '"išlaisvinti potencialą" → "padėti geriau"',
    },
    {
      from: /Mes turime suprasti, kad/gi,
      to: "Turime suprasti, kad",
      label: '"Mes turime suprasti, kad" → "Turime suprasti, kad"',
    },
    {
      from: /Jis mano, kad/gi,
      to: "Mano, kad",
      label: '"Jis mano, kad" → "Mano, kad"',
    },
    {
      from: /Ji sako, kad/gi,
      to: "Sako, kad",
      label: '"Ji sako, kad" → "Sako, kad"',
    },
    { from: /yra daroma/gi, to: "darosi", label: '"yra daroma" → "darosi"' },
    {
      from: /buvo pastebėta/gi,
      to: "pastebima",
      label: '"buvo pastebėta" → "pastebima"',
    },
    {
      from: /yra tikimasi/gi,
      to: "tikimasi",
      label: '"yra tikimasi" → "tikimasi"',
    },
    {
      from: /priėmėme sprendimą/gi,
      to: "mes nusprendėme",
      label: '"priėmėme sprendimą" → "mes nusprendėme"',
    },
    {
      from: /vykdyti tobulinimą/gi,
      to: "tobulinti",
      label: '"vykdyti tobulinimą" → "tobulinti"',
    },
  ];

  for (const { from, to, label } of safeFills) {
    if (from.test(result)) {
      result = result.replace(from, to);
      fixes.push(label);
    }
  }

  // Chatbot artifact removal (start/end of text) - Lithuanian
  const chatbotStart = [
    /^(Štai |Čia yra |Pateikiame )(išsami |trumpa |greita )?(apžvalga|santrauka|sąrašas|gidas|paaiškinimas|informacija)[^.]*\.\s*/i,
    /^(Žinoma|Be abejo|Tikrai|Su malonumu)!\s*/i,
    /^(Puikus|Geras|Įdomus) (klausimas|pastebėjimas)!\s*/i,
    /^(Tai|Tai yra) (puikus|geras|įdomus) (klausimas|pastebėjimas)!\s*/i,
    /^(Svarbu pažymėti, kad|Verta atkreipti dėmesį, kad)\s*/i,
  ];
  for (const regex of chatbotStart) {
    if (regex.test(result)) {
      result = result.replace(regex, "");
      fixes.push("Removed chatbot opening artifact");
    }
  }

  const chatbotEnd = [
    /\s*(Tikiuosi, kad tai padės|Leiskite žinoti, jei|Nedvejokite|Ar galiu dar kuo nors padėti)[^.]*[.!]\s*$/i,
    /\s*Džiaugiuosi galėdamas padėti[.!]?\s*$/i,
  ];
  for (const regex of chatbotEnd) {
    if (regex.test(result)) {
      result = result.replace(regex, "");
      fixes.push("Removed chatbot closing artifact");
    }
  }

  result = result.trim();
  return { text: result, fixes };
}

// ─── Suggestion Engine ───────────────────────────────────

/**
 * Generate humanization suggestions.
 *
 * @param {string} text    — Input text
 * @param {object} opts    — Options:
 *   - autofix {boolean}   Apply safe auto-fixes
 *   - verbose {boolean}   Show all matches
 *   - includeStats {boolean}  Include statistical suggestions
 * @returns {object}       — Suggestions report
 */
function humanize(text, opts = {}) {
  const { autofix = false, includeStats = true } = opts;

  const analysis = analyze(text, { verbose: true, includeStats });

  // Group by priority
  const critical = []; // weight 4-5: dead giveaways
  const important = []; // weight 2-3: noticeable
  const minor = []; // weight 1: subtle

  for (const finding of analysis.findings) {
    const suggestions = finding.matches.map((m) => ({
      pattern: finding.patternName,
      patternId: finding.patternId,
      category: finding.category,
      weight: finding.weight,
      text: m.match,
      line: m.line,
      column: m.column,
      suggestion: m.suggestion,
      confidence: m.confidence || "high",
    }));

    if (finding.weight >= 4) critical.push(...suggestions);
    else if (finding.weight >= 2) important.push(...suggestions);
    else minor.push(...suggestions);
  }

  // Auto-fix
  let fixedText = null;
  let appliedFixes = [];
  if (autofix) {
    const result = autoFix(text);
    fixedText = result.text;
    appliedFixes = result.fixes;
  }

  // Build guidance (pattern-based + statistical)
  const guidance = buildGuidance(analysis);
  const styleTips =
    includeStats && analysis.stats ? buildStyleTips(analysis.stats) : [];

  return {
    score: analysis.score,
    patternScore: analysis.patternScore,
    uniformityScore: analysis.uniformityScore,
    wordCount: analysis.wordCount,
    totalIssues: analysis.totalMatches,
    stats: analysis.stats,
    critical,
    important,
    minor,
    autofix: autofix ? { text: fixedText, fixes: appliedFixes } : null,
    guidance,
    styleTips,
  };
}

/**
 * Build pattern-based guidance.
 */
function buildGuidance(analysis) {
  const tips = [];
  const ids = new Set(analysis.findings.map((f) => f.patternId));

  if (ids.has(1) || ids.has(4)) {
    tips.push(
      "Replace inflated/promotional language with concrete facts. What specifically happened? Give dates, numbers, names.",
    );
  }
  if (ids.has(3)) {
    tips.push(
      "Cut trailing -ing phrases. If the point matters enough to mention, give it its own sentence.",
    );
  }
  if (ids.has(5)) {
    tips.push(
      'Name your sources. "Experts say" means nothing — who said it, when, and where?',
    );
  }
  if (ids.has(6)) {
    tips.push(
      'Replace formulaic "despite challenges" sections with specific problems and concrete outcomes.',
    );
  }
  if (ids.has(7)) {
    tips.push(
      'Swap AI vocabulary for plainer words. "Delve" → "look at". "Tapestry" → (be specific). "Showcase" → "show".',
    );
  }
  if (ids.has(13)) {
    tips.push(
      "Ease up on em dashes. Use commas, periods, or parentheses for variety.",
    );
  }
  if (ids.has(14) || ids.has(15)) {
    tips.push(
      "Strip mechanical bold formatting and inline-header lists. Let prose do the work.",
    );
  }
  if (ids.has(17)) {
    tips.push(
      "Remove emojis from professional text. They signal chatbot output.",
    );
  }
  if (analysis.score >= 50) {
    tips.push(
      "Consider rewriting from scratch. When AI patterns are this dense, patching individual phrases isn't enough — the structure itself needs rethinking.",
    );
  }

  return tips;
}

/**
 * Build statistical style tips based on text metrics.
 * These suggest structural improvements beyond word choice.
 */
function buildStyleTips(stats) {
  const tips = [];

  // Burstiness
  if (stats.burstiness < 0.25 && stats.sentenceCount > 4) {
    tips.push({
      metric: "burstiness",
      value: stats.burstiness,
      tip: "Sentence rhythm is very uniform. Mix short punchy sentences (3-8 words) with longer flowing ones (20+). Fragments work too. Like this.",
    });
  }

  // Sentence length variation
  if (stats.sentenceLengthVariation < 0.3 && stats.sentenceCount > 4) {
    tips.push({
      metric: "sentenceLengthVariation",
      value: stats.sentenceLengthVariation,
      tip: `Sentences are all roughly ${Math.round(stats.avgSentenceLength)} words. Vary your rhythm — alternate between short and long.`,
    });
  }

  // Very long average sentences
  if (stats.avgSentenceLength > 28) {
    tips.push({
      metric: "avgSentenceLength",
      value: stats.avgSentenceLength,
      tip: "Average sentence is quite long. Break some into shorter ones. Not every thought needs a subordinate clause.",
    });
  }

  // Low vocabulary diversity
  if (stats.typeTokenRatio < 0.4 && stats.wordCount > 100) {
    tips.push({
      metric: "typeTokenRatio",
      value: stats.typeTokenRatio,
      tip: "Vocabulary is repetitive. Try using more varied word choices — but don't synonym-cycle (that's also an AI tell).",
    });
  }

  // High trigram repetition
  if (stats.trigramRepetition > 0.1 && stats.wordCount > 100) {
    tips.push({
      metric: "trigramRepetition",
      value: stats.trigramRepetition,
      tip: "Repeated 3-word phrases detected. Vary your sentence structures.",
    });
  }

  // Add humanization techniques if text scores poorly
  if (tips.length >= 2) {
    tips.push({
      metric: "general",
      value: null,
      tip: "Try the read-aloud test: read the text out loud. If it sounds weird or robotic, rewrite those parts until they sound like something you'd actually say.",
    });
    tips.push({
      metric: "general",
      value: null,
      tip: 'Add first-person perspective where it fits: "I found", "We noticed", "In my experience". Real humans write from a point of view.',
    });
  }

  return tips;
}

// ─── Report Formatting ──────────────────────────────────

/**
 * Format humanization suggestions as readable terminal output.
 */
function formatSuggestions(result) {
  const lines = [];

  lines.push("");
  lines.push("╔══════════════════════════════════════════════════╗");
  lines.push("║           HUMANIZATION SUGGESTIONS               ║");
  lines.push("╚══════════════════════════════════════════════════╝");
  lines.push("");

  const filled = Math.round(result.score / 5);
  const bar = "█".repeat(filled) + "░".repeat(20 - filled);
  lines.push(`  AI Score: ${result.score}/100  [${bar}]`);
  lines.push(
    `  Issues: ${result.totalIssues}  |  Pattern: ${result.patternScore}  |  Uniformity: ${result.uniformityScore}`,
  );
  lines.push("");

  if (result.critical.length > 0) {
    lines.push("── CRITICAL (dead giveaways) ───────────────────────");
    for (const s of result.critical) {
      lines.push(
        `  L${s.line}: [${s.pattern}] "${truncate(s.text, 60)}" [${s.confidence}]`,
      );
      lines.push(`       → ${s.suggestion}`);
    }
    lines.push("");
  }

  if (result.important.length > 0) {
    lines.push("── IMPORTANT (noticeable patterns) ─────────────────");
    for (const s of result.important.slice(0, 15)) {
      lines.push(`  L${s.line}: [${s.pattern}] "${truncate(s.text, 60)}"`);
      lines.push(`       → ${s.suggestion}`);
    }
    if (result.important.length > 15) {
      lines.push(`  ... and ${result.important.length - 15} more`);
    }
    lines.push("");
  }

  if (result.minor.length > 0) {
    lines.push("── MINOR (subtle tells) ────────────────────────────");
    for (const s of result.minor.slice(0, 10)) {
      lines.push(`  L${s.line}: [${s.pattern}] "${truncate(s.text, 60)}"`);
      lines.push(`       → ${s.suggestion}`);
    }
    if (result.minor.length > 10) {
      lines.push(`  ... and ${result.minor.length - 10} more`);
    }
    lines.push("");
  }

  if (result.autofix) {
    lines.push("── AUTO-FIXES APPLIED ──────────────────────────────");
    for (const fix of result.autofix.fixes) {
      lines.push(`  ✓ ${fix}`);
    }
    lines.push("");
  }

  if (result.guidance.length > 0) {
    lines.push("── GUIDANCE ────────────────────────────────────────");
    for (const tip of result.guidance) {
      lines.push(`  • ${tip}`);
    }
    lines.push("");
  }

  if (result.styleTips.length > 0) {
    lines.push("── STYLE TIPS (statistical) ────────────────────────");
    for (const t of result.styleTips) {
      const metric = t.value !== null ? ` [${t.metric}: ${t.value}]` : "";
      lines.push(`  ◦ ${t.tip}${metric}`);
    }
    lines.push("");
  }

  lines.push("════════════════════════════════════════════════════");
  return lines.join("\n");
}

function truncate(str, len) {
  if (typeof str !== "string") return "";
  return str.length > len ? `${str.substring(0, len)}...` : str;
}

// ─── Exports ─────────────────────────────────────────────

module.exports = {
  humanize,
  autoFix,
  formatSuggestions,
  buildGuidance,
  buildStyleTips,
};
