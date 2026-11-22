#!/usr/bin/env python3
r"""
Importe des journaux de relevés dans le tableur.

Formats reconnus (on peut en donner plusieurs à la fois, de plusieurs testeurs) :
  - randomizer_journal.txt     (DLL)         lignes « Non repertorie » et « Releve auto » (mode relevé)
  - journal_non_repertorie.txt (Cheat Engine, appliquer_seed.lua)
  - journal_objets.txt         (Cheat Engine, journal_objets.lua) : « chemin=pose … brut10-2C=8 valeurs »

Onglet « Emplacements » : un emplacement = une pièce + son empreinte (8 valeurs fixes), pour un personnage
et une difficulté. Ceux déjà présents, ou en double dans les journaux, sont ignorés. Les objets « directs »
(sans empreinte) ne sont pas importés. Les ids absents de l'onglet « Objets » y sont ajoutés, avec leur nom
officiel lu dans les textes du jeu installé (noms_jeu.py) ; « (à nommer) » si le jeu n'est pas trouvé.

Onglet « Pièces relevées » : chaque ligne « Releve piece X : N objet(s) » du mode relevé (même une pièce
vide) y est notée pour le personnage et la difficulté donnés. Avec --nouvelle-partie, le relevé est
marqué complet (« Nouvelle partie = oui ») : c'est ce qui compte pour les barres d'avancement.

Avant d'écrire, une copie du tableur est faite dans sauvegardes\.

Utilisation :
    python importer_journal.py journal.txt [autres…]                 (aperçu, rien n'est écrit)
    python importer_journal.py journal.txt --ecrire                  (ajoute au tableur)
    options : --personnage Chris|Jill   --difficulte Facile|…   --nouvelle-partie
              --source "testeur Paul"   --fichier donnees.xlsx
"""
import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook

FICHIER_PAR_DEFAUT = Path(__file__).resolve().parent.parent / "donnees_randomizer_RE1.xlsx"
PERSONNAGES = ("Chris", "Jill")
DIFFICULTES = ("Très facile", "Facile", "Normal", "Difficile", "Real Survival")
HEX8 = r"[0-9A-Fa-f]{8}"
MOTIF_PIECE = re.compile(r"piece=([0-9A-Fa-f]+)")
MOTIF_ID = re.compile(r"\bid=(\d+)")
MOTIF_QTE = re.compile(r"\bqte=(\d+)")
MOTIF_HEURE = re.compile(r"^(\d{2}:\d{2}:\d{2})")
MOTIF_NUM = re.compile(r"\bnum=(\d+)")
MOTIF_VISITE = re.compile(r"Releve piece ([0-9A-Fa-f]+) : (\d+) objet")
# DLL v0.8.9+ : « Partie  perso=N  diff=N » (valeurs du jeu ; correspondance avec Chris/Jill et les difficultés
# à confirmer avant de s'en servir pour choisir le scénario tout seul)
MOTIF_PARTIE = re.compile(r"\tPartie\tperso=(\d+)\tdiff=(\d+)")
MOTIFS_EMPREINTE = (
    re.compile(rf"valeurs=[0-9A-Fa-f]+:((?:{HEX8},){{7}}{HEX8})"),     # DLL et appliquer_seed.lua
    re.compile(rf"brut10-2C=((?:{HEX8}\s+){{7}}{HEX8})"),               # journal_objets.lua
)
MOTIF_EMPREINTE_TABLEUR = re.compile(rf"brut \+0x10\.\.\+0x2C = ((?:{HEX8}\s*){{8}})")

# colonnes de l'onglet « Emplacements » (1 = A)
COL = dict(numero=1, piece=2, nom_piece=3, desc=4, ident=5, nom_obj=6, qte=7, chemin=8, verrou=9,
           statut=10, empreinte=11, remarque=12, personnage=13, difficulte=14)
# colonnes de l'onglet « Pièces relevées »
PR = dict(piece=1, nom=2, personnage=3, difficulte=4, nouvelle=5, objets=6, date=7, source=8)


