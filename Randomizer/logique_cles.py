"""
Logique des clés (Chris, nouvelle partie) : carte des portes du jeu et placement des clés mélangées pour que la partie
reste toujours finissable.

Carte des portes : pages des pièces d'evilresource.com (« This place is linked to the following locations », avec la
condition de chaque porte), relevées le 25/11/2026, reportées sur nos numéros de pièce (onglet « Pièces »), complétées
par l'onglet « Verrous » (conditions confirmées en jeu par le joueur) et par les énigmes connues. Règle de prudence :
dans le doute, la condition la plus stricte (une seed un peu moins variée, mais jamais impossible).

Une pièce = un numéro (les étages d'une même pièce, ex. le hall 106, partagent le numéro). « crypte » et
« chirurgien » : pièces sans numéro chez nous (aucun objet relevé).
"""
from collections import Counter
import random

DEPART = "106"                     # Chris commence dans le hall

# (pièce de départ, pièce d'arrivée, condition) : None = libre ; voir CONDITIONS
ARETES_SITE = [
    ("100", "101", None), ("101", "100", None), ("101", "102", "vieille"), ("101", "103", "armure"),
    ("101", "202", None), ("101", "203", "vieille"), ("101", "214", None), ("101", "215", "casque"),
    ("102", "101", None), ("103", "101", None), ("103", "105", None), ("103", "10c", None),
    ("103", "10d", None), ("103", "10e", None), ("103", "10f", "armure"), ("103", "112", None),
    ("103", "21c", "epee"), ("105", "103", None), ("105", "106", None), ("106", "105", None),
    ("106", "107", None), ("106", "10b", None), ("106", "111", "casque"), ("106", "202", None),
    ("106", "203", "autre_cote"), ("106", "204", "epee"), ("106", "212", None), ("106", "31a", "deux_objets_mp"),
    ("107", "106", None), ("107", "108", "epee"), ("107", "11c", "placard"), ("108", "107", "epee"),
    ("108", "109", None), ("109", "108", None), ("109", "10a", None), ("109", "114", "vieille"),
    ("109", "115", None), ("10a", "109", None), ("10a", "117", "armure"), ("10a", "119", "embleme"),
    ("10a", "11a", None), ("10a", "207", None), ("10b", "106", None), ("10b", "117", None),
    ("10b", "crypte", None), ("10c", "103", None), ("10d", "103", None), ("10e", "103", None),
    ("10f", "103", None), ("111", "106", None), ("112", "103", None), ("112", "214", None),
    ("114", "109", None), ("115", "109", None), ("115", "116", None), ("116", "115", None),
    ("117", "10a", None), ("117", "10b", "vieille"), ("118", "207", None), ("119", "10a", None),
    ("11a", "10a", None), ("11a", "11b", "objet_mp"), ("11b", "11a", None), ("11b", "300", None),
    ("11b", "311", None), ("11c", "107", None), ("202", "101", "epee"), ("202", "106", None),
    ("202", "214", "autre_cote"), ("203", "101", None), ("203", "106", None), ("204", "106", "epee"),
    ("204", "205", "armure"), ("204", "206", None), ("204", "207", "autre_cote"), ("204", "20d", "armure"),
    ("205", "204", None), ("206", "204", None), ("206", "207", None), ("207", "10a", None),
    ("207", "118", None), ("207", "204", None), ("207", "206", "impossible"), ("207", "208", "armure"),
    ("207", "20b", None), ("208", "207", None), ("208", "209", None), ("208", "20a", "vieille"),
    ("209", "208", None), ("20a", "208", None), ("20b", "207", None), ("20b", "20c", "casque"),
    ("20c", "20b", None), ("20c", "21a", None), ("20d", "204", None), ("20d", "20e", None),
    ("20e", "20d", None), ("20e", "20f", None), ("20e", "210", "bouclier"), ("20f", "20e", None),
    ("210", "20e", None), ("212", "106", None), ("213", "214", None), ("213", "219", None),
    ("214", "101", "autre_cote"), ("214", "112", None), ("214", "202", None), ("214", "213", "autre_cote"),
    ("214", "217", None), ("215", "101", None), ("216", "217", None), ("217", "214", None),
    ("217", "216", "casque"), ("219", "213", None), ("21a", "20c", None), ("21a", "21b", None),
    ("21b", "21a", None), ("21b", "21c", None), ("21c", "103", None), ("21c", "21b", None),
    ("300", "11b", None), ("300", "301", None), ("300", "302", None), ("301", "300", None),
    ("301", "302", None), ("302", "300", "batterie"), ("302", "301", None), ("302", "304", None),
    ("302", "307", None), ("303", "501", None), ("304", "302", None), ("304", "400", None),
    ("305", "315", None), ("305", "500", "medailles"), ("306", "30f", None), ("307", "302", None),
    ("307", "308", None), ("307", "30b", None), ("308", "307", None), ("308", "309", None),
    ("309", "308", None), ("309", "30a", None), ("309", "316", None), ("30a", "309", None),
    ("30b", "307", None), ("30b", "30c", None), ("30c", "30b", None), ("30c", "30d", None),
    ("30d", "30c", None), ("30d", "30f", None), ("30f", "306", None), ("30f", "30d", None),
    ("311", "11b", None), ("311", "312", None), ("312", "311", None), ("312", "313", None),
    ("313", "312", None), ("313", "314", None), ("314", "313", None), ("314", "319", None),
    ("315", "305", None), ("316", "309", None), ("316", "317", None), ("317", "316", None),
    ("317", "318", None), ("317", "319", None), ("318", "317", None), ("319", "314", None),
    ("319", "317", None), ("31a", "106", None), ("400", "304", None), ("400", "401", "cle_001"),
    ("400", "403", None), ("400", "404", None), ("400", "405", None), ("401", "400", None),
    ("401", "402", None), ("402", "401", None), ("403", "400", None), ("404", "400", None),
    ("405", "400", None), ("405", "408", "cle_galerie"), ("406", "407", None), ("406", "40d", None),
    ("407", "406", None), ("408", "405", None), ("408", "409", None), ("408", "40a", "cle_003"),
    ("408", "40c", None), ("409", "408", None), ("40a", "408", None), ("40a", "40b", None),
    ("40a", "40c", None), ("40b", "40a", None), ("40c", "408", None), ("40c", "40a", None),
    ("40d", "406", None), ("40d", "40e", None), ("40d", "410", None), ("40e", "40d", None),
    ("40e", "40f", None), ("40e", "411", "cle_controle"), ("40f", "40e", None), ("410", "40d", None),
    ("410", "411", None), ("410", "412", None), ("411", "40e", None), ("411", "410", None),
    ("412", "410", None), ("500", "305", None), ("500", "501", None), ("500", "502", None),
    ("501", "303", None), ("501", "500", None), ("502", "500", None), ("502", "503", None),
    ("503", "502", None), ("503", "504", None), ("503", "505", None), ("504", "503", None),
    ("505", "503", None), ("505", "506", None), ("505", "507", "cle_puissance"), ("505", "508", None),
    ("505", "50c", "cle_puissance"), ("506", "505", None), ("507", "505", None), ("507", "chirurgien", None),
    ("508", "505", None), ("508", "509", None), ("508", "50a", None), ("508", "50b", None),
    ("509", "508", None), ("50a", "508", None), ("50b", "508", None), ("50b", "512", None),
    ("50c", "505", None), ("50c", "50e", None), ("50c", "50f", None), ("50c", "514", None),
    ("50e", "50c", None), ("50f", "50c", None), ("50f", "510", None), ("510", "50f", None),
    ("510", "511", None), ("511", "510", None), ("512", "50b", None), ("513", "514", None),
    ("514", "50c", None), ("514", "513", None), ("chirurgien", "507", None), ("crypte", "10b", None),
]

