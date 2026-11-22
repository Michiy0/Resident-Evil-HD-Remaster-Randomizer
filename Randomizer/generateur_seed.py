#!/usr/bin/env python3
"""
Générateur de seeds (version 0.2) pour le randomizer Resident Evil HD Remaster (Chris, Facile).

Ce que fait cette version :
  - lit les emplacements relevés dans donnees_randomizer_RE1.xlsx (onglet « Emplacements »),
  - mélange entre eux les objets "libres" (chargeur, herbe verte, ruban encreur, trousse de premiers
    secours, poignard), en échangeant les paires (identifiant, quantité),
  - OPTION --armes-aleatoires : le pistolet entre aussi dans le mélange (Chris ne commence qu'avec son
    couteau, il devra trouver son arme à un emplacement quelconque) ; sans cette option il reste dans le hall,
  - laisse toutes les clés, objets inconnus et objets spéciaux à leur place d'origine,
  - écrit trois fichiers :
        seed_<graine>.json / .lua   (ce que lisent les programmes qui s'accrochent au jeu)
        seed_<graine>_spoiler.txt   (la liste lisible : pièce, objet d'origine, nouvel objet)
    Avec --armes-aleatoires, les noms de fichiers portent le suffixe "_armes".

Pourquoi les clés ne bougent pas : les cinq vieilles clés sont identiques entre elles, les mélanger
entre leurs propres emplacements ne changerait rien, et les déplacer ailleurs demande de savoir quelles
pièces sont accessibles avec quoi (la logique des verrous, pas encore écrite).

Utilisation :
    python generateur_seed.py                          (graine tirée au hasard)
    python generateur_seed.py 12345                    (graine choisie : même graine = même résultat)
    python generateur_seed.py 12345 --armes-aleatoires (le pistolet est aussi mélangé)
    python generateur_seed.py 12345 --fichier mon_fichier.xlsx
    python generateur_seed.py 12345 --installer        (copie aussi la seed dans le dossier du jeu,
                                                        sous le nom randomizer_seed.lua lu par la DLL)
    python generateur_seed.py 12345 --installer --dossier-jeu "D:\\Jeux\\RE HD"
                                                       (si le jeu n'est pas trouvé automatiquement)

Il faut Python 3 et la bibliothèque openpyxl (pip install openpyxl).
"""
import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

sys.path.insert(0, str(Path(__file__).resolve().parent))   # textes.py, même avec python -I
from textes import tr, Msg, rendre  # noqa: E402
from noms_objets import nom_officiel  # noqa: E402

FICHIER_PAR_DEFAUT = "donnees_randomizer_RE1.xlsx"

# Objets toujours mélangés sans risque
IDS_LIBRES_DE_BASE = {4, 17, 18, 25, 33, 34, 35, 36, 68, 101, 104, 112, 113, 131, 132}   # 18, 33, 35, 113 : 18/11/2026
# 25 (munitions de Magnum), 36 (herbe bleue), 104 (trousse : 1 herbe verte) ajoutés le 20/11/2026, relevé terminé.
# 131 / 132 (trousses : verte + bleue, 2 vertes) : pas de fichier i131p / i132p, le jeu leur prête le modèle i104
# (table des objets du jeu, lue par la DLL depuis la v0.9.4.1).
# 4 = pistolet d'autodéfense (une seule balle) : un objet comme le poignard, pas une arme de la liste (joueur, 19/11/2026)
# Armes de base du jeu : mélangées seulement avec l'option --armes-aleatoires.
# (clé du nom dans textes.py, id dans le jeu ou None s'il n'est pas encore relevé, personnage ou None = les deux)
ARMES = [
    ("arme_pistolet", 3, None),
    ("arme_fusil_pompe", 6, None),          # salon (116), x6 : récompense de l'énigme du piège, pas un objet de quête
    ("arme_fusil_assaut", 13, None),        # réservoir de l'Aqua Ring (412), x10 : sans risque (joueur, 19/11/2026)
    ("arme_lance_grenades", None, "Jill"),
    ("arme_lance_flammes", None, "Chris"),
    # Magnum : une seule case pour les deux personnages. Chris a le revolver Magnum (11, en 312, x6 : ajouté le
    # 21/11/2026), Jill le .44 Magnum de Barry (15, à relever). Test du joueur (21/11/2026) : Chris peut équiper le
    # Magnum de Barry, identique à son revolver ; le mélange ne crée pas d'objet, il n'y a donc qu'un Magnum par partie.
    # Le lance-grenades, lui, ne s'équipe PAS avec Chris (même test) : il reste « Jill uniquement ».
    # Pas de lance-roquettes de fin de jeu (id 10, héliport 303) : test du 21/11/2026, donné tôt il ne blesse que le
    # Tyran final ; et sans lui à l'héliport la fin devient impossible. Il ne doit jamais être déplacé.
    ("arme_magnum", 11, None),
]
IDS_ARMES = {i for _, i, _ in ARMES if i is not None}
# Armes bonus (option « Fun ») : ids confirmés par une seed de test le 19/11/2026 (munitions illimitées gérées par
# le jeu). Pas de modèle au sol (i005p / i014p n'existent pas) : la DLL les remplace seulement au ramassage.
# (clé du nom dans textes.py, id, quantité) : Samurai Edge, lance-roquettes illimité
ARMES_BONUS = [("arme_bonus_samurai", 5, 15), ("arme_bonus_roquettes", 14, 4)]
IDS_ARMES_BONUS = {i for _, i, _ in ARMES_BONUS}

