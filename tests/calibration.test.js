/**
 * calibration.test.js — Calibration tests for the scoring engine.
 *
 * Known AI samples should score high, known human samples should score low.
 */

import { describe, it, expect } from "vitest";
import { score } from "../src/analyzer.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function loadFixture(name) {
  return fs.readFileSync(path.join(__dirname, "fixtures", name), "utf-8");
}

// ─── AI Samples — Should Score High ─────────────────────

describe("AI sample calibration", () => {
  it("ai-sample-1.txt scores 55+", () => {
    const text = loadFixture("ai-sample-1.txt");
    const s = score(text);
    expect(s).toBeGreaterThanOrEqual(55);
  });

  it("ai-sample-2.txt scores 30+ (moderate AI)", () => {
    const text = loadFixture("ai-sample-2.txt");
    const s = score(text);
    expect(s).toBeGreaterThanOrEqual(30);
  });

  it("classic chatbot output scores very high", () => {
    const text = `Great question! Here is a comprehensive overview of machine learning.

Pasinerkime į mašininio mokymosi galimybes. Svarbu pažymėti, kad šiuolaikiniame skaitmeniniame amžiuje šios priemonės yra daroma vis geriau. Neabejotinai, verta atkreipti dėmesį į naujoves. Mes turime suprasti, kad nuolat besikeičiančiame kraštovaizdyje technologijos tobulėja.

Buvo pastebėta, kad AI priemonės padeda. Priėmėme sprendimą vykdyti tobulinimą, nes tai padeda įgalinti komandas ir išlaisvinti potencialą.

- **Greitis:** Apdorojimas yra daroma greičiau, kas įgalinti komandas dirbti efektyviau.
- **Kokybė:** Rezultatų kokybė yra tikimasi gerėsianti.
- **Pritaikymas:** Naudojimas auga, kas atskleisti naujus horizontus.

The future looks bright. Exciting times lie ahead as we continue this journey toward excellence. I hope this helps! Let me know if you'd like me to expand.`;
    const s = score(text);
    expect(s).toBeGreaterThanOrEqual(60);
  });

  it("promotional AI text scores high", () => {
    const text = `Pasinerkime į Vilniaus kultūrinę aplinką. Svarbu pažymėti, kad šiuolaikiniame skaitmeniniame amžiuje miestas yra daroma vis patrauklesnis. Neabejotinai, verta atkreipti dėmesį į miesto architektūrą ir istoriją.

Buvo pastebėta, kad turizmas auga. Priėmėme sprendimą vykdyti tobulinimą infrastruktūros srityje, nes tai padeda įgalinti verslą ir išlaisvinti potencialą. Nuolat besikeičiančiame kraštovaizdyje Vilnius tobulėja.

The future looks bright. Exciting times lie ahead.`;
    const s = score(text);
    expect(s).toBeGreaterThanOrEqual(55);
  });

  it("hedging + filler AI text scores high", () => {
    const text = `It could potentially be argued that in order to navigate challenges, it is important to adapt. Due to the fact that the landscape is ever-evolving, teams need to improve.

Svarbu pažymėti, kad šiuolaikiniame skaitmeniniame amžiuje priemonės yra daroma vis geriau. Neabejotinai, verta atkreipti dėmesį. Buvo pastebėta, kad reikia vykdyti tobulinimą. Pasinerkime į galimybes ir atskleisti potencialą.

In conclusion, the future looks bright. Exciting times lie ahead. I hope this helps! Let me know if you'd like me to expand.`;
    const s = score(text);
    expect(s).toBeGreaterThanOrEqual(50);
  });
});

// ─── Human Samples — Should Score Low ───────────────────

describe("human sample calibration", () => {
  it("human-sample-1.txt scores under 50", () => {
    const text = loadFixture("human-sample-1.txt");
    const s = score(text);
    expect(s).toBeLessThan(50);
  });

  it("casual human writing scores low", () => {
    const text = `I tried three different coffee shops this week. The one on 5th Ave had the best espresso but terrible wifi. The place near the park was quiet enough to work but their cold brew tasted like it had been sitting out since Tuesday.

Ended up going back to my usual spot. Nothing fancy. The barista knows my order. Sometimes that matters more than fancy latte art.`;
    const s = score(text);
    expect(s).toBeLessThan(50);
  });

  it("technical human writing scores low", () => {
    const text = `The bug was in the connection pooling code. When you hit exactly 256 concurrent connections, the pool silently dropped new requests instead of queuing them. No error, no log, just a hung request.

Found it by adding a counter to the pool checkout method. Took about 3 hours of staring at tcpdump output before I thought to look there.

Fixed it with a bounded semaphore. PR is up. The test covers the edge case now.`;
    const s = score(text);
    expect(s).toBeLessThan(50);
  });

  it("opinionated human writing scores low", () => {
    const text = `Look, I get why people like TypeScript. It catches some real bugs at compile time. But the productivity tax is real, and nobody wants to talk about it.

Last week I spent 45 minutes trying to satisfy the type checker on a function that was obviously correct. The types were right, the logic was right, but some intersection type was confusing the compiler.

I still use it for big projects. But for scripts and prototypes? Just give me plain JavaScript.`;
    const s = score(text);
    expect(s).toBeLessThan(50);
  });

  it("narrative human writing scores low", () => {
    const text = `My grandfather built his own house in 1962. Took him two years, working weekends. The foundation is slightly off-level — you can tell if you put a marble on the kitchen floor. It rolls toward the east wall every time.

He never fixed it. Said it gave the house character. I think he just didn't want to jack up a house he'd already put a roof on.

The house is still standing. My aunt lives there now.`;
    const s = score(text);
    expect(s).toBeLessThan(50);
  });
});

// ─── Relative Ordering ──────────────────────────────────

describe("relative scoring", () => {
  it("AI text always scores higher than human text", () => {
    const aiText = loadFixture("ai-sample-1.txt");
    const humanText = loadFixture("human-sample-1.txt");

    const aiScore = score(aiText);
    const humanScore = score(humanText);

    expect(aiScore).toBeGreaterThan(humanScore);
    expect(aiScore - humanScore).toBeGreaterThan(20);
  });

  it("more AI patterns → higher score", () => {
    const light =
      "The project has been interesting in scope. We worked hard on it last year.";
    const heavy =
      "Additionally, this groundbreaking project serves as a testament to innovation. In today's rapidly evolving landscape, it showcases the vibrant tapestry of modern technology, fostering seamless synergy. I hope this helps!";

    expect(score(heavy)).toBeGreaterThan(score(light));
  });
});
