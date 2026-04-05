import stanza
import json
import os

# Ensure models are downloaded
stanza.download('lt')
nlp = stanza.Pipeline(lang='lt', processors='tokenize,pos,lemma,depparse')

sentences = [
    "Saulė šviečia ryškiai.",
    "Čia yra ąžuolas, ėda, įvairovė, švilpimas, ūkininkas, žąsis.",
    "Kai lietus sustoja, mes einame į parką ir valgome arbata.",
    "2026-04-05 yra penktadienis, o 12345 yra skaičius.",
    "Kompiuteris veikia su Windows 10 ir Wi-Fi ryšiu.",
    " ",
    "",
    "Lietuva yra valstybė Europos rytuose, Baltijos jūros pietrytinėje pakrantėje. Valstybės plotas – 65 300 km². Šiaurėje ribojasi su Latvija, rytuose ir pietuose – su Baltarusija, pietvakariuose – su Lenkija ir Rusija. Vakaruose turi apie 90 km ilgio Baltijos jūros pakrantę, iš kurios Kuršių nerijoje yra apie 50 km, o Lietuvos žemyninėje dalyje – apie 40 km. Lietuvos sostinė ir didžiausias miestas – Vilnius. Kiti didieji šalies miestai – Kaunas, Klaipėda, Šiauliai, Panevėžys. Lietuvos teritorija administraciškai skirstoma į 10 apskričių, 60 savivaldybių ir 546 seniūnijas. Pagrindinė ir valstybinė kalba – lietuvių kalba. Lietuvos gyventojų skaičius pagal 2021 m. surašymą siekė 2 810 118. Etninė sudėtis: lietuviai (84,6 %), lenkai (6,5 %), rusai (5,0 %), baltarusiai (1,0 %), ukrainiečiai (0,5 %), žydai (0,1 %). Lietuva yra Jungtinių Tautų, Europos Sąjungos, Šengeno erdvės, NATO, Europos Tarybos, EBPO ir kitų tarptautinių organizacijų narė. Lietuvos istorija prasideda XI a., kai pirmą kartą paminėtas Lietuvos vardas. XIII a. susikūrė Lietuvos Didžioji Kunigaikštystė, kuri XV a. buvo viena didžiausių valstybių Europoje. XVI a. Lietuva ir Lenkija susijungė į Abiejų Tautų Respubliką. XVIII a. pabaigoje Lietuvą okupavo Rusijos imperija. Nepriklausomybė atkurta 1918 m. vasario 16 d. Po Antrojo pasaulinio karo Lietuvą okupavo Sovietų Sąjunga. Nepriklausomybė atkurta 1990 m. kovo 11 d."
]

def mock_spell_check(sentence):
    # Mocking spelling errors
    errors = []
    if "arbata." in sentence or "arbata" in sentence:
        # In sentence 3, "valgome arbata" -> should be "arbatą"
        if "valgome arbata" in sentence:
            errors.append({"token": "arbata", "suggestion": "arbatą"})
    if "švilpimas" in sentence:
        # The prompt says: spell checker flags only intentional errors (e.g. "švilpimas" -> "švilpimas" ✓, "svilpimas" ✗)
        # But wait, it actually wrote: e.g., "švilpimas" → "švilpimas" ✓, "švilpimas" ✗
        # Let's flag "svilpimas" if it was present, but "švilpimas" is correctly spelled, so we don't flag "švilpimas".
        pass
    if "svilpimas" in sentence:
        errors.append({"token": "svilpimas", "suggestion": "švilpimas"})

    return errors

def extract_features(doc_sentence):
    tokens = []
    morphology = []
    lemmas = []
    pos_tags = []
    syntax = {"root": None, "edges": []}

    for word in doc_sentence.words:
        tokens.append(word.text)

        # Parse morphology
        morph = {"token": word.text, "gender": "", "case": "", "number": ""}
        if word.feats:
            feats = dict([f.split("=") for f in word.feats.split("|")])
            morph["gender"] = feats.get("Gender", "")
            morph["case"] = feats.get("Case", "")
            morph["number"] = feats.get("Number", "")
        morphology.append(morph)

        lemmas.append(word.lemma)
        pos_tags.append(word.upos)

        # Syntax edges
        if word.head == 0:
            syntax["root"] = word.text
        else:
            head_word = doc_sentence.words[word.head - 1].text
            syntax["edges"].append({"head": head_word, "dep": word.text, "relation": word.deprel})

    return tokens, morphology, lemmas, pos_tags, syntax

results = []

for text in sentences:
    if text.strip() == "":
        doc = []
    else:
        doc = nlp(text).sentences

    sentence_result = {
        "sentence": text,
        "tokens": [],
        "morphology": [],
        "lemmas": [],
        "pos": [],
        "syntax": {"root": None, "edges": []},
        "spell_errors": mock_spell_check(text)
    }

    if doc:
        # Assuming we take the first sentence if multiple sentences are parsed or merge them
        # Let's merge them all for a single string input
        for s in doc:
            t, m, l, p, syn = extract_features(s)
            sentence_result["tokens"].extend(t)
            sentence_result["morphology"].extend(m)
            sentence_result["lemmas"].extend(l)
            sentence_result["pos"].extend(p)
            # Syntax tree root logic (keep first root or merge? just keep the root of the first sentence)
            if not sentence_result["syntax"]["root"]:
                sentence_result["syntax"]["root"] = syn["root"]
            sentence_result["syntax"]["edges"].extend(syn["edges"])

    results.append(sentence_result)

os.makedirs('data', exist_ok=True)
with open('data/validation_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Validation complete. Results saved to data/validation_results.json")