# Emplacements « dans un mécanisme » : le jeu y place l'objet à un point caché dans le décor, seul le modèle d'origine
# dépasse. Le nouvel objet visible par terre est remonté de y (cm). (pièce, id d'origine) -> y. Réglé en jeu :
#   50F, capsule de carburant (111) dans sa machine : 45 (test du 20/11/2026 : 0 et 30 cachés, 100 en l'air).
DECALAGES = {("50F", 111): 45}

MOTIF_EMPREINTE = re.compile(r"brut \+0x10\.\.\+0x2C = ((?:[0-9A-Fa-f]{8}\s*){8})")


# Difficulté -> valeur dans le jeu ([partie]+0x24, relevé le 22/11/2026). Dans le jeu : nouvelle partie « I. Old school »
# = Normal, « II. Gamer » = Facile (nos relevés), « III. Casual » = Débutant ; « Une fois de plus » : Débutant, Facile,
# Normal, Expert ; le mode Survie (Real Survival) vaut 2 comme Expert.
DIFFICULTE_JEU = {"Facile": 0, "Normal": 1, "Difficile": 2, "Très facile": 3, "Real Survival": 2}


def lire_emplacements(chemin, personnage="Chris", difficulte="Facile"):
    wb = load_workbook(chemin, data_only=True)
    # Noms des pièces lus directement dans l'onglet « Pièces » : la colonne « Pièce » d'Emplacements est
    # une formule, dont le résultat peut manquer si le fichier a été enregistré par un autre programme.
    noms_pieces = {}
    if "Pièces" in wb.sheetnames:
        for ident, _, _, nom, *_ in wb["Pièces"].iter_rows(min_row=2, values_only=True):
            if ident is not None and nom:
                noms_pieces[str(ident).lower()] = nom
    ws = wb["Emplacements"]
    emplacements, ignores, zones_vues = [], [], set()
    for ligne in ws.iter_rows(min_row=2, values_only=True):
        (_, piece, nom_piece, desc, ident, nom_obj, qte, chemin_ramassage,
         verrou, statut, empreinte, remarque, perso, diff) = (list(ligne) + [None] * 14)[:14]
        if ident is None or not piece:
            continue
        # seulement les relevés du scénario demandé (colonne vide = Chris / Facile, les premiers relevés)
        if (str(perso or "Chris"), str(diff or "Facile")) != (personnage, difficulte):
            continue
        m = MOTIF_EMPREINTE.search(empreinte or "")
        fiche = {
            "piece": str(piece).lower(),
            "nom_piece": nom_piece or noms_pieces.get(str(piece).lower(), ""),
            "description": desc or "",
            "id": int(ident),
            "quantite": int(qte) if qte is not None else 0,
            "chemin": chemin_ramassage or "",
            "empreinte": m.group(1).split() if m else None,
        }
        zone = (fiche["piece"], tuple(fiche["empreinte"] or ()))
        if fiche["chemin"] != "posé" or not fiche["empreinte"]:
            ignores.append((fiche, "pas de valeurs fixes complètes ou pas un objet posé"))
        elif zone in zones_vues:
            # plusieurs objets dans la même zone (ex. les symboles d'une tombe) : la DLL reconnaît un emplacement
            # à sa zone, elle ne saurait pas lequel remplacer → seul le premier est utilisé
            ignores.append((fiche, "zone partagée avec un autre objet de la pièce"))
        elif qte is None:
            # sans quantité, on placerait par exemple un chargeur vide ailleurs : on laisse l'objet en place
            fiche["description"] = (fiche["description"] or "") + " (quantité inconnue)"
            ignores.append((fiche, "quantité inconnue"))
        else:
            zones_vues.add(zone)
            emplacements.append(fiche)
    return emplacements, ignores


