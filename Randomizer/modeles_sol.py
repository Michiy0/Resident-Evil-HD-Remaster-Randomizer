"""
Modèles au sol « faits maison » (25/11/2026, idée du joueur) : couteau, Samurai Edge infini et lance-roquettes infini
n'ont pas de modèle d'objet posé dans le jeu. On en fabrique un à partir du modèle tenu en main par le personnage.

Aucun fichier du jeu n'est distribué : tout est fabriqué sur le PC du joueur, à partir de SES fichiers du jeu, à
l'installation de la DLL (et supprimé à sa désinstallation). Archives produites dans nativePC\\arc\\model\\item :
  i001p.arc (couteau, depuis arc\\wep\\wep01.arc), i005p.arc (Samurai Edge, wep0b), i014p.arc (lance-roquettes, wep07).
La DLL emprunte la classe d'un objet de Jill (19, 20, 7) et réécrit son chemin de modèle vers ces archives.

Format ARC (version 7, celle du jeu ; vérifié octet pour octet le 25/11/2026) : « ARC\\0 », version (2 octets),
nombre de fichiers (2), puis 80 octets par fichier : nom sur 64 (sans extension), hash du type, taille compressée,
taille | 0x40000000, position ; données compressées zlib à partir de 0x8000. Matériau (MRL v34) converti pour un
objet posé : voir convertir_materiau.
"""
import re
import struct
import zlib
from pathlib import Path

TYPES = {".tex": 0x241F5DEB, ".mrl": 0x2749C8A8, ".mod": 0x58A15856}
EXTENSIONS = {v: k for k, v in TYPES.items()}
# (id de l'objet, archive de l'arme tenue en main, nom de l'arme dans cette archive)
OBJETS = (("001", "wep01"), ("005", "wep0b"), ("014", "wep07"))
GABARIT = "i112p"            # le poignard : matériau d'objet posé, cubemap et EmiUV
MARQUE = "model\\wep\\wep00\\"   # nos archives contiennent les textures de l'arme tenue en main


def lire_arc(chemin):
    """[(nom avec extension, données)] d'une archive ARC du jeu."""
    d = Path(chemin).read_bytes()
    if d[:4] != b"ARC\0":
        raise ValueError(f"pas une archive ARC : {chemin}")
    n = struct.unpack_from("<H", d, 6)[0]
    fichiers = []
    for i in range(n):
        e = d[8 + i * 80:8 + (i + 1) * 80]
        nom = e[:64].split(b"\0")[0].decode("ascii")
        type_, taille_c, _, pos = struct.unpack_from("<IIII", e, 64)
        fichiers.append((nom + EXTENSIONS.get(type_, ".%08x" % type_), zlib.decompress(d[pos:pos + taille_c])))
    return fichiers


def ecrire_arc(chemin, fichiers):
    """Écrit une archive ARC version 7 (fichiers : [(nom avec extension, données)], dans l'ordre voulu)."""
    entetes, blocs, pos = [], [], 0x8000
    for nom, donnees in fichiers:
        base, ext = nom.rsplit(".", 1)
        c = zlib.compress(donnees)
        e = bytearray(80)
        e[:len(base)] = base.encode("ascii")
        struct.pack_into("<IIII", e, 64, TYPES["." + ext], len(c), len(donnees) | 0x40000000, pos)
        entetes.append(bytes(e))
        blocs.append(c)
        pos += len(c)
    tete = b"ARC\0" + struct.pack("<HH", 7, len(fichiers)) + b"".join(entetes)
    Path(chemin).write_bytes(tete + b"\0" * (0x8000 - len(tete)) + b"".join(blocs))


# --------------------------------------------------------------------- matériau (MRL version 34)
ROLE_NM, ROLE_BM, ROLE_CUBE, ROLE_MM, ROLE_EMI = 0x2266034C, 0xCD06F349, 0x64C43359, 0x0ED1B35D, 0xED93B360


