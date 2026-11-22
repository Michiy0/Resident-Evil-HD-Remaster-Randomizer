"""
Prépare une version publiable du projet dans le dossier publication/ :

  publication/depot/                  les fichiers à mettre sur GitHub (et seulement eux)
  publication/ResidentEvilHDRemasterRandomizer-v<x>-windows.zip à joindre à une « Release » GitHub ou à envoyer aux testeurs
                                      (Resident Evil HD Remaster Randomizer.exe + LISEZ-MOI.txt)

Seuls les fichiers de la liste FICHIERS sont copiés : sauvegardes, fichiers du jeu, outils de tiers et
seeds générées ne peuvent pas partir par erreur. Le tableur publié n'a pas l'onglet « Vocabulaire Benn ».
L'exe du zip est construit à partir de ces fichiers publiés (donc avec le tableur publié).

    python preparer_publication.py
"""
import io
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "Randomizer"))
from application import VERSION  # noqa: E402
import progression  # noqa: E402

ICI = Path(__file__).resolve().parent
SORTIE = ICI / "publication"
DEPOT = SORTIE / "depot"

# source (dans ce dossier)  ->  destination (dans le dépôt)
FICHIERS = {
    "README.md": "README.md",
    "README.de.md": "README.de.md",
    "README.es.md": "README.es.md",
    "README.it.md": "README.it.md",
    "README.pt.md": "README.pt.md",
    "README.ru.md": "README.ru.md",
    "README.ja.md": "README.ja.md",
    "README.zh.md": "README.zh.md",
    "LICENSE": "LICENSE",
    ".gitignore": ".gitignore",
    "LISEZ-MOI_testeur.txt": "LISEZ-MOI_testeur.txt",
    "LISEZ-MOI_linux.txt": "LISEZ-MOI_linux.txt",
    "preparer_publication.py": "preparer_publication.py",
    "donnees_randomizer_RE1.xlsx": "donnees_randomizer_RE1.xlsx",
    "DLL/randomizer.c": "DLL/randomizer.c",
    "DLL/xinput1_4.def": "DLL/xinput1_4.def",
    "DLL/compiler.bat": "DLL/compiler.bat",
    "DLL/compiler.sh": "DLL/compiler.sh",
    "DLL/LISEZMOI.md": "DLL/LISEZMOI.md",
    "Randomizer/application.py": "Randomizer/application.py",
    "Randomizer/generateur_seed.py": "Randomizer/generateur_seed.py",
    "Randomizer/importer_journal.py": "Randomizer/importer_journal.py",
    "Randomizer/progression.py": "Randomizer/progression.py",
    "Randomizer/textes.py": "Randomizer/textes.py",
    "Randomizer/noms_objets.py": "Randomizer/noms_objets.py",
    "Randomizer/mise_a_jour.py": "Randomizer/mise_a_jour.py",
    "Randomizer/noms_jeu.py": "Randomizer/noms_jeu.py",
    "images/progression.svg": "images/progression.svg",
    "images/progression_en.svg": "images/progression_en.svg",
    "images/appli_generer_fr.png": "images/appli_generer_fr.png",
    "images/appli_installation_fr.png": "images/appli_installation_fr.png",
    "images/appli_spoiler_fr.png": "images/appli_spoiler_fr.png",
    "images/appli_generer_en.png": "images/appli_generer_en.png",
    "images/appli_installation_en.png": "images/appli_installation_en.png",
    "images/appli_spoiler_en.png": "images/appli_spoiler_en.png",
    "images/avant_apres.gif": "images/avant_apres.gif",
    "Randomizer/creer_icone.py": "Randomizer/creer_icone.py",
    "Randomizer/construire_exe.bat": "Randomizer/construire_exe.bat",
    "Randomizer/construire_linux.sh": "Randomizer/construire_linux.sh",
    "Randomizer/icone.ico": "Randomizer/icone.ico",
    "Randomizer/icone.png": "Randomizer/icone.png",
    "Randomizer/creer_logo.py": "Randomizer/creer_logo.py",
    "Randomizer/logo.png": "Randomizer/logo.png",
    "Randomizer/logo_entete.png": "Randomizer/logo_entete.png",
    "outils/cheat_engine/appliquer_seed.lua": "outils/cheat_engine/appliquer_seed.lua",
    "outils/cheat_engine/journal_objets.lua": "outils/cheat_engine/journal_objets.lua",
    "outils/cheat_engine/test_remplacement.lua": "outils/cheat_engine/test_remplacement.lua",
}
ONGLETS_RETIRES = ["Vocabulaire Benn"]


def nettoyer_tableur(chemin):
    from openpyxl import load_workbook
    wb = load_workbook(chemin)          # formules conservées
    for nom in ONGLETS_RETIRES:
        if nom in wb.sheetnames:
            del wb[nom]
    ws = wb["Lisez-moi"]
    for ligne in range(ws.max_row, 0, -1):
        v = ws.cell(ligne, 1).value
        if isinstance(v, str) and any(v.startswith(n) for n in ONGLETS_RETIRES):
            ws.delete_rows(ligne)
    wb.save(chemin)