# Malle de départ (option « Malle de départ aléatoire », 21/11/2026) : ses objets deviennent des emplacements comme
# les autres. Pièce « malle », empreinte = numéro de case. La DLL (v0.9.5+) remplace la malle au début d'une nouvelle
# partie (lignes « malle = case, ancien, id, qte »), seulement si elle contient encore exactement son contenu d'origine.
PIECE_MALLE = "malle"
# Clé du placard (salle des costumes) : le jeu la met en tête de malle seulement dans une partie « Une fois de plus ».
# Option « Clé du placard dès le départ » : ajoutée dans la première case vide de la malle d'une nouvelle partie.
ID_CLE_PLACARD = 62
# Inventaire de départ (option « Couteau de départ aléatoire », v0.9.6) : le couteau de Chris (id 2, case 1) devient
# un emplacement comme les autres et le couteau part dans le mélange. Pièce « inventaire », empreinte = case.
PIECE_INVENTAIRE = "inventaire"
ID_COUTEAU = 2
PIECES_SPECIALES = (PIECE_MALLE, PIECE_INVENTAIRE)


def emplacement_couteau(personnage):
    if personnage != "Chris":                # Jill : pas encore relevée
        return []
    return [{"piece": PIECE_INVENTAIRE, "case": 0, "nom_piece": "", "description": "Couteau de départ (inventaire)",
             "id": ID_COUTEAU, "quantite": 1, "chemin": "inventaire", "empreinte": ["inv0"]}]


def lire_malle(chemin, personnage="Chris", difficulte="Facile"):
    """Contenu de départ de la malle (onglet « Coffre de départ »), dans l'ordre des cases."""
    wb = load_workbook(chemin, data_only=True)
    if "Coffre de départ" not in wb.sheetnames:
        return []
    cases = []
    for perso, diff, ident, _, qte, *_ in wb["Coffre de départ"].iter_rows(min_row=2, values_only=True):
        if ident is None or (str(perso or ""), str(diff or "")) != (personnage, difficulte):
            continue
        n = len(cases)
        cases.append({"piece": PIECE_MALLE, "case": n, "nom_piece": "", "description": f"Malle de départ, case {n + 1}",
                      "id": int(ident), "quantite": int(qte or 0), "chemin": "malle", "empreinte": [f"case{n}"]})
    return cases


def generer(emplacements, graine, ids_libres):
    rng = random.Random(graine)
    libres = [e for e in emplacements if e["id"] in ids_libres]
    contenus = [(e["id"], e["quantite"]) for e in libres]
    rng.shuffle(contenus)
    resultat = []
    for e, (nouvel_id, nouvelle_qte) in zip(libres, contenus):
        resultat.append({
            "piece": e["piece"],
            "empreinte": e["empreinte"],
            "ancien": {"id": e["id"], "quantite": e["quantite"]},
            "nouveau": {"id": nouvel_id, "quantite": nouvelle_qte},
            "description": e["description"],
            "nom_piece": e["nom_piece"],
        })
        if "case" in e:
            resultat[-1]["case"] = e["case"]
    return resultat


# Emplacement « de départ » : le pistolet du hall (106), atteint dans les premières minutes.
PIECE_DEPART, ID_DEPART = "106", 3


def garantir_arme_depart(resultat, graine, ids_armes):
    """Option « arme garantie au départ » (v0.9.6, choix du joueur le 21/11/2026) : une des armes mélangées, tirée
    au sort selon la graine (toutes ont la même chance, Magnum compris), est DONNÉE dans l'inventaire au début d'une
    nouvelle partie, avec ses munitions de base (celles de son emplacement d'origine). L'emplacement où le mélange
    l'avait placée reçoit à la place un objet de base tiré au sort (n'importe lequel des objets ordinaires du jeu,
    avec sa quantité habituelle ; choix du joueur, 21/11/2026). Le pistolet d'autodéfense n'est pas une arme de la
    liste : c'est un objet (IDS_LIBRES_DE_BASE). Renvoie {"id", "quantite"} de l'arme donnée, ou None."""
    armes = [r for r in resultat if r["nouveau"]["id"] in ids_armes]
    if not armes:
        return None
    choix = random.Random(graine ^ 0x5EED).choice(
        sorted(armes, key=lambda r: (r["piece"], r.get("case", 0), r["nouveau"]["id"])))
    arme = dict(choix["nouveau"])
    # objet de base tiré parmi ceux du mélange (sans les armes), avec leur quantité dans le jeu, AU PRORATA de leur
    # fréquence dans le jeu : herbes et munitions souvent, objets rares rarement (et les 4 sortes de trousses ne
    # comptent pas 4 fois)
    modeles = sorted((r["ancien"]["id"], r["ancien"]["quantite"]) for r in resultat
                     if r["ancien"]["id"] in IDS_LIBRES_DE_BASE)
    if modeles:
        oid, oqte = random.Random(graine ^ 0xBA5E).choice(modeles)
        choix["nouveau"] = {"id": oid, "quantite": oqte}
    else:
        choix["nouveau"] = {"id": 17, "quantite": 15}
    return arme