# Conditions de l'onglet « Verrous » et des énigmes (prudence : on ajoute, on n'enlève jamais une condition du site)
ARETES_EN_PLUS = [
    ("307", "30b", "manivelle_hex"), ("30b", "307", "manivelle_hex"),       # mur hexagonal (Verrous n°40)
    ("30d", "30f", "lance_flammes"),                                         # panneau à crochets (Verrous n°41)
    ("309", "316", "arbre_cylindre"), ("316", "309", "arbre_cylindre"),     # ascenseur du générateur (Verrous n°42)
    ("317", "319", "lance_flammes_casse"),                                   # panneau du souterrain (Verrous n°43)
    # portes absentes des pages du site (onglet « Pièces ») : chambre 002 sur le couloir central ; monte-plats de la
    # cuisine (200) vers le couloir de l'ascenseur au 1er étage
    ("405", "406", None), ("406", "405", None),
    ("21c", "213", None), ("213", "21c", None),
    ("31a", "315", None), ("315", "31a", None),                             # passage de l'autel -> tombe de Jessica
    # livre rouge (joueur, 26/11/2026) : posé dans la bibliothèque de la chambre 003, il ouvre une porte vers la salle
    # de la Plante 42 ; on en ressort par une autre double porte (vers la galerie)
    ("40a", "40c", "livre_rouge"),
]
# Prudence (à confirmer en jeu) : ascenseur jardin <-> chutes = batterie dans les deux sens ; passage des chutes vers la
# grotte (307) = bassin vidé avec la manivelle carrée ; trappe de la cabane vers la chambre de Lisa : seulement depuis
# la chambre de Lisa.
REMPLACEMENTS = {
    ("300", "302"): "batterie",
    # Cour (joueur, 26/11/2026) : la première fois, on passe du jardin aux chutes par le bassin, vidé avec la manivelle
    # carrée (ascenseur jardin <-> chutes : seulement avec la batterie, dans les deux sens). Pour entrer dans la grotte,
    # il faut arrêter la cascade : remonter par l'ascenseur (batterie), remettre l'eau du bassin (manivelle carrée) ;
    # le chemin du bassin est alors fermé pour de bon, mais on a l'ascenseur.
    ("301", "302"): "manivelle_carree", ("302", "301"): "manivelle_carree",
    ("302", "307"): "grotte", ("307", "302"): "grotte",
    ("314", "319"): "autre_cote",
    ("408", "40c"): "autre_cote",
    # Aqua Ring (joueur, 26/11/2026) : la réserve (410) n'est accessible, dans les deux sens, qu'une fois l'eau vidée
    # depuis la salle de contrôle (411), où l'on entre avec la clé de la salle de contrôle
    ("40d", "410"): "cle_controle", ("410", "40d"): "cle_controle",
    ("411", "410"): "cle_controle", ("410", "411"): "cle_controle",       # double porte galerie -> Plante 42 : on n'y entre pas par là (prudence)
    # Poignée cassable (joueur, 25/11/2026) : porte escalier de l'aile est (207) <-> couloir sombre (10A). Elle casse
    # après deux passages ; ensuite on ne passe plus que du couloir sombre vers l'escalier. On la considère cassée
    # dès le départ (jamais 207 -> 10A) ; et on n'entre par là dans l'aile est qu'avec de quoi en ressortir :
    # clé de l'épée (couloir en C -> hall) ou clé du casque (salle de repos -> passage secret -> sous-sol -> monte-plats).
    ("207", "10a"): "impossible",
    ("10a", "207"): "poignee",
    # Cellule (joueur, 26/11/2026) : les 3 disques MO passés dans les 3 terminaux (morgue 507, radiographie A 50a,
    # labyrinthe électrique B 510) donnent les codes qui ouvrent l'entrée de la cellule (50b)
    ("508", "50b"): "codes_mo",
    # passage vers l'héliport (joueur, 26/11/2026) : l'unité de fusibles (97), utilisée dans la pièce où on la trouve
    # (501), rallume l'ascenseur de l'héliport (50d ; la carte du site relie directement 501 et l'héliport 303)
    ("501", "303"): "fusibles",
    # capsule de carburant (joueur, 26/11/2026) : vide (111), remplie en radiographie A (50a), rapportée au
    # labyrinthe électrique A (50f) -> générateur -> ascenseur vers l'entrée du labo principal (514). Pleine : id 31.
    ("50c", "514"): "carburant",
}

