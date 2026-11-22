#!/usr/bin/env python3
r"""
Barres d'avancement des relevés, affichées sur la page GitHub (README).

Calcul, à partir du tableur :
  - pour chaque personnage et difficulté : pièces relevées en NOUVELLE partie (onglet « Pièces relevées »,
    « Nouvelle partie = oui ») sur le nombre total de pièces (onglet « Pièces »). C'est le pourcentage.
    Les pièces visitées en partie déjà commencée sont montrées en plus pâle (relevé incomplet).
  - armes bonus (onglet « Bonus ») : lignes dont l'ID objet est connu, sur toutes les lignes.

Produit images/progression.svg (français) et images/progression_en.svg (anglais), et remplace les sections
du README comprises entre <!-- progression:debut --> et <!-- progression:fin --> (partie française) et entre
<!-- progression-en:debut --> et <!-- progression-en:fin --> (partie anglaise).

    python Randomizer\progression.py            (appelé aussi par preparer_publication.py)
"""
import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from openpyxl import load_workbook

RACINE = Path(__file__).resolve().parent.parent
PERSONNAGES = ("Chris", "Jill")
DIFFICULTES = ("Très facile", "Facile", "Normal", "Difficile", "Real Survival")
BALISES = {"fr": ("<!-- progression:debut -->", "<!-- progression:fin -->"),
           "en": ("<!-- progression-en:debut -->", "<!-- progression-en:fin -->")}

# textes du graphique et du tableau, par langue
TEXTES = {
    "fr": {
        "titre": "Avancement des relevés",
        "sous_titre": "Pièces relevées en nouvelle partie, sur {n} pièces · mis à jour le {date}",
        "complete": "complète", "commencee": "partie commencée",
        "visitees": "+{n} visitées", "objets": "{n} objets",
        "bonus": "Armes bonus", "identifiees": "identifiées", "a_completer": "liste à compléter",
        "pct": "{p} %",
        "difficultes": dict(zip(DIFFICULTES, DIFFICULTES)),
        "detail": "Détail (texte)",
        "entete": "| Personnage | Difficulté | Pièces complètes | Visitées (partie commencée) | Objets relevés |",
        "pied": "Armes bonus : {bonus}. Mis à jour le {date}.",
        "date": "%d/%m/%Y",
    },
    "en": {
        "titre": "Survey progress",
        "sous_titre": "Rooms surveyed in a new game, out of {n} rooms · updated {date}",
        "complete": "complete", "commencee": "game in progress",
        "visitees": "+{n} visited", "objets": "{n} items",
        "bonus": "Bonus weapons", "identifiees": "identified", "a_completer": "list to be completed",
        "pct": "{p}%",
        "difficultes": dict(zip(DIFFICULTES, ("Very Easy", "Easy", "Normal", "Hard", "Real Survival"))),
        "detail": "Details (text)",
        "entete": "| Character | Difficulty | Complete rooms | Visited (game in progress) | Items surveyed |",
        "pied": "Bonus weapons: {bonus}. Updated {date}.",
        "date": "%Y-%m-%d",
    },
}

# mêmes couleurs que l'application
FOND, CARTE, BORD = "#15171c", "#1e2128", "#2c313b"
TEXTE, DISCRET, ACCENT, PALE, VIDE = "#e7e9ee", "#8a909c", "#b3262e", "#5a2a2e", "#262a33"
POLICE = "Segoe UI, Helvetica, Arial, sans-serif"


def calculer(fichier):
    wb = load_workbook(fichier, data_only=True)
    total_pieces = sum(1 for r in wb["Pièces"].iter_rows(min_row=2, values_only=True) if r[0])
    scenarios = {(p, d): {"completes": set(), "visitees": set(), "objets": 0}
                 for p in PERSONNAGES for d in DIFFICULTES}

    if "Pièces relevées" in wb.sheetnames:
        for piece, _, perso, diff, nouvelle, *_ in wb["Pièces relevées"].iter_rows(min_row=2, values_only=True):
            s = scenarios.get((str(perso or "Chris"), str(diff or "Facile")))
            if piece and s is not None:
                (s["completes"] if nouvelle == "oui" else s["visitees"]).add(str(piece).lower())
    for ligne in wb["Emplacements"].iter_rows(min_row=2, values_only=True):
        ligne = tuple(ligne) + (None,) * 14
        s = scenarios.get((str(ligne[12] or "Chris"), str(ligne[13] or "Facile")))
        if ligne[1] and ligne[4] is not None and s is not None:
            s["objets"] += 1

    bonus = []
    if "Bonus" in wb.sheetnames:
        bonus = [r for r in wb["Bonus"].iter_rows(min_row=2, values_only=True) if r[0]]
    return {
        "total_pieces": total_pieces,
        "scenarios": {k: {"completes": len(v["completes"]),
                          "visitees": len(v["visitees"] - v["completes"]),
                          "objets": v["objets"]} for k, v in scenarios.items()},
        "bonus_total": len(bonus),
        "bonus_connus": sum(1 for r in bonus if r[3] not in (None, "")),
    }


