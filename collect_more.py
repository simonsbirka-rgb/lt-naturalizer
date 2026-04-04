#!/usr/bin/env python3
"""Collect more Lithuanian text samples."""

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import re

HUMAN_DIR = Path("/home/simonas/Documents/lt/lt-naturalizer/corpus/human")
AI_DIR = Path("/home/simonas/Documents/lt/lt-naturalizer/corpus/ai")

def clean_text(text):
    if not text:
        return None
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_article(url, min_length=300):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        paragraphs = soup.find_all('p')
        text_parts = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50]
        full_text = ' '.join(text_parts)
        full_text = clean_text(full_text)
        
        return full_text if len(full_text) >= min_length else None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def collect_more_lrt():
    """Collect more LRT articles."""
    print("Collecting more LRT articles...")
    # Direct article URLs
    urls = [
        "https://www.lrt.lt/naujienos/lietuvoje/2/2888210/lietuvoje-prasidejo-savanorisku-ginklu-turimumo-patikrinimu-kampanija",
        "https://www.lrt.lt/naujienos/lietuvoje/2/2888195/prie-laisves-alos-vilniuje-vykdomi-darbai-pakeistas-eismo-organizavimas",
        "https://www.lrt.lt/naujienos/kultura/3/2888097/zmoniu-skundus-del-netinkamu-svietimo-istaigu-vadovu-veiksmu-tirs-speciali-komisija",
        "https://www.lrt.lt/naujienos/verslas/4/2888015/seime-pristatyta-lietuvos-kariuomenes-perejimo-prie-grandinines-ammunijos-gamybos-koncepcija",
        "https://www.lrt.lt/naujienos/lietuvoje/2/2887886/vilniaus-meras-is-gaisrininku-gauta-informacija-kad-is-ivykio-vietos-pasalintas-zmogus-turejo-buti-likviduotas",
        "https://www.lrt.lt/naujienos/pasaulis/5/2887827/karoukrainoj bus-tęsiamos-derybos-del-tautos-suvienijimo-vykdant-tikslingus-antpuolius-tikimasi-sulaukti-artimiausiomis-dienomis",
        "https://www.lrt.lt/naujienos/mokslas-ir-it/6/2887716/tema-ir-keliai-kurias-rinkosi-valstybe-galuty-galimybe-pasirinkti-geriausia-kelias-i-pries-sakiama-nauja-erdve",
        "https://www.lrt.lt/naujienos/kultura/3/2887693/parodos-restauravimo-vilniuje-vykdomas-specialus-projektas-atveria-naujas-erdves",
    ]
    
    collected = len(list(HUMAN_DIR.glob("lrt_*.txt")))
    for url in urls:
        if collected >= 15:
            break
        print(f"  Trying: {url[:60]}...")
        text = get_article(url)
        if text:
            filename = HUMAN_DIR / f"lrt_news_{collected+1}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"    Saved: {len(text)} chars")
            collected += 1
        time.sleep(1)
    return collected - len(list(HUMAN_DIR.glob("lrt_*.txt")))

def collect_government():
    """Collect from Lithuanian government sources."""
    print("Collecting from government sources...")
    urls = [
        "https://www.lrs.lt/sip/portal.show?p_r=35896&p_k=1&p_a=5&p_p_id=107588&p_tv=GA",
        "https://www.lrs.lt/sip/portal.show?p_r=35896&p_k=1&p_a=5&p_p_id=107587&p_tv=GA",
        "https://www.lrs.lt/sip/portal.show?p_r=35896&p_k=1&p_a=5&p_p_id=107586&p_tv=GA",
    ]
    
    collected = len(list(HUMAN_DIR.glob("gov_*.txt")))
    for url in urls:
        print(f"  Trying government document...")
        text = get_article(url)
        if text:
            filename = HUMAN_DIR / f"gov_{collected+1}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"    Saved: {len(text)} chars")
            collected += 1
        time.sleep(1)
    return collected

