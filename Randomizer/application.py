"""
Application du randomizer Resident Evil HD Remaster : génère et installe une seed en quelques clics.

Toute la logique est dans generateur_seed.py (partagée avec la ligne de commande) ; ce fichier ne fait
que l'interface. Les options pas encore prises en charge sont visibles mais grisées (« à venir »).

Lancer sans compiler :  python application.py
Construire le .exe   :  construire_exe.bat
"""
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
import tkinter as tk
import unicodedata
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkfont

import generateur_seed as gen
import mise_a_jour
import progression
import textes

VERSION = "0.9.7"
TAILLE_BHD_EXE = 9640360
URL_DEPOT = "https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer"
# Crédits (onglet Info) : (pseudo, nom complet, profil GitHub)
AUTEURS = [("Jojo / Michiyo", "Delage Jordan", "https://github.com/Michiy0")]
# (pseudo, nom complet, petit mot à côté du pseudo — non traduit)
TESTEURS = [("Nico", "De Oliveira Gomes Nicolas", "Number One Chris Fan")]
SHA256_BHD_EXE = "39B840663E4B1A6835C60CBD176E4EE6C21B9197FC2C2DD733F2A7C36A0B429A"
NOM_APPLI = "Resident Evil HD Remaster Randomizer"
TITRE = f"{NOM_APPLI} v{VERSION}"
SOUS_WINDOWS = sys.platform == "win32"
# Le jeu tourne sous Proton sur Linux / Steam Deck : la DLL doit être préférée à celle de Proton.
OPTION_PROTON = 'WINEDLLOVERRIDES="xinput1_4=n,b" %command%'
# avec BhdTool (ou un autre mod en dinput8.dll), Proton doit charger aussi ce dinput8.dll
OPTION_PROTON_DINPUT8 = 'WINEDLLOVERRIDES="xinput1_4=n,b;dinput8=n,b" %command%'


def dossier_programme():
    """Dossier de l'exe (version compilée) ou du script."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def trouver_ressource(nom, sous_dossiers=("", "..", "../DLL", "DLL")):
    """Cherche d'abord à côté du programme (pour pouvoir mettre à jour les données sans recompiler),
    puis dans la copie embarquée dans l'exe."""
    base = dossier_programme()
    for s in sous_dossiers:
        p = (base / s / nom).resolve()
        if p.exists():
            return p
    embarque = getattr(sys, "_MEIPASS", None)
    if embarque and (Path(embarque) / nom).exists():
        return Path(embarque) / nom
    return None


_versions_verifiees = {}


def dll_a_jour(installee, fournie):
    """Vrai si la DLL du jeu est identique à celle livrée avec l'application (ou si on ne peut pas comparer)."""
    try:
        return fournie is None or Path(installee).read_bytes() == Path(fournie).read_bytes()
    except OSError:
        return True


def version_jeu_ok(dossier):
    """Vrai si bhd.exe est exactement la version prise en charge (taille puis SHA-256, mis en cache)."""
    import hashlib
    exe = Path(dossier) / "bhd.exe"
    try:
        etat = exe.stat()
    except OSError:
        return False
    cle = (str(exe), etat.st_size, etat.st_mtime)
    if cle not in _versions_verifiees:
        ok = etat.st_size == TAILLE_BHD_EXE
        if ok:
            h = hashlib.sha256()
            with open(exe, "rb") as f:
                for morceau in iter(lambda: f.read(1 << 20), b""):
                    h.update(morceau)
            ok = h.hexdigest().upper() == SHA256_BHD_EXE
        _versions_verifiees[cle] = ok
    return _versions_verifiees[cle]


def lire_option_ini(dossier, cle):
    """Valeur d'une option de la section [Randomizer] de randomizer.ini (None si absente)."""
    ini = Path(dossier) / "randomizer.ini"
    if not ini.exists():
        return None
    section = False
    for ligne in ini.read_text(encoding="utf-8", errors="replace").splitlines():
        l = ligne.strip()
        if l.startswith("["):
            section = l.lower() == "[randomizer]"
        elif section and not l.startswith(";") and "=" in l and l.split("=", 1)[0].strip().lower() == cle.lower():
            return l.split("=", 1)[1].strip()
    return None


def ecrire_option_ini(dossier, cle, valeur):
    """Règle (ou retire si valeur est None) une option de [Randomizer] en gardant le reste du fichier."""
    ini = Path(dossier) / "randomizer.ini"
    lignes = ini.read_text(encoding="utf-8", errors="replace").splitlines() if ini.exists() else []
    if not any(l.strip().lower() == "[randomizer]" for l in lignes):
        lignes = ["[Randomizer]"] + lignes
    resultat, section, fait = [], False, False
    for ligne in lignes:
        l = ligne.strip()
        if l.startswith("["):
            if section and not fait and valeur is not None:
                resultat.append(f"{cle}={valeur}")
                fait = True
            section = l.lower() == "[randomizer]"
        elif section and not l.startswith(";") and "=" in l and l.split("=", 1)[0].strip().lower() == cle.lower():
            if valeur is not None and not fait:
                resultat.append(f"{cle}={valeur}")
                fait = True
            continue
        resultat.append(ligne)
    if section and not fait and valeur is not None:
        resultat.append(f"{cle}={valeur}")
    ini.write_text("\r\n".join(resultat) + "\r\n", encoding="utf-8", newline="")


def est_notre_dll(chemin):
    """Vrai si ce xinput1_4.dll est celui du randomizer (il contient le texte de son journal : nouveau nom depuis
    la v0.9.0, ancien nom avant)."""
    try:
        contenu = Path(chemin).read_bytes()
        return b"Resident Evil HD Remaster Randomizer" in contenu or b"Randomizer RE HD" in contenu
    except OSError:
        return False


# ---------------------------------------------------------------------- style
COULEURS = {
    "fond": "#15171c",        # fond de la fenêtre
    "carte": "#1e2128",       # fond des sections
    "bord": "#2c313b",
    "champ": "#262a33",       # champs de saisie, boutons secondaires
    "survol": "#313643",
    "texte": "#e7e9ee",
    "discret": "#8a909c",
    "lien": "#7fb2ff",        # liens cliquables (onglet Info)
    "grise": "#555b66",
    "accent": "#b3262e",      # rouge sombre
    "accent_survol": "#cf3540",
    "accent_presse": "#8f1d24",
    "ok": "#3fb97a",
    "alerte": "#e0a43a",
    "journal": "#101216",
}
POLICE = "Segoe UI"


def _png(largeur, hauteur, pixels):
    """Encode une liste de pixels RGBA (0..255) en PNG, sans bibliothèque externe."""
    import base64
    import struct
    import zlib
    brut = b"".join(b"\x00" + bytes(v for p in pixels[y * largeur:(y + 1) * largeur] for v in p)
                    for y in range(hauteur))

    def bloc(type_, donnees):
        return struct.pack(">I", len(donnees)) + type_ + donnees + struct.pack(">I", zlib.crc32(type_ + donnees))
    png = (b"\x89PNG\r\n\x1a\n" + bloc(b"IHDR", struct.pack(">IIBBBBB", largeur, hauteur, 8, 6, 0, 0, 0))
           + bloc(b"IDAT", zlib.compress(brut)) + bloc(b"IEND", b""))
    return base64.b64encode(png)


def _hex(couleur):
    return tuple(int(couleur[i:i + 2], 16) for i in (1, 3, 5))