# Clés de porte (id -> condition) et conditions spéciales
CLE = {"casque": 48, "armure": 46, "bouclier": 47, "epee": 45, "embleme": 63, "placard": 62, "batterie": 67,
       "cle_001": 49, "cle_003": 50, "cle_galerie": 30, "cle_controle": 110, "cle_puissance": 54, "fusibles": 97,
       "manivelle_hex": 61, "livre_rouge": 90, "manivelle_carree": 60, "lance_flammes": 12, "lance_flammes_casse": 107}
VIEILLE_CLE = 44

# Objets obtenus en atteignant une pièce, hors emplacements relevés (récompenses d'énigmes, combinaisons…) :
# (pièce, objet donné, objets nécessaires) ; pièce None : n'importe où (objet qu'on examine ou qu'on combine)
DONS = [
    # (l'emblème de la cheminée de 105 est un emplacement « examiné » : voir generateur_seed.EXAMENS_SPECIAUX)
    # emblème doré (joueur, 26/11/2026) : notes manquantes (32) + pages du milieu (129) -> partition jouée au piano du
    # bar -> la cachette s'ouvre ; on y échange l'emblème (69) contre l'emblème doré (sinon on reste enfermé)
    ("10f", 70, (69, 32, 129)),
    # collier (24) examiné -> bijou -> fausse clé (pour la dalle du passage de la Mort)
    (None, "fausse_cle", (24,)),
    ("215", 72, ()),                    # joyau rouge (tête de trophée)
    (None, 63, (102, 72)),              # boîte à bijoux 2 ouverte avec le joyau rouge -> broche -> clé emblème
    (None, 125, (103,)),                # boîte à bijoux 1 (salle des armures) -> masque sans visage
    (None, 45, (22,)),                  # Grimoire (Livre maudit) examiné -> clé de l'épée (joueur, 25/11/2026)
    (None, 51, (91,)),                  # dernier livre vol. 1 -> médaillon de l'aigle
    ("216", 52, ()),                    # serpent vaincu -> dernier livre vol. 2 -> médaillon du loup
    (None, "anneau", (99,)),            # boîte à bijoux 3 (chambre de Lisa) -> anneau de pierre
    (None, "objet_mp_2", (65, "anneau")),  # objet métallique + anneau de pierre -> 2e objet en métal et pierre
    # caisse de la réserve souterraine (318) mise sur la plateforme, amenée au compacteur (316) et écrasée : lance-
    # flammes cassé (joueur, 26/11/2026). 318 n'est atteignable que par 316 et 317 (libres) : atteindre 318 suffit.
    ("318", "caisse", ()),
    # terminaux MO (un disque chacun, n'importe lequel) : voir REMPLACEMENTS, condition « codes_mo »
    ("50a", "capsule_pleine", (111,)),
    ("20a", 115, ()), ("20a", 116, ()),  # spécimen d'abeille et leurre sans hameçon : sur les tableaux (non mélangés)
    (None, 118, (116, 117)),            # leurre d'abeille : leurre sans hameçon + hameçon (combinés n'importe où)
    ("507", "terminal_mo", ()), ("50a", "terminal_mo", ()), ("510", "terminal_mo", ()),
    ("215", 74, ()),                    # joyau jaune (tête de taureau des trophées)
    # (disque MO de la statue du tigre : emplacement relevé, voir CONDITIONS_EMPLACEMENT)
]
# Conditions propres à un emplacement relevé : (pièce, objet d'origine) -> objets nécessaires
CONDITIONS_EMPLACEMENT = {
    ("105", 47): (70,),                 # clé du bouclier : derrière l'horloge (emblème doré dans la cheminée)
    ("217", 46): ("fausse_cle",),       # clé de l'armure : sur la dalle (échange avec la fausse clé)
    ("412", 30): (110,),                # clé de la galerie : bassin du requin (prudence : salle de contrôle)
    # Crypte (enregistrée comme le cimetière, 10B ; joueur, 18 et 25/11/2026) : ouverte avec la pointe de la flèche
    # dorée (flèche 21 examinée) ; le Grimoire y est posé dès la première visite ; les 4 masques libèrent un boss qui
    # donne l'objet en métal et pierre (53). (Le masque sans bouche relevé en 10B était un fantôme : il n'est que dans
    # la grande galerie, 117.)
    ("10b", 22): (21,),
    # joueur, 19/11/2026 : joyau bleu (73) dans un oeil de la statue du tigre -> munitions de fusil ; double plaque en
    # bois (108) sur la cheminée de la salle de repos -> carte du manoir 2F
    ("10d", 18): (73,),
    ("203", 24): (96,),                 # collier du balcon : il faut le sifflet (le chien)
    ("316", 107): ("caisse",),          # lance-flammes cassé : caisse de la réserve écrasée dans le compacteur
    ("10d", 93): (74,),                 # disque MO : joyau jaune dans l'oeil de la statue du tigre
    ("116", 6): (75,),
    # serre (joueur, 26/11/2026) : le désherbant (76, extérieur de la chaufferie 114) tue la plante qui cache le
    # masque sans yeux ; le mauvais tuyau tue les herbes (emplacements protégés, generateur_seed.EMPLACEMENTS_RISQUES)
    ("10c", 126): (76,),
    # résidence (joueur, 26/11/2026) : l'insecticide (100) versé dans le trou derrière la carte de la résidence (couloir
    # central 405) tue les abeilles de la galerie : la clé de la salle 003, sous la ruche, devient accessible
    ("408", 50): (100,),
    # salle des données visuelles (joueur, 26/11/2026) : le filtre à diapos (109) dans le projecteur montre le code
    # (8462) du passage secret de la même pièce (équipement de montage, clé zone haute tension). Un joueur qui connaît
    # le code s'en passe, mais on garde le filtre accessible avant.
    ("504", 54): (109,),
    # aquarium (joueur, 27/11/2026) : le leurre d'abeille (118 = 116 + 117) et le spécimen d'abeille (115) sur les bons
    # tableaux de la même pièce : un tableau bouge et donne le symbole du vent. Rater ne coûte rien ; réussir fait
    # apparaître une abeille.
    ("20a", 57): (115, 118),
    # symboles (joueur, 26/11/2026) : le symbole du vent (57, bureau 20A) posé sur la tombe de droite (312) donne la
    # lune, le soleil et l'étoile (même position, repérés par leur identifiant d'objet) ; examinés puis mis dans la
    # tombe de gauche : Magnum
    ("312", 59): (57,), ("312", 56): (57,), ("312", 58): (57,),
    ("312", 11): (56, 58, 59),                  # fusil du salon : l'échanger contre le fusil cassé (sinon le plafond tombe)
    ("20b", 302): (108,),
    ("10b", 53): (21, 125, 126, 127, 128),
}
# But : sortir par l'héliport avec le partenaire (cellule, 3 disques MO ; fusibles)
BUT = (("512", (93, 94, 95)), ("514", ()), ("303", (97, 106)))   # 106 : fusées de signalisation (appel de l'hélicoptère)