def lire_journal(chemin):
    """Renvoie (relevés d'objets, visites de pièces en mode relevé, nb de lignes « directes » ignorées)."""
    releves, visites, directs = [], [], 0
    for ligne in Path(chemin).read_text(encoding="utf-8", errors="replace").splitlines():
        v = MOTIF_VISITE.search(ligne)
        if v:
            visites.append({"piece": v.group(1).lower(), "objets": int(v.group(2))})
            continue
        if "chemin=direct" in ligne:
            directs += 1
            continue
        empreinte = None
        for motif in MOTIFS_EMPREINTE:
            m = motif.search(ligne)
            if m:
                empreinte = [x.upper() for x in re.split(r"[,\s]+", m.group(1).strip())]
                break
        p, i = MOTIF_PIECE.search(ligne), MOTIF_ID.search(ligne)
        if not (empreinte and p and i):
            continue
        q, h, num = MOTIF_QTE.search(ligne), MOTIF_HEURE.search(ligne), MOTIF_NUM.search(ligne)
        releves.append({
            "piece": p.group(1).lower(), "id": int(i.group(1)),
            "qte": int(q.group(1)) if q else None,
            "empreinte": empreinte, "heure": h.group(1) if h else "?",
            "fichier": Path(chemin).name,
            "num": int(num.group(1)) if num else None,
            "auto": "Releve auto" in ligne,
        })
    return releves, visites, directs


def scenario_ligne(valeurs, col_perso, col_diff):
    """Personnage et difficulté d'une ligne (vide = Chris / Facile, comme les premiers relevés)."""
    return (str(valeurs[col_perso - 1] or "Chris"), str(valeurs[col_diff - 1] or "Facile"))


def deja_connus(ws):
    """{(pièce, empreinte, perso, difficulté): {ids des objets connus à cette zone}}.
    Plusieurs objets peuvent partager une même zone (ex. les 3 symboles de la même tombe, 312) : on les
    distingue par leur ID. (Pas par le « n° d'objet » num : il change quand on ramasse d'autres objets de la
    pièce, constaté le 19/11/2026 avec le spray de l'abri de jardin 11B, n° 2 puis n° 1.)"""
    connus = {}
    for ligne in ws.iter_rows(min_row=2, values_only=True):
        ligne = tuple(ligne) + (None,) * 14
        piece, empreinte = ligne[COL["piece"] - 1], ligne[COL["empreinte"] - 1]
        m = MOTIF_EMPREINTE_TABLEUR.search(str(empreinte or ""))
        if piece and m:
            cle = ((str(piece).lower(), tuple(v.upper() for v in m.group(1).split()))
                   + scenario_ligne(ligne, COL["personnage"], COL["difficulte"]))
            ident = ligne[COL["ident"] - 1]
            connus.setdefault(cle, set()).add(int(ident) if isinstance(ident, (int, float)) else None)
    return connus