def _lire_mrl(d):
    nmat, ntex = struct.unpack_from("<II", d, 8)
    to, mo = struct.unpack_from("<II", d, 0x14)
    tex = [d[to + i * 0x4C + 12:to + (i + 1) * 0x4C].split(b"\0")[0].decode("ascii") for i in range(ntex)]
    mats = []
    for i in range(nmat):
        h = list(struct.unpack_from("<15I", d, mo + i * 0x3C))
        mats.append((h, d[h[13]:h[13] + h[2]], d[h[14]:h[14] + h[12]] if h[12] else b""))
    return d[:0x1C], tex, mats


def _roles(cmd):
    """{rôle: (position du mot, indice de texture)} : dans la liste de commandes, un indice de texture (à partir de 1)
    est suivi du hash de son rôle (normales, couleur, cubemap, reflets, EmiUV)."""
    w = struct.unpack_from("<%dI" % (len(cmd) // 4), cmd)
    return {w[k + 1]: (k, w[k]) for k in range(len(w) - 1)
            if 0 < w[k] < 64 and w[k + 1] in (ROLE_NM, ROLE_BM, ROLE_CUBE, ROLE_MM, ROLE_EMI)}


def _texture(chemin):
    e = bytearray(0x4C)
    struct.pack_into("<I", e, 0, TYPES[".tex"])
    e[12:12 + len(chemin)] = chemin.encode("ascii")
    return bytes(e)


def convertir_materiau(arme, gabarit):
    """Matériau d'objet posé : pour chaque matériau de l'arme (même nom, le modèle s'y réfère), la liste de commandes
    et l'animation du gabarit, branchées sur les textures de l'arme ; cubemap et EmiUV partagés."""
    entete, tex, mats = _lire_mrl(arme)
    _, _, gmats = _lire_mrl(gabarit)
    gh, gcmd, ganim = gmats[0]
    groles = _roles(gcmd)
    chemins = list(tex)
    if "scr\\CubeMap\\r106_CM" not in chemins:
        chemins.append("scr\\CubeMap\\r106_CM")
    chemins.append("model\\common\\EmiUV_MM")
    i_cube, i_emi = chemins.index("scr\\CubeMap\\r106_CM") + 1, len(chemins)
    debut_mat = 0x1C + len(chemins) * 0x4C
    pos_cmd = debut_mat + len(mats) * 0x3C
    pos_anim = pos_cmd + len(mats) * len(gcmd)
    entetes, cmds, anims = [], [], []
    for h, cmd, _ in mats:
        r = _roles(cmd)
        c = bytearray(gcmd)
        for role, idx in ((ROLE_NM, r.get(ROLE_NM, (0, 0))[1]), (ROLE_BM, r.get(ROLE_BM, (0, 0))[1]),
                          (ROLE_CUBE, i_cube), (ROLE_MM, r.get(ROLE_MM, (0, 0))[1]), (ROLE_EMI, i_emi)):
            if role in groles and idx:
                struct.pack_into("<I", c, groles[role][0] * 4, idx)
        nh = list(gh)
        nh[1], nh[13], nh[14] = h[1], pos_cmd, pos_anim
        entetes.append(struct.pack("<15I", *nh))
        cmds.append(bytes(c))
        anims.append(ganim)
        pos_cmd += len(gcmd)
        pos_anim += len(ganim)
    e = bytearray(entete)
    struct.pack_into("<II", e, 8, len(mats), len(chemins))
    struct.pack_into("<II", e, 0x14, 0x1C, debut_mat)
    return bytes(e) + b"".join(_texture(c) for c in chemins) + b"".join(entetes) + b"".join(cmds) + b"".join(anims)


# --------------------------------------------------------------------- installation
def _dossier_item(dossier_jeu):
    return Path(dossier_jeu) / "nativePC" / "arc" / "model" / "item"


def est_notre_archive(chemin):
    try:
        # nos archives : textures de l'arme tenue en main (modèles faits maison) ou modèle « iNNNg » (versions qui
        # brillent) ; le jeu n'a ni l'un ni l'autre dans arc\model\item
        return any(nom.startswith(MARQUE) or re.fullmatch(r"model\\item\\i\d{3}\\i\d{3}g\.mod", nom)
                   for nom, _ in lire_arc(chemin))
    except (OSError, ValueError, zlib.error, struct.error):
        return False


def fabriquer(dossier_jeu):
    """Fabrique les archives manquantes. Renvoie la liste des archives écrites. Ne remplace jamais un fichier qui
    n'est pas à nous."""
    item = _dossier_item(dossier_jeu)
    wep = Path(dossier_jeu) / "nativePC" / "arc" / "wep"
    gabarit = dict(lire_arc(item / f"{GABARIT}.arc"))
    mrl_gabarit = gabarit[f"model\\item\\i112\\{GABARIT}.mrl"]
    ecrites = []
    for n, w in OBJETS:
        cible = item / f"i{n}p.arc"
        if cible.exists() and not est_notre_archive(cible):
            continue                                   # fichier d'un autre mod : on n'y touche pas
        arme = dict(lire_arc(wep / f"{w}.arc"))
        dossier = f"model\\wep\\wep00\\{w}"
        textures = sorted(k for k in arme if k.startswith(dossier + "_") and k.endswith(".tex"))
        fichiers = [(k, arme[k]) for k in textures]
        fichiers += [("scr\\CubeMap\\r106_CM.tex", gabarit["scr\\CubeMap\\r106_CM.tex"]),
                     ("model\\common\\EmiUV_MM.tex", gabarit["model\\common\\EmiUV_MM.tex"]),
                     (f"model\\item\\i{n}\\i{n}p.mrl", convertir_materiau(arme[dossier + ".mrl"], mrl_gabarit)),
                     (f"model\\item\\i{n}\\i{n}p.mod", arme[dossier + ".mod"])]
        ecrire_arc(cible, fichiers)
        ecrites.append(cible)
    return ecrites


def presents(dossier_jeu):
    item = _dossier_item(dossier_jeu)
    return all((item / f"i{n}p.arc").exists() for n, _ in OBJETS)


def retirer(dossier_jeu):
    """Supprime nos archives (seulement les nôtres). Renvoie la liste des fichiers supprimés."""
    item = _dossier_item(dossier_jeu)
    retirees = []
    for n, _ in OBJETS:
        cible = item / f"i{n}p.arc"
        if cible.exists() and est_notre_archive(cible):
            cible.unlink()
            retirees.append(cible)
    return retirees


# --------------------------------------------------------------------- éclat des objets (26/11/2026)
# 55 des 102 modèles d'objets posés n'ont pas l'éclat qui aide à les repérer (herbes, masques, manivelles…). On en
# fabrique une version qui brille, arc\model\item\iNNNg.arc (la DLL réécrit le chemin de modèle de la classe et
# charge iNNNg partout où le jeu charge iNNNp). MOD v210 : en-tête (nb maillages en 0x08, taille du tampon de sommets
# 0x18 ; décalages : maillages 0x30, sommets 0x34, indices 0x38, fin 0x3C) ; maillage de 0x30 octets (+0x02 nb de
# sommets, +0x0A taille d'un sommet, +0x0C premier sommet, +0x10 décalage dans le tampon, +0x14 format).
# Format 0xA8FAB018 (20 o) : position 8, normale 4, tangente 4, UV 4. Format 0xD877801B (32 o, objets qui brillent) :
# les mêmes 20 octets, puis 4 octets nuls, UV de l'éclat, 4 octets nuls (on y recopie l'UV de la texture).
FMT_20, FMT_32 = 0xA8FAB018, 0xD877801B


def convertir_modele(d):
    d = bytearray(d)
    nmesh = struct.unpack_from("<H", d, 8)[0]
    mo, vb, ib, fin = struct.unpack_from("<IIII", d, 0x30)
    taille_vb = struct.unpack_from("<I", d, 0x18)[0]
    mesh = []
    for i in range(nmesh):
        o = mo + i * 0x30
        n = struct.unpack_from("<H", d, o + 2)[0]
        stride = d[o + 0x0A]
        base, voff, fmt = struct.unpack_from("<III", d, o + 0x0C)
        mesh.append([o, n, stride, base, voff, fmt])
    # régions du tampon de sommets (plusieurs maillages peuvent partager une région)
    regions = {}
    for o, n, stride, base, voff, fmt in mesh:
        r = regions.setdefault(voff, [stride, fmt, 0])
        if (r[0], r[1]) != (stride, fmt):
            raise ValueError("région partagée par deux formats")
        r[2] = max(r[2], base + n)
    if any(fmt not in (FMT_20, FMT_32) and stride != 12 for stride, fmt, _ in regions.values()):
        raise ValueError("format de sommets inconnu")
    nouveau, correspondance = bytearray(), {}
    for voff in sorted(regions):
        stride, fmt, nb = regions[voff]
        correspondance[voff] = len(nouveau)
        bloc = d[vb + voff:vb + voff + stride * nb]
        if fmt == FMT_20:
            for k in range(nb):
                v = bloc[k * 20:(k + 1) * 20]
                nouveau += v + b"\0\0\0\0" + v[16:20] + b"\0\0\0\0"     # UV de l'éclat = UV de la texture
        else:
            nouveau += bloc
    for o, n, stride, base, voff, fmt in mesh:
        struct.pack_into("<I", d, o + 0x10, correspondance[voff])
        if fmt == FMT_20:
            d[o + 0x0A] = 32
            struct.pack_into("<I", d, o + 0x14, FMT_32)
    delta = len(nouveau) - taille_vb
    sortie = d[:vb] + nouveau + d[vb + taille_vb:]
    struct.pack_into("<I", sortie, 0x18, len(nouveau))
    struct.pack_into("<II", sortie, 0x38, ib + delta, fin + delta)
    return bytes(sortie)


def fabriquer_eclats(dossier_jeu):
    """Version qui brille de chaque modèle d'objet posé qui n'en a pas. Renvoie la liste des archives écrites."""
    item = _dossier_item(dossier_jeu)
    gabarit = dict(lire_arc(item / f"{GABARIT}.arc"))
    mrl_gabarit = gabarit[f"model\\item\\i112\\{GABARIT}.mrl"]
    ecrites = []
    for source in sorted(item.glob("i???p.arc")):
        n = source.name[1:4]
        cible = item / f"i{n}g.arc"
        if cible.exists() and not est_notre_archive(cible):
            continue
        try:
            fichiers = lire_arc(source)
            if any("EmiUV" in k for k, _ in fichiers):
                continue                                   # brille déjà
            base = f"model\\item\\i{n}\\i{n}"
            contenu = dict(fichiers)
            if base + "p.mod" not in contenu or base + "p.mrl" not in contenu:
                continue
            tex = [(k, v) for k, v in fichiers if k.endswith(".tex") and "EmiUV" not in k and "CubeMap" not in k]
            sortie = tex + [("scr\\CubeMap\\r106_CM.tex", gabarit["scr\\CubeMap\\r106_CM.tex"]),
                            ("model\\common\\EmiUV_MM.tex", gabarit["model\\common\\EmiUV_MM.tex"]),
                            (base + "g.mrl", convertir_materiau(contenu[base + "p.mrl"], mrl_gabarit)),
                            (base + "g.mod", convertir_modele(contenu[base + "p.mod"]))]
        except (ValueError, KeyError, struct.error, zlib.error):
            continue                                       # format inconnu : ce modèle garde son apparence
        ecrire_arc(cible, sortie)
        ecrites.append(cible)
    return ecrites


def retirer_eclats(dossier_jeu):
    retirees = []
    for cible in _dossier_item(dossier_jeu).glob("i???g.arc"):
        if est_notre_archive(cible):
            cible.unlink()
            retirees.append(cible)
    return retirees