# Clés et objets d'énigme qu'on peut mélanger (25/11/2026) : seulement ceux dont la logique connaît l'usage. Chaque
# entrée : (id, libellé si le nom du jeu ne suffit pas). Les vieilles clés (5) se cochent ensemble.
CLES_CHOIX = [(22, "epee"), (46, None), (47, None), (48, None), (44, None), (49, None), (50, None), (30, None),
              (110, None), (54, None)]                     # 22 : le Grimoire, qui donne la clé de l'épée
ENIGMES_CHOIX = [(93, "mo"), (94, "mo"), (95, "mo"), (109, None), (97, None), (111, None), (117, None), (100, None), (76, None), (57, None), (59, None), (58, None), (56, None), (32, None), (129, None), (75, None), (96, None), (24, None), (90, None), (107, None), (69, None), (73, None), (108, None), (21, None), (53, None), (67, None), (60, None), (61, None), (65, None), (122, None), (123, None),
                 (126, None), (127, None), (128, None), (91, None), (103, "1"), (102, "2"), (99, "3")]
IDS_CLES = {i for i, _ in CLES_CHOIX}
IDS_ENIGMES = {i for i, _ in ENIGMES_CHOIX}
# Jamais de clé ni d'objet d'énigme ici : pièces de la fin (joueur, 26/11/2026). On peut remonter du labo au manoir
# autant qu'on veut, sauf une fois le Tyran tué dans le labo principal : la porte de l'ascenseur vers la fontaine est
# bloquée, l'autodestruction démarre et on file à l'héliport. Exclues : entrée du labo principal (514), labo principal
# (513), entrée de la cellule (50b), cellule (512), passage vers l'héliport (501), ascenseur de l'héliport (50d),
# héliport (303). Le reste du labo est permis.
PIECES_FIN = {"514", "513", "50b", "512", "501", "50d", "303"}
PIECES_SANS_CLE_PREFIXES = ()
PIECES_SANS_CLE = PIECES_FIN
# Objets qui peuvent aller au labo, sauf dans certaines pièces (joueur, 26/11/2026). Disques MO : ils ne servent qu'à
# la bonne fin (libérer le partenaire de la cellule), mais la logique les garde accessibles avant les terminaux. Pièces
# exclues : entrée du labo principal (514), labo principal (513), entrée de la cellule (50b), cellule (512), passage
# vers l'héliport (501), ascenseur de l'héliport (50d), héliport (303).
# Clé zone haute tension (54, validée par le joueur le 26/11/2026) : mêmes pièces exclues ; la logique l'empêche déjà
# d'aller derrière ses propres portes (morgue 507, couloir de l'ascenseur 50c).
PIECES_INTERDITES_OBJET = {i: set(PIECES_FIN) for i in (93, 94, 95, 54, 109, 111)}
# fusées de signalisation (option « Pour les fous », 26/11/2026, à tester en jeu) : n'importe où avant l'héliport, ou
# sur l'héliport même (leur place d'origine)
ID_FUSEES = 106
PIECES_INTERDITES_OBJET[ID_FUSEES] = PIECES_INTERDITES_OBJET[93] - {"501", "303"}
# unité de fusibles : peut rester dans le passage vers l'héliport (501), où elle sert
PIECES_INTERDITES_OBJET[97] = PIECES_INTERDITES_OBJET[93] - {"501"}
# Malle et inventaire de départ : disponibles dès le début
PIECES_DE_DEPART = {"malle", "inventaire"}