def dessiner_svg(res, date, langue="fr"):
    tx = TEXTES[langue]
    largeur, x_label, x_barre, l_barre, x_texte = 800, 28, 200, 300, 520
    haut_ligne, y0 = 30, 92
    lignes = [(p, d) for p in PERSONNAGES for d in DIFFICULTES]
    hauteur = y0 + len(lignes) * haut_ligne + 22 + 26
    t = res["total_pieces"] or 1
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{largeur}" height="{hauteur}" '
         f'viewBox="0 0 {largeur} {hauteur}" font-family="{POLICE}" role="img" '
         f'aria-label="{escape(tx["titre"])}">',
         f'<rect width="{largeur}" height="{hauteur}" rx="14" fill="{FOND}"/>',
         f'<rect x="8" y="8" width="{largeur - 16}" height="{hauteur - 16}" rx="10" fill="{CARTE}" stroke="{BORD}"/>',
         f'<text x="{x_label}" y="44" font-size="20" font-weight="700" fill="{TEXTE}">{escape(tx["titre"])}</text>',
         f'<text x="{x_label}" y="66" font-size="12" fill="{DISCRET}">'
         f'{escape(tx["sous_titre"].format(n=res["total_pieces"], date=date))}</text>',
         # légende
         f'<rect x="{largeur - 252}" y="36" width="12" height="12" rx="3" fill="{ACCENT}"/>'
         f'<text x="{largeur - 234}" y="46" font-size="12" fill="{DISCRET}">{tx["complete"]}</text>',
         f'<rect x="{largeur - 160}" y="36" width="12" height="12" rx="3" fill="{PALE}"/>'
         f'<text x="{largeur - 142}" y="46" font-size="12" fill="{DISCRET}">{tx["commencee"]}</text>']

    def barre(y, part_pleine, part_pale):
        o.append(f'<rect x="{x_barre}" y="{y - 11}" width="{l_barre}" height="12" rx="6" fill="{VIDE}"/>')
        lp, lpale = round(l_barre * part_pleine), round(l_barre * (part_pleine + part_pale))
        if lpale > 0:
            o.append(f'<rect x="{x_barre}" y="{y - 11}" width="{max(lpale, 6)}" height="12" rx="6" fill="{PALE}"/>')
        if lp > 0:
            o.append(f'<rect x="{x_barre}" y="{y - 11}" width="{max(lp, 6)}" height="12" rx="6" fill="{ACCENT}"/>')

    y = y0
    perso_precedent = None
    for p, d in lignes:
        s = res["scenarios"][(p, d)]
        nom = p if p != perso_precedent else ""
        perso_precedent = p
        o.append(f'<text x="{x_label}" y="{y}" font-size="14" font-weight="700" fill="{TEXTE}">{escape(nom)}</text>')
        o.append(f'<text x="{x_label + 52}" y="{y}" font-size="14" fill="{TEXTE}">{escape(tx["difficultes"][d])}</text>')
        barre(y, s["completes"] / t, s["visitees"] / t)
        pct = round(100 * s["completes"] / t)
        detail = f'{s["completes"]}/{res["total_pieces"]}'
        if s["visitees"]:
            detail += " · " + tx["visitees"].format(n=s["visitees"])
        if s["objets"]:
            detail += " · " + tx["objets"].format(n=s["objets"])
        o.append(f'<text x="{x_texte}" y="{y}" font-size="14" font-weight="700" fill="{TEXTE}">'
                 f'{tx["pct"].format(p=pct)}</text>')
        o.append(f'<text x="{x_texte + 46}" y="{y}" font-size="12" fill="{DISCRET}">{escape(detail)}</text>')
        y += haut_ligne
        if d == DIFFICULTES[-1] and p != PERSONNAGES[-1]:
            o.append(f'<line x1="{x_label}" y1="{y - 20}" x2="{largeur - x_label}" y2="{y - 20}" stroke="{BORD}"/>')

    y += 22
    o.append(f'<line x1="{x_label}" y1="{y - 30}" x2="{largeur - x_label}" y2="{y - 30}" stroke="{BORD}"/>')
    o.append(f'<text x="{x_label}" y="{y}" font-size="14" font-weight="700" fill="{TEXTE}">{tx["bonus"]}</text>')
    if res["bonus_total"]:
        barre(y, res["bonus_connus"] / res["bonus_total"], 0)
        o.append(f'<text x="{x_texte}" y="{y}" font-size="14" font-weight="700" fill="{TEXTE}">'
                 f'{res["bonus_connus"]}/{res["bonus_total"]}</text>')
        o.append(f'<text x="{x_texte + 46}" y="{y}" font-size="12" fill="{DISCRET}">{tx["identifiees"]}</text>')
    else:
        barre(y, 0, 0)
        o.append(f'<text x="{x_texte}" y="{y}" font-size="12" fill="{DISCRET}">{tx["a_completer"]}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def bloc_readme(res, date, chemin_image, langue="fr"):
    tx = TEXTES[langue]
    debut, fin = BALISES[langue]
    t = res["total_pieces"]
    lignes = [debut, "",
              f'<img src="{chemin_image}" alt="{tx["titre"]}" width="800">', "",
              f"<details><summary>{tx['detail']}</summary>", "",
              tx["entete"],
              "|---|---|---|---|---|"]
    for (p, d), s in res["scenarios"].items():
        pct = tx["pct"].format(p=round(100 * s["completes"] / (t or 1)))
        lignes.append(f"| {p} | {tx['difficultes'][d]} | {s['completes']}/{t} ({pct}) "
                      f"| {s['visitees']} | {s['objets']} |")
    bonus = (f"{res['bonus_connus']}/{res['bonus_total']} {tx['identifiees']}" if res["bonus_total"]
             else tx["a_completer"])
    lignes += ["", tx["pied"].format(bonus=bonus, date=date), "", "</details>", "", fin]
    return "\n".join(lignes)


def mettre_a_jour(fichier, readmes, image):
    """image : le graphique français ; l'anglais est écrit à côté, avec le suffixe _en (progression_en.svg).
    readmes : un ou plusieurs README ; chaque langue va dans celui qui contient ses balises (depuis le 22/11/2026 :
    README.md en anglais, docs/README.fr.md en français). Le lien vers l'image est relatif à chaque README."""
    if isinstance(readmes, (str, Path)):
        readmes = [readmes]
    res = calculer(fichier)
    maintenant = datetime.now()
    image.parent.mkdir(parents=True, exist_ok=True)
    trouvees = set()
    for readme in map(Path, readmes):
        brut = readme.read_bytes()
        crlf = b"\r\n" in brut
        texte = brut.decode("utf-8").replace("\r\n", "\n")
        for langue in ("fr", "en"):
            suffixe = "" if langue == "fr" else "_" + langue
            date = maintenant.strftime(TEXTES[langue]["date"])
            fichier_image = image.with_name(image.stem + suffixe + image.suffix)
            fichier_image.write_text(dessiner_svg(res, date, langue), encoding="utf-8", newline="\n")
            debut, fin = BALISES[langue]
            motif = re.compile(re.escape(debut) + r".*?" + re.escape(fin), re.S)
            if not motif.search(texte):
                continue
            trouvees.add(langue)
            chemin = Path(os.path.relpath(fichier_image, readme.parent)).as_posix()
            bloc = bloc_readme(res, date, chemin, langue)
            texte = motif.sub(lambda _: bloc, texte)
        readme.write_bytes((texte.replace("\n", "\r\n") if crlf else texte).encode("utf-8"))
    for langue in ("fr", "en"):
        if langue not in trouvees:
            raise SystemExit(f"Balises {BALISES[langue][0]} … absentes des README")
    return res


def main():
    ap = argparse.ArgumentParser(description="Met à jour les barres d'avancement du README")
    ap.add_argument("--fichier", default=str(RACINE / "donnees_randomizer_RE1.xlsx"))
    ap.add_argument("--readme", nargs="+", default=[str(RACINE / "README.md"), str(RACINE / "docs" / "README.fr.md")])
    ap.add_argument("--image", default=str(RACINE / "images" / "progression.svg"))
    args = ap.parse_args()
    res = mettre_a_jour(Path(args.fichier), args.readme, Path(args.image))
    for (p, d), s in res["scenarios"].items():
        if s["completes"] or s["visitees"] or s["objets"]:
            print(f"{p} / {d} : {s['completes']}/{res['total_pieces']} complètes, +{s['visitees']} visitées, "
                  f"{s['objets']} objets")
    print(f"Armes bonus : {res['bonus_connus']}/{res['bonus_total']}")
    print(f"Écrit : {args.image} (+ version _en) et les sections du README")


if __name__ == "__main__":
    main()