def dessiner_indicateur(forme, remplissage, bord, coche=None, taille=18, marge=9):
    """Case (forme 'case') ou bouton radio (forme 'rond') lissés, avec coche ou point blanc."""
    def dist_rect(x, y, r=4.5):
        cx, cy, demi = taille / 2, taille / 2, taille / 2 - 1
        qx, qy = abs(x - cx) - (demi - r), abs(y - cy) - (demi - r)
        return (max(qx, 0) ** 2 + max(qy, 0) ** 2) ** 0.5 + min(max(qx, qy), 0) - r

    def dist_rond(x, y, rayon=None):
        return ((x - taille / 2) ** 2 + (y - taille / 2) ** 2) ** 0.5 - (rayon or taille / 2 - 1)

    def dist_segment(x, y, a, b):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)))
        return ((x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2) ** 0.5

    forme_dist = dist_rect if forme == "case" else dist_rond
    rf, rb, blanc = _hex(remplissage), _hex(bord), (255, 255, 255)
    pixels = []
    for y in range(taille):
        for x in range(taille):
            px, py = x + 0.5, y + 0.5
            d = forme_dist(px, py)
            couverture = max(0.0, min(1.0, 0.5 - d))
            dans_bord = max(0.0, min(1.0, 0.5 - abs(d + 0.5)))      # anneau de 1 px sur le pourtour
            couleur = tuple(round(f * (1 - dans_bord) + b * dans_bord) for f, b in zip(rf, rb))
            if coche == "coche":
                s = taille / 18
                dc = min(dist_segment(px, py, (4.6 * s, 9.4 * s), (7.6 * s, 12.4 * s)),
                         dist_segment(px, py, (7.6 * s, 12.4 * s), (13.4 * s, 5.8 * s))) - 1.05 * s
                k = max(0.0, min(1.0, 0.5 - dc))
                couleur = tuple(round(c_ * (1 - k) + w * k) for c_, w in zip(couleur, blanc))
            elif coche == "point":
                k = max(0.0, min(1.0, 0.5 - dist_rond(px, py, taille / 2 - 5.5)))
                couleur = tuple(round(c_ * (1 - k) + w * k) for c_, w in zip(couleur, blanc))
            pixels.append(couleur + (round(255 * couverture),))
        pixels.extend([(0, 0, 0, 0)] * marge)          # espace transparent avant le texte
    return _png(taille + marge, taille, pixels)


def creer_indicateurs(racine, style):
    """Remplace les indicateurs « à l'ancienne » de clam par des cases et ronds lissés."""
    c = COULEURS
    if getattr(racine, "_images_style", None):        # déjà créés : le thème est simplement réappliqué
        return
    racine._images_style = images = {}
    for forme, nom_ttk, marque in (("case", "TCheckbutton", "coche"), ("rond", "TRadiobutton", "point")):
        variantes = {
            "vide": (c["champ"], "#4a505c", None),
            "survol": (c["survol"], "#5d6472", None),
            "plein": (c["accent"], c["accent"], marque),
            "plein_survol": (c["accent_survol"], c["accent_survol"], marque),
            "grise": (c["carte"], "#3a3f49", None),
            "grise_plein": ("#3a3f49", "#3a3f49", marque),
        }
        for cle, (remp, bord, m) in variantes.items():
            images[f"{forme}_{cle}"] = tk.PhotoImage(master=racine, data=dessiner_indicateur(forme, remp, bord, m))
        element = f"Moderne.{forme}.indicator"
        style.element_create(element, "image", images[f"{forme}_vide"],
                             ("disabled", "selected", images[f"{forme}_grise_plein"]),
                             ("disabled", images[f"{forme}_grise"]),
                             ("selected", "active", images[f"{forme}_plein_survol"]),
                             ("selected", images[f"{forme}_plein"]),
                             ("active", images[f"{forme}_survol"]),
                             border=0, sticky="w")
        disposition = [("Checkbutton.padding", {"sticky": "nswe", "children": [
            (element, {"side": "left", "sticky": ""}),
            ("Checkbutton.label", {"side": "left", "sticky": "w", "expand": "1"})]})]
        for nom in (nom_ttk, f"Fond.{nom_ttk}"):
            style.layout(nom, disposition)
        style.configure(nom_ttk, padding=(0, 4))


def dessiner_onglet(remplissage, barre=None, largeur=64, hauteur=48, rayon=7, ecart=3, epaisseur=3):
    """Onglet « carte » : coins du haut arrondis, bas droit, une bande transparente à droite (espace entre
    onglets) et, pour l'onglet actif, une barre de couleur en haut."""
    rf = _hex(remplissage)
    rb = _hex(barre) if barre else rf
    corps = largeur - ecart
    pixels = []
    for y in range(hauteur):
        for x in range(largeur):
            if x >= corps:
                pixels.append((0, 0, 0, 0))
                continue
            px, py = x + 0.5, y + 0.5
            # distance au rectangle à coins du haut arrondis
            cx = min(max(px, rayon), corps - rayon)
            d = ((px - cx) ** 2 + (py - rayon) ** 2) ** 0.5 - rayon if py < rayon else -1
            couverture = max(0.0, min(1.0, 0.5 - d))
            couleur = rb if py < epaisseur else rf
            pixels.append(couleur + (round(255 * couverture),))
    return _png(largeur, hauteur, pixels)


def dessiner_icone(nom, couleur, taille=16):
    """Petite icône au trait (style « outline ») dessinée en distances signées, sans bibliothèque :
    telechargement, de, oeil, coeur, info."""
    def seg(x, y, a, b):
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)))
        return ((x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2) ** 0.5

    def cercle(x, y, cx, cy, r):
        return ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 - r

    def rrect(x, y, x0, y0, x1, y1, r):
        cx, cy, hx, hy = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 - r, (y1 - y0) / 2 - r
        qx, qy = abs(x - cx) - hx, abs(y - cy) - hy
        return (max(qx, 0) ** 2 + max(qy, 0) ** 2) ** 0.5 + min(max(qx, qy), 0) - r

    def triangle(x, y, a, b, c_):
        d = min(seg(x, y, a, b), seg(x, y, b, c_), seg(x, y, c_, a))
        def cote(p, q):
            return (q[0] - p[0]) * (y - p[1]) - (q[1] - p[1]) * (x - p[0])
        s1, s2, s3 = cote(a, b), cote(b, c_), cote(c_, a)
        dedans = (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)
        return -d if dedans else d

    trait = 0.75                                     # demi-épaisseur du trait (1,5 px)

    def distance(x, y):
        if nom == "telechargement":
            return min(seg(x, y, (8, 2.5), (8, 10.5)), seg(x, y, (4.5, 7.5), (8, 11)), seg(x, y, (11.5, 7.5), (8, 11)),
                       seg(x, y, (2.5, 13.5), (13.5, 13.5))) - trait
        if nom == "de":
            return min(abs(rrect(x, y, 2, 2, 14, 14, 3)) - trait, cercle(x, y, 5.5, 5.5, 1.25),
                       cercle(x, y, 8, 8, 1.25), cercle(x, y, 10.5, 10.5, 1.25))
        if nom == "oeil":
            # amande : intersection de deux grands cercles, plus la pupille
            amande = max(cercle(x, y, 8, 13.5, 9), cercle(x, y, 8, 2.5, 9))
            return min(abs(amande) - trait, cercle(x, y, 8, 8, 2.1))
        if nom == "coeur":
            coeur = min(cercle(x, y, 5.4, 6.2, 3.1), cercle(x, y, 10.6, 6.2, 3.1),
                        triangle(x, y, (2.45, 7.2), (13.55, 7.2), (8, 13.6)))
            return abs(coeur) - trait
        if nom == "reseau":
            return min(seg(x, y, (4, 11.5), (8, 4.5)) - trait * 0.8, seg(x, y, (8, 4.5), (12, 11.5)) - trait * 0.8,
                       seg(x, y, (4, 11.5), (12, 11.5)) - trait * 0.8,
                       cercle(x, y, 8, 4.5, 2.4), cercle(x, y, 4, 11.5, 2.4), cercle(x, y, 12, 11.5, 2.4))
        if nom == "info":
            return min(abs(cercle(x, y, 8, 8, 6.3)) - trait, cercle(x, y, 8, 5.2, 1.0),
                       seg(x, y, (8, 7.6), (8, 11.3)) - trait)
        return 99

    r, g, b = _hex(couleur)
    pixels = []
    for y in range(taille):
        for x in range(taille):
            # 4 échantillons par pixel pour un bord lisse
            cov = sum(max(0.0, min(1.0, 0.5 - distance(x + dx, y + dy) * 1.0))
                      for dx in (0.25, 0.75) for dy in (0.25, 0.75)) / 4
            pixels.append((r, g, b, round(255 * cov)))
    return _png(taille, taille, pixels)


def creer_icones_onglets(racine):
    """Icônes des onglets, une image par état : gris (normal), blanc (actif / survol), gris foncé (grisé).
    Renvoie {nom: spécification d'image ttk}."""
    c = COULEURS
    if getattr(racine, "_icones_onglets", None):
        return racine._icones_onglets
    garde, specs = [], {}
    for nom in ("telechargement", "de", "oeil", "reseau", "coeur", "info"):
        normal, blanc, grise = (tk.PhotoImage(master=racine, data=dessiner_icone(nom, coul))
                                for coul in (c["discret"], "#ffffff", c["grise"]))
        garde += [normal, blanc, grise]
        specs[nom] = (normal, "disabled", grise, "selected", blanc, "active", blanc)
    racine._icones_garde = garde
    racine._icones_onglets = specs
    return specs


def creer_onglets(racine, style):
    """Onglets façon intercalaires (style « G ») : l'actif est rouge, posé sur un trait rouge."""
    c = COULEURS
    if getattr(racine, "_images_onglets", None):       # déjà créés : le thème est simplement réappliqué
        return
    racine._images_onglets = im = {
        "normal": tk.PhotoImage(master=racine, data=dessiner_onglet(c["carte"])),
        "survol": tk.PhotoImage(master=racine, data=dessiner_onglet(c["survol"])),
        "actif": tk.PhotoImage(master=racine, data=dessiner_onglet(c["accent"])),
        "actif_survol": tk.PhotoImage(master=racine, data=dessiner_onglet(c["accent_survol"])),
        "grise": tk.PhotoImage(master=racine, data=dessiner_onglet("#191b20")),
    }
    # bas de la rangée d'onglets : un trait rouge, sur lequel l'onglet actif se pose
    # (image assez grande : Tk recopie le centre en mosaïque sur toute la page, une petite image = des milliers
    # de copies à chaque affichage et des onglets qui rament)
    cote = 256
    haut, bas = _hex(c["accent"]) + (255,), _hex(c["fond"]) + (255,)
    ligne = [haut if y < 3 else bas for y in range(cote) for _ in range(cote)]
    im["ligne"] = tk.PhotoImage(master=racine, data=_png(cote, cote, ligne))
    style.element_create("Intercalaire.tab", "image", im["normal"],
                         ("disabled", im["grise"]), ("selected", "active", im["actif_survol"]),
                         ("selected", im["actif"]), ("active", im["survol"]),
                         border=(10, 8, 13, 2), sticky="nsew")
    style.element_create("Intercalaire.client", "image", im["ligne"], border=(0, 3, 0, 0), sticky="nsew")
    # sous-onglets (« Générer une seed ») : même dessin, image plus basse (ttk ne rétrécit pas une image sous sa
    # taille : avec l'image de 48 px, les sous-onglets avaient du vide sous le texte)
    for cle, couleur in (("normal", c["carte"]), ("survol", c["survol"]), ("actif", c["accent"]),
                         ("actif_survol", c["accent_survol"]), ("grise", "#191b20")):
        im["sous_" + cle] = tk.PhotoImage(master=racine, data=dessiner_onglet(couleur, hauteur=24, rayon=6))
    style.element_create("SousIntercalaire.tab", "image", im["sous_normal"],
                         ("disabled", im["sous_grise"]), ("selected", "active", im["sous_actif_survol"]),
                         ("selected", im["sous_actif"]), ("active", im["sous_survol"]),
                         border=(10, 6, 13, 2), sticky="nsew")


def appliquer_style(racine):
    c = COULEURS
    racine.configure(bg=c["fond"])
    s = ttk.Style(racine)
    s.theme_use("clam")
    s.configure(".", background=c["fond"], foreground=c["texte"], font=(POLICE, 10),
                bordercolor=c["bord"], lightcolor=c["bord"], darkcolor=c["bord"],
                troughcolor=c["champ"], focuscolor=c["accent"], selectbackground=c["accent"],
                selectforeground="#ffffff", insertcolor=c["texte"])
    s.map(".", foreground=[("disabled", c["grise"])])

    s.configure("TFrame", background=c["fond"])
    s.configure("Carte.TFrame", background=c["carte"], relief="solid", borderwidth=1)
    s.configure("TLabel", background=c["fond"])
    s.configure("Carte.TLabel", background=c["carte"])
    s.configure("Titre.TLabel", font=(POLICE, 20, "bold"), foreground="#ffffff")
    s.configure("SousTitre.TLabel", font=(POLICE, 10), foreground=c["discret"])
    s.configure("Section.TLabel", background=c["carte"], font=(POLICE, 9, "bold"), foreground=c["discret"])
    s.configure("Note.TLabel", background=c["carte"], font=(POLICE, 9), foreground=c["discret"])
    s.configure("Nom.TLabel", background=c["carte"], font=(POLICE, 11, "bold"), foreground=c["texte"])
    s.configure("Mot.TLabel", background=c["carte"], font=(POLICE, 10), foreground=c["discret"])
    s.configure("Emoji.TLabel", background=c["carte"], font=("Segoe UI Emoji", 13), foreground=c["texte"])
    s.configure("Lien.TLabel", background=c["carte"], font=(POLICE, 10, "underline"), foreground=c["lien"])
    for nom, couleur in (("Ok", c["ok"]), ("Neutre", c["discret"]), ("Alerte", c["alerte"])):
        s.configure(f"{nom}.TLabel", background=c["carte"], foreground=couleur, font=(POLICE, 10))

    for nom in ("TCheckbutton", "TRadiobutton"):
        s.configure(nom, background=c["carte"], indicatorbackground=c["champ"],
                    indicatorforeground="#ffffff", indicatorrelief="flat", indicatormargin=(0, 0, 8, 0),
                    upperbordercolor=c["bord"], lowerbordercolor=c["bord"], padding=(0, 3))
        s.map(nom, background=[("active", c["carte"])],
              indicatorbackground=[("disabled", c["carte"]), ("selected", c["accent"]),
                                   ("active", c["survol"])],
              foreground=[("disabled", c["grise"])])
    creer_indicateurs(racine, s)
    s.configure("Fond.TCheckbutton", background=c["fond"])
    s.map("Fond.TCheckbutton", background=[("active", c["fond"])])
    for nom in ("TCheckbutton", "TRadiobutton", "Fond.TCheckbutton"):
        s.configure(nom, padding=(0, 4))

    s.configure("TEntry", fieldbackground=c["champ"], foreground=c["texte"], padding=(8, 6),
                bordercolor=c["bord"], lightcolor=c["champ"], darkcolor=c["champ"])
    s.map("TEntry", bordercolor=[("focus", c["accent"])], lightcolor=[("focus", c["accent"])])

    s.configure("TButton", background=c["champ"], foreground=c["texte"], padding=(14, 7),
                borderwidth=1, bordercolor=c["bord"], lightcolor=c["champ"], darkcolor=c["champ"],
                focusthickness=0, relief="flat")
    s.map("TButton", background=[("disabled", c["carte"]), ("pressed", c["fond"]), ("active", c["survol"])],
          lightcolor=[("active", c["survol"])], darkcolor=[("active", c["survol"])],
          foreground=[("disabled", c["grise"])])
    s.configure("Accent.TButton", background=c["accent"], foreground="#ffffff", bordercolor=c["accent"],
                lightcolor=c["accent"], darkcolor=c["accent"], font=(POLICE, 11, "bold"), padding=(26, 10))
    s.configure("Maj.Accent.TButton", font=(POLICE, 10, "bold"), padding=(12, 5))   # bouton de mise à jour (en-tête)
    # boutons des fenêtres d'alerte : même police et même marge pour le bouton rouge et le bouton gris
    s.configure("Dialogue.Accent.TButton", font=(POLICE, 10, "bold"), padding=(16, 8))
    s.configure("Dialogue.TButton", font=(POLICE, 10, "bold"), padding=(16, 8))
    s.map("Accent.TButton",
          background=[("disabled", c["champ"]), ("pressed", c["accent_presse"]), ("active", c["accent_survol"])],
          lightcolor=[("active", c["accent_survol"])], darkcolor=[("active", c["accent_survol"])],
          bordercolor=[("active", c["accent_survol"])])
    s.configure("Danger.TButton", foreground="#f08a8f")
    # barre de défilement fine, sans flèches
    s.layout("Mince.Vertical.TScrollbar", [("Vertical.Scrollbar.trough", {"sticky": "ns", "children": [
        ("Vertical.Scrollbar.thumb", {"expand": "1", "sticky": "nswe"})]})])
    s.configure("Mince.Vertical.TScrollbar", background=c["survol"], troughcolor=c["journal"], borderwidth=0,
                bordercolor=c["journal"], lightcolor=c["survol"], darkcolor=c["survol"], arrowsize=8,
                gripcount=0, width=8 if SOUS_WINDOWS else 14)
    s.map("Mince.Vertical.TScrollbar", background=[("active", "#4a505c")],
          lightcolor=[("active", "#4a505c")], darkcolor=[("active", "#4a505c")])
    # onglets façon intercalaires : coins du haut arrondis, l'actif rouge posé sur un trait rouge, icônes
    creer_onglets(racine, s)
    s.configure("TNotebook", background=c["fond"], borderwidth=0, tabmargins=(0, 0, 0, 0))
    s.layout("TNotebook", [("Intercalaire.client", {"sticky": "nswe"})])
    s.layout("TNotebook.Tab", [("Intercalaire.tab", {"sticky": "nswe", "children": [
        ("Notebook.padding", {"side": "top", "sticky": "nswe", "children": [
            ("Notebook.label", {"side": "top", "sticky": ""})]})]})])
    s.configure("TNotebook.Tab", compound="left")
    s.configure("TNotebook.Tab", background=c["fond"], foreground=c["discret"], padding=(10, 8, 7, 6),
                font=(POLICE, 10, "bold"))
    s.map("TNotebook.Tab", foreground=[("disabled", c["grise"]), ("selected", "#ffffff"), ("active", c["texte"])],
          expand=[("selected", (0, 0, 0, 0))], padding=[("selected", (10, 8, 7, 6))])
    # sous-onglets de « Générer une seed » : mêmes intercalaires, plus petits
    s.configure("Sous.TNotebook", background=c["fond"], borderwidth=0, tabmargins=(0, 0, 0, 0))
    s.layout("Sous.TNotebook", [("Intercalaire.client", {"sticky": "nswe"})])
    s.layout("Sous.TNotebook.Tab", [("SousIntercalaire.tab", {"sticky": "nswe", "children": [
        ("Notebook.padding", {"side": "top", "sticky": "nswe", "children": [
            ("Notebook.label", {"side": "top", "sticky": ""})]})]})])
    s.configure("Sous.TNotebook.Tab", background=c["fond"], foreground=c["discret"], padding=(12, 4, 10, 3),
                font=(POLICE, 9, "bold"))
    s.map("Sous.TNotebook.Tab", foreground=[("disabled", c["grise"]), ("selected", "#ffffff"), ("active", c["texte"])],
          expand=[("selected", (0, 0, 0, 0))], padding=[("selected", (12, 4, 10, 3))])
    # liste déroulante (sélecteur de langue)
    s.configure("TCombobox", fieldbackground=c["champ"], background=c["champ"], foreground=c["texte"],
                arrowcolor=c["texte"], bordercolor=c["bord"], lightcolor=c["champ"], darkcolor=c["champ"],
                padding=(8, 4))
    s.map("TCombobox", fieldbackground=[("readonly", c["champ"])], foreground=[("readonly", c["texte"])],
          selectbackground=[("readonly", c["champ"])], selectforeground=[("readonly", c["texte"])],
          background=[("active", c["survol"])], bordercolor=[("focus", c["accent"])])
    racine.option_add("*TCombobox*Listbox.background", c["champ"])
    racine.option_add("*TCombobox*Listbox.foreground", c["texte"])
    racine.option_add("*TCombobox*Listbox.selectBackground", c["accent"])
    racine.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
    racine.option_add("*TCombobox*Listbox.font", (POLICE, 10))


# Polices candidates, de la préférée à la plus courante (Windows puis Linux / Steam Deck)
CANDIDATES_POLICES = {
    "base": ("Segoe UI", "Noto Sans", "Cantarell", "DejaVu Sans", "Helvetica"),
    "ja": ("Yu Gothic UI", "Noto Sans CJK JP", "Noto Sans JP", "IPAGothic", "Droid Sans Fallback", "Helvetica"),
    "zh": ("Microsoft YaHei UI", "Noto Sans CJK SC", "Noto Sans SC", "WenQuanYi Micro Hei", "Droid Sans Fallback",
           "Helvetica"),
    "mono": ("Consolas", "DejaVu Sans Mono", "Noto Sans Mono", "Liberation Mono", "Courier"),
}
POLICE_MONO = "Consolas"


def premiere_police(candidates):
    """Première police installée de la liste (la dernière, générique, sinon)."""
    try:
        installees = set(tkfont.families())
    except tk.TclError:
        installees = set()
    return next((p for p in candidates if p in installees), candidates[-1])


def choisir_police(langue):
    """Polices de l'interface : une police avec idéogrammes pour le japonais et le chinois."""
    global POLICE, POLICE_MONO
    POLICE = premiere_police(CANDIDATES_POLICES.get(langue if langue in ("ja", "zh") else "base"))
    POLICE_MONO = premiere_police(CANDIDATES_POLICES["mono"])


def ouvrir(chemin):
    """Ouvre un fichier ou un dossier avec le programme du système."""
    if SOUS_WINDOWS:
        os.startfile(chemin)
    else:
        subprocess.Popen(["xdg-open", str(chemin)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def fichier_preferences():
    """Préférences de l'appli. Dossier renommé en v0.9.0 : l'ancien fichier (RandomizerREHD) est recopié
    une fois dans le nouveau dossier, pour garder la langue choisie."""
    if os.environ.get("APPDATA"):
        base = Path(os.environ["APPDATA"])
    else:                                       # Linux : ~/.config
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    fichier = base / "ResidentEvilHDRemasterRandomizer" / "preferences.ini"
    ancien = base / "RandomizerREHD" / "preferences.ini"
    if not fichier.exists() and ancien.exists():
        try:
            fichier.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ancien, fichier)
        except OSError:
            return ancien
    return fichier


def lire_langue():
    """Préférence enregistrée : « auto » (langue de Windows) ou un code de langue. « auto » par défaut."""
    try:
        for ligne in fichier_preferences().read_text(encoding="utf-8").splitlines():
            if ligne.startswith("langue="):
                code = ligne.split("=", 1)[1].strip()
                if code == "auto" or code in textes.LANGUES:
                    return code
    except OSError:
        pass
    return "auto"


def langue_effective(preference):
    """Langue réellement utilisée : la langue de Windows si « auto » (anglais si elle n'est pas proposée)."""
    return textes.langue_systeme() if preference == "auto" else preference


def enregistrer_langue(code):
    try:
        f = fichier_preferences()
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"langue={code}\n", encoding="utf-8")
    except OSError:
        pass                        # préférence perdue, sans gravité


class Infobulle:
    """Petite bulle d'aide qui apparaît au survol d'un widget."""

    def __init__(self, widget, texte):
        self.widget, self.texte, self.bulle = widget, texte, None
        widget.bind("<Enter>", self.montrer, add="+")
        widget.bind("<Leave>", self.cacher, add="+")

    def montrer(self, _=None):
        if self.bulle or not self.texte:
            return
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() - 34
        self.bulle = tk.Toplevel(self.widget)
        self.bulle.wm_overrideredirect(True)
        self.bulle.wm_geometry(f"+{x}+{y}")
        tk.Label(self.bulle, text=self.texte, bg=COULEURS["carte"], fg=COULEURS["texte"], padx=8, pady=4,
                 relief="solid", borderwidth=1, font=(POLICE, 9)).pack()

    def cacher(self, _=None):
        if self.bulle:
            self.bulle.destroy()
            self.bulle = None


class Defilable(ttk.Frame):
    """Zone qui défile verticalement quand son contenu dépasse (petits écrans, Steam Deck 1280×800).
    Le contenu se place dans .interieur ; la barre n'apparaît que si elle sert."""

    def __init__(self, parent):
        super().__init__(parent)
        self.toile = tk.Canvas(self, bg=COULEURS["fond"], highlightthickness=0, borderwidth=0,
                               yscrollincrement=24)
        self.barre = ttk.Scrollbar(self, orient="vertical", style="Mince.Vertical.TScrollbar",
                                   command=self.toile.yview)
        self.interieur = ttk.Frame(self.toile)
        self._fenetre = self.toile.create_window(0, 0, window=self.interieur, anchor="nw")
        self.toile.configure(yscrollcommand=self._regler_barre)
        self.toile.pack(side="left", fill="both", expand=True)
        self.interieur.bind("<Configure>", lambda _: self.toile.configure(scrollregion=self.toile.bbox("all")))
        self.toile.bind("<Configure>", lambda e: self.toile.itemconfigure(self._fenetre, width=e.width))

    def _regler_barre(self, debut, fin):
        self.barre.set(debut, fin)
        utile = float(debut) > 0 or float(fin) < 1
        if utile and not self.barre.winfo_ismapped():
            self.barre.pack(side="right", fill="y", padx=(6, 0), before=self.toile)
        elif not utile and self.barre.winfo_ismapped():
            self.barre.pack_forget()

    def defiler(self, pas):
        if self.toile.yview() != (0.0, 1.0):
            self.toile.yview_scroll(pas, "units")


def barre_titre_sombre(fenetre):
    """Barre de titre sombre sous Windows 10/11 (sans effet ailleurs)."""
    try:
        import ctypes
        fenetre.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(fenetre.winfo_id())
        valeur = ctypes.c_int(1)
        for attribut in (20, 19):          # DWMWA_USE_IMMERSIVE_DARK_MODE (récent, puis ancien)
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, attribut, ctypes.byref(valeur), 4) == 0:
                break
    except Exception:
        pass


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITRE)
        # taille adaptée à l'écran : le Steam Deck (1280×800, barre des tâches comprise) laisse ~720 px
        largeur_ecran, hauteur_ecran = self.winfo_screenwidth(), self.winfo_screenheight()
        self.minsize(640, 480)
        self.geometry(f"{min(1140, largeur_ecran - 40)}x{min(950, hauteur_ecran - 80)}")
        icone = trouver_ressource("icone.ico" if SOUS_WINDOWS else "icone.png", ("",))
        if icone:
            try:
                if SOUS_WINDOWS:
                    self.iconbitmap(default=str(icone))   # barre de titre et barre des tâches
                else:
                    self._icone = tk.PhotoImage(file=str(icone))
                    self.iconphoto(True, self._icone)
            except tk.TclError:
                pass
        self.preference_langue = lire_langue()                 # « auto » ou un code de langue
        self.langue = tk.StringVar(value=langue_effective(self.preference_langue))
        choisir_police(self.langue.get())
        appliquer_style(self)
        self.donnees = trouver_ressource(gen.FICHIER_PAR_DEFAUT)
        self.dll = trouver_ressource("xinput1_4.dll")

        self.personnage = tk.StringVar(value="Chris")
        self.difficulte = tk.StringVar(value="Facile")
        self.armes = tk.BooleanVar(value=False)
        self.visibles = tk.BooleanVar(value=True)              # objets visibles par terre et dans l'aperçu
        self.malle = tk.BooleanVar(value=True)                 # malle de départ mélangée avec les autres objets
        self.couteau = tk.BooleanVar(value=False)              # couteau de départ mélangé (risque : partir sans arme)
        # une case par arme de base (cochées par défaut, sauf celles pas encore relevées) ; visibles seulement avec « Armes aléatoires »
        self.arme_depart = tk.BooleanVar(value=True)           # une arme toujours au pistolet du hall
        self.armes_cochees = {cle: tk.BooleanVar(value=id_arme is not None) for cle, id_arme, _ in gen.ARMES}
        self.cles = tk.BooleanVar(value=False)
        self.sans_logique = tk.BooleanVar(value=False)         # option à venir (grisée) : clés sans logique
        self.ennemis = tk.BooleanVar(value=False)              # option à venir (grisée)
        self.armes_bonus = tk.BooleanVar(value=False)          # option « Fun » : Samurai Edge + lance-roquettes
        self.bonus_coches = {ident: tk.BooleanVar(value=True) for _, ident, _ in gen.ARMES_BONUS}
        self.graine = tk.StringVar(value=str(gen.tirer_graine()))
        jeu = gen.trouver_dossier_jeu()
        self.dossier_jeu = tk.StringVar(value=str(jeu) if jeu else "")
        self.installer = tk.BooleanVar(value=True)
        self.afficher_spoiler = tk.BooleanVar(value=False)
        self.recherche_spoiler = tk.StringVar()              # filtre du spoiler (vide = tout afficher)
        self.recherche_spoiler.trace_add("write", lambda *_: self.afficher_resultat())
        self.releve = tk.BooleanVar(value=False)
        self.proton_dinput8 = tk.BooleanVar(value=False)      # option de lancement : charger aussi dinput8.dll
        self.option_proton = tk.StringVar(value=OPTION_PROTON)
        self._dossier_dinput8 = None                          # dossier pour lequel la case a été réglée
        self.etat_jeu = tk.StringVar()             # résumé texte de l'état (utilisé par les tests)
        self.dossier_seeds = dossier_programme() / "seeds"
        self.dernier_resultat = None               # (messages, spoiler, ok) de la dernière génération

        self.maj = None                            # mise à jour disponible (infos GitHub) ou None
        self.dll_prete = False                     # DLL du randomizer installée et à jour
        self.construire()
        threading.Thread(target=self.verifier_mise_a_jour, daemon=True).start()
        self.dossier_jeu.trace_add("write", lambda *_: self.actualiser_etat())
        self.personnage.trace_add("write", lambda *_: self.afficher_liste_armes())
        self.actualiser_etat()
        self.afficher_resultat()
        if self.dll_prete:                         # sinon on reste sur « Installation »
            self.onglets.select(self.page_generer)
        barre_titre_sombre(self)
        # molette (Windows) et molette / pavé tactile (Linux) : fait défiler la zone sous le pointeur
        self.bind_all("<MouseWheel>", lambda e: self.molette(e, -1 if e.delta > 0 else 1))
        self.bind_all("<Button-4>", lambda e: self.molette(e, -1))
        self.bind_all("<Button-5>", lambda e: self.molette(e, 1))

    def molette(self, evenement, sens):
        w = self.winfo_containing(evenement.x_root, evenement.y_root)
        while w is not None:
            if isinstance(w, (tk.Text, ttk.Combobox)):   # ils défilent déjà tout seuls
                return
            if isinstance(w, Defilable):
                w.defiler(3 * sens)
                return
            w = w.master

    def t(self, cle, **valeurs):
        """Texte dans la langue choisie."""
        return textes.tr(cle, self.langue.get(), **valeurs)

    # ------------------------------------------------------------------ interface
    def carte(self, parent, titre):
        """Section à fond légèrement plus clair, avec un petit titre en capitales."""
        cadre = ttk.Frame(parent, style="Carte.TFrame", padding=(16, 12, 16, 14))
        ttk.Label(cadre, text=titre.upper(), style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        interieur = ttk.Frame(cadre, style="Carte.TFrame", borderwidth=0)
        interieur.pack(fill="both", expand=True)
        return cadre, interieur

    def police_texte(self):
        """Police des zones de texte : Consolas (latin, cyrillique) ou la police de la langue."""
        return (POLICE_MONO, 10) if self.langue.get() not in ("ja", "zh") else (POLICE, 10)

    def construire(self):
        self.racine = racine = ttk.Frame(self, padding=(20, 16, 20, 20))
        racine.pack(fill="both", expand=True)

        entete = ttk.Frame(racine)
        entete.pack(fill="x", pady=(0, 12))
        # logo (le zombie qui croque un dé) : logo_entete.png, déjà réduit à 40 px pour rester net
        if not getattr(self, "_logo_entete", None):
            self._logo_entete = None
            logo = trouver_ressource("logo_entete.png", ("",))
            try:
                if logo:
                    self._logo_entete = tk.PhotoImage(master=self, file=str(logo))
            except tk.TclError:
                pass
        if self._logo_entete:
            ttk.Label(entete, image=self._logo_entete).pack(side="left", padx=(0, 10), pady=(3, 0))
        ttk.Label(entete, text=NOM_APPLI, style="Titre.TLabel").pack(side="left")
        # le sous-titre est placé en dernier : si la fenêtre est étroite, c'est lui qui est raccourci
        self.sous_titre = ttk.Label(entete, text=f"v{VERSION}",
                                    style="SousTitre.TLabel")
        # sélecteur de langue, en haut à droite
        auto = f"{self.t('langue_auto')} ({textes.LANGUES[textes.langue_systeme()]})"
        noms = [auto] + list(textes.LANGUES.values())
        self.choix_langue = ttk.Combobox(entete, values=noms, state="readonly", font=(POLICE, 10),
                                         width=max(12, len(auto) + 2))
        self.choix_langue.set(auto if self.preference_langue == "auto" else textes.LANGUES[self.langue.get()])
        if not SOUS_WINDOWS or os.environ.get("RANDOMIZER_LINUX"):
            # Steam Deck en mode Jeu : la fenêtre n'a pas de barre de titre, donc pas de croix pour fermer
            ttk.Button(entete, text=self.t("quitter"), style="Danger.TButton",
                       command=self.destroy).pack(side="right", padx=(12, 0), pady=(8, 0))
        self.choix_langue.pack(side="right", pady=(8, 0))
        self.choix_langue.bind("<<ComboboxSelected>>", lambda _: self.changer_langue())
        if SOUS_WINDOWS:                            # sous Linux, pas toujours de police d'emoji
            ttk.Label(entete, text="🌐", style="SousTitre.TLabel").pack(side="right", padx=(0, 6), pady=(8, 0))
        # bouton de mise à jour, à gauche des langues ; affiché seulement si une version plus récente existe
        self.bouton_maj = ttk.Button(entete, style="Maj.Accent.TButton", command=self.mettre_a_jour)
        self.sous_titre.pack(side="left", padx=(12, 0), pady=(10, 0))
        if self.maj:
            self.afficher_bouton_maj()

        self.onglets = ttk.Notebook(racine)
        self.onglets.pack(fill="both", expand=True)
        # Installation d'abord ; « Générer une seed » et « Spoiler » restent grisés tant que la DLL
        # n'est pas installée et à jour (voir verrouiller_onglets)
        self.page_install = ttk.Frame(self.onglets, padding=(0, 14, 0, 0))
        self.page_generer = ttk.Frame(self.onglets, padding=(0, 14, 0, 0))
        self.page_spoiler = ttk.Frame(self.onglets, padding=(0, 14, 0, 0))
        page_aide = ttk.Frame(self.onglets, padding=(0, 14, 0, 0))
        icones = creer_icones_onglets(self)
        page_info = ttk.Frame(self.onglets, padding=(0, 14, 0, 0))
        page_archipelago = ttk.Frame(self.onglets, padding=(0, 14, 0, 0))
        for page, cle, icone in ((self.page_install, "onglet_installation", "telechargement"),
                                 (self.page_generer, "onglet_generer", "de"),
                                 (self.page_spoiler, "onglet_spoiler", "oeil"),
                                 (page_archipelago, "onglet_archipelago", "reseau"),
                                 (page_aide, "onglet_aide", "coeur"),
                                 (page_info, "onglet_info", "info")):
            self.onglets.add(page, text=" " + self.t(cle), image=icones[icone], compound="left")
        self.construire_installation(self.page_install)
        self.construire_generation(self.page_generer)
        self.construire_spoiler(self.page_spoiler)
        self.construire_archipelago(page_archipelago)
        self.construire_aide(page_aide)
        self.construire_info(page_info)

        if not self.donnees:
            self.ecrire(self.t("donnees_absentes", fichier=gen.FICHIER_PAR_DEFAUT))
            self.bouton_generer.state(["disabled"])
        else:
            self.ecrire(self.t("pret"))

    def changer_langue(self):
        i = self.choix_langue.current()            # 0 = automatique, puis les langues dans l'ordre
        preference = "auto" if i <= 0 else textes.ORDRE[i - 1]
        code = langue_effective(preference)
        if preference == self.preference_langue and code == self.langue.get():
            return
        onglet = self.onglets.index("current")
        self.preference_langue = preference
        self.langue.set(code)
        enregistrer_langue(preference)
        choisir_police(code)
        appliquer_style(self)                       # polices du thème dans la nouvelle langue
        self.racine.destroy()                       # on reconstruit la fenêtre : les choix sont gardés
        self.construire()
        self.onglets.select(onglet)
        self.actualiser_etat()
        self.afficher_resultat()

    # --- onglet « Installation » : dossier du jeu et DLL (obligatoire avant de générer une seed)
    def construire_installation(self, page):
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)
        defile = Defilable(page)
        defile.grid(row=0, column=0, sticky="nsew")
        cadre = defile.interieur
        cadre.columnconfigure(0, weight=1)
        etapes = self.t("install_etapes")
        if not SOUS_WINDOWS or os.environ.get("RANDOMIZER_LINUX"):
            etapes += "\n" + self.t("install_etape_proton")
        ttk.Label(cadre, text=etapes, wraplength=680, justify="left").grid(row=0, column=0, sticky="w",
                                                                         pady=(0, 14))

        jeu, j = self.carte(cadre, self.t("carte_jeu"))
        jeu.grid(row=1, column=0, sticky="nsew")
        j.columnconfigure(0, weight=1)
        ttk.Entry(j, textvariable=self.dossier_jeu).grid(row=0, column=0, sticky="ew")
        ttk.Button(j, text=self.t("parcourir"), command=self.choisir_dossier).grid(row=0, column=1, padx=(8, 0))
        etats = ttk.Frame(j, style="Carte.TFrame", borderwidth=0)
        etats.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.badge_dll = ttk.Label(etats, style="Neutre.TLabel")
        self.badge_dll.pack(side="left")
        self.badge_seed = ttk.Label(etats, style="Neutre.TLabel")
        self.badge_seed.pack(side="left", padx=(24, 0))
        self.badge_version = ttk.Label(j, style="Alerte.TLabel", wraplength=640, justify="left")
        self.badge_version.grid(row=2, column=0, columnspan=2, sticky="w")
        gestion = ttk.Frame(j, style="Carte.TFrame", borderwidth=0)
        gestion.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.bouton_dll = ttk.Button(gestion, text=self.t("installer_dll"), command=self.installer_dll)
        self.bouton_dll.pack(side="left")
        self.bouton_retirer_dll = ttk.Button(gestion, text=self.t("desinstaller_dll"), style="Danger.TButton",
                                             command=self.retirer_dll)
        self.bouton_retirer_dll.pack(side="left", padx=8)
        ttk.Label(j, text=self.t("note_desinstaller"),
                  style="Note.TLabel").grid(row=4, column=0, columnspan=2, sticky="w", pady=(6, 0))
        if not SOUS_WINDOWS or os.environ.get("RANDOMIZER_LINUX"):
            # Sous Linux / Steam Deck, le jeu passe par Proton : l'option de lancement fait charger notre DLL
            ttk.Label(j, text=self.t("proton_titre"), style="Carte.TLabel").grid(
                row=5, column=0, columnspan=2, sticky="w", pady=(12, 2))
            option = ttk.Entry(j, font=(POLICE_MONO, 10), textvariable=self.option_proton)
            option.state(["readonly"])
            option.grid(row=6, column=0, sticky="ew")
            ttk.Button(j, text=self.t("copier"), command=self.copier_option_proton).grid(
                row=6, column=1, padx=(8, 0))
            self.case_dinput8 = ttk.Checkbutton(j, variable=self.proton_dinput8,
                                                command=self.regler_option_proton)
            self.case_dinput8.grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 0))
            ttk.Label(j, text=self.t("proton_note"), style="Note.TLabel", wraplength=640,
                      justify="left").grid(row=8, column=0, columnspan=2, sticky="w", pady=(4, 0))
            self.regler_option_proton()

        bas = ttk.Frame(page)
        bas.grid(row=1, column=0, sticky="ew", pady=(14, 0))
        self.bouton_suivant = ttk.Button(bas, text=self.t("suivant_generer"), style="Accent.TButton",
                                         command=lambda: self.onglets.select(self.page_generer))
        self.bouton_suivant.pack(side="right")

    # --- onglet « Générer une seed » : partie, options, puis génération
    def construire_generation(self, page):
        # Sous-onglets, dans cet ordre (demande du joueur, 21/11/2026) : Personnage et difficulté, Options
        # (+ « Pour les fous » dans sa propre tuile, sous les clés aléatoires), Ennemis, Fun. Les sous-onglets restent
        # toujours visibles : seul le contenu de chacun défile (petits écrans). Le bouton Générer et le journal, en
        # bas, gardent la même taille quel que soit le sous-onglet.
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)
        self.sous_onglets = ttk.Notebook(page, style="Sous.TNotebook")
        self.sous_onglets.grid(row=0, column=0, sticky="nsew")
        pages = {}
        for cle in ("carte_partie", "carte_options", "carte_ennemis", "carte_fun"):
            conteneur = ttk.Frame(self.sous_onglets, padding=(0, 12, 0, 0))
            self.sous_onglets.add(conteneur, text=self.t(cle))
            defile = Defilable(conteneur)
            defile.pack(fill="both", expand=True)
            pages[cle] = defile.interieur
        gauche = pages["carte_partie"]

        # --- Personnage et difficulté
        partie, p = self.carte(gauche, self.t("carte_partie"))
        partie.pack(fill="x")
        p.columnconfigure(1, weight=1)
        a_venir = f"  · {self.t('a_venir')}"
        ttk.Label(p, text=self.t("personnage"), style="Carte.TLabel").grid(row=0, column=0, sticky="w")
        for i, (nom, dispo) in enumerate((("Chris", True), ("Jill", False))):
            ttk.Radiobutton(p, text=nom if dispo else nom + a_venir, value=nom, variable=self.personnage,
                            state="normal" if dispo else "disabled").grid(row=1 + i, column=0, sticky="w")
        ttk.Label(p, text=self.t("difficulte"), style="Carte.TLabel").grid(row=0, column=1, sticky="w",
                                                                         padx=(24, 0))
        for i, nom in enumerate(("Très facile", "Facile", "Normal", "Difficile", "Real Survival")):
            dispo = nom == "Facile"          # nos relevés sont en Facile (réponse « II. Gamer », 22/11/2026)
            libelle = self.t(f"diff_{nom}")
            ttk.Radiobutton(p, text=libelle if dispo else libelle + a_venir, value=nom,
                            variable=self.difficulte, state="normal" if dispo else "disabled"
                            ).grid(row=1 + i, column=1, sticky="w", padx=(24, 0))
        # comment choisir la bonne difficulté dans le jeu (la DLL n'applique pas la seed sinon)
        ttk.Label(p, text=self.t("note_difficulte"), style="Alerte.TLabel", wraplength=300,
                  justify="left").grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 0))

        # --- Fun : options qui rendent la partie plus facile
        fun, f = self.carte(pages["carte_fun"], self.t("carte_fun"))
        fun.pack(fill="x")
        ttk.Label(f, text=self.t("note_fun"), style="Note.TLabel", wraplength=300,
                  justify="left").pack(anchor="w", pady=(0, 6))
        ttk.Checkbutton(f, text=self.t("armes_bonus"), variable=self.armes_bonus,
                        command=self.afficher_liste_bonus).pack(anchor="w")
        self.note_bonus = ttk.Label(f, text=self.t("note_armes_bonus_fun"), style="Note.TLabel", wraplength=300,
                                    justify="left")
        self.note_bonus.pack(anchor="w", padx=(27, 0))
        # une case par arme bonus, visible seulement quand « Armes bonus » est cochée
        self.liste_bonus = ttk.Frame(f, style="Carte.TFrame", borderwidth=0)
        for cle, ident, _ in gen.ARMES_BONUS:
            ttk.Checkbutton(self.liste_bonus, text=self.t(cle), variable=self.bonus_coches[ident]).pack(anchor="w")
        self.afficher_liste_bonus()
        ttk.Label(f, text=self.t("note_armes_bonus"), style="Note.TLabel", wraplength=300,
                  justify="left").pack(anchor="w", padx=(27, 0), pady=(4, 0))

        # --- Options
        options, o = self.carte(pages["carte_options"], self.t("carte_options"))
        options.pack(fill="x")
        ttk.Checkbutton(o, text=self.t("objets_visibles"), variable=self.visibles).pack(anchor="w")
        ttk.Label(o, text=self.t("note_objets_visibles"), style="Note.TLabel", wraplength=280,
                  justify="left").pack(anchor="w", padx=(27, 0))
        ttk.Checkbutton(o, text=self.t("malle_aleatoire"), variable=self.malle).pack(anchor="w", pady=(6, 0))
        ttk.Label(o, text=self.t("note_malle_aleatoire"), style="Note.TLabel", wraplength=280,
                  justify="left").pack(anchor="w", padx=(27, 0))
        ttk.Checkbutton(o, text=self.t("armes_aleatoires"), variable=self.armes,
                        command=self.afficher_liste_armes).pack(anchor="w", pady=(6, 0))
        self.note_armes = ttk.Label(o, text=self.t("note_armes"), style="Note.TLabel", wraplength=280,
                                    justify="left")
        self.note_armes.pack(anchor="w", padx=(27, 0))
        self.liste_armes = ttk.Frame(o, style="Carte.TFrame", borderwidth=0)
        self.cases_armes = {}
        for cle, id_arme, perso in gen.ARMES:
            texte = self.t(cle)            # armes d'un seul personnage : cachées pour l'autre (afficher_liste_armes)
            if id_arme is None:
                texte += a_venir
            case = ttk.Checkbutton(self.liste_armes, text=texte, variable=self.armes_cochees[cle])
            self.cases_armes[cle] = (case, id_arme, perso)
        # « Arme garantie au départ » : juste sous les armes aléatoires (grisée sans elles)
        self.case_arme_depart = ttk.Checkbutton(o, text=self.t("arme_depart"), variable=self.arme_depart)
        self.case_arme_depart.pack(anchor="w", pady=(6, 0))
        ttk.Label(o, text=self.t("note_arme_depart"), style="Note.TLabel", wraplength=280,
                  justify="left").pack(anchor="w", padx=(27, 0))
        # « Couteau de départ aléatoire » : sans arme garantie, on peut commencer sans arme (avertissement en orange)
        ttk.Checkbutton(o, text=self.t("couteau_aleatoire"), variable=self.couteau).pack(anchor="w", pady=(6, 0))
        ttk.Label(o, text=self.t("note_couteau_aleatoire"), style="Alerte.TLabel", wraplength=280,
                  justify="left").pack(anchor="w", padx=(27, 0))
        self.afficher_liste_armes()
        ttk.Checkbutton(o, text=self.t("cles_aleatoires") + a_venir, variable=self.cles,
                        state="disabled").pack(anchor="w", pady=(6, 0))

        # --- Pour les fous : options qui peuvent rendre la partie impossible à finir
        fous, fo = self.carte(pages["carte_options"], self.t("carte_fous"))
        fous.pack(fill="x", pady=(16, 0))
        ttk.Checkbutton(fo, text=self.t("sans_logique") + a_venir, variable=self.sans_logique,
                        state="disabled").pack(anchor="w")
        ttk.Label(fo, text=self.t("note_sans_logique"), style="Note.TLabel", wraplength=280,
                  justify="left").pack(anchor="w", padx=(27, 0))

        # --- Ennemis
        ennemis, en = self.carte(pages["carte_ennemis"], self.t("carte_ennemis"))
        ennemis.pack(fill="x")
        ttk.Checkbutton(en, text=self.t("ennemis_aleatoires") + a_venir, variable=self.ennemis,
                        state="disabled").pack(anchor="w")

        for interieur in pages.values():
            self.notes_pleine_largeur(interieur)

        # --- Actions
        boutons = ttk.Frame(page)
        boutons.grid(row=1, column=0, sticky="ew", pady=(14, 0))
        self.bouton_generer = ttk.Button(boutons, text=self.t("generer"), style="Accent.TButton",
                                         command=self.generer)
        self.bouton_generer.pack(side="left")
        # graine juste à côté du bouton Générer (même graine + mêmes options = même résultat)
        ttk.Label(boutons, text=self.t("graine")).pack(side="left", padx=(16, 6))
        champ_graine = ttk.Entry(boutons, textvariable=self.graine, width=10, font=(POLICE, 11))
        champ_graine.pack(side="left")
        ttk.Button(boutons, text=self.t("au_hasard"),
                   command=lambda: self.graine.set(str(gen.tirer_graine()))).pack(side="left", padx=(8, 0))
        Infobulle(champ_graine, self.t("note_graine"))
        ttk.Checkbutton(boutons, text=self.t("installer_seed_case"), style="Fond.TCheckbutton",
                        variable=self.installer).pack(side="left", padx=(16, 0))
        ttk.Button(boutons, text=self.t("dossier_seeds"),
                   command=self.ouvrir_seeds).pack(side="right")
        # supprimer la seed installée : juste à gauche de « Dossier des seeds »
        self.bouton_retirer_seed = ttk.Button(boutons, text=self.t("supprimer_seed"),
                                              style="Danger.TButton", command=self.retirer_seed)
        self.bouton_retirer_seed.pack(side="right", padx=(0, 8))

        # --- Journal de l'application
        zone = tk.Frame(page, bg=COULEURS["bord"], padx=1, pady=1)
        zone.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        self.journal = tk.Text(zone, width=1, height=5, wrap="word", state="disabled", font=self.police_texte(),
                               bg=COULEURS["journal"], fg=COULEURS["texte"], insertbackground=COULEURS["texte"],
                               selectbackground=COULEURS["accent"], relief="flat", borderwidth=0,
                               padx=12, pady=10, highlightthickness=0)
        defil = ttk.Scrollbar(zone, orient="vertical", style="Mince.Vertical.TScrollbar",
                              command=self.journal.yview)
        self.journal.configure(yscrollcommand=defil.set)
        defil.pack(side="right", fill="y")
        self.journal.pack(side="left", fill="both", expand=True)
        page.rowconfigure(2, weight=0)                # journal : hauteur fixe (5 lignes), le reste aux sous-onglets

    # --- onglet « Spoiler » : la liste complète des changements, cachée tant qu'on ne coche pas
    def construire_spoiler(self, cadre):
        cadre.columnconfigure(0, weight=1)
        cadre.rowconfigure(0, weight=1)
        carte, s = self.carte(cadre, self.t("carte_spoiler"))
        carte.grid(row=0, column=0, sticky="nsew")
        ttk.Checkbutton(s, text=self.t("afficher_spoiler"), variable=self.afficher_spoiler,
                        command=self.afficher_resultat).pack(anchor="w")
        self.note_spoiler = ttk.Label(s, style="Note.TLabel", wraplength=660, justify="left")
        self.note_spoiler.pack(anchor="w", padx=(27, 0), pady=(2, 10))
        # barre de recherche : ne garde que les lignes qui contiennent le texte (sans tenir compte des accents)
        barre = ttk.Frame(s, style="Carte.TFrame", borderwidth=0)
        barre.pack(anchor="w", fill="x", pady=(0, 8))
        ttk.Label(barre, text=self.t("rechercher"), style="Carte.TLabel").pack(side="left")
        self.champ_recherche = ttk.Entry(barre, textvariable=self.recherche_spoiler, width=32,
                                         font=(POLICE, 11))
        self.champ_recherche.pack(side="left", padx=(8, 0))
        ttk.Button(barre, text=self.t("effacer_recherche"),
                   command=lambda: self.recherche_spoiler.set("")).pack(side="left", padx=(8, 0))
        self.compte_recherche = ttk.Label(barre, style="Note.TLabel")
        self.compte_recherche.pack(side="left", padx=(12, 0))
        # tableau en 3 colonnes : lieu | objet d'origine | objet qui le remplace (clic sur un titre = tri)
        zone = tk.Frame(s, bg=COULEURS["bord"], padx=1, pady=1)
        zone.pack(fill="both", expand=True)
        st = ttk.Style(self)
        st.configure("Spoiler.Treeview", background=COULEURS["journal"], fieldbackground=COULEURS["journal"],
                     foreground=COULEURS["texte"], rowheight=28, font=(POLICE, 10), borderwidth=0)
        st.map("Spoiler.Treeview", background=[("selected", COULEURS["survol"])],
               foreground=[("selected", "#ffffff")])
        st.configure("Spoiler.Treeview.Heading", background=COULEURS["carte"], foreground=COULEURS["discret"],
                     font=(POLICE, 10, "bold"), relief="flat", padding=(8, 6))
        st.map("Spoiler.Treeview.Heading", background=[("active", COULEURS["survol"])])
        st.layout("Spoiler.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        colonnes = ("lieu", "origine", "nouveau")
        self.zone_spoiler = ttk.Treeview(zone, columns=colonnes, show="headings", style="Spoiler.Treeview",
                                         selectmode="browse")
        self.tri_spoiler = ("lieu", False)          # (colonne, ordre inverse)
        for col, largeur in zip(colonnes, (420, 260, 300)):
            self.zone_spoiler.heading(col, text=self.t(f"col_{col}"), anchor="w",
                                      command=lambda c=col: self.trier_spoiler(c))
            self.zone_spoiler.column(col, width=largeur, minwidth=120, anchor="w", stretch=True)
        self.zone_spoiler.tag_configure("impair", background=COULEURS["carte"])
        self.zone_spoiler.tag_configure("meme", foreground=COULEURS["discret"])     # objet inchangé
        self.zone_spoiler.tag_configure("bonus", foreground="#ff6b6b", font=(POLICE, 10, "bold"))
        defil = ttk.Scrollbar(zone, orient="vertical", style="Mince.Vertical.TScrollbar",
                              command=self.zone_spoiler.yview)
        self.zone_spoiler.configure(yscrollcommand=defil.set)
        defil.pack(side="right", fill="y")
        self.zone_spoiler.pack(side="left", fill="both", expand=True)
        # lignes verticales entre les colonnes (le Treeview n'en dessine pas) : posées par-dessus, recalées
        # quand la fenêtre ou une colonne change de taille
        self.separateurs_spoiler = [tk.Frame(self.zone_spoiler, bg=COULEURS["bord"], width=1,
                                             cursor="sb_h_double_arrow") for _ in colonnes[1:]]
        self.glisse_colonne = None                  # (n° de la limite, x de départ, largeurs de départ)
        t = self.zone_spoiler
        t.bind("<Configure>", lambda _: self.after_idle(self.placer_separateurs), add="+")
        t.bind("<Motion>", self.survol_colonnes, add="+")
        t.bind("<ButtonPress-1>", self.saisir_colonne, add="+")
        t.bind("<B1-Motion>", self.glisser_colonne, add="+")
        t.bind("<ButtonRelease-1>", self.lacher_colonne, add="+")
        for ligne in self.separateurs_spoiler:     # la ligne elle-même s'attrape aussi
            ligne.bind("<ButtonPress-1>", lambda e, l=ligne: self.saisir_colonne(e, l.winfo_x() + e.x))
            ligne.bind("<B1-Motion>", lambda e, l=ligne: self.glisser_colonne(e, l.winfo_x() + e.x))
            ligne.bind("<ButtonRelease-1>", self.lacher_colonne)
        self.after_idle(self.placer_separateurs)

    # --- largeur des colonnes du spoiler : on attrape une limite (dans les titres ou les lignes) et on glisse
    def limite_proche(self, x, marge=5):
        """N° de la limite de colonne à moins de « marge » pixels de x, ou None."""
        bord = 0
        for i, col in enumerate(self.zone_spoiler["columns"][:-1]):
            bord += self.zone_spoiler.column(col, "width")
            if abs(x - bord) <= marge:
                return i
        return None

    def survol_colonnes(self, e):
        if self.glisse_colonne is None:
            self.zone_spoiler.configure(cursor="sb_h_double_arrow" if self.limite_proche(e.x) is not None else "")

    def saisir_colonne(self, e, x=None):
        x = e.x if x is None else x
        i = self.limite_proche(x)
        if i is None:
            return None
        cols = self.zone_spoiler["columns"]
        self.glisse_colonne = (i, x, self.zone_spoiler.column(cols[i], "width"),
                               self.zone_spoiler.column(cols[i + 1], "width"))
        return "break"

    def glisser_colonne(self, e, x=None):
        if self.glisse_colonne is None:
            return None
        x = e.x if x is None else x
        i, x0, gauche, droite = self.glisse_colonne
        dx = max(80 - gauche, min(x - x0, droite - 80))     # chaque colonne garde au moins 80 px
        cols = self.zone_spoiler["columns"]
        self.zone_spoiler.column(cols[i], width=gauche + dx)
        self.zone_spoiler.column(cols[i + 1], width=droite - dx)
        self.placer_separateurs()
        return "break"

    def lacher_colonne(self, _=None):
        if self.glisse_colonne is None:
            return None
        self.glisse_colonne = None
        self.placer_separateurs()
        return "break"

    def placer_separateurs(self):
        """Place les lignes de séparation à la limite droite de chaque colonne (sauf la dernière)."""
        x = 0
        for col, ligne in zip(self.zone_spoiler["columns"], self.separateurs_spoiler):
            x += self.zone_spoiler.column(col, "width")
            ligne.place(x=x - 1, y=0, width=1, relheight=1)

    def trier_spoiler(self, colonne):
        """Clic sur un titre de colonne : trie le tableau du spoiler (un 2e clic inverse l'ordre)."""
        actuelle, inverse = self.tri_spoiler
        self.tri_spoiler = (colonne, not inverse if colonne == actuelle else False)
        self.afficher_resultat()

    def notes_pleine_largeur(self, racine_widget):
        """Les petites notes grises suivent la largeur de leur carte (au lieu d'une largeur fixe qui laisse la
        moitié droite des cartes vide) : chaque note se recalcule quand sa carte change de taille."""
        def parcourir(w):
            for enfant in w.winfo_children():
                if isinstance(enfant, ttk.Label) and str(enfant.cget("style")) in ("Note.TLabel", "Alerte.TLabel"):
                    try:
                        retrait = enfant.pack_info().get("padx", 0)
                    except tk.TclError:
                        retrait = 0
                    if isinstance(retrait, (tuple, list)):
                        retrait = retrait[0]
                    elif isinstance(retrait, str):
                        retrait = int(str(retrait).split()[0])
                    enfant.master.bind("<Configure>", lambda e, l=enfant, r=int(retrait):
                                       l.configure(wraplength=max(160, e.width - r - 12)), add="+")
                parcourir(enfant)
        parcourir(racine_widget)

    def afficher_liste_bonus(self):
        """Cases des armes bonus sous « Armes bonus » (seulement quand la case est cochée)."""
        if self.armes_bonus.get():
            self.liste_bonus.pack(anchor="w", padx=(27, 0), pady=(4, 0), after=self.note_bonus)
        else:
            self.liste_bonus.pack_forget()

    def armes_bonus_choisies(self):
        """Ids des armes bonus cochées (vide si l'option est décochée)."""
        if not self.armes_bonus.get():
            return set()
        return {ident for ident, v in self.bonus_coches.items() if v.get()}

    def afficher_liste_armes(self):
        """Liste des armes sous « Armes aléatoires » (seulement quand la case est cochée).
        Une arme dont l'id n'est pas encore connu reste grisée ; celle de l'autre personnage est cachée."""
        if self.armes.get():
            self.liste_armes.pack(anchor="w", padx=(27, 0), pady=(4, 0), after=self.note_armes)
        else:
            self.liste_armes.pack_forget()
        # seulement les armes du personnage choisi (lance-grenades : Jill, lance-flammes : Chris ; tests en jeu du
        # 21/11/2026 : l'autre personnage ne peut pas s'en servir), dans l'ordre de gen.ARMES
        for case, id_arme, perso in self.cases_armes.values():
            case.pack_forget()
            if perso in (None, self.personnage.get()):
                case.pack(anchor="w")
                case.state(["!disabled"] if id_arme is not None else ["disabled"])
        if hasattr(self, "case_arme_depart"):
            self.case_arme_depart.state(["!disabled"] if self.armes.get() else ["disabled"])

    def armes_choisies(self):
        """Ids des armes cochées et utilisables (envoyés au générateur)."""
        return {id_arme for cle, (case, id_arme, perso) in self.cases_armes.items()
                if id_arme is not None and perso in (None, self.personnage.get()) and self.armes_cochees[cle].get()}

    def spoiler_actuel(self):
        """(titre, contenu de la seed .json) du spoiler : dernière seed générée, sinon celle installée dans le jeu."""
        if self.dernier_resultat and self.dernier_resultat[1]:
            return self.t("spoiler_genere"), self.dernier_resultat[1]
        dossier = self.dossier_jeu.get()
        seed = gen.seed_installee(dossier) if dossier and Path(dossier).exists() else None
        if seed:
            base = f"seed_{seed[0]}{'_armes' if seed[1] else ''}"
            # avec ou sans armes bonus : on prend le spoiler le plus récent de cette graine
            fichiers = [f for f in (self.dossier_seeds / f"{base}.json",
                                    self.dossier_seeds / f"{base}_bonus.json") if f.exists()]
            if fichiers:
                fichier = max(fichiers, key=lambda f: f.stat().st_mtime)
                try:
                    return self.t("spoiler_installe"), json.loads(fichier.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    pass
        return None, None

    # --- onglet « Info » : crédits et liens
    def lien(self, parent, texte, url):
        """Texte cliquable qui ouvre une page dans le navigateur."""
        l = ttk.Label(parent, text=texte, style="Lien.TLabel", cursor="hand2")
        l.bind("<Button-1>", lambda _: webbrowser.open(url))
        return l

    def construire_info(self, page):
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)
        defile = Defilable(page)
        defile.grid(row=0, column=0, sticky="nsew")
        cadre = defile.interieur
        cadre.columnconfigure(0, weight=1)

        projet, p = self.carte(cadre, self.t("carte_projet"))
        projet.grid(row=0, column=0, sticky="nsew")
        ttk.Label(p, text=f"{NOM_APPLI}  ·  v{VERSION}", style="Nom.TLabel"
                  ).pack(anchor="w")
        ttk.Label(p, text=self.t("info_description"), style="Carte.TLabel", wraplength=660,
                  justify="left").pack(anchor="w", pady=(4, 6))
        self.lien(p, "→  " + self.t("lien_projet"), URL_DEPOT).pack(anchor="w")
        ttk.Label(p, text=self.t("info_licence"), style="Note.TLabel").pack(anchor="w", pady=(8, 0))
        ttk.Label(p, text=self.t("info_fan"), style="Note.TLabel", wraplength=660, justify="left"
                  ).pack(anchor="w")

        auteur, a = self.carte(cadre, self.t("carte_auteur"))
        auteur.grid(row=1, column=0, sticky="nsew", pady=(16, 0))
        for nom, nom_complet, url in AUTEURS:
            ttk.Label(a, text=nom, style="Nom.TLabel").pack(anchor="w")
            ttk.Label(a, text=nom_complet, style="Carte.TLabel").pack(anchor="w")
            if url:
                self.lien(a, "→  " + self.t("lien_profil"), url).pack(anchor="w", pady=(2, 0))

        tests, te = self.carte(cadre, self.t("carte_tests"))
        tests.grid(row=2, column=0, sticky="nsew", pady=(16, 0))
        for nom, nom_complet, mot in TESTEURS:
            ligne = ttk.Frame(te, style="Carte.TFrame", borderwidth=0)
            ligne.pack(anchor="w")
            ttk.Label(ligne, text=nom, style="Nom.TLabel").pack(side="left")
            if mot:
                ttk.Label(ligne, text=f"« {mot} »", style="Mot.TLabel").pack(side="left", padx=(10, 0), pady=(1, 0))
                if SOUS_WINDOWS:                      # sous Linux, pas toujours de police d'emoji
                    ttk.Label(ligne, text="👊", style="Emoji.TLabel").pack(side="left", padx=(6, 0))
            ttk.Label(te, text=nom_complet, style="Carte.TLabel").pack(anchor="w", pady=(0, 6))

        merci, m = self.carte(cadre, self.t("carte_remerciements"))
        merci.grid(row=3, column=0, sticky="nsew", pady=(16, 0))
        ttk.Label(m, text=self.t("info_bhdtool"), style="Carte.TLabel", wraplength=660, justify="left"
                  ).pack(anchor="w")
        self.lien(m, "→  github.com/eleval/BhdTool", "https://github.com/eleval/BhdTool").pack(anchor="w", pady=(2, 8))
        ttk.Label(m, text=self.t("info_inspiration"), style="Carte.TLabel", wraplength=660, justify="left"
                  ).pack(anchor="w")

    # --- onglet « Archipelago » : préparé pour plus tard (champs grisés, liste de ce qu'il reste à faire)
    def construire_archipelago(self, page):
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)
        defile = Defilable(page)
        defile.grid(row=0, column=0, sticky="nsew")
        cadre = defile.interieur
        cadre.columnconfigure(0, weight=1)

        intro, i = self.carte(cadre, self.t("carte_archipelago"))
        intro.grid(row=0, column=0, sticky="nsew")
        ttk.Label(i, text=self.t("ap_intro"), style="Carte.TLabel", wraplength=640, justify="left"
                  ).pack(anchor="w", fill="x")
        self.lien(i, "→  archipelago.gg", "https://archipelago.gg").pack(anchor="w", pady=(8, 0))

        # connexion : tout est prêt mais grisé tant que le support n'existe pas
        connexion, c = self.carte(cadre, self.t("carte_ap_connexion"))
        connexion.grid(row=1, column=0, sticky="nsew", pady=(16, 0))
        c.columnconfigure(1, weight=1)
        self.ap_serveur = tk.StringVar(value="archipelago.gg:38281")
        self.ap_joueur = tk.StringVar()
        self.ap_mot_de_passe = tk.StringVar()
        self.ap_deathlink = tk.BooleanVar(value=False)
        for ligne, (cle, variable, cache) in enumerate((("ap_serveur", self.ap_serveur, False),
                                                        ("ap_joueur", self.ap_joueur, False),
                                                        ("ap_mot_de_passe", self.ap_mot_de_passe, True))):
            ttk.Label(c, text=self.t(cle), style="Carte.TLabel").grid(row=ligne, column=0, sticky="w",
                                                                    pady=4, padx=(0, 12))
            champ = ttk.Entry(c, textvariable=variable, width=36, font=(POLICE, 11), show="•" if cache else "")
            champ.grid(row=ligne, column=1, sticky="w", pady=4)
            champ.state(["disabled"])
        ttk.Checkbutton(c, text=self.t("ap_deathlink"), variable=self.ap_deathlink, state="disabled"
                        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))
        bas = ttk.Frame(c, style="Carte.TFrame", borderwidth=0)
        bas.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        bouton = ttk.Button(bas, text=self.t("ap_connecter"), style="Accent.TButton")
        bouton.pack(side="left")
        bouton.state(["disabled"])
        ttk.Label(bas, text=self.t("ap_etat"), style="Note.TLabel").pack(side="left", padx=(12, 0))

        # ce qu'il reste à faire pour qu'Archipelago fonctionne
        reste, r = self.carte(cadre, self.t("carte_ap_avancement"))
        reste.grid(row=2, column=0, sticky="nsew", pady=(16, 0))
        couleurs = {"ap_fait": "Ok.TLabel", "ap_en_cours": "Alerte.TLabel", "ap_a_faire": "Neutre.TLabel"}
        for etape, etat in (("ap_etape_releves", "ap_en_cours"), ("ap_etape_cles", "ap_a_faire"),
                            ("ap_etape_envoyer", "ap_a_faire"), ("ap_etape_recevoir", "ap_a_faire"),
                            ("ap_etape_monde", "ap_a_faire"), ("ap_etape_objectif", "ap_a_faire")):
            ligne = ttk.Frame(r, style="Carte.TFrame", borderwidth=0)
            ligne.pack(anchor="w", fill="x", pady=2)
            ttk.Label(ligne, text=f"●  {self.t(etat)}", style=couleurs[etat], width=16).pack(side="left")
            ttk.Label(ligne, text=self.t(etape), style="Carte.TLabel", wraplength=560, justify="left"
                      ).pack(side="left")

    # --- onglet « Aider le projet » : mode relevé et avancement des relevés
    def construire_aide(self, page):
        page.columnconfigure(0, weight=1)
        page.rowconfigure(0, weight=1)
        defile = Defilable(page)
        defile.grid(row=0, column=0, sticky="nsew")
        cadre = defile.interieur
        cadre.columnconfigure(0, weight=1)

        releve, r = self.carte(cadre, self.t("carte_releve"))
        releve.grid(row=0, column=0, sticky="nsew")
        ttk.Label(r, text=self.t("releve_intro"), style="Carte.TLabel", wraplength=640, justify="left"
                  ).pack(anchor="w", fill="x")
        self.case_releve = ttk.Checkbutton(r, text=self.t("releve_case"),
                                           variable=self.releve, command=self.basculer_releve)
        self.case_releve.pack(anchor="w", pady=(10, 2))
        ttk.Label(r, text=self.t("releve_prevention"), style="Alerte.TLabel", wraplength=610,
                  justify="left").pack(anchor="w", padx=(27, 0), pady=(0, 6))
        for etape in ("etape1", "etape2", "etape3", "etape4"):
            ttk.Label(r, text=self.t(etape), style="Note.TLabel", wraplength=610,
                      justify="left").pack(anchor="w", padx=(27, 0), pady=1)
        ttk.Label(r, text=self.t("releve_saccade"), style="Note.TLabel", wraplength=610,
                  justify="left").pack(anchor="w", padx=(27, 0), pady=(6, 0))
        liens = ttk.Frame(r, style="Carte.TFrame", borderwidth=0)
        liens.pack(anchor="w", pady=(12, 0))
        ttk.Button(liens, text=self.t("journal_du_jeu"), command=self.ouvrir_journal).pack(side="left")
        ttk.Button(liens, text=self.t("signaler_github"),
                   command=lambda: webbrowser.open(URL_DEPOT + "/issues")).pack(side="left", padx=(8, 0))

        avancement, a = self.carte(cadre, self.t("carte_avancement"))
        avancement.grid(row=1, column=0, sticky="nsew", pady=(16, 0))
        cadre.rowconfigure(1, weight=1)
        self.toile = tk.Canvas(a, bg=COULEURS["carte"], highlightthickness=0, height=330)
        self.toile.pack(fill="both", expand=True)
        self.note_avancement = ttk.Label(a, style="Note.TLabel", wraplength=660, justify="left")
        self.note_avancement.pack(anchor="w", pady=(6, 0))
        self.avancement = None
        if self.donnees:
            try:
                self.avancement = progression.calculer(self.donnees)
            except Exception as e:  # données illisibles : on l'affiche sans bloquer l'application
                self.note_avancement.configure(text=self.t("avancement_indispo", e=e))
        self.toile.bind("<Configure>", lambda _: self.dessiner_avancement())

    def dessiner_avancement(self):
        """Mêmes barres que sur la page GitHub (calculées par progression.py)."""
        c, t = COULEURS, self.toile
        t.delete("all")
        res = self.avancement
        if not res:
            return
        largeur = max(t.winfo_width(), 400)
        x_perso, x_diff, x_barre = 0, 56, 196
        x_pct = largeur - 210
        l_barre = max(x_pct - x_barre - 18, 60)
        total = res["total_pieces"] or 1
        y = 12

        def barre(y, plein, pale):
            t.create_rectangle(x_barre, y - 5, x_barre + l_barre, y + 5, fill=c["champ"], outline="")
            if pale > 0:
                t.create_rectangle(x_barre, y - 5, x_barre + max(round(l_barre * (plein + pale)), 4), y + 5,
                                   fill="#5a2a2e", outline="")
            if plein > 0:
                t.create_rectangle(x_barre, y - 5, x_barre + max(round(l_barre * plein), 4), y + 5,
                                   fill=c["accent"], outline="")

        precedent = None
        for (perso, diff), s in res["scenarios"].items():
            if precedent and perso != precedent:
                t.create_line(0, y - 13, largeur, y - 13, fill=c["bord"])
            if perso != precedent:
                t.create_text(x_perso, y, text=perso, anchor="w", fill=c["texte"], font=(POLICE, 10, "bold"))
            precedent = perso
            t.create_text(x_diff, y, text=self.t(f"diff_{diff}"), anchor="w", fill=c["texte"], font=(POLICE, 10))
            barre(y, s["completes"] / total, s["visitees"] / total)
            t.create_text(x_pct, y, text=f"{round(100 * s['completes'] / total)} %", anchor="w",
                          fill=c["texte"], font=(POLICE, 10, "bold"))
            detail = f"{s['completes']}/{res['total_pieces']}"
            if s["visitees"]:
                detail += self.t("visitees", n=s["visitees"])
            t.create_text(x_pct + 44, y, text=detail, anchor="w", fill=c["discret"], font=(POLICE, 9))
            y += 26
        t.create_line(0, y - 13, largeur, y - 13, fill=c["bord"])
        y += 6
        t.create_text(x_perso, y, text=self.t("armes_bonus"), anchor="w", fill=c["texte"],
                      font=(POLICE, 10, "bold"))
        if res["bonus_total"]:
            barre(y, res["bonus_connus"] / res["bonus_total"], 0)
            t.create_text(x_pct, y, text=self.t("bonus_identifiees", a=res["bonus_connus"], b=res["bonus_total"]),
                          anchor="w", fill=c["texte"], font=(POLICE, 10, "bold"))
        else:
            barre(y, 0, 0)
            t.create_text(x_pct, y, text=self.t("liste_a_completer"), anchor="w", fill=c["discret"],
                          font=(POLICE, 9))
        self.note_avancement.configure(text=self.t("note_avancement", total=res["total_pieces"], version=VERSION))

    # ------------------------------------------------------------------ actions
    def ecrire(self, texte, effacer=False):
        self.journal.configure(state="normal")
        if effacer:
            self.journal.delete("1.0", "end")
        self.journal.insert("end", texte + "\n")
        self.journal.see("end")
        self.journal.configure(state="disabled")

    def choisir_dossier(self):
        d = filedialog.askdirectory(title=self.t("choisir_dossier"), initialdir=self.dossier_jeu.get() or None)
        if d:
            self.dossier_jeu.set(str(Path(d)))

    # ------------------------------------------------------------------ mise à jour de l'application
    def verifier_mise_a_jour(self):
        """(fil secondaire) Demande à GitHub s'il existe une version plus récente."""
        mise_a_jour.nettoyer()                 # restes d'une mise à jour précédente
        info = mise_a_jour.chercher(VERSION)
        if info:
            try:
                self.after(0, lambda: self.signaler_mise_a_jour(info))
            except (RuntimeError, tk.TclError):    # fenêtre déjà fermée
                pass

    def signaler_mise_a_jour(self, info):
        self.maj = info
        self.afficher_bouton_maj()

    def afficher_bouton_maj(self):
        self.bouton_maj.configure(text=self.t("maj_disponible", version=self.maj["version"]))
        self.bouton_maj.state(["!disabled"])
        if not self.bouton_maj.winfo_ismapped():
            self.bouton_maj.pack(side="right", padx=(0, 12), pady=(8, 0), before=self.sous_titre)

    def mettre_a_jour(self):
        info, cible = self.maj, mise_a_jour.programme_actuel()
        if not cible:                          # script Python : pas de remplacement automatique
            if messagebox.askyesno(TITRE, self.t("maj_page", version=info["version"], actuelle=VERSION)):
                webbrowser.open(info["page"] or URL_DEPOT + "/releases/latest")
            return
        if not messagebox.askyesno(TITRE, self.t("maj_confirmer", version=info["version"], actuelle=VERSION)):
            return
        self.bouton_maj.state(["disabled"])
        self.bouton_maj.configure(text=self.t("maj_telechargement", pct=0))

        def progres(fraction):
            self.after(0, lambda: self.bouton_maj.configure(
                text=self.t("maj_telechargement", pct=int(fraction * 100))))

        def travail():
            try:
                nouveau = mise_a_jour.telecharger(info, cible, progres)
                self.after(0, lambda: self.installer_mise_a_jour(nouveau, cible))
            except Exception as e:
                self.after(0, lambda e=e: self.echec_mise_a_jour(e))
        threading.Thread(target=travail, daemon=True).start()

    def installer_mise_a_jour(self, nouveau, cible):
        try:
            mise_a_jour.remplacer_et_relancer(nouveau, cible)
        except Exception as e:
            self.echec_mise_a_jour(e)
            return
        self.destroy()

    def echec_mise_a_jour(self, erreur):
        self.afficher_bouton_maj()
        if messagebox.askyesno(TITRE, self.t("maj_erreur", e=erreur)):
            webbrowser.open(self.maj.get("page") or URL_DEPOT + "/releases/latest")

    def actualiser_etat(self):
        d = Path(self.dossier_jeu.get()) if self.dossier_jeu.get() else None
        if not d or not (d / "bhd.exe").exists():
            self.etat_jeu.set("Jeu introuvable : indique le dossier qui contient bhd.exe.")
            self.badge_dll.configure(text=self.t("badge_jeu_introuvable"), style="Alerte.TLabel")
            self.badge_seed.configure(text="")
            self.badge_version.configure(text="")
            for b in (self.bouton_dll, self.bouton_retirer_dll, self.bouton_retirer_seed, self.case_releve):
                b.state(["disabled"])
            self.verrouiller_onglets(False)
            return
        self.case_releve.state(["!disabled"])
        if self._dossier_dinput8 != str(d):
            self._dossier_dinput8 = str(d)
            self.proton_dinput8.set((d / "dinput8.dll").exists())
        self.regler_option_proton()
        self.releve.set(lire_option_ini(d, "Releve") == "1")
        dll = d / "xinput1_4.dll"
        dll_ok = dll.exists()
        etranger = dll_ok and not est_notre_dll(dll)
        seed = gen.seed_installee(d)
        if etranger:
            self.badge_dll.configure(text=self.t("badge_autre_dll"), style="Alerte.TLabel")
        elif dll_ok and not dll_a_jour(dll, self.dll):
            self.badge_dll.configure(text=self.t("badge_dll_ancienne"), style="Alerte.TLabel")
        elif dll_ok:
            self.badge_dll.configure(text=self.t("badge_installe"), style="Ok.TLabel")
        else:
            self.badge_dll.configure(text=self.t("badge_origine"), style="Neutre.TLabel")
        self.badge_version.configure(text="" if version_jeu_ok(d) else self.t("badge_version"))
        if seed:
            self.badge_seed.configure(text=self.t("badge_seed", graine=seed[0],
                                                  armes=self.t("badge_armes") if seed[1] else ""),
                                      style="Ok.TLabel")
        else:
            self.badge_seed.configure(text=self.t("badge_aucune_seed"), style="Neutre.TLabel")
        # résumé texte (non affiché, gardé en français pour les tests)
        self.etat_jeu.set(
            "DLL du randomizer : " + ("installée" if dll_ok and not etranger else
                                      "un AUTRE xinput1_4.dll est présent (pas celui du randomizer)"
                                      if etranger else "NON installée (jeu d'origine)") + "\n"
            f"Seed installée : {f'{seed[0]}' + (' (armes)' if seed[1] else '') if seed else 'aucune'}")
        self.bouton_dll.configure(text=self.t("maj_dll") if dll_ok and not etranger else self.t("installer_dll"))
        self.bouton_dll.state(["!disabled"] if self.dll and not etranger else ["disabled"])
        self.bouton_retirer_dll.state(["!disabled"] if dll_ok and not etranger else ["disabled"])
        self.bouton_retirer_seed.state(["!disabled"] if seed else ["disabled"])
        self.verrouiller_onglets(dll_ok and not etranger and dll_a_jour(dll, self.dll))

    def verrouiller_onglets(self, dll_prete):
        """« Générer une seed » : seulement avec notre DLL installée et à jour.
        « Spoiler » : en plus, seulement s'il y a une seed (générée ou installée) dont on a la liste."""
        self.dll_prete = dll_prete
        spoiler = dll_prete and self.spoiler_actuel()[1] is not None
        courant = self.onglets.select()            # avant de griser : Tk changerait d'onglet tout seul
        if not dll_prete and courant in (str(self.page_generer), str(self.page_spoiler)):
            self.onglets.select(self.page_install)
        elif not spoiler and courant == str(self.page_spoiler):
            self.onglets.select(self.page_generer)
        self.onglets.tab(self.page_generer, state="normal" if dll_prete else "disabled")
        self.onglets.tab(self.page_spoiler, state="normal" if spoiler else "disabled")
        self.bouton_suivant.state(["!disabled"] if dll_prete else ["disabled"])

    def alerte_releve(self):
        """Fenêtre d'alerte : objets visibles désactivés par le mode relevé. Renvoie « desactiver » ou « garder »."""
        c = COULEURS
        choix = {"valeur": "garder"}
        f = tk.Toplevel(self)
        f.title(self.t("alerte_releve_titre"))
        f.configure(bg=c["carte"])
        f.resizable(False, False)
        f.transient(self)
        if getattr(self, "_logo_entete", None):
            try:
                f.iconphoto(False, self._logo_entete)
            except tk.TclError:
                pass
        cadre = tk.Frame(f, bg=c["carte"], padx=24, pady=20)
        cadre.pack(fill="both", expand=True)
        tk.Label(cadre, text="⚠", bg=c["carte"], fg="#e8a33a", font=(POLICE, 26)).grid(row=0, column=0, rowspan=2,
                                                                                    sticky="n", padx=(0, 16))
        tk.Label(cadre, text=self.t("alerte_releve_titre"), bg=c["carte"], fg=c["texte"],
                 font=(POLICE, 12, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(cadre, text=self.t("alerte_releve"), bg=c["carte"], fg=c["texte"], font=(POLICE, 10),
                 wraplength=420, justify="left").grid(row=1, column=1, sticky="w", pady=(6, 16))
        boutons = tk.Frame(cadre, bg=c["carte"])
        boutons.grid(row=2, column=0, columnspan=2, sticky="e")

        def fermer(valeur):
            choix["valeur"] = valeur
            f.destroy()
        # deux boutons de même taille (colonnes « uniform »)
        boutons.columnconfigure((0, 1), uniform="bouton")
        ttk.Button(boutons, text=self.t("alerte_releve_desactiver"), style="Dialogue.Accent.TButton",
                   command=lambda: fermer("desactiver")).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(boutons, text=self.t("alerte_releve_garder"), style="Dialogue.TButton",
                   command=lambda: fermer("garder")).grid(row=0, column=1, sticky="ew")
        f.protocol("WM_DELETE_WINDOW", lambda: fermer("garder"))
        f.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - f.winfo_reqwidth()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - f.winfo_reqheight()) // 3
        f.geometry(f"+{max(0, x)}+{max(0, y)}")
        if SOUS_WINDOWS:
            barre_titre_sombre(f)
        f.grab_set()
        f.focus_set()
        self.wait_window(f)
        return choix["valeur"]

    def basculer_releve(self):
        d = Path(self.dossier_jeu.get())
        actif = self.releve.get()
        try:
            ecrire_option_ini(d, "Releve", "1" if actif else None)
        except OSError as e:
            messagebox.showerror(TITRE, self.t("err_ini", e=e))
            self.releve.set(not actif)
            return
        if actif:
            self.ecrire(self.t("releve_active")
                        + ("" if (d / "xinput1_4.dll").exists() else self.t("releve_dll_absente")), effacer=True)
        else:
            self.ecrire(self.t("releve_desactive"), effacer=True)

    def supprimer(self, fichier, cle_message):
        try:
            fichier.unlink()
            self.ecrire(self.t(cle_message, chemin=fichier), effacer=True)
        except FileNotFoundError:
            pass
        except OSError as e:
            messagebox.showerror(TITRE, self.t("err_supprimer", nom=fichier.name, e=e))
        self.actualiser_etat()

    def retirer_dll(self):
        dll = Path(self.dossier_jeu.get()) / "xinput1_4.dll"
        if not est_notre_dll(dll):        # sécurité : ne jamais supprimer la DLL d'un autre mod
            messagebox.showwarning(TITRE, self.t("pas_notre_dll"))
            self.actualiser_etat()
            return
        if messagebox.askyesno(TITRE, self.t("confirmer_desinstaller")):
            self.supprimer(dll, "dll_supprimee")
            if not dll.exists():
                self.ecrire(self.t("sans_randomizer"))

    def retirer_seed(self):
        cible = Path(self.dossier_jeu.get()) / gen.NOM_SEED_JEU
        seed = gen.seed_installee(cible.parent)
        if seed and messagebox.askyesno(TITRE, self.t("confirmer_supprimer_seed", graine=seed[0],
                                                      armes=self.t("avec_armes") if seed[1] else "")):
            self.supprimer(cible, "seed_supprimee")

    def installer_dll(self):
        cible = Path(self.dossier_jeu.get()) / "xinput1_4.dll"
        if not version_jeu_ok(cible.parent) and not messagebox.askyesno(TITRE, self.t("version_confirmer")):
            return
        try:
            shutil.copyfile(self.dll, cible)
            self.ecrire(self.t("dll_installee", chemin=cible))
        except OSError as e:
            messagebox.showerror(TITRE, self.t("err_copier_dll", e=e))
        self.actualiser_etat()

    def regler_option_proton(self):
        """Ligne à copier selon la case dinput8, et mention « détecté » si le fichier est là."""
        self.option_proton.set(OPTION_PROTON_DINPUT8 if self.proton_dinput8.get() else OPTION_PROTON)
        if hasattr(self, "case_dinput8"):
            d = Path(self.dossier_jeu.get()) if self.dossier_jeu.get() else None
            detecte = d is not None and (d / "dinput8.dll").exists()
            self.case_dinput8.configure(text=self.t("proton_dinput8")
                                        + (self.t("proton_detecte") if detecte else ""))

    def copier_option_proton(self):
        self.clipboard_clear()
        self.clipboard_append(self.option_proton.get())
        self.ecrire(self.t("copie_ok"), effacer=True)

    def ouvrir_journal(self):
        journal = Path(self.dossier_jeu.get()) / "randomizer_journal.txt"
        if journal.exists():
            ouvrir(journal)
        else:
            messagebox.showinfo(TITRE, self.t("pas_de_journal"))

    def ouvrir_seeds(self):
        self.dossier_seeds.mkdir(parents=True, exist_ok=True)
        ouvrir(self.dossier_seeds)

    def generer(self):
        try:
            graine = int(self.graine.get().strip())
            if graine < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(TITRE, self.t("graine_invalide"))
            return
        installer = self.installer.get()
        if installer and not (Path(self.dossier_jeu.get()) / "bhd.exe").exists():
            messagebox.showwarning(TITRE, self.t("dossier_introuvable"))
            return

        if installer and self.visibles.get() and self.releve.get():
            if self.alerte_releve() == "desactiver":
                self.releve.set(False)
                self.basculer_releve()
                self.after(50, lambda: self.ecrire(self.t("alerte_releve_fait")))

        self.bouton_generer.state(["disabled"])
        self.ecrire(self.t("generation"), effacer=True)
        # messages : textes.Msg traduits à l'affichage (changer de langue réaffiche le journal dans la nouvelle)
        messages, spoiler = [], []
        langue = self.langue.get()
        armes = self.armes_choisies()
        if self.armes.get() and not armes:         # « Armes aléatoires » sans aucune arme cochée
            messages.append(textes.Msg("aucune_arme"))

        def travail():
            try:
                ok = gen.produire(graine, self.armes.get(), self.donnees, self.dossier_seeds,
                                  installer, self.dossier_jeu.get() or None, messages.append,
                                  personnage=self.personnage.get(), difficulte=self.difficulte.get(),
                                  langue=langue, dire_spoiler=spoiler.append, armes_choisies=armes,
                                  objets_visibles=self.visibles.get(), arme_depart=self.arme_depart.get(),
                                  malle_aleatoire=self.malle.get(), couteau_aleatoire=self.couteau.get(),
                                  armes_bonus=self.armes_bonus_choisies(), messages_differes=True)
            except Exception as e:  # on affiche l'erreur plutôt que de fermer l'application
                messages.append(textes.Msg("erreur", e=e))
                ok = False
            self.after(0, lambda: self.fin_generation(messages, spoiler[0] if spoiler else None, ok))

        threading.Thread(target=travail, daemon=True).start()

    def fin_generation(self, messages, spoiler, ok):
        self.dernier_resultat = (messages, spoiler, ok)
        self.afficher_resultat()
        self.bouton_generer.state(["!disabled"])
        self.actualiser_etat()

    def afficher_resultat(self):
        """Journal de l'onglet Générer : résumé seulement. Onglet Spoiler : liste complète, si la case est cochée.
        Tout est rendu dans la langue actuelle (la seed est gardée sous forme de données, pas de texte)."""
        langue = self.langue.get()
        if self.dernier_resultat:
            messages, spoiler, ok = self.dernier_resultat
            lignes = []
            if spoiler:
                lignes.append("\n".join(gen.resume_spoiler(spoiler, langue)) + "\n" + self.t("renvoi_spoiler"))
            lignes += [textes.rendre(m, langue) for m in messages]
            self.ecrire("\n".join(lignes), effacer=True)
            if not ok:
                self.ecrire("\n" + self.t("echec_generation"))
        titre, seed = self.spoiler_actuel()
        if seed is None:
            note, contenu = self.t("spoiler_aucun"), None
        elif self.afficher_spoiler.get():
            note, contenu = titre, seed
        else:
            note, contenu = self.t("spoiler_masque", titre=titre), None
        if not hasattr(self, "zone_spoiler"):
            return                                  # appelé pendant la construction de la fenêtre
        lignes = []
        if contenu:
            note += "\n" + "  ·  ".join(gen.resume_spoiler(contenu, langue))
            lignes = [(f"{piece} · {nom}" if nom else piece, avant, apres, bonus)
                      for piece, nom, avant, apres, bonus in gen.lignes_spoiler(contenu, langue)]
        self.note_spoiler.configure(text=note)
        cherche = sans_accents(self.recherche_spoiler.get().strip())
        if cherche:
            lignes = [l for l in lignes if cherche in sans_accents(" ".join(l[:3]))]
        self.compte_recherche.configure(text=self.t("resultats_recherche", n=len(lignes)) if cherche and contenu else "")
        colonne, inverse = self.tri_spoiler
        i_col = ("lieu", "origine", "nouveau").index(colonne)
        lignes.sort(key=lambda l: sans_accents(l[i_col]), reverse=inverse)
        self.zone_spoiler.delete(*self.zone_spoiler.get_children())
        for n, (lieu, origine, nouveau, bonus) in enumerate(lignes):
            tags = ["impair"] if n % 2 else []
            if bonus:
                tags.append("bonus")
            elif origine == nouveau:
                tags.append("meme")
            self.zone_spoiler.insert("", "end", values=(lieu, origine, nouveau), tags=tags)


def sans_accents(texte):
    """Minuscules sans accents, même longueur que le texte (pour la recherche dans le spoiler)."""
    return "".join(unicodedata.normalize("NFD", c)[0] for c in texte).lower()


if __name__ == "__main__":
    Application().mainloop()