def _id(x):
    """Objet d'un emplacement : un id, ou un tuple (id, quantité)."""
    return x[0] if isinstance(x, tuple) else x


def piece_sans_cle(piece, objet=None):
    """Pièce où l'objet (clé ou objet d'énigme) ne doit pas aller."""
    if objet in PIECES_INTERDITES_OBJET:
        return piece in PIECES_INTERDITES_OBJET[objet]
    return piece in PIECES_SANS_CLE


# Portes à clé d'après les pages des CLÉS d'evilresource (chaque page liste toutes ses portes) : elles priment sur
# les pages des pièces, qui oublient parfois la condition d'un côté (partie test du 25/11/2026, seed 982599 : la grille
# cimetière -> grande galerie, la porte couloir nord -> escalier ouest et le patio étaient crus libres). Verrouillées
# dans les deux sens.
PORTES_A_CLE = {
    "armure": [("101", "103"), ("103", "10f"), ("106", "212"), ("10a", "117"), ("207", "208"), ("204", "205"),
               ("204", "20d")],
    "epee": [("202", "101"), ("103", "21c"), ("107", "108"), ("106", "204")],
    "bouclier": [("20e", "210")],
    "casque": [("106", "111"), ("101", "215"), ("20b", "20c"), ("217", "216")],
    "vieille": [("101", "203"), ("208", "20a"), ("101", "102"), ("117", "10b"), ("109", "114")],
}