def placer_armes_bonus(resultat, graine, ids_bonus=None):
    """Option « Armes bonus » (Fun) : chaque arme bonus choisie (Samurai Edge, lance-roquettes illimité) remplace un
    objet ordinaire choisi selon la graine (jamais une arme, ni l'emplacement de départ du hall). ids_bonus : ids
    à placer (None = toutes). Chaque arme garde sa place, qu'on coche l'autre ou non. Renvoie les pièces."""
    candidats = [r for r in resultat if r["nouveau"]["id"] not in IDS_ARMES
                 and not (r["piece"].lower() == PIECE_DEPART and r["ancien"]["id"] == ID_DEPART)]
    candidats.sort(key=lambda r: (r["piece"], r["empreinte"]))
    choix = random.Random(graine ^ 0xB0B05).sample(candidats, min(len(ARMES_BONUS), len(candidats)))
    places = []
    for r, (_, ident, qte) in zip(choix, ARMES_BONUS):
        if ids_bonus is None or ident in ids_bonus:
            r["nouveau"] = {"id": ident, "quantite": qte}
            places.append(r["piece"])
    return places


def nom_objet(ident, langue="fr"):
    """Nom officiel de l'objet dans le jeu (anglais si le jeu n'a pas la langue) ; armes bonus : textes.py."""
    if ident in IDS_ARMES_BONUS:
        return tr(f"objet_{ident}", langue)
    return nom_officiel(ident, langue) or f"#{ident}"


def _fois(objet):
    """Quantité affichée, sauf pour les armes bonus : munitions illimitées (le nom le dit déjà)."""
    return "" if objet["id"] in IDS_ARMES_BONUS else f" x{objet['quantite']}"


def resume_spoiler(sortie, langue="fr"):
    """Lignes de résumé du spoiler (graine, nombre d'objets mélangés), à partir du contenu du fichier .json."""
    armes = sortie.get("options", {}).get("armes_aleatoires", False)
    lignes = [tr("gen_resume", langue, graine=sortie["graine"], armes=tr("gen_oui" if armes else "gen_non", langue))]
    if sortie.get("depart"):                 # arme donnée au début de la partie (v0.9.6)
        lignes.append(tr("gen_arme_depart", langue, arme=nom_objet(sortie["depart"]["id"], langue)
                         + _fois(sortie["depart"])))
    if "laisses" in sortie:                  # absent des seeds d'avant la v0.9.3
        lignes.append(tr("gen_compte", langue, n=len(sortie["remplacements"]), m=sortie["laisses"],
                         pistolet="" if armes else tr("gen_pistolet", langue)))
    return lignes


def lignes_spoiler(sortie, langue="fr"):
    """Lignes du tableau du spoiler, triées par pièce :
    (pièce, nom de la pièce, objet d'origine, nouvel objet, arme bonus ?)."""
    def lieu(r):
        if r["piece"] == PIECE_MALLE:
            return tr("malle_depart", langue), tr("malle_case", langue, n=r.get("case", 0) + 1)
        if r["piece"] == PIECE_INVENTAIRE:
            return tr("inventaire_depart", langue), tr("malle_case", langue, n=r.get("case", 0) + 1)
        return r["piece"].upper(), r.get("nom_piece") or ""
    return [(*lieu(r),
             nom_objet(r["ancien"]["id"], langue) + _fois(r["ancien"]),
             nom_objet(r["nouveau"]["id"], langue) + _fois(r["nouveau"]),
             r["nouveau"]["id"] in IDS_ARMES_BONUS)
            for r in sorted(sortie["remplacements"], key=lambda x: (x["piece"], x.get("case", 0)))]


