/**
 * humanizer.test.js — Tests for the humanization engine.
 */

import { describe, it, expect } from "vitest";
import { humanize, autoFix, formatSuggestions } from "../src/humanizer.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function loadFixture(name) {
  return fs.readFileSync(path.join(__dirname, "fixtures", name), "utf-8");
}

// ─── autoFix ─────────────────────────────────────────────

describe("autoFix", () => {
  it("replaces curly double quotes with straight quotes", () => {
    const { text, fixes } = autoFix("He said \u201Chello\u201D to her.");
    expect(text).toBe('He said "hello" to her.');
    expect(fixes.length).toBeGreaterThan(0);
  });

  it("replaces curly single quotes with straight quotes", () => {
    const { text } = autoFix("It\u2019s a fine day.");
    expect(text).toBe("It's a fine day.");
  });

  it('replaces "pasinerkime į" with "pažiūrėkime"', () => {
    const { text } = autoFix("Pasinerkime į šią temą ir suprasime.");
    expect(text).toContain("pažiūrėkime");
    expect(text).not.toContain("Pasinerkime į");
  });

  it('replaces "neabejotinai" with "tikrai"', () => {
    const { text } = autoFix("Tai neabejotinai padės.");
    expect(text).toContain("tikrai");
    expect(text).not.toContain("neabejotinai");
  });

  it('replaces "šiuolaikiniame skaitmeniniame amžiuje" with "dabar"', () => {
    const { text } = autoFix(
      "Šiuolaikiniame skaitmeniniame amžiuje mes gyvename greitai.",
    );
    expect(text).toContain("dabar");
    expect(text).not.toContain("Šiuolaikiniame skaitmeniniame amžiuje");
  });

  it('replaces "išlaisvinti potencialą" with "padėti geriau"', () => {
    const { text } = autoFix("Turime išlaisvinti potencialą savo komandoje.");
    expect(text).toContain("padėti geriau");
    expect(text).not.toContain("išlaisvinti potencialą");
  });

  it('replaces "Jis mano, kad" with "Mano, kad"', () => {
    const { text } = autoFix("Jis mano, kad tai veikia.");
    expect(text).toContain("Mano, kad");
    expect(text).not.toContain("Jis mano, kad");
  });

  it("removes chatbot opening artifacts", () => {
    const { text, fixes } = autoFix(
      "Tai puikus klausimas! Atsakymas yra paprastas.",
    );
    expect(text).not.toContain("puikus klausimas!");
    expect(fixes.some((f) => f.includes("chatbot"))).toBe(true);
  });

  it("removes chatbot closing artifacts", () => {
    const { text, fixes } = autoFix(
      "Atsakymas yra 42. Tikiuosi, kad tai padės!",
    );
    expect(text).not.toContain("Tikiuosi, kad tai padės");
    expect(fixes.some((f) => f.includes("chatbot"))).toBe(true);
  });

  it("handles text with no fixable issues", () => {
    const { text, fixes } = autoFix("Katinas sėdi ant kilimėlio.");
    expect(text).toBe("Katinas sėdi ant kilimėlio.");
    expect(fixes.length).toBe(0);
  });

  it("applies multiple fixes in one pass", () => {
    const input =
      "Tai puikus klausimas! Pasinerkime į šią temą ir suprasime. Tai\u2019s gerai. Tikiuosi, kad tai padės!";
    const { text, fixes } = autoFix(input);
    expect(fixes.length).toBeGreaterThanOrEqual(3);
    expect(text).not.toContain("Pasinerkime į");
    expect(text).not.toContain("\u2019");
  });
});

// ─── humanize ────────────────────────────────────────────

describe("humanize", () => {
  it("returns a valid suggestion object", () => {
    const result = humanize("This is a testament to great things.");
    expect(result).toHaveProperty("score");
    expect(result).toHaveProperty("critical");
    expect(result).toHaveProperty("important");
    expect(result).toHaveProperty("minor");
    expect(result).toHaveProperty("guidance");
    expect(result).toHaveProperty("totalIssues");
    expect(result).toHaveProperty("styleTips");
  });

  it("categorizes issues by severity", () => {
    const text = loadFixture("ai-sample-1.txt");
    const result = humanize(text);
    expect(result.critical.length).toBeGreaterThan(0);
    expect(result.important.length).toBeGreaterThan(0);
  });

  it("provides guidance tips", () => {
    const text = loadFixture("ai-sample-1.txt");
    const result = humanize(text);
    expect(result.guidance.length).toBeGreaterThan(0);
    expect(
      result.guidance.some((g) => typeof g === "string" && g.length > 10),
    ).toBe(true);
  });

  it("returns autofix results when requested", () => {
    const text = "Tai puikus klausimas! Pasinerkime į šią temą ir suprasime.";
    const result = humanize(text, { autofix: true });
    expect(result.autofix).not.toBeNull();
    expect(result.autofix.text).not.toContain("Pasinerkime į");
    expect(result.autofix.fixes.length).toBeGreaterThan(0);
  });

  it("returns null autofix when not requested", () => {
    const result = humanize("Some text here.", { autofix: false });
    expect(result.autofix).toBeNull();
  });

  it("scores human text low", () => {
    const text = loadFixture("human-sample-1.txt");
    const result = humanize(text);
    expect(result.score).toBeLessThan(50);
  });

  it("each suggestion has required fields", () => {
    const text = loadFixture("ai-sample-1.txt");
    const result = humanize(text);
    const allSuggestions = [
      ...result.critical,
      ...result.important,
      ...result.minor,
    ];
    for (const s of allSuggestions) {
      expect(s).toHaveProperty("pattern");
      expect(s).toHaveProperty("patternId");
      expect(s).toHaveProperty("category");
      expect(s).toHaveProperty("suggestion");
      expect(s).toHaveProperty("line");
    }
  });

  it("includes style tips for AI-like text", () => {
    const text = loadFixture("ai-sample-1.txt");
    const result = humanize(text);
    expect(result.styleTips).toBeDefined();
    expect(Array.isArray(result.styleTips)).toBe(true);
  });
});

// ─── formatSuggestions ───────────────────────────────────

describe("formatSuggestions", () => {
  it("produces readable output", () => {
    const text = loadFixture("ai-sample-1.txt");
    const result = humanize(text);
    const output = formatSuggestions(result);
    expect(typeof output).toBe("string");
    expect(output).toContain("HUMANIZATION SUGGESTIONS");
    expect(output).toContain("AI Score:");
  });

  it("includes guidance section", () => {
    const text = loadFixture("ai-sample-1.txt");
    const result = humanize(text);
    const output = formatSuggestions(result);
    expect(output).toContain("GUIDANCE");
  });
});