def _aretes():
    """Arêtes avec conditions : celles du site (sens par sens), plus les conditions de l'onglet Verrous et les remplacements prudents."""
    sens = {}
    for a, b, c in ARETES_SITE:
        sens[(a, b)] = c
    # Pas de symétrie automatique : le site donne la condition vue depuis chaque pièce (une porte « libre » d'un côté
    # est souvent une pièce sans issue où l'on n'entre qu'avec la clé). Les portes douteuses sont dans PORTES_A_VERIFIER.
    for cle, portes in PORTES_A_CLE.items():
        for a, b in portes:
            sens[(a, b)] = cle
            sens[(b, a)] = cle
    # Grille du fond de la grande galerie vers le cimetière (joueur, 26/11/2026) : elle ne s'ouvre que depuis la
    # grande galerie (vieille clé) ; du cimetière, on ne peut pas passer.
    sens[("10b", "117")] = "impossible"
    for (a, b), c in REMPLACEMENTS.items():
        sens[(a, b)] = c
    liste = [(a, b, c) for (a, b), c in sens.items() if c not in ("autre_cote", "impossible")]
    for a, b, c in ARETES_EN_PLUS:
        liste = [x for x in liste if (x[0], x[1]) != (a, b)] + [(a, b, c)]
    return liste