def texte_spoiler(sortie, langue="fr"):
    """Spoiler complet en texte (fichier *_spoiler.txt et ligne de commande)."""
    lignes = resume_spoiler(sortie, langue) + [""]
    lignes += [f"[{piece:>3}] {nom}: {avant}  ->  {apres}" for piece, nom, avant, apres, _ in lignes_spoiler(sortie, langue)]
    if sortie.get("non_utilises"):
        lignes += ["", tr("gen_non_utilises", langue)]
        lignes += [f"  - [{piece}] {description}" for piece, description in sortie["non_utilises"]]
    return "\n".join(lignes)


def verifier(resultat):
    """Contrôles simples : on ne perd ni ne crée aucun objet."""
    avant = Counter((r["ancien"]["id"], r["ancien"]["quantite"]) for r in resultat)
    apres = Counter((r["nouveau"]["id"], r["nouveau"]["quantite"]) for r in resultat)
    assert avant == apres, "Les objets avant et après ne correspondent pas"
    cles = {(r["piece"], tuple(r["empreinte"])) for r in resultat}
    assert len(cles) == len(resultat), "Deux emplacements ont la même clé d'identification"


NOM_DOSSIER_JEU = "Resident Evil Biohazard HD REMASTER"
NOM_SEED_JEU = "randomizer_seed.lua"


def trouver_dossier_jeu():
    """Cherche le dossier du jeu dans les bibliothèques Steam (registre + libraryfolders.vdf)."""
    racines = []
    try:
        import winreg
        for ruche, cle, valeur in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                                   (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath")):
            try:
                with winreg.OpenKey(ruche, cle) as k:
                    racines.append(Path(winreg.QueryValueEx(k, valeur)[0]))
            except OSError:
                pass
    except ImportError:
        pass
    if sys.platform == "win32":
        racines.append(Path(r"C:\Program Files (x86)\Steam"))
    else:                                   # Linux, Steam Deck (Steam natif ou Flatpak)
        maison = Path.home()
        racines += [maison / ".steam" / "steam", maison / ".steam" / "root", maison / ".local" / "share" / "Steam",
                    maison / ".var" / "app" / "com.valvesoftware.Steam" / ".local" / "share" / "Steam"]

    bibliotheques = []
    for r in racines:
        bibliotheques.append(r)
        vdf = r / "steamapps" / "libraryfolders.vdf"
        if vdf.exists():
            for m in re.finditer(r'"path"\s+"([^"]+)"', vdf.read_text(encoding="utf-8", errors="replace")):
                bibliotheques.append(Path(m.group(1).replace("\\\\", "\\")))
    for b in bibliotheques:
        d = b / "steamapps" / "common" / NOM_DOSSIER_JEU
        if (d / "bhd.exe").exists():
            return d
    return None


def seed_installee(dossier):
    """Renvoie (graine, armes) de la seed présente dans le dossier du jeu, ou None."""
    cible = Path(dossier) / NOM_SEED_JEU
    if not cible.exists():
        return None
    texte = cible.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"graine\s*=\s*(\d+)", texte)
    a = re.search(r"armes_aleatoires\s*=\s*(true|false)", texte)
    return (m.group(1) if m else "?", bool(a and a.group(1) == "true"))


def installer_seed(fichier_lua, dossier_jeu, graine, armes, dire=print, langue="fr", messages_differes=False):
    """messages_differes : dire reçoit des textes.Msg (traduits à l'affichage) au lieu de textes."""
    if not messages_differes:
        dire_texte = dire
        dire = lambda m: dire_texte(rendre(m, langue))   # noqa: E731
    dossier = Path(dossier_jeu) if dossier_jeu else trouver_dossier_jeu()
    if dossier is None or not (dossier / "bhd.exe").exists():
        dire(Msg("gen_install_impossible"))
        return False
    ancienne = seed_installee(dossier)
    cible = dossier / NOM_SEED_JEU
    cible.write_bytes(Path(fichier_lua).read_bytes())
    suffixe = Msg("gen_armes")
    remplace = Msg("gen_remplace", ancienne=Msg(None, ancienne[0], suffixe if ancienne[1] else "")) if ancienne else ""
    dire(Msg("gen_installee", remplace, graine=graine, armes=suffixe if armes else "", chemin=cible))

    ini = dossier / "randomizer.ini"
    if ini.exists():
        texte = ini.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?im)^\s*Seed\s*=\s*(.+?)\s*$", texte)
        if m and m.group(1).lower() != NOM_SEED_JEU:
            dire(Msg("gen_ini_autre", seed=m.group(1), nom=NOM_SEED_JEU))
        if re.search(r"(?im)^\s*Actif\s*=\s*0", texte):
            dire(Msg("gen_ini_inactif"))
    if not (dossier / "xinput1_4.dll").exists():
        dire(Msg("gen_dll_absente"))
    dire(Msg("gen_relance"))
    return True


