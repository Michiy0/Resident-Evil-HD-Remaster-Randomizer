# Resident Evil HD Remaster Randomizer (PC / Steam)

[English](README.md) · [Français](README.md#français) · **Deutsch** · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [中文](README.zh.md)

> ⚠️ **Diese Übersetzung wurde noch nicht von einem Muttersprachler geprüft.** Die englische Fassung
> ([README.md](README.md)) ist die Referenz und kann aktueller sein. Fehler bitte in einem
> [Issue](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/issues) melden.

**[⬇ Neueste Version herunterladen](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/releases)** ·
[Problem melden](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/issues)

Der Randomizer **verteilt die Gegenstände des Spiels neu**: Munition, Kräuter, Farbbänder… liegen nicht mehr
dort, wo man sie erwartet, und jedes neue Spiel läuft anders ab. Der neue Gegenstand erscheint direkt am Boden
und in der Vorschau vor dem Aufheben.

Jede Mischung hat eine Nummer, den **Seed**. Derselbe Seed ergibt immer genau dieselbe Mischung: Teile die
Nummer, und ein Freund kann dasselbe Spiel spielen wie du, jeder auf seinem PC oder Steam Deck, um Zeiten
oder Strategien zu vergleichen.

> Inoffizielles **Fanprojekt**, nicht mit Capcom verbunden. Es sind keine Spieldateien enthalten: Du brauchst
> [Resident Evil HD Remaster auf Steam](https://store.steampowered.com/app/304240/).

## Kurz gesagt

- **Gegenstände wechseln den Platz**: Munition, Kräuter, Farbbänder, Dolche… Schlüssel und Questgegenstände
  bleiben, wo sie sind, damit das Spiel immer schaffbar bleibt.
- **Eine einfache App**: Randomizer installieren, Optionen wählen, Seed erstellen, fertig. Ein Klick bringt
  das Originalspiel zurück.
- **Sonst nichts zu installieren**: Eine kleine DLL wird mit dem Spiel geladen und erledigt die Arbeit. Der
  Code des Spiels wird nie verändert.
- **Windows und Steam Deck**: eine Windows-App und eine native Linux-App für das Steam Deck.
- **9 Sprachen**: Englisch, Französisch, Deutsch, Italienisch, Japanisch, Spanisch, Portugiesisch, Russisch
  und Chinesisch (standardmäßig die Systemsprache).
- **Gemeinschaftsprojekt**: Jeder Spieler kann mit dem eingebauten Erfassungsmodus helfen, die Gegenstände
  des Spiels zu erfassen.
- **Archipelago-Unterstützung in Vorbereitung**: siehe [Archipelago](#archipelago-demnächst).

## Bilder

<p align="center"><img src="images/avant_apres.gif" alt="Derselbe Raum im Originalspiel und mit dem Randomizer" width="640"><br><sub>Derselbe Raum, erst Originalspiel, dann Randomizer: Der Dolch auf dem Tisch ist jetzt ein grünes Kraut, und das Gewehr an der Wand wurde durch ein Pistolenmagazin ersetzt — sofort sichtbar, ohne etwas aufzuheben</sub></p>

<table>
<tr>
<td align="center"><img src="images/appli_generer_en.png" alt="Seed erstellen" width="420"><br><sub>Seed erstellen: Optionen und Waffenwahl</sub></td>
<td align="center"><img src="images/appli_installation_en.png" alt="Installation" width="420"><br><sub>Installation: die DLL mit einem Klick</sub></td>
</tr>
<tr>
<td align="center" colspan="2"><img src="images/appli_spoiler_en.png" alt="Spoiler" width="420"><br><sub>Spoiler: die vollständige Liste der Änderungen</sub></td>
</tr>
</table>

## Stand

| Unterstützt | Demnächst |
|---|---|
| Chris, Schwierigkeit Normal (ganzes Spiel erfasst, Labor inklusive) | Jill, weitere Schwierigkeitsgrade |
| 164 Fundorte: Munition (Pistole, Gewehr, Magnum), grüne, rote und blaue Kräuter, Farbbänder, Dolche, Blendgranaten, Selbstverteidigungswaffe, Erste-Hilfe-Sprays und -Kästen | Schlüssel und Questgegenstände (mit einer Logik, die das Spiel schaffbar hält) |
| **Gegenstände am Boden sichtbar**: Der neue Gegenstand erscheint im Raum und in der Vorschau; Option **Zufällige Kiste am Start** | Sichtbare Questgegenstände und Gegenstände, die man durch Untersuchen erhält (Edelsteine der Trophäen, Angelhaken…: von der DLL bereits unterstützt), mit den Schlüsseln |
| Option **Zufällige Waffen** (Pistole, Gewehr, Kampfgewehr, Magnum) und **Garantierte Startwaffe** (zu Spielbeginn ins Inventar, mit Munition); Option **Zufälliges Startmesser** (du kannst ohne Waffe beginnen!) | Weitere Waffen (Granatwerfer, Flammenwerfer), zufällige Gegner |
| Bereich **Spaß**: **Bonuswaffen** (Samurai Edge und Raketenwerfer mit unendlicher Munition) | — |
| Windows und **Steam Deck** (im Spiel unter Proton getestet, auch SD-Karte); Linux | **[Archipelago](#archipelago-demnächst)** |

**Benötigte Spielversion**: die aktuelle Steam-`bhd.exe` (9.640.360 Bytes). Die App prüft das; bei jeder
anderen Version bleibt der Randomizer inaktiv und das Spiel unverändert.

## Archipelago (demnächst)

[Archipelago](https://archipelago.gg) ist ein Multi-Game-Randomizer: Die Gegenstände deines Spiels können in
den Spielen anderer Spieler landen (und umgekehrt), jeder in seinem eigenen Spiel, gleichzeitig. Die
Unterstützung für Resident Evil HD Remaster ist in Vorbereitung: Der Tab *Archipelago* der App zeigt bereits
das (noch ausgegraute) Verbindungsformular und was noch zu tun ist. Zuerst müssen die Schlüssel mit Logik
gemischt werden.

## Fortschritt der Erfassung

Anteil der in einem **neuen Spiel** erfassten Räume, je Charakter und Schwierigkeit (siehe
[Projekt unterstützen](#projekt-unterstützen)). Details in der [englischen Fassung](README.md#survey-progress).

<img src="images/progression_en.svg" alt="Fortschritt der Erfassung" width="800">

## Installation

### Windows

1. Lade `ResidentEvilHDRemasterRandomizer-v…-windows.zip` von den
   **[Releases](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/releases)** herunter und entpacke es irgendwo.
2. Starte `Resident Evil HD Remaster Randomizer.exe`. Der Spielordner wird automatisch gefunden (sonst: **Durchsuchen…**).
3. Tab **Installation**: Klicke einmal auf **DLL installieren**. Der Tab **Seed erstellen** wird freigeschaltet.
4. Wähle deine Optionen und klicke auf **Seed erstellen** (lass „Seed im Spiel installieren“ angehakt).
5. Starte das Spiel über Steam: **neues Spiel, Chris, Normal**.

Für einen anderen Seed: einen neuen erstellen und das Spiel neu starten. Die App **aktualisiert sich selbst**.

> **SmartScreen / Antivirus**: Die exe ist nicht signiert (Hobbyprojekt). Windows kann „Der Computer wurde
> durch Windows geschützt“ anzeigen → *Weitere Informationen* → *Trotzdem ausführen*. Manche Antivirenprogramme
> melden die DLL fälschlich: Sie nutzt einen Hardware-Haltepunkt (wie Cheat Engine). Der gesamte Quellcode
> ist in diesem Repository.

### Steam Deck / Linux

Die App gibt es als **native Linux-Version** (ohne Proton); das Spiel selbst läuft weiter mit Proton.

1. Lade im **Desktop-Modus** `ResidentEvilHDRemasterRandomizer-v…-linux.tar.gz` herunter und entpacke es.
2. Doppelklicke auf `Resident Evil HD Remaster Randomizer` (falls nötig: Rechtsklick → *Eigenschaften* →
   *Berechtigungen* → „Ausführbar“). Das Spiel wird in deiner Steam-Bibliothek gefunden, auch auf der SD-Karte.
3. Tab **Installation**: **DLL installieren**, dann die Startoption **Kopieren** und einmal in Steam einfügen
   (*Eigenschaften des Spiels → Startoptionen*):
   ```
   WINEDLLOVERRIDES="xinput1_4=n,b" %command%
   ```
   Wenn du **BhdTool** (oder einen anderen Mod in `dinput8.dll`) nutzt, hake *Auch dinput8.dll laden* an.
4. **Seed erstellen**, dann das Spiel starten.

Die App kann auch als **Nicht-Steam-Spiel** hinzugefügt werden, um sie im **Spielmodus** zu nutzen: Der Knopf
**Beenden** oben rechts schließt sie sauber.

**Zurück zum Originalspiel**: in der App **DLL deinstallieren** (auf dem Steam Deck auch die Startoption
entfernen).

## Benutzung

Die App hat sechs Tabs und oben rechts eine Sprachauswahl („Automatisch“ = Systemsprache).

- **Installation** — Spielordner, Status von Randomizer und installiertem Seed, DLL installieren /
  aktualisieren / deinstallieren (und die Startoption auf dem Steam Deck).
- **Seed erstellen** — mit vier Untertabs:
  - *Charakter und Schwierigkeit*;
  - *Optionen*: Gegenstände am Boden sichtbar, Zufällige Kiste am Start, Zufällige Waffen (mit Waffenliste),
    Garantierte Startwaffe (ins Inventar, mit Munition; ihr Fundort erhält einen zufälligen Gegenstand) und
    Zufälliges Startmesser; darunter *Für die Verrückten* (Ohne Logik, demnächst);
  - *Gegner*: Zufällige Gegner (demnächst);
  - *Spaß*: Bonuswaffen (Samurai Edge, Raketenwerfer oder beide);
  - **Seed erstellen** mit dem Seed (oder „Zufällig“) daneben — gleicher Seed + gleiche Optionen = gleiches
    Ergebnis.
- **Spoiler** — die vollständige Liste der Änderungen als Tabelle, mit Suche und Sortierung, verborgen, bis du
  *Spoiler anzeigen* anhakst.
- **Archipelago** — demnächst.
- **Projekt unterstützen** — Erfassungsmodus und Fortschrittsbalken.
- **Info** — Mitwirkende und ein Link zu dieser Seite.

### Kompatibilität

- **BhdTool**: kompatibel (es nutzt `dinput8.dll`, der Randomizer `xinput1_4.dll`).
- **Ein anderer Mod, der eine `xinput1_4.dll` installiert**: nicht kompatibel. Die App erkennt ihn und rührt ihn nie an.

## Empfohlene Mods

### Resident Evil Fusion Fix

[Resident Evil Fusion Fix](https://github.com/ThirteenAG/WidescreenFixesPack/releases/tag/re1) (ThirteenAG)
macht das Spiel angenehmer: alle Auflösungen, randloses Fenster, Türanimationen überspringen, freie
Bildrate (optional)… Installation: `ResidentEvil.FusionFix.zip` in den Spielordner entpacken.

- Funktioniert zusammen mit dem Randomizer.
- Nutzt `dinput8.dll`, **wie BhdTool**: beide gleichzeitig geht nicht. Fusion Fix zum **Spielen**, BhdTool
  für die **Erfassung**.
- Auf dem Steam Deck auch *Auch dinput8.dll laden* anhaken.

## Projekt unterstützen

Der Randomizer mischt nur bereits **erfasste** Gegenstände. Jeder kann durch Spielen helfen:

1. Tab **Projekt unterstützen** → **Erfassungsmodus** anhaken (DLL installiert).
2. Ein **neues Spiel** starten.
3. Räume besuchen, ohne etwas aufzuheben; etwa 2 Sekunden in jedem bleiben.
4. Das Protokoll öffnen (Knopf **Spielprotokoll**) und an ein
   [Issue](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/issues) anhängen, mit Charakter und Schwierigkeit.

**Tipp: [BhdTool](https://github.com/eleval/BhdTool) spart viel Zeit** (Sprung in jeden Raum, Türen
überspringen; Menü mit **F5**).

## Problem melden

Öffne ein [Issue](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/issues) und hänge
`randomizer_journal.txt` an (Knopf **Spielprotokoll**), mit Seed, Optionen, Plattform und dem, was passiert ist.

## Für Entwickler

Siehe die [englische Fassung](README.md#for-developers) (Funktionsweise, Inhalt des Repositorys, Bauen).

## Mitwirkende

- **Autor**: **Jojo / Michiyo** (Delage Jordan) — [GitHub-Profil](https://github.com/Michiy0).
- **Tests und Erfassung der Gegenstände**: **Nico** (De Oliveira Gomes Nicolas) — „Number One Chris Fan“ 👊
- **[BhdTool](https://github.com/eleval/BhdTool)** (eleval, GPLv3): Raumnamen und -verbindungen, große Hilfe bei der Erfassung.
- Inspiriert von Community-Randomizern (BioRand, der frühere Randomizer von Benn Powell).

## Lizenz

GPLv3 — siehe [LICENSE](LICENSE).