def construire_exe(depot):
    """Compile la DLL puis l'exe dans une copie temporaire du dépôt (le dépôt reste propre)."""
    with tempfile.TemporaryDirectory(prefix="randomizer_publication_") as tmp:
        copie = Path(tmp) / "depot"
        shutil.copytree(depot, copie)
        for script in ("DLL/compiler.bat", "Randomizer/construire_exe.bat"):
            r = subprocess.run(["cmd", "/c", str(copie / script)], capture_output=True, text=True,
                               encoding="cp850", errors="replace")
            if r.returncode != 0:
                sys.exit(f"Échec de {script} :\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
        exe = SORTIE / "Resident Evil HD Remaster Randomizer.exe"
        shutil.copyfile(copie / "Randomizer" / "dist" / "Resident Evil HD Remaster Randomizer.exe", exe)
        return exe


DISTRIBUTION_LINUX = "Ubuntu-22.04"   # glibc 2.35 : le binaire démarre aussi sur Steam Deck (SteamOS 3.5+)


def chemin_wsl(chemin):
    """C:\\Users\\… -> /mnt/c/Users/…"""
    chemin = str(Path(chemin).resolve())
    return "/mnt/" + chemin[0].lower() + chemin[2:].replace("\\", "/")


def wsl_disponible():
    try:
        r = subprocess.run(["wsl", "-l", "-q"], capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return False
    noms = r.stdout.decode("utf-16-le", errors="ignore").replace("\0", "").split()
    return DISTRIBUTION_LINUX in noms


def construire_linux(depot):
    """Construit Resident Evil HD Remaster Randomizer dans WSL (Ubuntu 22.04), à partir d'une copie du dépôt.
    Renvoie le chemin du binaire, ou None si WSL n'est pas disponible."""
    if not wsl_disponible():
        print(f"WSL « {DISTRIBUTION_LINUX} » absent : pas de version Linux cette fois.")
        return None
    with tempfile.TemporaryDirectory(prefix="rehdr_randomizer_linux_") as tmp:
        shutil.copytree(depot, Path(tmp) / "depot", ignore=shutil.ignore_patterns(".git"))
        script = Path(tmp) / "construire.sh"
        script.write_bytes((
            "set -e\n"
            f"SRC='{chemin_wsl(Path(tmp) / 'depot')}'\n"
            "rm -rf /root/build && cp -r \"$SRC\" /root/build\n"
            "sh /root/build/DLL/compiler.sh\n"
            "sh /root/build/Randomizer/construire_linux.sh\n"
            "cp \"/root/build/Randomizer/dist/Resident Evil HD Remaster Randomizer\" \"$SRC/../programme-linux\"\n"
        ).encode("utf-8"))
        r = subprocess.run(["wsl", "-d", DISTRIBUTION_LINUX, "-u", "root", "--", "sh", chemin_wsl(script)],
                           capture_output=True)
        if r.returncode != 0:
            sortie = (r.stdout + r.stderr).decode("utf-8", errors="replace")
            sys.exit(f"Échec de la construction Linux :\n{sortie[-3000:]}")
        binaire = SORTIE / "Resident Evil HD Remaster Randomizer"
        shutil.copyfile(Path(tmp) / "programme-linux", binaire)
        return binaire


def ajouter_tar(tar, nom, donnees, mode):
    info = tarfile.TarInfo(nom)
    info.size, info.mode, info.mtime = len(donnees), mode, int(time.time())
    tar.addfile(info, io.BytesIO(donnees))


def main():
    # Barres d'avancement (images/progression.svg et section du README) à jour avant la copie
    progression.mettre_a_jour(ICI / "donnees_randomizer_RE1.xlsx", ICI / "README.md",
                              ICI / "images" / "progression.svg")
    print("Barres d'avancement mises à jour.")

    # On vide le dépôt sauf son historique git (.git), pour que les fichiers retirés de la liste
    # disparaissent aussi du dépôt.
    if DEPOT.exists():
        for element in DEPOT.iterdir():
            if element.name == ".git":
                continue
            shutil.rmtree(element) if element.is_dir() else element.unlink()
    for src, dst in FICHIERS.items():
        cible = DEPOT / dst
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ICI / src, cible)
    nettoyer_tableur(DEPOT / "donnees_randomizer_RE1.xlsx")
    print(f"Dépôt prêt : {DEPOT} ({len(FICHIERS)} fichiers)")

    exe = construire_exe(DEPOT)
    archive = SORTIE / f"ResidentEvilHDRemasterRandomizer-v{VERSION}-windows.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(exe, "Resident Evil HD Remaster Randomizer.exe")
        z.write(ICI / "LISEZ-MOI_testeur.txt", "LISEZ-MOI.txt")
    exe.unlink()
    print(f"Archive prête : {archive} ({archive.stat().st_size // 1024} Ko)")

    binaire = construire_linux(DEPOT)
    if binaire:
        archive_linux = SORTIE / f"ResidentEvilHDRemasterRandomizer-v{VERSION}-linux.tar.gz"
        with tarfile.open(archive_linux, "w:gz") as tar:          # tar.gz : garde le droit d'exécution
            ajouter_tar(tar, "ResidentEvilHDRemasterRandomizer/Resident Evil HD Remaster Randomizer", binaire.read_bytes(), 0o755)
            ajouter_tar(tar, "ResidentEvilHDRemasterRandomizer/LISEZ-MOI.txt", (ICI / "LISEZ-MOI_linux.txt").read_bytes(), 0o644)
        binaire.unlink()
        print(f"Archive Linux prête : {archive_linux} ({archive_linux.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
