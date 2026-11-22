RESIDENT EVIL HD REMASTER RANDOMIZER — Linux / Steam Deck
========================================================

The app runs natively on Linux (no Proton needed). The game itself runs with Proton as
usual. (Français : voir LISEZ-MOI.txt)

INSTALLING (only once)
1. On Steam Deck, switch to Desktop mode (Steam button → Power → Switch to Desktop).
2. Extract this archive wherever you like, for example in your home folder.
3. If needed, make the file executable: right-click Resident Evil HD Remaster Randomizer →
   Properties → Permissions → tick "Is executable".
4. Double-click Resident Evil HD Remaster Randomizer.
   The game is found automatically in your Steam library (otherwise "Browse…").
5. Click "Install the DLL".
6. Click "Copy" next to the launch option, then in Steam:
   Resident Evil → Properties → Launch Options → paste:
       WINEDLLOVERRIDES="xinput1_4=n,b" %command%
   With BhdTool (or another dinput8.dll mod): tick "Also load dinput8.dll" before copying
   (it is ticked automatically if the file is found). The line becomes:
       WINEDLLOVERRIDES="xinput1_4=n,b;dinput8=n,b" %command%

PLAYING
1. "Generate a seed" tab: pick your options, then "Generate seed".
2. Start the game: NEW GAME with CHRIS, on EASY difficulty.
   At the question "What is your play style?", pick the 2nd answer: "II. Gamer".
   From a cleared save ("Once Again"): pick "Easy".
   On any other difficulty, the seed is not applied.
3. The "Spoiler" tab shows the full list of changes.

UPDATES
The app updates itself: it offers the new version when it starts.

CHECKING THAT IT WORKS
After picking up an item, the "Game log" button ("Help the project" tab) should show
"Point d'arret pose" then "objet remplace" (the log is in French). Tested and confirmed on
Steam Deck. If something goes wrong, open an "issue" on the project's GitHub page with this log.

GETTING THE ORIGINAL GAME BACK
"Uninstall the DLL" in the app, and remove the launch option in Steam.