def noms_du_jeu():
    """Noms officiels {id: nom} en français et en anglais, lus dans le jeu installé ({} si introuvable)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import generateur_seed as gen
        import noms_jeu
        jeu = gen.trouver_dossier_jeu()
        if jeu:
            return noms_jeu.lire_noms(jeu, "fr"), noms_jeu.lire_noms(jeu, "en")
    except Exception as e:  # jeu absent, autre version des fichiers… : on garde « (à nommer) »
        print(f"(noms des objets non lus dans le jeu : {e})")
    return {}, {}


def premiere_ligne_libre(ws, colonne):
    derniere = max((r for r in range(2, ws.max_row + 1) if ws.cell(r, colonne).value), default=1)
    return derniere + 1


def formule(colonne_source, onglet, colonne_resultat, ligne, fin):
    return (f'=IFERROR(INDEX({onglet}!${colonne_resultat}$2:${colonne_resultat}${fin},'
            f'MATCH({colonne_source}{ligne},{onglet}!$A$2:$A${fin},0)),"")')


def main():
    ap = argparse.ArgumentParser(description="Importe des journaux de relevés dans le tableur")
    ap.add_argument("journaux", nargs="+", help="fichiers journaux à importer")
    ap.add_argument("--fichier", default=str(FICHIER_PAR_DEFAUT), help="tableur de données")
    ap.add_argument("--personnage", default="Chris", choices=PERSONNAGES, help="personnage de la partie relevée")
    ap.add_argument("--difficulte", default="Facile", choices=DIFFICULTES, help="difficulté de la partie relevée")
    ap.add_argument("--nouvelle-partie", action="store_true",
                    help="le relevé a été fait en nouvelle partie (rien encore ramassé) : pièces relevées complètes")
    ap.add_argument("--source", default="", help="qui a fait le relevé (noté dans les remarques)")
    ap.add_argument("--ecrire", action="store_true", help="écrit dans le tableur (sinon simple aperçu)")
    args = ap.parse_args()
    scenario = (args.personnage, args.difficulte)

    tableur = Path(args.fichier)
    if not tableur.exists():
        sys.exit(f"Tableur introuvable : {tableur}")
    wb = load_workbook(tableur)
    ws, objets = wb["Emplacements"], wb["Objets"]
    pr = wb["Pièces relevées"] if "Pièces relevées" in wb.sheetnames else None
    connus = deja_connus(ws)
    # Une zone de ramassage n'appartient qu'à une pièce : celle où elle a été vue en premier. Revue ailleurs,
    # c'est un « fantôme » : l'objet de la pièce précédente encore en mémoire au moment du relevé (constaté le
    # 18/11/2026 : l'herbe de l'escalier est (207) notée aussi en 118, 204 et 20B).
    piece_de_zone = {}                                          # (empreinte, perso, difficulté) -> pièce
    for ligne in ws.iter_rows(min_row=2, values_only=True):    # les lignes déjà marquées « fantôme » ne comptent pas
        ligne = tuple(ligne) + (None,) * 14
        m = MOTIF_EMPREINTE_TABLEUR.search(str(ligne[COL["empreinte"] - 1] or ""))
        if ligne[COL["piece"] - 1] and m and ligne[COL["chemin"] - 1] != "fantôme":
            piece_de_zone.setdefault((tuple(v.upper() for v in m.group(1).split()),)
                                     + scenario_ligne(ligne, COL["personnage"], COL["difficulte"]),
                                     str(ligne[COL["piece"] - 1]).lower())
    noms_pieces = {str(r[0]).lower(): r[3] for r in wb["Pièces"].iter_rows(min_row=2, values_only=True) if r[0]}
    ids_objets = {objets.cell(r, 1).value for r in range(2, objets.max_row + 1)}

    nouveaux, doublons, directs, visites, fantomes = [], 0, 0, {}, []
    for j in args.journaux:
        if not Path(j).exists():
            sys.exit(f"Journal introuvable : {j}")
        releves, vis, d = lire_journal(j)
        directs += d
        for v in vis:                        # une pièce revisitée : on garde le plus grand nombre d'objets
            visites[v["piece"]] = max(visites.get(v["piece"], 0), v["objets"])
        # ids vus EN MÊME TEMPS à une même zone (même relevé automatique : même heure, même pièce)
        ensemble = {}
        for r in releves:
            if r["auto"]:
                ensemble.setdefault((r["heure"], r["piece"], tuple(r["empreinte"])), set()).add(r["id"])
        for r in releves:
            cle = (r["piece"], tuple(r["empreinte"])) + scenario
            ids = connus.get(cle)
            # Zone déjà connue : un AUTRE id n'est un nouvel objet que s'il est vu en même temps qu'un id déjà
            # connu à cette zone (ex. les 3 symboles d'une tombe, 312). Sinon c'est le même emplacement qui a
            # changé d'objet (ex. le fusil du salon échangé contre le fusil cassé, 116) : doublon.
            if ids is not None:
                vus = ensemble.get((r["heure"], r["piece"], tuple(r["empreinte"])), set()) if r["auto"] else set()
                if r["id"] in ids or ids == {None} or not (vus - {r["id"]}) & ids:
                    doublons += 1
                    continue
            autre = piece_de_zone.get(cle[1:])
            if autre and autre != r["piece"]:
                fantomes.append((r, autre))
                continue
            connus.setdefault(cle, set()).add(r["id"])
            piece_de_zone[cle[1:]] = r["piece"]
            nouveaux.append(r)

    # Pièces relevées : nouvelles lignes, ou passage à « Nouvelle partie = oui »
    pieces_nouvelles, pieces_completees, lignes_pr = [], [], {}
    if pr is not None:
        for r in range(2, pr.max_row + 1):
            p = pr.cell(r, PR["piece"]).value
            if p:
                lignes_pr[(str(p).lower(), str(pr.cell(r, PR["personnage"]).value or "Chris"),
                           str(pr.cell(r, PR["difficulte"]).value or "Facile"))] = r
        for piece in sorted(visites):
            r = lignes_pr.get((piece,) + scenario)
            if r is None:
                pieces_nouvelles.append(piece)
            elif args.nouvelle_partie and pr.cell(r, PR["nouvelle"]).value != "oui":
                pieces_completees.append(piece)

    vus = set()
    for j in args.journaux:
        for ligne in Path(j).read_text(encoding="utf-8", errors="replace").splitlines():
            m = MOTIF_PARTIE.search(ligne)
            if m:
                vus.add((int(m.group(1)), int(m.group(2))))
    if vus:
        print("Valeurs du jeu notées par la DLL (perso, diff) : " + ", ".join(f"{a}, {b}" for a, b in sorted(vus)))
    print(f"Scénario : {args.personnage} / {args.difficulte}"
          + (" (nouvelle partie)" if args.nouvelle_partie else " (partie déjà commencée)"))
    print(f"{len(nouveaux)} nouvel(s) emplacement(s), {doublons} déjà connu(s) ou en double"
          + (f", {directs} objet(s) « direct(s) » ignoré(s) (pas d'empreinte)" if directs else "") + ".")
    for r, autre in fantomes:
        print(f"  fantôme ignoré : [{r['piece'].upper():>3}] id {r['id']} — zone déjà relevée en {autre.upper()}")
    noms_apercu = noms_du_jeu()[0] if nouveaux else {}
    for r in nouveaux:
        qte = "?" if r["qte"] is None else r["qte"]
        inconnu = "" if r["id"] in ids_objets else "   <- id nouveau"
        nom = f" ({noms_apercu[r['id']]})" if r["id"] in noms_apercu else ""
        print(f"  [{r['piece'].upper():>3}] {noms_pieces.get(r['piece'], '?')}: id {r['id']}{nom} x{qte}{inconnu}")
    if pr is not None:
        print(f"{len(pieces_nouvelles)} pièce(s) relevée(s) à ajouter, {len(pieces_completees)} à marquer complète(s)"
              + (f" : {', '.join(p.upper() for p in pieces_nouvelles + pieces_completees)}"
                 if pieces_nouvelles or pieces_completees else "") + ".")
    if not (nouveaux or pieces_nouvelles or pieces_completees):
        return
    if not args.ecrire:
        print("\nAperçu seulement : relance avec --ecrire pour les ajouter au tableur.")
        return

    sauvegarde = tableur.parent / "sauvegardes" / f"{tableur.stem}_avant_import_{datetime.now():%Y-%m-%d_%H%M%S}.xlsx"
    sauvegarde.parent.mkdir(exist_ok=True)
    shutil.copyfile(tableur, sauvegarde)

    date = datetime.now().strftime("%d/%m/%Y")
    source = f" par {args.source}" if args.source else ""
    ligne = premiere_ligne_libre(ws, COL["piece"])
    numero = max((c.value for c in ws["A"][1:] if isinstance(c.value, int)), default=0)
    for r in nouveaux:
        numero += 1
        if ws.cell(ligne, COL["numero"]).value is None:
            ws.cell(ligne, COL["numero"]).value = numero
        # Les lignes préparées ont déjà les formules ; au-delà, on les ajoute.
        if not ws.cell(ligne, COL["nom_piece"]).value:
            ws.cell(ligne, COL["nom_piece"]).value = formule("B", "Pièces", "D", ligne, 119)
        if not ws.cell(ligne, COL["nom_obj"]).value:
            ws.cell(ligne, COL["nom_obj"]).value = formule("E", "Objets", "C", ligne, 300)
        ws.cell(ligne, COL["piece"]).value = r["piece"]
        ws.cell(ligne, COL["desc"]).value = (f"Objet n°{r['num']} de la pièce, position à décrire"
                                             if r["num"] else "(position à décrire)")
        ws.cell(ligne, COL["ident"]).value = r["id"]
        ws.cell(ligne, COL["qte"]).value = r["qte"]
        ws.cell(ligne, COL["chemin"]).value = "posé"
        ws.cell(ligne, COL["statut"]).value = "relevé"
        ws.cell(ligne, COL["empreinte"]).value = "brut +0x10..+0x2C = " + " ".join(r["empreinte"])
        ws.cell(ligne, COL["remarque"]).value = (f"Importé{source} le {date} depuis {r['fichier']} "
                                                 f"(ligne de {r['heure']})."
                                                 + (" Relevé automatique à l'entrée de la pièce." if r["auto"] else "")
                                                 + ("" if r["qte"] is not None else " Quantité absente du journal."))
        ws.cell(ligne, COL["personnage"]).value = args.personnage
        ws.cell(ligne, COL["difficulte"]).value = args.difficulte
        ligne += 1

    libre = next((i for i in range(2, objets.max_row + 2) if objets.cell(i, 1).value is None), objets.max_row + 1)
    noms_fr, noms_en = noms_du_jeu()
    for ident in sorted({r["id"] for r in nouveaux} - ids_objets):
        exemple = next(r for r in nouveaux if r["id"] == ident)
        objets.cell(libre, 1).value = ident
        objets.cell(libre, 2).value = f"=DEC2HEX(A{libre})"
        objets.cell(libre, 3).value = noms_fr.get(ident, "(à nommer)")
        objets.cell(libre, 4).value = "vu en jeu"
        qte = "inconnue" if exemple["qte"] is None else exemple["qte"]
        objets.cell(libre, 5).value = (f"Posé en {exemple['piece'].upper()}, quantité {qte} (import du {date})."
                                       + (" Nom tiré des textes du jeu." if ident in noms_fr else " Objet à nommer."))
        if ident in noms_fr:
            objets.cell(libre, 6).value = noms_fr[ident]
            objets.cell(libre, 7).value = noms_en.get(ident)
        libre += 1

    if pr is not None:
        noms_journaux = ", ".join(Path(j).name for j in args.journaux)
        for piece in pieces_completees:
            r = lignes_pr[(piece,) + scenario]
            pr.cell(r, PR["nouvelle"]).value = "oui"
            pr.cell(r, PR["objets"]).value = visites[piece]
            pr.cell(r, PR["date"]).value = date
            pr.cell(r, PR["source"]).value = f"Complété{source} depuis {noms_journaux}"
        r = premiere_ligne_libre(pr, PR["piece"])
        for piece in pieces_nouvelles:
            pr.cell(r, PR["piece"]).value = piece
            pr.cell(r, PR["nom"]).value = noms_pieces.get(piece, "")
            pr.cell(r, PR["personnage"]).value = args.personnage
            pr.cell(r, PR["difficulte"]).value = args.difficulte
            pr.cell(r, PR["nouvelle"]).value = "oui" if args.nouvelle_partie else "non"
            pr.cell(r, PR["objets"]).value = visites[piece]
            pr.cell(r, PR["date"]).value = date
            pr.cell(r, PR["source"]).value = f"Importé{source} depuis {noms_journaux}"
            r += 1

    wb.calculation.fullCalcOnLoad = True       # Excel recalcule les formules à l'ouverture
    wb.save(tableur)
    print(f"\nAjouté au tableur. Copie de l'ancien fichier : {sauvegarde}")


if __name__ == "__main__":
    main()