ARETES = _aretes()


def _ouvre(cond, possede, vieilles_utilisees):
    if cond is None:
        return True
    if cond == "vieille":
        return possede[VIEILLE_CLE] > vieilles_utilisees
    if cond == "objet_mp":
        return possede[53] >= 1
    if cond == "deux_objets_mp":
        return possede[53] >= 1 and possede["objet_mp_2"] >= 1
    if cond == "grotte":
        return possede[67] >= 1 and possede[60] >= 1
    if cond == "poignee":
        return possede[45] >= 1 or possede[48] >= 1
    if cond == "carburant":
        return possede["capsule_pleine"] >= 1 or possede[31] >= 1
    if cond == "codes_mo":
        return all(possede[x] >= 1 for x in (93, 94, 95)) and possede["terminal_mo"] >= 3
    if cond == "medailles":
        return possede[51] >= 1 and possede[52] >= 1
    if cond == "arbre_cylindre":
        return possede[122] >= 1 and possede[123] >= 1
    return possede[CLE[cond]] >= 1


def parcourir(emplacements, contenu, depart_possede=(), sans_vieilles=False):
    """Joue la partie : depuis le hall, ouvre tout ce qui peut l'être, ramasse tout ce qui est atteignable, et
    recommence tant que ça avance. emplacements : liste des emplacements (piece, id d'origine) ; contenu : index ->
    objet posé (id). Renvoie (pièces atteintes, index des emplacements ramassés, objets possédés)."""
    possede = Counter(depart_possede)
    ramasses, pieces = set(), {DEPART} | PIECES_DE_DEPART
    vieilles_portes = set()            # portes à vieille clé déjà ouvertes (une clé chacune, deux sens)
    dons_faits = set()
    while True:
        avance = False
        # pièces : on ouvre d'abord tout ce qui ne coûte pas de vieille clé
        for _ in range(200):
            nouvelles = False
            for a, b, c in ARETES:
                if a in pieces and b not in pieces:
                    if c == "vieille":
                        porte = frozenset((a, b))
                        if porte in vieilles_portes:
                            pieces.add(b); nouvelles = True
                        continue
                    if _ouvre(c, possede, 0):
                        pieces.add(b); nouvelles = True
            if not nouvelles:
                break
        # emplacements
        for i, (piece, origine) in enumerate(emplacements):
            if i in ramasses or piece not in pieces:
                continue
            besoin = CONDITIONS_EMPLACEMENT.get((piece, origine), ())
            if all(possede[x] >= 1 for x in besoin):
                ramasses.add(i); possede[_id(contenu[i])] += 1; avance = True
        for k, (piece, objet, besoin) in enumerate(DONS):
            if k not in dons_faits and (piece is None or piece in pieces) and all(possede[x] >= 1 for x in besoin):
                dons_faits.add(k); possede[objet] += 1; avance = True
        if avance:
            continue
        if sans_vieilles:
            return pieces, ramasses, possede
        # plus rien : on dépense une vieille clé sur une porte qui mène à une pièce nouvelle
        for a, b, c in ARETES:
            if c == "vieille" and a in pieces and b not in pieces and possede[VIEILLE_CLE] > len(vieilles_portes):
                vieilles_portes.add(frozenset((a, b))); avance = True
                break
        if not avance or sans_vieilles:
            return pieces, ramasses, possede


def finissable(emplacements, contenu, ids=None, but_seulement=False):
    """La partie est finissable : but atteint et tous les objets mélangés (ids) ramassables (but_seulement : le but
    suffit, option « Fin garantie seulement »)."""
    ids = IDS_CLES if ids is None else ids
    pieces, ramasses, possede = parcourir(emplacements, contenu)
    for piece, besoin in BUT:
        if piece not in pieces or not all(possede[x] >= 1 for x in besoin):
            return False
    return but_seulement or all(i in ramasses for i, objet in enumerate(contenu) if _id(objet) in ids)


