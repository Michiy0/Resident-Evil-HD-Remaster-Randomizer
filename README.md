# Resident Evil HD Remaster Randomizer (PC / Steam)

🌐 **English** · [Français](docs/README.fr.md) · [Deutsch](docs/README.de.md) · [Español](docs/README.es.md) · [Italiano](docs/README.it.md) · [Português](docs/README.pt.md) · [Русский](docs/README.ru.md) · [日本語](docs/README.ja.md) · [中文](docs/README.zh.md)

**[⬇ Download the latest version](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/releases)** ·
[Report a problem](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/issues)

The randomizer **moves the game's items around**: ammo, herbs, ink ribbons… are no longer where you
expect them, and every new game plays differently. The new item shows up directly on the floor and in the
preview before pickup.

Each shuffle has a number, the **seed**. The same seed always gives exactly the same shuffle: share the
number and a friend can play the same game as you, each on their own PC or Steam Deck, to compare times
or strategies.

> Unofficial **fan project**, not affiliated with Capcom. No game files are included: you need to own
> [Resident Evil HD Remaster on Steam](https://store.steampowered.com/app/304240/).

## In short

- **Items change places**: ammo, herbs, ink ribbons, daggers… Keys and quest items stay where they are,
  so the game is always completable.
- **A simple app**: install the randomizer, choose your options, generate a seed, and you're ready. One
  click brings back the original game.
- **Nothing else to install**: a small DLL loads with the game and does the work. The game's code is never
  modified.
- **Windows and Steam Deck**: a Windows app, and a native Linux app for the Steam Deck.
- **9 languages**: English, French, German, Italian, Japanese, Spanish, Portuguese, Russian and Chinese (system language
  by default).
- **Community project**: every player can help survey the game's items with the built-in survey mode.
- **Archipelago support coming**: the randomizer is being prepared for [Archipelago](https://archipelago.gg),
  the multi-game randomizer (see [Archipelago](#archipelago-coming-soon)).

## Screenshots

<p align="center"><img src="images/avant_apres.gif" alt="Same room in the original game and with the randomizer: the dagger on the table becomes a green herb and the shotgun on the wall becomes a handgun magazine" width="640"><br><sub>Same room, original game then randomizer: the dagger on the table is now a green herb, and the shotgun hanging on the wall is replaced by a handgun magazine — visible right away, no need to pick them up</sub></p>

<table>
<tr>
<td align="center"><img src="images/appli_generer_en.png" alt="Generate a seed: options and weapon choice" width="420"><br><sub>Generate a seed: options and weapon choice</sub></td>
<td align="center"><img src="images/appli_installation_en.png" alt="Installation: the DLL in one click" width="420"><br><sub>Installation: the DLL in one click</sub></td>
</tr>
<tr>
<td align="center"><img src="images/appli_difficulte_en.png" alt="Character and difficulty: which answer to pick in the game" width="420"><br><sub>Character and difficulty: which answer to pick in the game</sub></td>
<td align="center"><img src="images/appli_spoiler_en.png" alt="Spoiler: the full list of changes" width="420"><br><sub>Spoiler: the full list of changes</sub></td>
</tr>
</table>

## Status: version 0.9.7.2 (test)

| Supported | Coming |
|---|---|
| Chris, Easy difficulty (whole game surveyed, laboratory included) | Jill, other difficulties |
| 164 placed-item locations: ammo (handgun, shotgun and magnum), green, red and blue herbs, ink ribbons, daggers, flash grenades, self-defense gun, first aid sprays and boxes | Keys and quest items (with logic that keeps the game completable) |
| **Items visible on the ground**: the new item appears in the room and in the preview before pickup; **random starting item box** option | Visible quest items and items obtained by examining something (trophy gems, fish hook…: already supported by the game DLL, name and preview included), with keys |
| **Random weapons** option, with a choice of which weapons to shuffle (handgun, shotgun, assault shotgun, magnum) and a **guaranteed starting weapon** option (given in the inventory at the start, with its ammo); **random starting knife** option (you may start with no weapon!) | The other weapons (grenade launcher, flamethrower), random enemies, random doors |
| **Fun** section: **bonus weapons** (unlimited Samurai Edge and rocket launcher, each replacing a random item) | — |
| Windows and **Steam Deck** (tested in game under Proton, SD card included); Linux | **[Archipelago](#archipelago-coming-soon)** support |

**Required game version**: the current Steam `bhd.exe` (9,640,360 bytes, SHA-256
`39B840663E4B1A6835C60CBD176E4EE6C21B9197FC2C2DD733F2A7C36A0B429A`). The app checks it; on any other
version the randomizer stays inactive and the game is untouched.

## What's left to do

The randomizer is already playable, but a lot is still planned. Roughly in order:

1. **Random keys with logic**: keys and quest items shuffled too, while the game always stays finishable (a key
   never ends up behind the door it opens). This is the big next step: it also unlocks the *No logic* option and
   Archipelago.
2. **Jill**: survey all of her item locations (she has a bigger inventory, her own weapons and some different
   items).
3. **Other difficulties**: survey Very Easy, Normal and Hard (items change with the difficulty), and maybe set the
   difficulty automatically at the start of the game.
4. **The other weapons**: grenade launcher and flamethrower (each one can only be used by one character).
5. **Random enemies**: shuffle which enemies appear in each room.
6. **Random doors**: each door leads to a different room than usual.
7. **[Archipelago](#archipelago-coming-soon)**: play in a multiworld with other games.

You can help right now by surveying item locations: see [Help the project](#help-the-project).

## Archipelago (coming soon)

[Archipelago](https://archipelago.gg) is a multi-game randomizer: the items of your game can end up in other
players' games (and the other way round), each on their own game, at the same time. Support for Resident Evil
HD Remaster is being prepared.

- **Already in the app**: an *Archipelago* tab with the connection form (server, player name, password,
  DeathLink), greyed out for now, and the list of what is left to do.
- **Still to do**: keys and quest items shuffled with logic (this comes first), reporting each picked-up
  location to the server, receiving other players' items (into the item box, then a waiting list when it is full), the game's Archipelago "world"
  (`.apworld` file: items, locations, rules) and sending the goal (ending) to the server.

No date yet: the keys-with-logic step has to be finished first.

## Survey progress

Percentage of rooms surveyed in a **new game**, for each character and difficulty (see
[Help the project](#help-the-project)). Updated with every version.

<!-- progression-en:debut -->

<img src="images/progression_en.svg" alt="Survey progress" width="800">

<details><summary>Details (text)</summary>

| Character | Difficulty | Complete rooms | Visited (game in progress) | Items surveyed |
|---|---|---|---|---|
| Chris | Very Easy | 0/118 (0%) | 0 | 0 |
| Chris | Easy | 118/118 (100%) | 0 | 260 |
| Chris | Normal | 0/118 (0%) | 0 | 0 |
| Chris | Hard | 0/118 (0%) | 0 | 0 |
| Chris | Real Survival | 0/118 (0%) | 0 | 0 |
| Jill | Very Easy | 0/118 (0%) | 0 | 0 |
| Jill | Easy | 0/118 (0%) | 0 | 0 |
| Jill | Normal | 0/118 (0%) | 0 | 0 |
| Jill | Hard | 0/118 (0%) | 0 | 0 |
| Jill | Real Survival | 0/118 (0%) | 0 | 0 |

Bonus weapons: 2/2 identified. Updated 2026-11-22.

</details>

<!-- progression-en:fin -->

## Installing

### Windows

1. Download `ResidentEvilHDRemasterRandomizer-v…-windows.zip` from the
   **[Releases](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/releases)** and extract it anywhere.
2. Run `Resident Evil HD Remaster Randomizer.exe`. The game folder is found automatically (otherwise: **Browse…**).
3. **Installation** tab: click **Install the DLL** (once). The **Generate a seed** tab unlocks.
4. Choose your options, then **Generate seed** (keep “Install the seed in the game” ticked).
5. Start the game from Steam: **new game, Chris, Easy**. At the question “What is your play style?”, pick the 2nd answer, **“II. Gamer”** (that is Easy). From a cleared save (“Once Again”), pick **Easy**. On any other difficulty the seed is not applied.

To change seeds: generate a new one, then restart the game.

**Updates**: the app updates itself automatically since **v0.7**.

> **SmartScreen / antivirus**: the exe is not signed (hobby project). Windows may show “Windows protected
> your PC” → *More info* → *Run anyway*. Some antivirus tools may also flag the DLL by mistake: it uses a
> hardware breakpoint (like Cheat Engine) to detect the item being picked up. The full source code is in
> this repository.

### Steam Deck / Linux

The app has a **native Linux** version (no Proton needed for it); the game itself still runs with Proton.

1. In **Desktop Mode**, download `ResidentEvilHDRemasterRandomizer-v…-linux.tar.gz` and extract it.
2. Double-click `Resident Evil HD Remaster Randomizer` (if needed: right-click → *Properties* → *Permissions* → “Is
   executable”). The game is found in your Steam library, SD card included.
3. **Installation** tab: click **Install the DLL**, then **Copy** the launch option, and paste it once
   in Steam (*game Properties → Launch Options*):
   ```
   WINEDLLOVERRIDES="xinput1_4=n,b" %command%
   ```
   If you use **BhdTool** (or another mod in `dinput8.dll`), tick *Also load dinput8.dll* (ticked
   automatically when it is found): the line becomes `WINEDLLOVERRIDES="xinput1_4=n,b;dinput8=n,b" %command%`.
4. **Generate seed**, then start the game.

The app can also be added to Steam as a **non-Steam game** to use it in **Game Mode**: the **Quit** button, at the top right, closes it cleanly.

> **Tested and confirmed on Steam Deck**: the DLL works in game under Proton (game installed on the SD
> card). If something goes wrong, the **Game log** button shows what happened.

**Back to the original game**: in the app, **Uninstall the DLL** (on Steam Deck, also remove the launch
option). “Remove the installed seed” only removes the seed: without a seed, the DLL changes nothing.

## Usage

The app has six tabs, and a language selector at the top right (“Automatic” = system language, English
otherwise).

- **Installation** — game folder, randomizer and installed seed status, install / update / uninstall the
  DLL (and the launch option on Steam Deck). The app opens here until the DLL is installed and up to date.
- **Generate a seed** — unlocked once the DLL is in place, with four sub-tabs:
  - *Character and difficulty*;
  - *Options*: items visible on the ground (ticked by default; unticked, you see the original item until
    pickup), random starting item box (ticked by default; new game only), random weapons (ticking it shows the weapon list; untick those that should stay in place) and
    guaranteed starting weapon (given in the inventory, with its ammo; its location gets a random item instead) and random
    starting knife (the knife ends up elsewhere: without a guaranteed weapon, you may start with no weapon); below,
    in its own card, *For the crazy ones* (no logic, coming soon);
  - *Enemies*: random enemies (coming soon);
  - *Doors*: random doors, each door leads to a different room (coming soon);
  - *Fun*: bonus weapons (choose the Samurai Edge, the rocket launcher or both);
  - **Generate seed**, with the seed (or “Random”) next to it — same seed + same options = same result: writes
    the seed to the `seeds` folder and installs it in the game.
- **Spoiler** — unlocked as soon as there is a seed: the full list of changes as a table (location, original
  item, replacement), with search and sorting, hidden until you tick *Show spoiler*.
- **Archipelago** — coming soon: the connection form (greyed out) and what is left to do.
- **Help the project** — survey mode and the progress bars (see below).
- **Info** — the credits (author, testers, thanks) and a link to this page.

Options marked “coming soon” (keys, enemies, other weapons, Archipelago…) are visible but greyed out.

### Compatibility

- **BhdTool**: compatible (it uses `dinput8.dll`, the randomizer uses `xinput1_4.dll`).
- **Another mod that installs an `xinput1_4.dll`**: incompatible. The app detects it and never touches it.

## Recommended mods

Optional mods that make the game nicer to play with the randomizer. None of them is required.

### Resident Evil Fusion Fix

[Resident Evil Fusion Fix](https://github.com/ThirteenAG/WidescreenFixesPack/releases/tag/re1) (ThirteenAG)
makes the game more comfortable: every resolution your screen supports, borderless window, door animation
skip, unlocked frame rate (optional), noise filter and color correction can be turned off.
Install: extract `ResidentEvil.FusionFix.zip` into the game folder (settings in
`scripts/ResidentEvil.FusionFix.ini`).

- It works alongside the randomizer (they use different DLLs).
- It uses `dinput8.dll`, **like BhdTool**: you can't have both at once. Fusion Fix is recommended for
  **playing**; for **surveys**, BhdTool is more convenient (see *Help the project*).
- On Steam Deck, also tick *Add dinput8.dll* under the app's launch option.

## Help the project

The randomizer only shuffles items that have already been **surveyed**. Anyone can help by playing:

1. **Help the project** tab → tick **Survey mode** (DLL installed).
2. Start a **new game**: items already picked up no longer exist in memory.
3. Visit rooms without picking anything up; stay about 2 seconds in each. The DLL records the items in
   the game log (small stutter of about 0.3 s when entering a room).
4. Open the log (**Game log** button) and attach it to an
   [issue](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/issues), stating your character and difficulty.

**Tip: [BhdTool](https://github.com/eleval/BhdTool) saves a lot of time.** This tool by eleval, made for speedrun practice, is
installed by copying its `dinput8.dll` (and `rooms.json`) into the game folder; it works alongside the
randomizer. In game, **F5** opens its menu:
- its tool to **jump to any room** lets you go around the mansion in a few minutes in survey mode (still
  stay about 2 seconds in each room);
- **Door Skip** removes the door-opening animations.

On Steam Deck, also tick *Also load dinput8.dll* under the app's launch option.

Translations were made for the project: if you speak one of the 9 languages and spot a mistake, please
report it too (texts are in `Randomizer/textes.py`).

## Reporting a problem

Open an [issue](https://github.com/Michiy0/Resident-Evil-HD-Remaster-Randomizer/issues) and attach `randomizer_journal.txt`
(**Game log** button), with the seed, options, platform (Windows or Steam Deck) and what happened.

## For developers

### How it works

- **The app** (`Randomizer/application.py`, Python + Tk) builds a seed from the spreadsheet
  `donnees_randomizer_RE1.xlsx` (locations surveyed in game) and writes it to the game folder as
  `randomizer_seed.lua`. All the logic is in `generateur_seed.py`, also usable from the command line.
- **The DLL** (`DLL/randomizer.c`) poses as `xinput1_4.dll` and forwards every controller function to the
  real Windows DLL. It sets a **hardware breakpoint** on `bhd.exe+1512ED` (where the picked-up item is
  read) and, if the location is in the seed, replaces the item id and quantity. A location is identified
  by its room and its **fingerprint**: the 4 corners (x, z) of its pick-up area, identical on every PC.
- **Survey mode** (`Releve=1` in `randomizer.ini`) finds the placed items in memory when entering each
  room, using their signature (`00C233F4` / `00C2286C`), without picking anything up.
- `bhd.exe` is protected by SteamStub (code encrypted on disk): the DLL never modifies the code and goes
  idle on any other game version.

### Repository contents

```
donnees_randomizer_RE1.xlsx   data: rooms, items, locations, surveyed rooms, bonus
DLL/                          the DLL (randomizer.c, xinput1_4.def) and its build scripts
Randomizer/
  application.py              the app (6 tabs, 9 languages)
  mise_a_jour.py              automatic update from the GitHub Releases
  noms_jeu.py                 official item names, read from the installed game's texts
  generateur_seed.py          seed generation (also command line)
  importer_journal.py         imports survey logs into the spreadsheet
  progression.py              progress bars of this README
  textes.py                   all translations
  construire_exe.bat / construire_linux.sh, creer_icone.py, icons
docs/                         the README in other languages and the archives' read-me files
preparer_publication.py       prepares the repository, the Windows zip and the Linux archive
```

### Building

- **Windows** — Python 3 (`pip install openpyxl pyinstaller`) and 32-bit GCC from MSYS2
  (`pacman -S mingw-w64-i686-gcc`):
  ```bat
  DLL\compiler.bat
  Randomizer\construire_exe.bat
  ```
- **Linux** (or WSL; Ubuntu 22.04 recommended to stay compatible with the Steam Deck) —
  `sudo apt install python3 python3-venv python3-tk gcc-mingw-w64-i686`:
  ```sh
  sh DLL/compiler.sh
  sh Randomizer/construire_linux.sh
  ```
- **Without building**: `python Randomizer/application.py`, or from the command line
  `python Randomizer/generateur_seed.py 12345 --armes-aleatoires --installer`.
- **Importing surveys**:
  `python Randomizer/importer_journal.py journal.txt --personnage Chris --difficulte Facile --nouvelle-partie --ecrire`
  (without `--nouvelle-partie` if the game was already in progress: rooms then only count as visited).

The code, file names and command-line options are in French (the project's working language).

## Credits

- **Author**: **Jojo / Michiyo** (Delage Jordan) — [GitHub profile](https://github.com/Michiy0).
- **Testing and item surveys**: **Nico** (De Oliveira Gomes Nicolas) — “Number One Chris Fan” 👊
- **[BhdTool](https://github.com/eleval/BhdTool)** (eleval, GPLv3): its `rooms.json` provides the room names and connections, and
  the tool is a great help for surveys (see [Help the project](#help-the-project)).
- Inspired by community randomizers (BioRand, Benn Powell's former randomizer).

## License

GPLv3 — see [LICENSE](LICENSE).