def tirer_graine():
    return random.SystemRandom().randrange(10**6)


def produire(graine, armes_aleatoires, fichier, dossier_sortie=".", installer=False, dossier_jeu=None,
             dire=print, personnage="Chris", difficulte="Facile", langue="fr", dire_spoiler=None,
             armes_choisies=None, objets_visibles=True, arme_depart=False, armes_bonus=False,
             messages_differes=False, malle_aleatoire=False, couteau_aleatoire=False, cle_placard=False, une_fois_de_plus=False):
    """Génère une seed et écrit ses fichiers. Partagé par la ligne de commande et l'application.
    Renvoie True si tout s'est bien passé. langue : langue des messages et du spoiler (textes.py).
    dire_spoiler : si donné, reçoit le contenu de la seed (dictionnaire du fichier .json, à afficher avec
    resume_spoiler / lignes_spoiler dans n'importe quelle langue) ; sinon le spoiler texte passe par dire.
    messages_differes : dire reçoit des textes.Msg (traduits à l'affichage, voir textes.rendre).
    armes_choisies : ids des armes à mélanger avec armes_aleatoires (None = toutes celles connues).
    objets_visibles : la DLL remplace aussi les objets posés (modèle par terre et aperçu) avant ramassage.
    arme_depart : avec armes_aleatoires, une arme est toujours placée au pistolet du hall (106).
    armes_bonus : ids des armes bonus à placer (option « Fun ») ; True = toutes, False / None / vide = aucune.
    malle_aleatoire : les objets de la malle de départ sont mélangés avec les autres (nouvelle partie seulement).
    couteau_aleatoire : le couteau de départ (Chris) est mélangé avec les autres objets (nouvelle partie seulement).
    cle_placard : la clé du placard (salle des costumes) est ajoutée à la malle de départ (nouvelle partie seulement).
    une_fois_de_plus : partie « Une fois de plus » (jeu déjà terminé) : le jeu met la clé du placard en case 1 de la
    malle, le contenu de départ est donc décalé d'une case (hypothèse du 22/11/2026, à confirmer en jeu)."""
    dire_brut = dire
    if not messages_differes:
        dire = lambda m: dire_brut(rendre(m, langue))   # noqa: E731
    if not Path(fichier).exists():
        dire(Msg("gen_donnees", fichier=fichier))
        return False
    ids_armes = set(IDS_ARMES) if armes_choisies is None else set(armes_choisies) & IDS_ARMES
    armes_aleatoires = bool(armes_aleatoires and ids_armes)   # aucune arme cochée = option sans effet
    ids_libres = set(IDS_LIBRES_DE_BASE) | (ids_armes if armes_aleatoires else set())
    if couteau_aleatoire:
        ids_libres.add(ID_COUTEAU)
    if armes_bonus is True:
        armes_bonus = set(IDS_ARMES_BONUS)
    armes_bonus = set(armes_bonus or ()) & IDS_ARMES_BONUS
    nom = f"seed_{graine}{'_armes' if armes_aleatoires else ''}{'_bonus' if armes_bonus else ''}"
    sortie_dir = Path(dossier_sortie)
    sortie_dir.mkdir(parents=True, exist_ok=True)

    emplacements, ignores = lire_emplacements(fichier, personnage, difficulte)
    if not emplacements:
        dire(Msg("gen_aucun", personnage=personnage, difficulte=Msg(f"diff_{difficulte}")))
        return False
    if malle_aleatoire:
        emplacements = emplacements + lire_malle(fichier, personnage, difficulte)
    if couteau_aleatoire:
        emplacements = emplacements + emplacement_couteau(personnage)
    resultat = generer(emplacements, graine, ids_libres)
    verifier(resultat)       # avant l'arme de départ et les armes bonus : elles changent des objets (voulu)
    depart = garantir_arme_depart(resultat, graine, ids_armes) if arme_depart and armes_aleatoires else None
    if armes_bonus:
        placer_armes_bonus(resultat, graine, armes_bonus)

    sortie = {
        "version_jeu": {"taille_bhd_exe": 9640360,
                        "sha256": "39B840663E4B1A6835C60CBD176E4EE6C21B9197FC2C2DD733F2A7C36A0B429A"},
        "personnage": personnage, "difficulte": difficulte,
        "graine": graine, "options": {"armes_aleatoires": armes_aleatoires, "objets_visibles": bool(objets_visibles),
                                      "arme_depart": bool(arme_depart and armes_aleatoires),
                                      "armes_bonus": sorted(armes_bonus),
                                      "malle_aleatoire": bool(malle_aleatoire),
                                      "couteau_aleatoire": bool(couteau_aleatoire),
                                      "cle_placard": bool(cle_placard and not une_fois_de_plus),
                                      "une_fois_de_plus": bool(une_fois_de_plus)},
        "depart": depart,
        "remplacements": resultat,
        "laisses": len(emplacements) - len(resultat),
        "non_utilises": [[f["piece"].upper(), f["description"]] for f, _ in ignores],
        # objets examinés (joyaux des trophées…) : [pièce, id d'origine, nouvel id, quantité]. Lus par la DLL v0.9.3+
        # (point d'arrêt en bhd.exe+151284). Vide tant que ces objets (surtout des objets de quête) ne sont pas mélangés.
        "examens": [],
    }
    (sortie_dir / f"{nom}.json").write_text(json.dumps(sortie, indent=1, ensure_ascii=False), encoding="utf-8")

    # Version Lua : lue par la DLL (randomizer_seed.lua) et par appliquer_seed.lua dans Cheat Engine
    lua = ["-- seed générée par generateur_seed.py : ne pas modifier à la main",
           "return {", f"  graine = {graine},",
           f"  armes_aleatoires = {'true' if armes_aleatoires else 'false'},",
           f"  objets_visibles = {'true' if objets_visibles else 'false'},",
           # valeur de la difficulté dans le jeu ([partie]+0x24) : la DLL n'applique la seed que dans celle-ci
           f"  difficulte = {DIFFICULTE_JEU[difficulte]},",
           # clé du placard dès le départ : la DLL (v0.9.7.3+) active aussi la porte de la salle des costumes
           f"  placard = {1 if cle_placard and not une_fois_de_plus else 0},",
           # « Une fois de plus » : la DLL (v0.9.7.3+) retire les armes infinies et remet un départ normal
           f"  ufp = {1 if une_fois_de_plus else 0},", "  remplacements = {"]
    posees = [r for r in resultat if r["piece"] not in PIECES_SPECIALES]
    inventaire = sorted((r for r in resultat if r["piece"] == PIECE_INVENTAIRE), key=lambda r: r["case"])
    malle = sorted((r for r in resultat if r["piece"] == PIECE_MALLE), key=lambda r: r["case"])
    for r in posees:
        emp = ", ".join("0x" + v.upper() for v in r["empreinte"])
        lua.append(f"    {{ piece = 0x{r['piece'].upper()}, empreinte = {{ {emp} }}, "
                   f"id = {r['nouveau']['id']}, qte = {r['nouveau']['quantite']} }},")
    lua.append("  },")
    # Modèles décoratifs (ex. fusil accroché au mur du salon) : le jeu les crée à part, à partir de l'id d'origine.
    # La DLL (v0.8.7+) remplace le modèle « ancien » de la pièce par le « nouveau ». Clé « salle » (et non
    # « piece ») : les DLL plus anciennes ignorent ces lignes. Une pièce où le même objet d'origine devient deux
    # objets différents est laissée de côté (on ne saurait pas quel modèle remplacer).
    decors = {}
    for r in posees:
        cle = (r["piece"].upper(), r["ancien"]["id"])
        if r["ancien"]["id"] != r["nouveau"]["id"]:
            decors.setdefault(cle, set()).add(r["nouveau"]["id"])
    lua.append("  decors = {")
    for (piece, ancien), nouveaux in sorted(decors.items()):
        if len(nouveaux) == 1:
            lua.append(f"    {{ salle = 0x{piece}, ancien = {ancien}, nouveau = {next(iter(nouveaux))} }},")
    lua += ["  },", "  examens = {"]
    for piece, ancien, nouvel_id, qte in sortie["examens"]:
        lua.append(f"    {{ examen = 0x{piece.upper()}, ancien = {ancien}, id = {nouvel_id}, qte = {qte} }},")
    lua += ["  },", "  decalages = {"]
    for piece, ancien in sorted({(r["piece"].upper(), r["ancien"]["id"]) for r in posees
                                 if r["ancien"]["id"] != r["nouveau"]["id"]}):
        if (piece, ancien) in DECALAGES:
            lua.append(f"    {{ decalage = 0x{piece}, ancien = {ancien}, y = {DECALAGES[(piece, ancien)]} }},")
    # Malle de départ : toutes les cases (même inchangées), la DLL vérifie le contenu d'origine case par case.
    lua += ["  },", "  coffre = {"]
    coffre = {r["case"]: (r["ancien"]["id"], r["nouveau"]["id"], r["nouveau"]["quantite"]) for r in malle}
    if une_fois_de_plus and coffre:
        # « Une fois de plus » : la clé du placard est en case 1, le contenu de départ commence en case 2
        coffre = {case + 1: v for case, v in coffre.items()}
        coffre[0] = (ID_CLE_PLACARD, ID_CLE_PLACARD, 1)
    elif cle_placard:
        # La DLL ne touche à la malle que si chaque case listée a son contenu d'origine (nouvelle partie) : on liste
        # aussi les cases inchangées, puis la clé dans la première case vide (« ancien = 0 »). Dans une partie
        # « Une fois de plus », la clé est déjà en tête de malle : le contenu ne correspond pas, rien n'est ajouté.
        origine = lire_malle(fichier, personnage, difficulte)
        for c in origine:
            coffre.setdefault(c["case"], (c["id"], c["id"], c["quantite"]))
        if origine:
            coffre[len(origine)] = (0, ID_CLE_PLACARD, 1)
    for case, (ancien, nouvel_id, qte) in sorted(coffre.items()):
        lua.append(f"    {{ malle = {case}, ancien = {ancien}, id = {nouvel_id}, qte = {qte} }},")
    # Inventaire de départ (DLL v0.9.6+) : couteau remplacé, arme donnée ; nouvelle partie seulement.
    lua += ["  },", "  inventaire = {"]
    for r in inventaire:
        lua.append(f"    {{ inv = {r['case']}, ancien = {r['ancien']['id']}, id = {r['nouveau']['id']}, "
                   f"qte = {r['nouveau']['quantite']} }},")
    lua += ["  },", "  donner = {"]
    if depart:
        lua.append(f"    {{ depart = {depart['id']}, qte = {depart['quantite']} }},")
    lua += ["  },", "}"]
    fichier_lua = sortie_dir / f"{nom}.lua"
    fichier_lua.write_text("\n".join(lua) + "\n", encoding="utf-8")

    texte = texte_spoiler(sortie, langue)
    (sortie_dir / f"{nom}_spoiler.txt").write_text(texte, encoding="utf-8")
    if dire_spoiler:
        dire_spoiler(sortie)
    else:
        dire(texte)
    dire(Msg("gen_fichiers", dossier=sortie_dir.resolve(), a=f"{nom}.json", b=f"{nom}.lua", c=f"{nom}_spoiler.txt"))
    if installer:
        return installer_seed(fichier_lua, dossier_jeu, graine, armes_aleatoires, dire, langue, messages_differes=True)
    return True


