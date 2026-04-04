#!/usr/bin/env python3
"""Add more AI-like Lithuanian samples."""

from pathlib import Path

AI_DIR = Path("/home/simonas/Documents/lt/lt-naturalizer/corpus/ai")

ai_samples = [
    """Demografija yra viena iš svarbiausių Lietuvos problemų. Gyventojų skaičius nuolat mažėja dėl emigracijos ir mažo gimstamumo. Ši problema turi įtakos šalies ekonomikai ir socialinei sistemai.

Vyriausybė įgyvendina įvairias priemones, skirtas stabdyti emigraciją ir skatinti gimstamumą. Pavyzdžiui, didinamos vaikų išmokos ir sukuriamos naujos darbo vietos. Be to, vykdomos programos, skirtos pritraukti emigrantus grįžti į Lietuvą.

Išvadai, demografinės problemos sprendimas reikalauja kompleksinio požiūrio. Svarbu užtikrinti, kad jauni žmonės turėtų galimybes įsidarbinti ir sukurti šeimas Lietuvoje. Investicijos į švietimą ir sveikatos priežiūrą yra būtinos.""",

    """Skaitmeninė transformacija keičia Lietuvos verslą ir viešąjį sektorių. Naujos technologijos leidžia efektyviau teikti paslaugas ir valdyti procesus. Elektroninės paslaugos tampa vis prieinamesnės gyventojams.

Valstybės institucijos diegia skaitmeninius sprendimus, siekdamos pagerinti tarnybų darbą. Pavyzdžiui, elektroninis parašas leidžia gyventojams pasirašyti dokumentus nuotoliniu būdu. Be to, sukurtos portalai, kuriuose galima gauti įvairias paslaugas internetu.

Apskritai, skaitmeninė transformacija yra neišvengiamas procesas. Lietuva siekia tapti viena iš pažangiausių skaitmeninių šalių Europoje. Svarbu užtikrinti, kad visi gyventojai galėtų naudotis skaitmeninėmis paslaugomis.""",

    """Nekilnojamas turtas Lietuvoje patiria reikšmingų pokyčių. Nekilnojamojo turto kainos didžiuosiuose miestuose auga dėl paklausos ir investicijų. Vilnius ir Kaunas pritraukia daugiausia pirkėjų ir investuotojų.

Statybos sektorius aktyviai plėtojasi, statomi nauji gyvenamieji kompleksai ir komerciniai pastatai. Be to, renovuojami seni pastatai, siekiant pagerinti jų energinį efektyvumą. Vyriausybė teikia paramą būsto įsigijimui ir renovacijai.

Išvadai, nekilnojamojo turto rinka turi gerą potencialą augti. Svarbu užtikrinti, kad būstas būtų prieinamas įvairioms gyventojų grupėms. Subalansuota plėtra yra būtina tvarios miestų raidai.""",

    """Moksliniai tyrimai Lietuvoje plėtojami universitetuose ir mokslinių tyrimų institutuose. Šalis investuoja į mokslą, siekdama sukurti inovacijas ir pagerinti ekonomikos konkurencingumą. Svarbios sritys apima biotechnologijas, informacines technologijas ir fiziką.

Lietuvos mokslininkai aktyviai dalyvauja tarptautiniuose moksliniuose projektuose. Europos Sąjungos finansavimas leidžia įgyvendinti ambicingus tyrimus. Be to, skatinamas bendradarbiavimas tarp mokslo ir verslo.

Apskritai, mokslo raida yra svarbi šalies ateiciai. Investicijos į mokslą ir inovacijas yra būtinos žinių ekonomikai plėtoti. Svarbu paminėti, kad jaunųjų mokslininkų parama yra prioritetas.""",
]

existing = len(list(AI_DIR.glob("*.txt")))
for i, text in enumerate(ai_samples):
    filename = AI_DIR / f"ai_sample_{existing + i + 1}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Created: {filename.name}")

total = len(list(AI_DIR.glob("*.txt")))
print(f"\nTotal AI corpus files: {total}")