def liberer(emplacements, contenu, graine, interdits=(), ids=None):
    """Option « Fin garantie seulement » (27/11/2026, idée du joueur) : après un placement avec logique, chaque clé /
    objet d'énigme (ordre tiré au sort) est échangé avec un emplacement pris au hasard, n'importe où (même derrière
    une porte qu'on n'ouvrira jamais) ; l'échange est gardé si l'on peut encore finir le jeu. contenu est modifié
    sur place. Renvoie le nombre d'échanges gardés."""
    rng = random.Random(graine ^ 0xF1A1)
    ids = IDS_CLES if ids is None else set(ids)
    interdits = set(interdits)
    libres = [i for i in range(len(contenu)) if i not in interdits]
    gardes = 0
    for _ in range(PASSES_LIBERER):          # plusieurs passes : plus de désordre (une seule en laisse peu)
        cles = [i for i in libres if _id(contenu[i]) in ids]
        rng.shuffle(cles)
        gardes += _liberer_passe(emplacements, contenu, rng, libres, cles, ids)
    return gardes


PASSES_LIBERER = 3


def _liberer_passe(emplacements, contenu, rng, libres, cles, ids):
    gardes = 0
    for i in cles:
        j = rng.choice(libres)
        if j == i:
            continue
        contenu[i], contenu[j] = contenu[j], contenu[i]
        if finissable(emplacements, contenu, ids, but_seulement=True):
            gardes += 1
        else:
            contenu[i], contenu[j] = contenu[j], contenu[i]
    return gardes


def placer_cles(emplacements, contenu, graine, interdits=(), essais=2000, ids=None):
    """Mélange les clés (IDS_CLES) parmi les emplacements, en gardant la partie finissable. emplacements : liste
    (piece, id d'origine) ; contenu : objets posés (même ordre), modifié sur place. interdits : index où une clé ne
    doit pas aller (ex. plantes de la serre). Méthode : on retire les clés, puis on les replace une à une sur un
    emplacement atteignable en supposant qu'on a toutes celles pas encore placées (« remplissage supposé »).
    Renvoie True si réussi."""
    rng = random.Random(graine ^ 0xC1E5)
    ids = IDS_CLES if ids is None else set(ids)
    interdits = set(interdits)
    # pièces interdites selon l'objet (labo et héliport pour presque tous)
    hors_piece = {o: {i for i, (p, _) in enumerate(emplacements) if piece_sans_cle(p, o)}
                  for o in {_id(x) for x in contenu if _id(x) in ids} | {None}}
    cles_idx = [i for i, o in enumerate(contenu) if _id(o) in ids]
    cles = [contenu[i] for i in cles_idx]
    for _ in range(essais):
        essai = list(contenu)
        a_placer = list(cles)
        rng.shuffle(a_placer)
        # les clés libèrent leur emplacement : un objet ordinaire tiré au hasard parmi ceux mélangés prendra la place
        libres = {i for i, o in enumerate(essai) if _id(o) not in ids and i not in interdits}
        for i in cles_idx:
            essai[i] = None
        # un trou laissé par une clé interdite (ex. clé d'origine au labo) : jamais (les clés relevées n'y sont pas)
        ok = True
        while a_placer:
            cle = a_placer.pop()
            hypo = list(essai)
            # emplacements vides : objets ordinaires neutres pour le parcours
            hypo = [x if x is not None else 0 for x in hypo]
            vieille = _id(cle) == VIEILLE_CLE
            # une vieille clé ne va jamais derrière une porte à vieille clé : le joueur pourrait avoir dépensé les
            # siennes ailleurs et rester enfermé (5 clés pour 5 portes)
            pieces, ramasses, _ = parcourir(emplacements, hypo, depart_possede=[_id(x) for x in a_placer],
                                            sans_vieilles=vieille)
            exclus = hors_piece.get(_id(cle), hors_piece[None])
            candidats = [i for i in ramasses if i not in interdits and i not in exclus
                         and (essai[i] is None or i in libres)
                         and (essai[i] is None or _id(essai[i]) not in ids)]
            if not candidats:
                ok = False
                break
            i = rng.choice(sorted(candidats))
            if essai[i] is not None:            # on prend la place d'un objet ordinaire : il va dans un trou laissé par une clé
                trou = next(j for j in cles_idx if essai[j] is None)
                essai[trou] = essai[i]
            essai[i] = cle
        if ok and None not in essai and finissable(emplacements, essai, ids):
            contenu[:] = essai
            return True
    return False