def main():
    parser = argparse.ArgumentParser(description="Générateur de seeds du randomizer Resident Evil HD Remaster")
    parser.add_argument("graine", nargs="?", type=int, help="numéro de graine (au hasard si absent)")
    parser.add_argument("--armes-aleatoires", action="store_true",
                        help="mélange aussi le pistolet (Chris doit alors trouver son arme)")
    parser.add_argument("--objets-invisibles", action="store_true",
                        help="ne remplace les objets qu'au ramassage (par terre, on voit l'objet d'origine)")
    parser.add_argument("--armes-bonus", action="store_true",
                        help="Samurai Edge et lance-roquettes illimité à la place de deux objets (option Fun)")
    parser.add_argument("--fichier", default=FICHIER_PAR_DEFAUT, help="tableur de données")
    parser.add_argument("--personnage", default="Chris", choices=("Chris", "Jill"))
    parser.add_argument("--difficulte", default="Facile",
                        choices=("Très facile", "Facile", "Normal", "Difficile", "Real Survival"))
    parser.add_argument("--installer", action="store_true",
                        help=f"copie la seed dans le dossier du jeu sous le nom {NOM_SEED_JEU}")
    parser.add_argument("--dossier-jeu", help="dossier du jeu (sinon cherché dans les bibliothèques Steam)")
    args = parser.parse_args()

    graine = args.graine if args.graine is not None else tirer_graine()
    if not produire(graine, args.armes_aleatoires, args.fichier, ".", args.installer, args.dossier_jeu,
                    personnage=args.personnage, difficulte=args.difficulte,
                    objets_visibles=not args.objets_invisibles, armes_bonus=args.armes_bonus):
        sys.exit(1)


if __name__ == "__main__":
    main()