def create_more_ai_samples():
    """Create more AI-like samples."""
    print("Creating more AI samples...")
    
    ai_samples = [
        """Klimato kaita yra viena iš svarbiausių pasaulio problemų šiandien. Mokslininkai įspėja, kad pasaulinis temperatūros kilimas gali turėti rimtų pasekmių žmonijai. Lietuva taip pat jaučia klimato kaitos poveikį.

Pastaraisiais metais pastebimi vis dažnesni ekstremalūs orai. Vasaros tampa karštesnės, o žiemos šiltesnės. Be to, kritulių kiekis keičiasi netolygiai, kas daro įtaką žemės ūkiui.

Išvadai, klimato kaitos problemos sprendimas reikalauja tarptautinio bendradarbiavimo. Lietuva dalyvauja įvairiose iniciatyvose, skirtose šiai problemai spręsti. Svarbu paminėti, kad kiekvienas žmogus gali prisidėti prie aplinkos apsaugos.""",

        """Sveikatos priežiūros sistema Lietuvoje pergyvena reikšmingus pokyčius. Naujos technologijos leidžia gerinti paslaugų kokybę ir prieinamumą. Telemedicinos paslaugos tampa vis populiaresnės tarp pacientų.

Lietuvos ligoninės modernizuojamos ir aprūpinamos nauja įranga. Be to, vykdomos įvairios prevencinės programos, skirtos užkirsti kelią ligoms. Svarbu paminėti, kad sveikos gyvensenos skatinimas yra vienas iš prioritetų.

Apskritai, sveikatos priežiūros plėtra yra svarbi šalies raidai. Investicijos į šią sritį pagerina gyventojų sveikatą ir gyvenimo kokybę. Ateities perspektyvos atrodo optimistiškai.""",

        """Transportas yra svarbi Lietuvos ekonomikos dalis. Šalis turi gerai išvystytą kelių tinklą, jungiantį visas didžiąsias miestas. Be to, geležinkelių transportas plėtojamas siekiant užtikrinti efektyvų krovinių pervežimą.

Vilniaus oro uostas yra didžiausias šalyje ir aptarnauja milijonus keleivių kasmet. Tarptautiniai skrydžiai jungia Lietuvą su daugeliu Europos miestų. Be to, vykdomi oro uosto plėtros projektai.

Išvadai, transporto infrastruktūros plėtra yra būtina šalies konkurencingumui užtikrinti. Vyriausybė investuoja į naujus projektus ir esamų infrastruktūros objektų modernizavimą. Svarbu paminėti, kad tvarus transportas tampa vis svarbesnis.""",

        """Mažosios ir vidutinės įmonės yra Lietuvos ekonomikos stuburas. Šios įmonės kuria daugumą darbo vietų ir prisideda prie šalies BVP augimo. Verslo aplinka Lietuvoje palanki verslo plėtrai.

Vyriausybė įgyvendina įvairias verslo paramos programas. Pavyzdžiui, teikiamos subsidijos naujoms įmonėms steigti ir esamoms plėsti. Be to, organizuojami mokymai ir konsultacijos verslininkams.

Apskritai, verslo plėtra yra svarbi Lietuvos ekonomikai. Naujos įmonės kuria inovacijas ir stiprina šalies konkurencingumą tarptautinėje arenoje. Investicijos į verslą yra investicijos į ateitį.""",

        """Turizmas Lietuvoje auga kiekvienais metais. Šalis pritraukia turistus savo unikalia kultūra, istorija ir gamta. Vilnius, Kaunas ir Klaipėda yra populiariausi turistų lankomi miestai.

Senamiestis Vilniuje yra įtrauktas į UNESCO pasaulio paveldo sąrašą. Turistai gali grožėtis architektūros paminklais, lankyti muziejus ir dalyvauti kultūriniuose renginiuose. Be to, Lietuvos gamta siūlo įvairias poilsiavimo galimybes.

Išvadai, turizmo sektorius turi didelį potencialą augti. Vyriausybė remia turizmo plėtrą ir investuoja į infrastruktūros gerinimą. Svarbu paminėti, kad tvarus turizmas yra prioritetas ateityje.""",

        """Švietimas yra kiekvienos valstybės pagrindas. Lietuvoje švietimo sistema nuolat tobulinama siekiant užtikrinti kokybišką išsilavinimą visiems mokiniams. Nauji mokymo metodai ir technologijos diegiami mokyklose.

Universitetai siūlo įvairias studijų programas, pritaikytas šiuolaikinės rinkos poreikiams. Studentai gali rinktis įvairias specialybes nuo technologijų iki humanitarinių mokslų. Be to, vykdomos mokslinio tyrimo programos.

Apskritai, išsilavinimas yra investicija į ateitį. Lietuvos švietimo įstaigos siekia rengti kompetentingus specialistus, galinčius konkuruoti tarptautinėje darbo rinkoje. Svarbu paminėti, kad tęstinis mokymasis tampa vis svarbesnis.""",

        """Kultūra ir menas yra neatsiejama Lietuvos tapatybės dalis. Šalis turi turtingą kultūros paveldą, kurį sudaro istoriniai paminklai, literatūra ir tradicijos. Lietuvių kalba yra viena seniausių indoeuropiečių kalbų.

Vilnius yra svarbus kultūros centras, kuriame vyksta įvairūs festivaliai ir parodos. Nacionalinis dramos teatras, operos ir baleto teatras bei filharmonija siūlo aukšto lygio pasirodymus. Be to, veikia daug muziejų ir galerijų.

Išvadai, kultūros vaidmuo visuomenėje yra labai svarbus. Kultūra vienija žmones ir perduoda vertybes iš kartos į kartą. Vyriausybė remia kultūros plėtrą ir menininkų veiklą.""",

        """Sportas Lietuvoje turi gilias tradicijas. Krepšinis yra laikomas antrąja religija šalyje. Lietuvos rinktinė yra pasiekusi daug pergalių tarptautinėse varžybose. Be to, šalis turi stiprių atstovų ir kitose sporto šakose.

Olimpinės žaidynės yra svarbiausias sporto įvykis, kuriame Lietuva dalyvauja nuo nepriklausomybės atkūrimo. Lietuvos sportininkai yra iškovoję daugybę medalių įvairiose sporto šakose. Svarbu paminėti, kad sportas skatina sveiką gyvenseną.

Apskritai, sportas turi didelę įtaką visuomenei. Jis ne tik stiprina sveikatą, bet ir ugdo charakterį bei komandinę dvasią. Vyriausybė remia sporto plėtrą ir jaunųjų sportininkų rengimą.""",

        """Žemės ūkis yra svarbi Lietuvos ekonomikos šaka. Šalis turi palankias sąlygas žemės ūkio veiklai dėl derlingų dirvožemių ir tinkamo klimato. Pagrindinės auginamos kultūros yra javai, bulvės ir rapsai.

Lietuvos ūkininkai taiko modernias žemės ūkio technologijas, siekdami padidinti derlių ir sumažinti aplinkos taršą. Be to, plėtojamas ekologinis žemės ūkis, kurio produkcija vis labiau vertinama vartotojų.

Išvadai, žemės ūkio sektorius turi gerą potencialą augti. Europos Sąjungos parama leidžia ūkininkams modernizuoti ūkius ir įgyvendinti inovacijas. Svarbu užtikrinti, kad žemės ūkio plėtra būtų tvari ir darni.""",

        """Energetika yra strategiškai svarbi sritis Lietuvos ekonomikai. Šalis siekia energetinės nepriklausomybės, plėtodama atsinaujinančių energijos šaltinių gamybą. Vėjo ir saulės elektrinių skaičius kasmet didėja.

Nepriklausomo elektros tiekimo užtikrinimas buvo svarbus Lietuvos energetikos sektoriaus pasiekimas. Be to, vykdomi projektai, skirti gamtinių dujų tiekimo diversifikavimui. Klaipėdos suskystintų gamtinių dujų terminalas yra svarbus infrastruktūros objektas.

Apskritai, energetikos sektoriaus plėtra yra būtina šalies saugumui užtikrinti. Investicijos į atsinaujinančius energijos šaltinius prisideda prie klimato tikslų įgyvendinimo. Svarbu paminėti, kad energetinė efektyvumas tampa vis svarbesnis.""",
    ]
    
    existing = len(list(AI_DIR.glob("*.txt")))
    for i, text in enumerate(ai_samples):
        filename = AI_DIR / f"ai_sample_{existing + i + 1}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  Created AI sample {existing + i + 1}: {len(text)} chars")
    
    return len(ai_samples)

def main():
    print("Collecting more Lithuanian samples...")
    print()
    
    human_count = len(list(HUMAN_DIR.glob("*.txt")))
    ai_count = len(list(AI_DIR.glob("*.txt")))
    print(f"Starting with: {human_count} human, {ai_count} AI samples")
    print()
    
    collect_more_lrt()
    collect_government()
    create_more_ai_samples()
    
    print()
    print("=" * 50)
    human_count = len(list(HUMAN_DIR.glob("*.txt")))
    ai_count = len(list(AI_DIR.glob("*.txt")))
    print(f"Final: {human_count} human, {ai_count} AI samples")
    print("=" * 50)

if __name__ == "__main__":
    main()
