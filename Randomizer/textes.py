"""
Textes de l'application et du générateur, en 9 langues.

Chaque entrée : clé -> (français, anglais, japonais, espagnol, portugais, russe, chinois), puis
allemand et italien dans ALLEMAND_ITALIEN (fusionnés dans T à la fin du dictionnaire).
Les textes français sont la référence ; les autres ont été traduits pour le projet et peuvent être
améliorés par des locuteurs natifs (il suffit de modifier la chaîne, en gardant les {variables}).

    from textes import tr, LANGUES
    tr("generer", "en")                       -> "Generate seed"
    tr("dll_installee", "ja", chemin="C:\\…")  -> texte avec la variable remplie
"""

LANGUES = {          # code -> nom affiché dans le sélecteur (dans sa propre langue)
    "fr": "Français",
    "en": "English",
    "ja": "日本語",
    "es": "Español",
    "pt": "Português",
    "ru": "Русский",
    "zh": "中文",
    "de": "Deutsch",
    "it": "Italiano",
}
ORDRE = tuple(LANGUES)
PAR_DEFAUT = "en"

# Police par langue : Segoe UI n'a pas les idéogrammes, on prend la police système adaptée.
POLICES = {"ja": "Yu Gothic UI", "zh": "Microsoft YaHei UI"}

T = {
    # ------------------------------------------------------------ onglets et cartes
    "onglet_randomizer": ("Randomizer", "Randomizer", "ランダマイザー", "Randomizer", "Randomizer",
                          "Рандомайзер", "随机器"),
    "onglet_spoiler": ("Spoiler", "Spoiler", "ネタバレ", "Spoiler", "Spoiler", "Спойлер", "剧透"),
    "onglet_aide": ("Aider le projet", "Help the project", "プロジェクトに協力", "Ayudar al proyecto",
                    "Ajudar o projeto", "Помочь проекту", "协助项目"),
    "onglet_installation": ("Installation", "Installation", "インストール", "Instalación", "Instalação",
                            "Установка", "安装"),
    "onglet_generer": ("Générer une seed", "Generate a seed", "シード生成", "Generar una semilla",
                       "Gerar uma semente", "Создать сид", "生成种子"),
    "install_etapes": (
        "À faire une seule fois :\n"
        "1.  Vérifie le dossier du jeu (il est trouvé tout seul la plupart du temps).\n"
        "2.  Clique « Installer la DLL ».\n"
        "3.  Les onglets « Générer une seed » et « Spoiler » se débloquent.",
        "Only once:\n"
        "1.  Check the game folder (it is usually found automatically).\n"
        "2.  Click “Install the DLL”.\n"
        "3.  The “Generate a seed” and “Spoiler” tabs unlock.",
        "最初に一度だけ：\n"
        "1.  ゲームのフォルダーを確認（ほとんどの場合は自動で見つかります）。\n"
        "2.  「DLLをインストール」をクリック。\n"
        "3.  「シード生成」と「スポイラー」のタブが使えるようになります。",
        "Solo una vez:\n"
        "1.  Comprueba la carpeta del juego (casi siempre se encuentra sola).\n"
        "2.  Haz clic en «Instalar la DLL».\n"
        "3.  Las pestañas «Generar una semilla» y «Spoiler» se desbloquean.",
        "Só uma vez:\n"
        "1.  Confira a pasta do jogo (quase sempre é encontrada sozinha).\n"
        "2.  Clique em “Instalar a DLL”.\n"
        "3.  As abas “Gerar uma semente” e “Spoiler” são liberadas.",
        "Только один раз:\n"
        "1.  Проверьте папку игры (обычно она находится сама).\n"
        "2.  Нажмите «Установить DLL».\n"
        "3.  Вкладки «Создать сид» и «Спойлер» станут доступны.",
        "只需一次：\n"
        "1.  确认游戏文件夹（通常会自动找到）。\n"
        "2.  点击“安装 DLL”。\n"
        "3.  “生成种子”和“剧透”选项卡随即解锁。"),
    "install_etape_proton": (
        "Sur Steam Deck / Linux : colle aussi l'option de lancement ci-dessous dans Steam.",
        "On Steam Deck / Linux: also paste the launch option below into Steam.",
        "Steam Deck / Linux：下の起動オプションもSteamに貼り付けてください。",
        "En Steam Deck / Linux: pega también la opción de lanzamiento de abajo en Steam.",
        "No Steam Deck / Linux: cole também a opção de inicialização abaixo na Steam.",
        "На Steam Deck / Linux: вставьте также параметр запуска ниже в Steam.",
        "在 Steam Deck / Linux 上：还需把下方的启动选项粘贴到 Steam 中。"),
    "suivant_generer": ("Suivant : générer une seed  →", "Next: generate a seed  →", "次へ：シード生成  →",
                        "Siguiente: generar una semilla  →", "Próximo: gerar uma semente  →",
                        "Далее: создать сид  →", "下一步：生成种子  →"),
    "carte_jeu": ("Jeu", "Game", "ゲーム", "Juego", "Jogo", "Игра", "游戏"),
    "carte_partie": ("Personnage et difficulté", "Character and difficulty", "キャラクターと難易度",
                     "Personaje y dificultad", "Personagem e dificuldade", "Персонаж и сложность", "角色与难度"),
    "carte_options": ("Options", "Options", "オプション", "Opciones", "Opções", "Параметры", "选项"),
    "carte_fun": ("Fun", "Fun", "おたのしみ", "Diversión", "Diversão", "Для веселья", "娱乐"),
    "note_fun": ("Des options pour s'amuser : elles rendent la partie beaucoup plus facile.",
                 "Options just for fun: they make the game much easier.",
                 "お楽しみ用のオプションです。ゲームがかなり簡単になります。",
                 "Opciones para divertirse: hacen la partida mucho más fácil.",
                 "Opções para se divertir: deixam o jogo bem mais fácil.",
                 "Опции для веселья: игра становится намного проще.",
                 "娱乐选项：会让游戏变得容易得多。"),
    "note_armes_bonus_fun": (
        "Chaque arme cochée, à munitions illimitées, remplace un objet au hasard. "
        "Par terre, on voit l'objet d'origine jusqu'au ramassage.",
        "Each ticked weapon, with unlimited ammo, replaces a random item. "
        "On the ground you see the original item until you pick it up.",
        "チェックした武器（無限弾）が、それぞれランダムなアイテム1つと入れ替わります。"
        "拾うまでは元のアイテムが見えます。",
        "Cada arma marcada, con munición ilimitada, sustituye a un objeto al azar. "
        "En el suelo se ve el objeto original hasta recogerlo.",
        "Cada arma marcada, com munição ilimitada, substitui um item aleatório. "
        "No chão, você vê o item original até pegá-lo.",
        "Каждое отмеченное оружие с бесконечными патронами заменяет случайный предмет. "
        "На полу виден исходный предмет, пока его не подобрать.",
        "每把勾选的无限弹药武器会替换一个随机物品。拾取之前，地上显示的是原来的物品。"),
    "arme_bonus_samurai": ("Samurai Edge", "Samurai Edge", "サムライエッジ", "Samurai Edge", "Samurai Edge",
                           "Samurai Edge", "武士之刃"),
    "arme_bonus_roquettes": ("Lance-roquettes", "Rocket launcher", "ロケットランチャー", "Lanzacohetes",
                             "Lança-foguetes", "Ракетница", "火箭筒"),
    "col_lieu": ("Lieu", "Location", "場所", "Lugar", "Local", "Место", "地点"),
    "col_origine": ("Objet d'origine", "Original item", "元のアイテム", "Objeto original", "Item original",
                    "Исходный предмет", "原物品"),
    "col_nouveau": ("Remplacé par", "Replaced by", "入れ替え後", "Reemplazado por", "Substituído por", "Заменён на",
                    "替换为"),
    "rechercher": ("Rechercher", "Search", "検索", "Buscar", "Pesquisar", "Поиск", "搜索"),
    "effacer_recherche": ("Effacer", "Clear", "クリア", "Borrar", "Limpar", "Очистить", "清除"),
    "resultats_recherche": ("{n} ligne(s) trouvée(s)", "{n} line(s) found", "{n} 行見つかりました",
                            "{n} línea(s) encontrada(s)", "{n} linha(s) encontrada(s)", "Найдено строк: {n}",
                            "找到 {n} 行"),
    "carte_fous": ("Pour les fous", "For the crazy ones", "命知らず向け", "Para los locos", "Para os loucos",
                   "Для безумцев", "疯狂玩家专用"),
    "carte_ennemis": ("Ennemis", "Enemies", "敵", "Enemigos", "Inimigos", "Враги", "敌人"),
    "carte_portes": ("Portes", "Doors", "ドア", "Puertas", "Portas", "Двери", "门"),
    "carte_spoiler": ("Spoiler", "Spoiler", "ネタバレ", "Spoiler", "Spoiler", "Спойлер", "剧透"),
    "carte_releve": ("Mode relevé", "Survey mode", "調査モード", "Modo registro", "Modo levantamento",
                     "Режим сбора данных", "记录模式"),
    "carte_avancement": ("Avancement des relevés", "Survey progress", "調査の進み具合", "Progreso del registro",
                         "Progresso do levantamento", "Прогресс сбора данных", "记录进度"),
    "langue": ("Langue", "Language", "言語", "Idioma", "Idioma", "Язык", "语言"),
    "langue_auto": ("Automatique", "Automatic", "自動", "Automático", "Automático", "Автоматически", "自动"),

    # ------------------------------------------------------------ carte Jeu
    "parcourir": ("Parcourir…", "Browse…", "参照…", "Examinar…", "Procurar…", "Обзор…", "浏览…"),
    "installer_dll": ("Installer la DLL", "Install the DLL", "DLLをインストール", "Instalar la DLL",
                      "Instalar a DLL", "Установить DLL", "安装 DLL"),
    "maj_dll": ("Mettre à jour la DLL", "Update the DLL", "DLLを更新", "Actualizar la DLL", "Atualizar a DLL",
                "Обновить DLL", "更新 DLL"),
    "desinstaller_dll": ("Désinstaller la DLL", "Uninstall the DLL", "DLLをアンインストール", "Desinstalar la DLL",
                         "Desinstalar a DLL", "Удалить DLL", "卸载 DLL"),
    "supprimer_seed": ("Supprimer la seed installée", "Remove the installed seed", "インストール済みのシードを削除",
                       "Eliminar la seed instalada", "Remover a seed instalada", "Удалить установленный сид",
                       "删除已安装的种子"),
    "note_desinstaller": ("Désinstaller la DLL suffit pour retrouver le jeu d'origine.",
                          "Uninstalling the DLL is enough to get the original game back.",
                          "DLLをアンインストールすれば元のゲームに戻ります。",
                          "Desinstalar la DLL basta para recuperar el juego original.",
                          "Desinstalar a DLL basta para voltar ao jogo original.",
                          "Чтобы вернуть исходную игру, достаточно удалить DLL.",
                          "卸载 DLL 即可恢复原版游戏。"),
    "badge_jeu_introuvable": ("●  Jeu introuvable : indique le dossier qui contient bhd.exe",
                              "●  Game not found: choose the folder that contains bhd.exe",
                              "●  ゲームが見つかりません：bhd.exe があるフォルダーを指定してください",
                              "●  Juego no encontrado: indica la carpeta que contiene bhd.exe",
                              "●  Jogo não encontrado: indique a pasta que contém bhd.exe",
                              "●  Игра не найдена: укажите папку с bhd.exe",
                              "●  未找到游戏：请选择包含 bhd.exe 的文件夹"),
    "badge_autre_dll": ("●  Un autre xinput1_4.dll est présent", "●  Another xinput1_4.dll is present",
                        "●  別の xinput1_4.dll があります", "●  Hay otro xinput1_4.dll",
                        "●  Há outro xinput1_4.dll", "●  Обнаружен другой xinput1_4.dll",
                        "●  存在另一个 xinput1_4.dll"),
    "badge_installe": ("●  Randomizer installé", "●  Randomizer installed", "●  ランダマイザー導入済み",
                       "●  Randomizer instalado", "●  Randomizer instalado", "●  Рандомайзер установлен",
                       "●  随机器已安装"),
    "badge_dll_ancienne": ("●  DLL à mettre à jour", "●  DLL needs updating", "●  DLLの更新が必要",
                           "●  Hay que actualizar la DLL", "●  A DLL precisa ser atualizada",
                           "●  DLL нужно обновить", "●  DLL 需要更新"),
    "maj_disponible": ("Mise à jour v{version}", "Update v{version}", "アップデート v{version}",
                       "Actualización v{version}", "Atualização v{version}", "Обновление v{version}",
                       "更新 v{version}"),
    "maj_confirmer": (
        "La version {version} est disponible (tu as la {actuelle}).\n\nLa télécharger et l'installer maintenant ? "
        "L'application redémarrera toute seule.",
        "Version {version} is available (you have {actuelle}).\n\nDownload and install it now? "
        "The app will restart by itself.",
        "バージョン {version} が利用できます（現在 {actuelle}）。\n\n今すぐダウンロードしてインストールしますか？"
        "アプリは自動的に再起動します。",
        "La versión {version} está disponible (tienes la {actuelle}).\n\n¿Descargarla e instalarla ahora? "
        "La aplicación se reiniciará sola.",
        "A versão {version} está disponível (você tem a {actuelle}).\n\nBaixar e instalar agora? "
        "O aplicativo reiniciará sozinho.",
        "Доступна версия {version} (у вас {actuelle}).\n\nСкачать и установить сейчас? "
        "Приложение перезапустится само.",
        "版本 {version} 已发布（当前为 {actuelle}）。\n\n现在下载并安装吗？应用将自动重启。"),
    "maj_telechargement": ("Téléchargement… {pct} %", "Downloading… {pct} %", "ダウンロード中… {pct} %",
                           "Descargando… {pct} %", "Baixando… {pct} %", "Загрузка… {pct} %", "下载中… {pct} %"),
    "maj_erreur": (
        "La mise à jour a échoué :\n{e}\n\nOuvrir la page de téléchargement ?",
        "The update failed:\n{e}\n\nOpen the download page?",
        "アップデートに失敗しました：\n{e}\n\nダウンロードページを開きますか？",
        "La actualización falló:\n{e}\n\n¿Abrir la página de descarga?",
        "A atualização falhou:\n{e}\n\nAbrir a página de download?",
        "Обновление не удалось:\n{e}\n\nОткрыть страницу загрузки?",
        "更新失败：\n{e}\n\n打开下载页面吗？"),
    "maj_page": (
        "La version {version} est disponible (tu as la {actuelle}).\n\nOuvrir la page de téléchargement ?",
        "Version {version} is available (you have {actuelle}).\n\nOpen the download page?",
        "バージョン {version} が利用できます（現在 {actuelle}）。\n\nダウンロードページを開きますか？",
        "La versión {version} está disponible (tienes la {actuelle}).\n\n¿Abrir la página de descarga?",
        "A versão {version} está disponível (você tem a {actuelle}).\n\nAbrir a página de download?",
        "Доступна версия {version} (у вас {actuelle}).\n\nОткрыть страницу загрузки?",
        "版本 {version} 已发布（当前为 {actuelle}）。\n\n打开下载页面吗？"),
    "badge_origine": ("●  Jeu d'origine (DLL non installée)", "●  Original game (DLL not installed)",
                      "●  元のゲーム（DLL未インストール）", "●  Juego original (DLL no instalada)",
                      "●  Jogo original (DLL não instalada)", "●  Исходная игра (DLL не установлена)",
                      "●  原版游戏（未安装 DLL）"),
    "badge_version": ("●  Version de bhd.exe non prise en charge : le randomizer restera inactif (jeu inchangé).",
                      "●  Unsupported bhd.exe version: the randomizer will stay inactive (game unchanged).",
                      "●  未対応の bhd.exe のバージョンです：ランダマイザーは動作しません（ゲームは変更されません）。",
                      "●  Versión de bhd.exe no compatible: el randomizer quedará inactivo (juego sin cambios).",
                      "●  Versão do bhd.exe não suportada: o randomizer ficará inativo (jogo inalterado).",
                      "●  Версия bhd.exe не поддерживается: рандомайзер будет неактивен (игра не изменится).",
                      "●  不支持此 bhd.exe 版本：随机器将保持停用（游戏不变）。"),
    "badge_seed": ("●  Seed {graine}{armes}", "●  Seed {graine}{armes}", "●  シード {graine}{armes}",
                   "●  Seed {graine}{armes}", "●  Seed {graine}{armes}", "●  Сид {graine}{armes}",
                   "●  种子 {graine}{armes}"),
    "badge_armes": (" · armes", " · weapons", " · 武器", " · armas", " · armas", " · оружие", " · 武器"),
    "badge_aucune_seed": ("●  Aucune seed installée", "●  No seed installed", "●  シード未インストール",
                          "●  Ninguna seed instalada", "●  Nenhuma seed instalada", "●  Сид не установлен",
                          "●  未安装种子"),

    "proton_titre": ("Steam Deck / Linux : option de lancement du jeu", "Steam Deck / Linux: game launch option",
                     "Steam Deck / Linux：ゲームの起動オプション", "Steam Deck / Linux: opción de lanzamiento del juego",
                     "Steam Deck / Linux: opção de inicialização do jogo",
                     "Steam Deck / Linux: параметр запуска игры", "Steam Deck / Linux：游戏启动选项"),
    "proton_note": ("Le jeu tourne sous Proton : colle cette option une fois dans Steam (Propriétés du jeu → "
                    "Options de lancement) pour que la DLL soit chargée.",
                    "The game runs under Proton: paste this option once in Steam (game Properties → Launch "
                    "Options) so the DLL is loaded.",
                    "ゲームは Proton で動作します：DLL を読み込ませるため、Steam（ゲームのプロパティ → 起動オプション）に"
                    "この設定を一度貼り付けてください。",
                    "El juego funciona con Proton: pega esta opción una vez en Steam (Propiedades del juego → "
                    "Opciones de lanzamiento) para que se cargue la DLL.",
                    "O jogo roda no Proton: cole esta opção uma vez no Steam (Propriedades do jogo → Opções de "
                    "inicialização) para que a DLL seja carregada.",
                    "Игра работает через Proton: один раз вставьте этот параметр в Steam (Свойства игры → "
                    "Параметры запуска), чтобы DLL загружалась.",
                    "游戏通过 Proton 运行：请将此选项粘贴到 Steam（游戏属性 → 启动选项）中一次，以便加载 DLL。"),
    "proton_dinput8": ("Ajouter dinput8.dll (pour BhdTool ou un autre mod qui l'utilise)",
                       "Also load dinput8.dll (for BhdTool or another mod that uses it)",
                       "dinput8.dll も読み込む（BhdTool など、これを使う MOD 用）",
                       "Cargar también dinput8.dll (para BhdTool u otro mod que lo use)",
                       "Carregar também dinput8.dll (para o BhdTool ou outro mod que o use)",
                       "Также загружать dinput8.dll (для BhdTool или другого мода, который её использует)",
                       "同时加载 dinput8.dll（用于 BhdTool 或其他使用它的模组）"),
    "proton_detecte": ("  · détecté dans le dossier du jeu", "  · found in the game folder", "  ・ゲームフォルダーで検出",
                       "  · detectado en la carpeta del juego", "  · detectado na pasta do jogo",
                       "  · найден в папке игры", "  · 已在游戏文件夹中检测到"),
    "copier": ("Copier", "Copy", "コピー", "Copiar", "Copiar", "Копировать", "复制"),
    "copie_ok": ("Option de lancement copiée : colle-la dans Steam, Propriétés du jeu → Options de lancement.",
                 "Launch option copied: paste it in Steam, game Properties → Launch Options.",
                 "起動オプションをコピーしました：Steam のゲームのプロパティ → 起動オプションに貼り付けてください。",
                 "Opción de lanzamiento copiada: pégala en Steam, Propiedades del juego → Opciones de lanzamiento.",
                 "Opção de inicialização copiada: cole-a no Steam, Propriedades do jogo → Opções de inicialização.",
                 "Параметр запуска скопирован: вставьте его в Steam, Свойства игры → Параметры запуска.",
                 "已复制启动选项：请粘贴到 Steam 的 游戏属性 → 启动选项 中。"),

    # ------------------------------------------------------------ carte Partie
    "personnage": ("Personnage", "Character", "キャラクター", "Personaje", "Personagem", "Персонаж", "角色"),
    "difficulte": ("Difficulté", "Difficulty", "難易度", "Dificultad", "Dificuldade", "Сложность", "难度"),
    "a_venir": ("à venir", "coming soon", "近日対応", "próximamente", "em breve", "скоро", "即将推出"),
    "diff_Très facile": ("Débutant", "Very Easy", "ベリーイージー", "Muy fácil", "Muito fácil", "Очень легко",
                         "非常简单"),
    "diff_Facile": ("Facile", "Easy", "イージー", "Fácil", "Fácil", "Легко", "简单"),
    "diff_Normal": ("Normal", "Normal", "ノーマル", "Normal", "Normal", "Нормально", "普通"),
    "diff_Difficile": ("Expert", "Hard", "ハード", "Difícil", "Difícil", "Сложно", "困难"),
    "diff_Real Survival": ("Real Survival", "Real Survival", "リアルサバイバル", "Real Survival", "Real Survival",
                           "Real Survival", "Real Survival"),

    # ------------------------------------------------------------ carte Options
    "armes_aleatoires": ("Armes aléatoires", "Random weapons", "武器もランダム", "Armas aleatorias",
                         "Armas aleatórias", "Случайное оружие", "随机武器"),
    "note_armes": (
        "Les armes de base du jeu sont mélangées avec les objets. Décoche celles qui doivent rester à leur place.",
        "The game's standard weapons are shuffled with the items. Untick those that should stay in place.",
        "ゲームの基本武器もアイテムと一緒にシャッフルされます。元の場所に残したい武器はチェックを外してください。",
        "Las armas básicas del juego se mezclan con los objetos. Desmarca las que deban quedarse en su sitio.",
        "As armas básicas do jogo são embaralhadas com os itens. Desmarque as que devem ficar no lugar.",
        "Обычное оружие игры перемешивается с предметами. Снимите отметку с того, что должно остаться на месте.",
        "游戏的基础武器会与物品一起打乱。取消勾选要留在原位的武器。"),
    "arme_pistolet": ('Pistolet', 'Handgun', 'ハンドガン', 'Pistola', 'Pistola', 'Пистолет', '手枪'),
    "arme_fusil_pompe": ('Fusil à pompe', 'Shotgun', 'ショットガン', 'Escopeta', 'Espingarda', 'Дробовик', '霰弹枪'),
    "arme_fusil_assaut": ("Fusil d'assaut", 'Assault shotgun', 'アサルトショットガン', 'Escopeta de asalto', 'Espingarda de assalto', 'Штурмовой дробовик', '突击霰弹枪'),
    "arme_lance_grenades": ('Lance-grenades', 'Grenade launcher', 'グレネードランチャー', 'Lanzagranadas', 'Lança-granadas', 'Гранатомёт', '榴弹发射器'),
    "arme_lance_flammes": ('Lance-flammes', 'Flamethrower', '火炎放射器', 'Lanzallamas', 'Lança-chamas', 'Огнемёт', '火焰喷射器'),
    "arme_autodefense": ("Pistolet d'autodéfense", 'Self-defense gun', '護身用ハンドガン', 'Pistola de autodefensa', 'Pistola de autodefesa', 'Пистолет самообороны', '自卫手枪'),
    "arme_lance_roquettes": ('Lance-roquettes (fin du jeu)', 'Rocket launcher (end of game)', 'ロケットランチャー（終盤）', 'Lanzacohetes (final del juego)', 'Lança-foguetes (fim do jogo)', 'Ракетница (конец игры)', '火箭筒（游戏结尾）'),
    "arme_magnum": ("Magnum", "Magnum", "マグナム", "Magnum", "Magnum", "Магнум", "麦格农"),
    "chris_uniquement": ('Chris uniquement', 'Chris only', 'クリスのみ', 'solo Chris', 'só Chris', 'только Крис', '仅克里斯'),
    "jill_uniquement": ('Jill uniquement', 'Jill only', 'ジルのみ', 'solo Jill', 'só Jill', 'только Джилл', '仅吉尔'),
    "cles_aleatoires": ("Clés aléatoires", "Random keys", "鍵もランダム", "Llaves aleatorias", "Chaves aleatórias",
                        "Случайные ключи", "随机钥匙"),
    "ennemis_aleatoires": ("Ennemis aléatoires", "Random enemies", "敵もランダム", "Enemigos aleatorios",
                           "Inimigos aleatórios", "Случайные враги", "随机敌人"),
    "partie_nouvelle": ("Nouvelle partie", "New game", "ニューゲーム", "Partida nueva", "Novo jogo", "Новая игра",
                        "新游戏"),
    "note_partie_nouvelle": ("Réponse à « Quel est votre style de jeu ? »",
                             "Answer to “What is your play style?”", "「プレイスタイル」の質問への答え",
                             "Respuesta a la pregunta sobre tu estilo de juego",
                             "Resposta à pergunta sobre o seu estilo de jogo", "Ответ на вопрос о стиле игры",
                             "对“游戏风格”问题的回答"),
    "partie_ufp": ("Une fois de plus", "Once Again", "2周目", "Nueva partida+", "Novo jogo+", "Новая игра+", "二周目"),
    "note_partie_ufp": ("Jeu déjà terminé : on choisit la difficulté par son nom. Les armes infinies débloquées ne sont pas données (voir Armes bonus).",
                        "Game already finished: you pick the difficulty by name. Unlocked infinite weapons are not given (see Bonus weapons).",
                        "クリア後：難易度を名前で選びます。解放済みの無限武器は支給されません（ボーナス武器を参照）。", "Juego ya terminado: eliges la dificultad por su nombre. Las armas infinitas desbloqueadas no se dan (ver Armas extra).",
                        "Jogo já zerado: você escolhe a dificuldade pelo nome. As armas infinitas desbloqueadas não são dadas (veja Armas bônus).",
                        "Игра уже пройдена: сложность выбирается по названию. Открытое бесконечное оружие не выдаётся (см. Бонусное оружие).", "已通关：按名称选择难度。已解锁的无限武器不会给予（见奖励武器）。"),
    "note_cle_placard_ufp": ("En « Une fois de plus », le jeu met déjà la clé du placard dans la malle.",
                             "In “Once Again”, the game already puts the Closet Key in the item box.",
                             "2周目では、ゲームがもともとクローゼットのカギをアイテムボックスに入れます。",
                             "En Nueva partida+, el juego ya pone la llave del armario en el baúl.",
                             "No Novo jogo+, o jogo já coloca a chave do armário no baú.",
                             "В новой игре+ игра уже кладёт ключ от кладовой в сундук.",
                             "二周目时，游戏本来就会把衣柜钥匙放进道具箱。"),
    "cle_placard": ("Clé du placard dès le départ", "Closet Key from the start", "最初からクローゼットのカギ",
                    "Llave del armario desde el inicio", "Chave do armário desde o início",
                    "Ключ от кладовой с самого начала", "开局即有衣柜钥匙"),
    "note_cle_placard": (
        "La clé de la salle des costumes est dans la malle dès le début, comme quand on a déjà fini le jeu. "
        "Nouvelle partie seulement (en « Une fois de plus », le jeu la donne déjà).",
        "The key to the costume room is in the item box from the start, as when you have already finished the game. "
        "New game only (in “Once Again”, the game already gives it).",
        "衣装部屋のカギが、クリア後と同じように最初からアイテムボックスに入っています。ニューゲームのみ"
        "（クリアデータからのゲームでは、もともと入っています）。",
        "La llave de la sala de trajes está en el baúl desde el principio, como cuando ya has terminado el juego. "
        "Solo en partida nueva (desde una partida terminada, el juego ya la da).",
        "A chave da sala de roupas está no baú desde o início, como quando você já zerou o jogo. "
        "Só em um novo jogo (a partir de um save zerado, o jogo já a dá).",
        "Ключ от комнаты с костюмами лежит в сундуке с самого начала, как после прохождения игры. "
        "Только для новой игры (при игре с сохранения пройденной игры он уже есть).",
        "服装间的钥匙从一开始就在道具箱里，就像已经通关时一样。仅限新游戏（从通关存档开始时，游戏本来就会给）。"),
    "portes_aleatoires": ("Portes aléatoires", "Random doors", "ドアもランダム", "Puertas aleatorias",
                          "Portas aleatórias", "Случайные двери", "随机门"),
    "note_portes": (
        "Chaque porte mène vers une autre pièce que d'habitude : le manoir devient un vrai labyrinthe.",
        "Each door leads to a different room than usual: the mansion becomes a real maze.",
        "それぞれのドアがいつもとは違う部屋につながり、洋館が本物の迷路になります。",
        "Cada puerta lleva a una sala distinta de la habitual: la mansión se convierte en un verdadero laberinto.",
        "Cada porta leva a uma sala diferente da habitual: a mansão vira um verdadeiro labirinto.",
        "Каждая дверь ведёт не в ту комнату, что обычно: особняк превращается в настоящий лабиринт.",
        "每扇门都会通往与平常不同的房间：洋馆变成真正的迷宫。"),
    "armes_bonus": ("Armes bonus", "Bonus weapons", "ボーナス武器", "Armas extra", "Armas bônus",
                    "Бонусное оружие", "奖励武器"),
    "note_armes_bonus": (
        "Samurai Edge et lance-roquettes à munitions illimitées : normalement débloqués en finissant le jeu "
        "en Normal ou Difficile, en moins de 5 h et en moins de 3 h.",
        "Samurai Edge and rocket launcher with unlimited ammo: normally unlocked by finishing the game "
        "on Normal or Hard in under 5 h and under 3 h.",
        "無限弾のサムライエッジとロケットランチャー：通常はノーマルかハードを5時間以内・3時間以内に"
        "クリアすると手に入ります。",
        "Samurai Edge y lanzacohetes con munición ilimitada: normalmente se desbloquean al terminar el juego "
        "en Normal o Difícil en menos de 5 h y de 3 h.",
        "Samurai Edge e lança-foguetes com munição ilimitada: normalmente liberados ao terminar o jogo "
        "no Normal ou Difícil em menos de 5 h e de 3 h.",
        "Samurai Edge и ракетница с бесконечными патронами: обычно открываются за прохождение на «Нормально» "
        "или «Сложно» быстрее 5 ч и 3 ч.",
        "无限弹药的武士之刃与火箭筒：通常需以普通或困难难度分别在 5 小时、3 小时内通关解锁。"),
    "aucune_arme": ("Aucune arme cochée : les armes restent à leur place.",
                    "No weapon ticked: weapons stay in place.", "武器が選ばれていません：武器は元の場所のままです。",
                    "Ningún arma marcada: las armas se quedan en su sitio.",
                    "Nenhuma arma marcada: as armas ficam no lugar.",
                    "Оружие не выбрано: оно останется на своих местах.", "未勾选任何武器：武器保持原位。"),
    "malle_aleatoire": ("Malle de départ aléatoire", "Random starting item box", "スタート時のアイテムボックスをランダム化",
                        "Baúl inicial aleatorio", "Baú inicial aleatório", "Случайный стартовый сундук",
                        "随机初始道具箱"),
    "note_malle_aleatoire": (
        "Les objets de la malle au début de la partie sont mélangés avec les autres. Seulement pour une nouvelle partie.",
        "The items in the item box at the start are shuffled with the others. New game only.",
        "ゲーム開始時のアイテムボックスの中身を他のアイテムと混ぜます。ニューゲームのみ。",
        "Los objetos del baúl al empezar se mezclan con los demás. Solo en partida nueva.",
        "Os itens do baú no início são misturados com os outros. Só em um novo jogo.",
        "Предметы в сундуке в начале игры перемешиваются с остальными. Только для новой игры.",
        "开局时道具箱中的物品会与其他物品混合。仅限新游戏。"),
    "malle_depart": ("Malle de départ", "Starting item box", "スタート時のアイテムボックス", "Baúl inicial",
                     "Baú inicial", "Стартовый сундук", "初始道具箱"),
    "malle_case": ("case {n}", "slot {n}", "{n}番目", "casilla {n}", "espaço {n}", "ячейка {n}", "第 {n} 格"),
    "objets_visibles": ("Objets visibles par terre", "Items visible on the ground", "床の上でも見える",
                        "Objetos visibles en el suelo", "Itens visíveis no chão", "Предметы видны на полу",
                        "地上可见物品"),
    "note_objets_visibles": (
        "Le nouvel objet apparaît directement dans le décor et dans l'aperçu avant ramassage. "
        "Décoché : on voit l'objet d'origine jusqu'au ramassage.",
        "The new item shows up directly in the room and in the preview before pickup. "
        "Unticked: you see the original item until you pick it up.",
        "新しいアイテムが部屋の中と拾う前のプレビューにそのまま表示されます。"
        "オフ：拾うまで元のアイテムが表示されます。",
        "El nuevo objeto aparece directamente en la sala y en la vista previa antes de recogerlo. "
        "Desmarcado: se ve el objeto original hasta recogerlo.",
        "O novo item aparece direto no cenário e na prévia antes de pegar. "
        "Desmarcado: vê-se o item original até pegá-lo.",
        "Новый предмет сразу виден в комнате и в предпросмотре перед подбором. "
        "Без отметки: до подбора виден исходный предмет.",
        "新物品会直接出现在场景和拾取前的预览中。不勾选：拾取前看到的是原物品。"),
    "onglet_archipelago": ("Archipelago", "Archipelago", "Archipelago", "Archipelago", "Archipelago",
                           "Archipelago", "Archipelago"),
    "carte_archipelago": ("Archipelago  ·  à venir", "Archipelago  ·  coming soon", "Archipelago  ·  近日対応",
                          "Archipelago  ·  próximamente", "Archipelago  ·  em breve", "Archipelago  ·  скоро",
                          "Archipelago  ·  即将推出"),
    "ap_intro": (
        "Archipelago est un randomizer multi-jeux : les objets de ta partie peuvent se retrouver dans le jeu "
        "d'autres joueurs (et inversement), chacun sur son propre jeu, en même temps. Le support de Resident Evil "
        "HD Remaster est en préparation : cet onglet servira à se connecter à une partie Archipelago.",
        "Archipelago is a multi-game randomizer: the items of your game can end up in other players' games (and "
        "the other way round), each on their own game, at the same time. Support for Resident Evil HD Remaster is "
        "being prepared: this tab will be used to connect to an Archipelago game.",
        "Archipelago は複数のゲームをまたぐランダマイザーです。あなたのゲームのアイテムが他のプレイヤーのゲームに"
        "（その逆も）置かれ、各自が自分のゲームを同時に遊びます。Resident Evil HD Remaster への対応は準備中で、"
        "このタブから Archipelago のゲームに接続できるようになります。",
        "Archipelago es un randomizer multijuego: los objetos de tu partida pueden acabar en los juegos de otros "
        "jugadores (y al revés), cada uno en su propio juego, a la vez. El soporte de Resident Evil HD Remaster "
        "está en preparación: esta pestaña servirá para conectarse a una partida de Archipelago.",
        "Archipelago é um randomizer multijogos: os itens do seu jogo podem ir parar nos jogos de outros jogadores "
        "(e vice-versa), cada um no próprio jogo, ao mesmo tempo. O suporte a Resident Evil HD Remaster está em "
        "preparação: esta aba servirá para se conectar a uma partida do Archipelago.",
        "Archipelago — это рандомайзер для нескольких игр: предметы из вашей игры могут оказаться в играх других "
        "игроков (и наоборот), каждый играет в свою игру одновременно. Поддержка Resident Evil HD Remaster "
        "готовится: эта вкладка будет нужна для подключения к игре Archipelago.",
        "Archipelago 是一个跨游戏的随机器：你游戏中的物品可能出现在其他玩家的游戏里（反之亦然），大家同时玩各自的游戏。"
        "Resident Evil HD Remaster 的支持正在准备中：此标签页将用于连接 Archipelago 游戏。"),
    "ap_site": ("Site d'Archipelago", "Archipelago website", "Archipelago のサイト", "Sitio de Archipelago",
                "Site do Archipelago", "Сайт Archipelago", "Archipelago 网站"),
    "carte_ap_connexion": ("Connexion", "Connection", "接続", "Conexión", "Conexão", "Подключение", "连接"),
    "ap_serveur": ("Serveur (adresse:port)", "Server (address:port)", "サーバー（アドレス:ポート）",
                   "Servidor (dirección:puerto)", "Servidor (endereço:porta)", "Сервер (адрес:порт)",
                   "服务器（地址:端口）"),
    "ap_joueur": ("Nom du joueur (slot)", "Player name (slot)", "プレイヤー名（スロット）", "Nombre del jugador (slot)",
                  "Nome do jogador (slot)", "Имя игрока (слот)", "玩家名称（槽位）"),
    "ap_mot_de_passe": ("Mot de passe (si la partie en a un)", "Password (if the game has one)",
                        "パスワード（設定されている場合）", "Contraseña (si la partida tiene una)",
                        "Senha (se a partida tiver uma)", "Пароль (если он задан)", "密码（如有）"),
    "ap_connecter": ("Se connecter", "Connect", "接続", "Conectar", "Conectar", "Подключиться", "连接"),
    "ap_etat": ("Non connecté  ·  pas encore disponible", "Not connected  ·  not available yet",
                "未接続  ·  まだ利用できません", "No conectado  ·  aún no disponible", "Não conectado  ·  ainda indisponível",
                "Не подключено  ·  пока недоступно", "未连接  ·  暂不可用"),
    "ap_deathlink": ("DeathLink (quand un joueur meurt, tout le monde meurt)",
                     "DeathLink (when one player dies, everyone dies)",
                     "DeathLink（誰かが死ぬと全員が死ぬ）", "DeathLink (si un jugador muere, mueren todos)",
                     "DeathLink (quando um jogador morre, todos morrem)", "DeathLink (смерть одного — смерть всех)",
                     "DeathLink（一人死亡，全员死亡）"),
    "carte_ap_avancement": ("Ce qu'il reste à faire", "What's left to do", "残りの作業", "Lo que falta por hacer",
                            "O que falta fazer", "Что осталось сделать", "剩余工作"),
    "ap_fait": ("fait", "done", "完了", "hecho", "feito", "готово", "已完成"),
    "ap_en_cours": ("en cours", "in progress", "進行中", "en curso", "em andamento", "в работе", "进行中"),
    "ap_a_faire": ("à faire", "to do", "未着手", "por hacer", "a fazer", "сделать", "待完成"),
    "ap_etape_releves": ("Relevé de tous les emplacements d'objets (Chris / Facile en cours)",
                         "Survey of every item location (Chris / Easy in progress)",
                         "全アイテム配置の調査（クリス／イージーを調査中）",
                         "Registro de todos los lugares de objetos (Chris / Fácil en curso)",
                         "Levantamento de todos os locais de itens (Chris / Fácil em andamento)",
                         "Сбор всех мест предметов (Крис / Лёгкая — в работе)",
                         "记录所有物品位置（克里斯／简单 进行中）"),
    "ap_etape_cles": ("Clés et objets de quête avec la logique (pour que la partie reste finissable)",
                      "Keys and quest items with logic (so the game stays beatable)",
                      "ロジック付きの鍵・クエストアイテム（クリア可能を保証）",
                      "Llaves y objetos de misión con lógica (para que la partida se pueda terminar)",
                      "Chaves e itens de missão com lógica (para o jogo continuar zerável)",
                      "Ключи и квестовые предметы с логикой (чтобы игру можно было пройти)",
                      "带逻辑的钥匙与任务物品（保证可通关）"),
    "ap_etape_envoyer": ("Signaler au serveur chaque emplacement ramassé", "Report every picked-up location to the server",
                         "拾った配置をサーバーに送信", "Avisar al servidor de cada lugar recogido",
                         "Avisar o servidor de cada local coletado", "Сообщать серверу о каждом подобранном месте",
                         "向服务器报告每个已拾取的位置"),
    "ap_etape_recevoir": ("Recevoir dans l'inventaire les objets envoyés par les autres joueurs",
                          "Receive the items sent by other players into the inventory",
                          "他のプレイヤーから届いたアイテムをインベントリに受け取る",
                          "Recibir en el inventario los objetos enviados por otros jugadores",
                          "Receber no inventário os itens enviados por outros jogadores",
                          "Получать в инвентарь предметы от других игроков",
                          "把其他玩家发来的物品收进物品栏"),
    "ap_etape_monde": ("Le « monde » Archipelago du jeu (fichier .apworld : objets, emplacements, règles)",
                       "The game's Archipelago \"world\" (.apworld file: items, locations, rules)",
                       "ゲームの Archipelago「ワールド」（.apworld ファイル：アイテム・配置・ルール）",
                       "El «mundo» de Archipelago del juego (archivo .apworld: objetos, lugares, reglas)",
                       "O \"mundo\" do Archipelago do jogo (arquivo .apworld: itens, locais, regras)",
                       "«Мир» Archipelago для игры (файл .apworld: предметы, места, правила)",
                       "游戏的 Archipelago「世界」（.apworld 文件：物品、位置、规则）"),
    "ap_etape_objectif": ("Objectif de la partie (fin du jeu) envoyé au serveur",
                          "Game goal (ending) sent to the server", "ゲームの目標（エンディング）をサーバーに送信",
                          "Objetivo de la partida (final del juego) enviado al servidor",
                          "Objetivo da partida (final do jogo) enviado ao servidor",
                          "Цель игры (концовка) отправляется на сервер", "将游戏目标（通关）发送到服务器"),
    "onglet_info": ('Info', 'Info', '情報', 'Info', 'Info', 'Инфо', '信息'),
    "carte_projet": ('Projet', 'Project', 'プロジェクト', 'Proyecto', 'Projeto', 'Проект', '项目'),
    "carte_auteur": ('Auteur', 'Author', '作者', 'Autor', 'Autor', 'Автор', '作者'),
    "carte_tests": ('Tests et relevés des objets', 'Testing and item surveys', 'テストとアイテム調査', 'Pruebas y registro de objetos', 'Testes e levantamento de itens', 'Тестирование и сбор данных о предметах', '测试与物品记录'),
    "carte_remerciements": ('Remerciements', 'Thanks', '謝辞', 'Agradecimientos', 'Agradecimentos', 'Благодарности', '致谢'),
    "info_description": ('Mélange les objets du manoir à chaque partie.', "Shuffles the mansion's items for every playthrough.", 'プレイごとに洋館のアイテムをシャッフルします。', 'Mezcla los objetos de la mansión en cada partida.', 'Embaralha os itens da mansão a cada partida.', 'Перемешивает предметы особняка в каждой игре.', '每局打乱洋馆中的物品。'),
    "lien_projet": ('Page du projet sur GitHub', 'Project page on GitHub', 'GitHub のプロジェクトページ', 'Página del proyecto en GitHub', 'Página do projeto no GitHub', 'Страница проекта на GitHub', 'GitHub 项目主页'),
    "lien_profil": ('Profil GitHub', 'GitHub profile', 'GitHub プロフィール', 'Perfil de GitHub', 'Perfil no GitHub', 'Профиль на GitHub', 'GitHub 个人主页'),
    "info_licence": ('Licence GPLv3 : code source libre.', 'GPLv3 licence: free and open source.', 'GPLv3 ライセンス：オープンソース。', 'Licencia GPLv3: código abierto.', 'Licença GPLv3: código aberto.', 'Лицензия GPLv3: открытый исходный код.', 'GPLv3 许可证：开源。'),
    "info_fan": ('Projet de fan, non officiel, sans lien avec Capcom. Resident Evil est une marque de Capcom.', 'Unofficial fan project, not affiliated with Capcom. Resident Evil is a trademark of Capcom.', '非公式のファンプロジェクトであり、カプコンとは無関係です。バイオハザードはカプコンの商標です。', 'Proyecto de fans no oficial, sin relación con Capcom. Resident Evil es una marca de Capcom.', 'Projeto de fã não oficial, sem ligação com a Capcom. Resident Evil é uma marca da Capcom.', 'Неофициальный фанатский проект, не связанный с Capcom. Resident Evil — торговая марка Capcom.', '非官方粉丝项目，与 Capcom 无关。Resident Evil 是 Capcom 的商标。'),
    "info_bhdtool": ('BhdTool (eleval) : noms et liaisons des pièces, et aide précieuse pour les relevés.', 'BhdTool (eleval): room names and connections, and a great help for surveys.', 'BhdTool（eleval）：部屋の名前とつながり、調査にも大いに役立ちました。', 'BhdTool (eleval): nombres y conexiones de las salas, y gran ayuda para los registros.', 'BhdTool (eleval): nomes e ligações das salas, e grande ajuda nos levantamentos.', 'BhdTool (eleval): названия и связи комнат, большая помощь при сборе данных.', 'BhdTool（eleval）：房间名称与连接，并为物品记录提供了很大帮助。'),
    "info_inspiration": ("Inspiré des randomizers de la communauté : BioRand et l'ancien randomizer de Benn Powell.", "Inspired by community randomizers: BioRand and Benn Powell's earlier randomizer.", 'コミュニティのランダマイザー（BioRand、Benn Powell 氏の旧ランダマイザー）に着想を得ています。', 'Inspirado en randomizers de la comunidad: BioRand y el antiguo randomizer de Benn Powell.', 'Inspirado nos randomizers da comunidade: BioRand e o antigo randomizer de Benn Powell.', 'Вдохновлено рандомайзерами сообщества: BioRand и прежним рандомайзером Benn Powell.', '灵感来自社区随机器：BioRand 以及 Benn Powell 早期的随机器。'),
    "quitter": ("Quitter", "Quit", "終了", "Salir", "Sair", "Выход", "退出"),
    "sans_logique": ("Sans logique", "No logic", "ロジックなし", "Sin lógica", "Sem lógica", "Без логики", "无逻辑"),
    "note_sans_logique": (
        "Les clés peuvent tomber n'importe où : la partie risque d'être impossible à finir.",
        "Keys can end up anywhere: the run may be impossible to finish.",
        "鍵がどこにでも置かれるため、クリアできなくなる可能性があります。",
        "Las llaves pueden acabar en cualquier sitio: la partida podría no poder terminarse.",
        "As chaves podem ir para qualquer lugar: a partida pode ficar impossível de terminar.",
        "Ключи могут оказаться где угодно: игру, возможно, не удастся пройти.",
        "钥匙可能出现在任何地方：本局可能无法通关。"),
    "arme_depart": ("Arme garantie au départ", "Guaranteed starting weapon", "序盤に武器を確保",
                    "Arma garantizada al inicio", "Arma garantida no início", "Оружие в начале игры",
                    "开局保证有武器"),
    "note_arme_depart": (
        "Une des armes mélangées est donnée dans l'inventaire au début de la partie, avec ses munitions de base. "
        "Son emplacement reçoit un objet au hasard à la place. Nouvelle partie seulement.",
        "One of the shuffled weapons is given in the inventory at the start, with its basic ammo. Its location "
        "gets a random item instead. New game only.",
        "シャッフルされた武器の1つが、基本の弾薬とともにゲーム開始時にインベントリに入ります。その場所には代わりに"
        "ランダムなアイテムが置かれます。ニューゲームのみ。",
        "Una de las armas mezcladas se da en el inventario al empezar, con su munición básica. Su ubicación recibe "
        "un objeto al azar en su lugar. Solo en partida nueva.",
        "Uma das armas embaralhadas é dada no inventário no início, com sua munição básica. O local dela recebe "
        "um item aleatório no lugar. Só em um novo jogo.",
        "Одно из перемешанных орудий выдаётся в инвентарь в начале игры, с базовыми патронами. На его месте будет "
        "случайный предмет. Только для новой игры.",
        "被打乱的武器之一会在开局时连同基础弹药放入物品栏，其原位置改为放置一个随机物品。仅限新游戏。"),
    "couteau_aleatoire": ("Couteau de départ aléatoire", "Random starting knife", "初期装備のナイフをランダム化",
                          "Cuchillo inicial aleatorio", "Faca inicial aleatória", "Случайный стартовый нож",
                          "随机初始小刀"),
    "note_difficulte": (
        "Les seeds sont faites pour la difficulté Facile (la seule relevée pour l'instant) : choisis la même dans le "
        "jeu, sinon la seed ne s'applique pas.",
        "Seeds are made for the Easy difficulty (the only one surveyed so far): pick the same one in the game, "
        "otherwise the seed is not applied.",
        "シードは難易度イージー用です（現在調査済みはこれだけです）。ゲームでも同じ難易度を選んでください。"
        "違う場合、シードは適用されません。",
        "Las semillas están hechas para la dificultad Fácil (la única registrada por ahora): elige la misma en el "
        "juego; si no, la semilla no se aplica.",
        "As seeds são feitas para a dificuldade Fácil (a única levantada por enquanto): escolha a mesma no jogo; "
        "senão, a seed não é aplicada.",
        "Сиды сделаны для сложности «Легко» (пока собрана только она): выберите её же в игре, иначе сид не "
        "применяется.",
        "种子是为“简单”难度制作的（目前只记录了这一难度）：请在游戏中选择相同难度，否则种子不会生效。"),
    "note_couteau_aleatoire": (
        "Le couteau du début est remplacé par un objet au hasard et se retrouve ailleurs. Sans « Arme garantie au "
        "départ », tu risques de commencer la partie sans aucune arme ! Nouvelle partie seulement.",
        "The starting knife is replaced by a random item and ends up somewhere else. Without “Guaranteed starting "
        "weapon”, you may start the game with no weapon at all! New game only.",
        "最初のナイフがランダムなアイテムに置き換わり、別の場所に移ります。「序盤に武器を確保」なしでは、武器なしで"
        "始まることがあります！ニューゲームのみ。",
        "El cuchillo inicial se sustituye por un objeto al azar y acaba en otro sitio. Sin «Arma garantizada al "
        "inicio», ¡puedes empezar sin ninguna arma! Solo en partida nueva.",
        "A faca inicial é substituída por um item aleatório e vai parar em outro lugar. Sem “Arma garantida no "
        "início”, você pode começar sem nenhuma arma! Só em um novo jogo.",
        "Стартовый нож заменяется случайным предметом и оказывается в другом месте. Без «Гарантированного оружия» "
        "можно начать игру вообще без оружия! Только для новой игры.",
        "开局的小刀会被随机物品替换并出现在别处。如果不勾选“开局保证有武器”，可能会在没有任何武器的情况下开始游戏！"
        "仅限新游戏。"),
    "inventaire_depart": ("Inventaire de départ", "Starting inventory", "初期インベントリ", "Inventario inicial",
                          "Inventário inicial", "Стартовый инвентарь", "初始物品栏"),
    "gen_arme_depart": ("Arme donnée au départ : {arme}", "Weapon given at the start: {arme}",
                        "開始時に渡される武器：{arme}", "Arma dada al inicio: {arme}", "Arma dada no início: {arme}",
                        "Оружие в начале игры: {arme}", "开局获得的武器：{arme}"),
    "graine": ("Graine", "Seed", "シード", "Semilla", "Semente", "Сид", "种子"),
    "au_hasard": ("Au hasard", "Random", "ランダム", "Al azar", "Aleatória", "Случайно", "随机"),
    "note_graine": ("Même graine + mêmes options = même résultat.", "Same seed + same options = same result.",
                    "同じシード＋同じオプション＝同じ結果。", "Misma semilla + mismas opciones = mismo resultado.",
                    "Mesma semente + mesmas opções = mesmo resultado.",
                    "Тот же сид + те же параметры = тот же результат.", "相同种子 + 相同选项 = 相同结果。"),

    # ------------------------------------------------------------ actions et journal
    "generer": ("Générer la seed", "Generate seed", "シードを生成", "Generar la seed", "Gerar a seed",
                "Создать сид", "生成种子"),
    "installer_seed_case": ("Installer la seed dans le jeu", "Install the seed in the game",
                            "シードをゲームにインストール", "Instalar la seed en el juego", "Instalar a seed no jogo",
                            "Установить сид в игру", "将种子安装到游戏"),
    "dossier_seeds": ("Dossier des seeds", "Seeds folder", "シードのフォルダー", "Carpeta de seeds",
                      "Pasta das seeds", "Папка сидов", "种子文件夹"),
    "pret": ("Prêt. Choisis tes options puis « Générer la seed ».",
             "Ready. Choose your options, then click “Generate seed”.",
             "準備完了。オプションを選んで「シードを生成」を押してください。",
             "Listo. Elige tus opciones y pulsa «Generar la seed».",
             "Pronto. Escolha as opções e clique em “Gerar a seed”.",
             "Готово. Выберите параметры и нажмите «Создать сид».",
             "就绪。选择选项后点击“生成种子”。"),
    "donnees_absentes": ("Fichier de données {fichier} introuvable : génération impossible.",
                         "Data file {fichier} not found: cannot generate.",
                         "データファイル {fichier} が見つかりません：生成できません。",
                         "No se encuentra el archivo de datos {fichier}: no se puede generar.",
                         "Arquivo de dados {fichier} não encontrado: impossível gerar.",
                         "Файл данных {fichier} не найден: создание невозможно.",
                         "找不到数据文件 {fichier}：无法生成。"),
    "generation": ("Génération…", "Generating…", "生成中…", "Generando…", "Gerando…", "Создание…", "生成中…"),
    "erreur": ("ERREUR : {e}", "ERROR: {e}", "エラー：{e}", "ERROR: {e}", "ERRO: {e}", "ОШИБКА: {e}", "错误：{e}"),
    "echec_generation": ("La génération ou l'installation a échoué.", "Generation or installation failed.",
                         "生成またはインストールに失敗しました。", "La generación o la instalación ha fallado.",
                         "A geração ou a instalação falhou.", "Не удалось создать или установить сид.",
                         "生成或安装失败。"),
    "renvoi_spoiler": ("(liste complète des changements : onglet « Spoiler »)",
                       "(full list of changes: “Spoiler” tab)", "（変更の全一覧：「ネタバレ」タブ）",
                       "(lista completa de cambios: pestaña «Spoiler»)",
                       "(lista completa das mudanças: aba “Spoiler”)",
                       "(полный список изменений: вкладка «Спойлер»)", "（完整更改列表：“剧透”标签页）"),

    # ------------------------------------------------------------ onglet Spoiler
    "afficher_spoiler": ("Afficher le spoiler", "Show spoiler", "ネタバレを表示", "Mostrar el spoiler",
                         "Mostrar o spoiler", "Показать спойлер", "显示剧透"),
    "spoiler_aucun": ("Aucune seed générée ou installée pour l'instant.", "No seed generated or installed yet.",
                      "まだシードが生成・インストールされていません。", "Todavía no hay ninguna seed generada o instalada.",
                      "Nenhuma seed gerada ou instalada ainda.", "Пока нет созданного или установленного сида.",
                      "尚未生成或安装种子。"),
    "spoiler_genere": ("Dernière seed générée", "Last generated seed", "最後に生成したシード",
                       "Última seed generada", "Última seed gerada", "Последний созданный сид", "最近生成的种子"),
    "spoiler_installe": ("Seed installée dans le jeu", "Seed installed in the game", "ゲームにインストール済みのシード",
                         "Seed instalada en el juego", "Seed instalada no jogo", "Сид, установленный в игру",
                         "已安装到游戏的种子"),
    "spoiler_masque": ("{titre} : spoiler masqué. Coche la case pour voir quel objet remplace quoi.",
                       "{titre}: spoiler hidden. Tick the box to see which item replaces which.",
                       "{titre}：ネタバレは非表示です。チェックを入れるとどのアイテムが何に置き換わったか表示されます。",
                       "{titre}: spoiler oculto. Marca la casilla para ver qué objeto sustituye a cuál.",
                       "{titre}: spoiler oculto. Marque a caixa para ver qual item substitui qual.",
                       "{titre}: спойлер скрыт. Отметьте флажок, чтобы увидеть, какой предмет чем заменён.",
                       "{titre}：剧透已隐藏。勾选即可查看哪件物品替换了哪件。"),

    # ------------------------------------------------------------ onglet Aider le projet
    "releve_intro": ("Le randomizer ne mélange que les objets déjà relevés. Tu peux aider à compléter la liste en "
                     "jouant : la DLL note les objets de chaque pièce visitée, sans rien changer à ta partie.",
                     "The randomizer only shuffles items that have already been surveyed. You can help complete "
                     "the list by playing: the DLL records the items of every room you visit, without changing "
                     "your game.",
                     "ランダマイザーは調査済みのアイテムだけをシャッフルします。プレイするだけでリスト作りに協力できます："
                     "DLL が訪れた部屋のアイテムを記録します（ゲームには何も影響しません）。",
                     "El randomizer solo mezcla objetos ya registrados. Puedes ayudar a completar la lista "
                     "jugando: la DLL anota los objetos de cada sala que visitas, sin cambiar nada de tu partida.",
                     "O randomizer só embaralha itens já levantados. Você pode ajudar a completar a lista "
                     "jogando: a DLL anota os itens de cada sala visitada, sem alterar nada na sua partida.",
                     "Рандомайзер перемешивает только уже собранные предметы. Вы можете помочь дополнить список, "
                     "просто играя: DLL записывает предметы каждой посещённой комнаты, не меняя вашу игру.",
                     "随机器只会打乱已记录的物品。你可以边玩边帮忙完善列表：DLL 会记录你进入的每个房间里的物品，"
                     "不会改变你的游戏。"),
    "releve_case": ("Activer le mode relevé (au prochain lancement du jeu)",
                    "Enable survey mode (next time the game starts)", "調査モードを有効にする（次回のゲーム起動時）",
                    "Activar el modo registro (en el próximo inicio del juego)",
                    "Ativar o modo levantamento (no próximo início do jogo)",
                    "Включить режим сбора (при следующем запуске игры)", "启用记录模式（下次启动游戏时生效）"),
    "etape1": ("1.  Installe la DLL (onglet Installation) et coche la case ci-dessus.",
               "1.  Install the DLL (Installation tab) and tick the box above.",
               "1.  DLL をインストールし（インストールタブ）、上のボックスにチェックを入れます。",
               "1.  Instala la DLL (pestaña Instalación) y marca la casilla de arriba.",
               "1.  Instale a DLL (aba Instalação) e marque a caixa acima.",
               "1.  Установите DLL (вкладка «Установка») и отметьте флажок выше.",
               "1.  安装 DLL（安装标签页）并勾选上方的复选框。"),
    "releve_prevention": (
        "⚠  Pendant le mode relevé, les objets visibles par terre et leur aperçu sont désactivés. Pour jouer avec "
        "une seed, décoche cette case puis relance le jeu. Pour relever, supprime d'abord la seed installée.",
        "⚠  While survey mode is on, items visible on the ground and their preview are turned off. To play with a "
        "seed, untick this box and restart the game. To survey, remove the installed seed first.",
        "⚠  調査モード中は、地面に見えるアイテムとそのプレビューが無効になります。シードで遊ぶときは、このボックスの"
        "チェックを外してゲームを再起動してください。調査するときは、先にインストール済みのシードを削除してください。",
        "⚠  Con el modo registro activo, los objetos visibles en el suelo y su vista previa se desactivan. Para "
        "jugar con una seed, desmarca esta casilla y reinicia el juego. Para registrar, borra antes la seed instalada.",
        "⚠  Com o modo levantamento ativo, os itens visíveis no chão e a prévia ficam desativados. Para jogar com "
        "uma seed, desmarque esta caixa e reinicie o jogo. Para fazer o levantamento, remova antes a seed instalada.",
        "⚠  В режиме сбора данных предметы на полу и их предпросмотр отключены. Чтобы играть с сидом, снимите "
        "этот флажок и перезапустите игру. Для сбора данных сначала удалите установленный сид.",
        "⚠  记录模式开启时，地上可见的物品及其预览会被关闭。要用种子游玩，请取消勾选此框并重启游戏。"
        "要进行记录，请先删除已安装的种子。"),
    "alerte_releve_titre": ("Mode relevé actif", "Survey mode is on", "調査モードが有効です", "Modo registro activo",
                            "Modo levantamento ativo", "Режим сбора данных включён", "记录模式已开启"),
    "alerte_releve": (
        "Les objets visibles par terre (et leur aperçu avant ramassage) sont désactivés car le mode relevé est "
        "actif. Les objets seront seulement remplacés au moment du ramassage.\n\nDésactive le mode relevé pour "
        "les voir, puis relance le jeu.",
        "Items visible on the ground (and their preview before pickup) are turned off because survey mode is on. "
        "Items will only be replaced when you pick them up.\n\nTurn survey mode off to see them, then restart "
        "the game.",
        "調査モードが有効なため、地面に見えるアイテム（拾う前のプレビューも）は無効です。アイテムは拾ったときにだけ"
        "入れ替わります。\n\n表示するには調査モードを無効にして、ゲームを再起動してください。",
        "Los objetos visibles en el suelo (y su vista previa) están desactivados porque el modo registro está "
        "activo. Los objetos solo se sustituirán al recogerlos.\n\nDesactiva el modo registro para verlos y "
        "reinicia el juego.",
        "Os itens visíveis no chão (e a prévia antes de pegar) estão desativados porque o modo levantamento está "
        "ativo. Os itens só serão trocados ao pegá-los.\n\nDesative o modo levantamento para vê-los e reinicie "
        "o jogo.",
        "Предметы на полу (и их предпросмотр) отключены, потому что включён режим сбора данных. Предметы будут "
        "заменяться только при подборе.\n\nОтключите режим сбора данных, чтобы их видеть, и перезапустите игру.",
        "由于记录模式已开启，地上可见的物品（及拾取前的预览）被关闭，物品只会在拾取时替换。\n\n"
        "请关闭记录模式以显示它们，然后重启游戏。"),
    "alerte_releve_desactiver": ("Désactiver le mode relevé", "Turn survey mode off", "調査モードを無効にする",
                                 "Desactivar el modo registro", "Desativar o modo levantamento",
                                 "Отключить режим сбора данных", "关闭记录模式"),
    "alerte_releve_garder": ("Garder le mode relevé", "Keep survey mode", "調査モードのままにする",
                             "Mantener el modo registro", "Manter o modo levantamento",
                             "Оставить режим сбора данных", "保持记录模式"),
    "alerte_releve_fait": ("Mode relevé désactivé : relance le jeu pour voir les objets par terre.",
                           "Survey mode turned off: restart the game to see the items on the ground.",
                           "調査モードを無効にしました。地面のアイテムを見るにはゲームを再起動してください。",
                           "Modo registro desactivado: reinicia el juego para ver los objetos en el suelo.",
                           "Modo levantamento desativado: reinicie o jogo para ver os itens no chão.",
                           "Режим сбора данных отключён: перезапустите игру, чтобы видеть предметы на полу.",
                           "记录模式已关闭：重启游戏即可看到地上的物品。"),
    "etape2": ("2.  Lance une NOUVELLE partie : les objets déjà ramassés n'existent plus en mémoire.",
               "2.  Start a NEW game: items already picked up no longer exist in memory.",
               "2.  ニューゲームで始めます：拾ったアイテムはメモリから消えています。",
               "2.  Empieza una partida NUEVA: los objetos ya recogidos ya no existen en memoria.",
               "2.  Comece um jogo NOVO: itens já pegos não existem mais na memória.",
               "2.  Начните НОВУЮ игру: подобранные предметы исчезают из памяти.",
               "2.  开始新游戏：已拾取的物品不再存在于内存中。"),
    "etape3": ("3.  Visite les pièces sans rien ramasser ; reste environ 2 secondes dans chacune.",
               "3.  Visit rooms without picking anything up; stay about 2 seconds in each.",
               "3.  何も拾わずに部屋を回り、各部屋に約2秒とどまります。",
               "3.  Visita las salas sin recoger nada; quédate unos 2 segundos en cada una.",
               "3.  Visite as salas sem pegar nada; fique cerca de 2 segundos em cada uma.",
               "3.  Обходите комнаты, ничего не подбирая; задерживайтесь в каждой примерно на 2 секунды.",
               "3.  进入各个房间但不要拾取任何物品；在每个房间停留约 2 秒。"),
    "etape4": ("4.  Envoie le journal du jeu (bouton ci-dessous) en précisant le personnage et la difficulté.",
               "4.  Send the game log (button below), stating the character and difficulty.",
               "4.  ゲームのログ（下のボタン）を、キャラクターと難易度を添えて送ってください。",
               "4.  Envía el registro del juego (botón de abajo) indicando el personaje y la dificultad.",
               "4.  Envie o registro do jogo (botão abaixo) informando o personagem e a dificuldade.",
               "4.  Отправьте журнал игры (кнопка ниже), указав персонажа и сложность.",
               "4.  发送游戏日志（下方按钮），并注明角色和难度。"),
    "releve_saccade": ("Petite saccade (~0,3 s) en entrant dans une pièce : décoche la case pour jouer normalement.",
                       "Small stutter (~0.3 s) when entering a room: untick the box to play normally.",
                       "部屋に入るときに少しカクつきます（約0.3秒）：普通に遊ぶときはチェックを外してください。",
                       "Pequeño tirón (~0,3 s) al entrar en una sala: desmarca la casilla para jugar con normalidad.",
                       "Pequeno travamento (~0,3 s) ao entrar numa sala: desmarque a caixa para jogar normalmente.",
                       "Небольшое подтормаживание (~0,3 с) при входе в комнату: снимите флажок для обычной игры.",
                       "进入房间时会有轻微卡顿（约 0.3 秒）：正常游玩时请取消勾选。"),
    "journal_du_jeu": ("Journal du jeu", "Game log", "ゲームのログ", "Registro del juego", "Registro do jogo",
                       "Журнал игры", "游戏日志"),
    "signaler_github": ("Signaler / envoyer sur GitHub", "Report / send on GitHub", "GitHub で報告・送信",
                        "Informar / enviar en GitHub", "Reportar / enviar no GitHub", "Сообщить / отправить на GitHub",
                        "在 GitHub 上反馈/发送"),
    "visitees": (" · +{n} visitées", " · +{n} visited", " · +{n} 訪問済み", " · +{n} visitadas", " · +{n} visitadas",
                 " · +{n} посещено", " · +{n} 已访问"),
    "armes_bonus": ("Armes bonus", "Bonus weapons", "ボーナス武器", "Armas extra", "Armas bônus", "Бонусное оружие",
                    "奖励武器"),
    "bonus_identifiees": ("{a}/{b} identifiées", "{a}/{b} identified", "{a}/{b} 判明", "{a}/{b} identificadas",
                          "{a}/{b} identificadas", "{a}/{b} определено", "已识别 {a}/{b}"),
    "liste_a_completer": ("liste à compléter", "list to be completed", "リスト作成中", "lista por completar",
                          "lista a completar", "список пополняется", "列表待完善"),
    "note_avancement": ("Pièces relevées en nouvelle partie, sur {total}. Rouge : complètes · rouge pâle : visitées "
                        "en partie commencée. Données de la version {version} : tes relevés apparaîtront à la "
                        "version suivante.",
                        "Rooms surveyed in a new game, out of {total}. Red: complete · pale red: visited in a game "
                        "already in progress. Data from version {version}: your surveys will appear in the next "
                        "version.",
                        "ニューゲームで調査済みの部屋（全{total}室中）。赤：完了・薄い赤：プレイ途中のデータで訪問済み。"
                        "バージョン{version}のデータです。あなたの調査結果は次のバージョンに反映されます。",
                        "Salas registradas en partida nueva, de {total}. Rojo: completas · rojo claro: visitadas en "
                        "una partida ya empezada. Datos de la versión {version}: tus registros aparecerán en la "
                        "siguiente versión.",
                        "Salas levantadas em jogo novo, de {total}. Vermelho: completas · vermelho claro: visitadas "
                        "num jogo já começado. Dados da versão {version}: seus levantamentos aparecerão na próxima "
                        "versão.",
                        "Комнаты, собранные в новой игре, из {total}. Красный: полностью · бледно-красный: посещены "
                        "в уже начатой игре. Данные версии {version}: ваши данные появятся в следующей версии.",
                        "在新游戏中记录的房间（共 {total} 个）。红色：已完成 · 浅红色：在进行中的存档里访问过。"
                        "数据来自 {version} 版：你的记录会出现在下一版本中。"),
    "avancement_indispo": ("Avancement indisponible : {e}", "Progress unavailable: {e}", "進み具合を表示できません：{e}",
                           "Progreso no disponible: {e}", "Progresso indisponível: {e}", "Прогресс недоступен: {e}",
                           "无法显示进度：{e}"),

    # ------------------------------------------------------------ messages et boîtes de dialogue
    "choisir_dossier": ("Dossier du jeu (celui qui contient bhd.exe)", "Game folder (the one containing bhd.exe)",
                        "ゲームフォルダー（bhd.exe があるフォルダー）", "Carpeta del juego (la que contiene bhd.exe)",
                        "Pasta do jogo (a que contém bhd.exe)", "Папка игры (с файлом bhd.exe)",
                        "游戏文件夹（包含 bhd.exe 的文件夹）"),
    "err_ini": ("Impossible de modifier randomizer.ini :\n{e}", "Cannot modify randomizer.ini:\n{e}",
                "randomizer.ini を変更できません：\n{e}", "No se puede modificar randomizer.ini:\n{e}",
                "Não foi possível modificar randomizer.ini:\n{e}", "Не удалось изменить randomizer.ini:\n{e}",
                "无法修改 randomizer.ini：\n{e}"),
    "releve_active": ("Mode relevé activé (au prochain lancement du jeu). À chaque nouvelle pièce, les objets présents "
                      "sont notés dans le journal du jeu (lignes « Releve auto »).",
                      "Survey mode enabled (next time the game starts). In each new room, the items present are "
                      "written to the game log (“Releve auto” lines).",
                      "調査モードを有効にしました（次回のゲーム起動時から）。新しい部屋に入るたびに、そこにあるアイテムが"
                      "ゲームのログ（「Releve auto」行）に記録されます。",
                      "Modo registro activado (en el próximo inicio del juego). En cada sala nueva, los objetos "
                      "presentes se anotan en el registro del juego (líneas «Releve auto»).",
                      "Modo levantamento ativado (no próximo início do jogo). Em cada sala nova, os itens presentes "
                      "são anotados no registro do jogo (linhas “Releve auto”).",
                      "Режим сбора включён (со следующего запуска игры). В каждой новой комнате предметы "
                      "записываются в журнал игры (строки «Releve auto»).",
                      "已启用记录模式（下次启动游戏时生效）。每进入一个新房间，其中的物品都会写入游戏日志"
                      "（“Releve auto”行）。"),
    "releve_dll_absente": ("\nAttention : la DLL n'est pas installée, clique « Installer la DLL ».",
                           "\nWarning: the DLL is not installed, click “Install the DLL”.",
                           "\n注意：DLL がインストールされていません。「DLLをインストール」を押してください。",
                           "\nAtención: la DLL no está instalada, pulsa «Instalar la DLL».",
                           "\nAtenção: a DLL não está instalada, clique em “Instalar a DLL”.",
                           "\nВнимание: DLL не установлена, нажмите «Установить DLL».",
                           "\n注意：DLL 未安装，请点击“安装 DLL”。"),
    "releve_desactive": ("Mode relevé désactivé (au prochain lancement du jeu).",
                         "Survey mode disabled (next time the game starts).", "調査モードを無効にしました（次回のゲーム起動時から）。",
                         "Modo registro desactivado (en el próximo inicio del juego).",
                         "Modo levantamento desativado (no próximo início do jogo).",
                         "Режим сбора отключён (со следующего запуска игры).", "已停用记录模式（下次启动游戏时生效）。"),
    "dll_supprimee": ("DLL du randomizer supprimée : {chemin}", "Randomizer DLL removed: {chemin}",
                      "ランダマイザーの DLL を削除しました：{chemin}", "DLL del randomizer eliminada: {chemin}",
                      "DLL do randomizer removida: {chemin}", "DLL рандомайзера удалена: {chemin}",
                      "已删除随机器 DLL：{chemin}"),
    "seed_supprimee": ("Seed installée supprimée : {chemin}", "Installed seed removed: {chemin}",
                       "インストール済みのシードを削除しました：{chemin}", "Seed instalada eliminada: {chemin}",
                       "Seed instalada removida: {chemin}", "Установленный сид удалён: {chemin}",
                       "已删除已安装的种子：{chemin}"),
    "err_supprimer": ("Impossible de supprimer {nom} :\n{e}\n\nLe jeu est-il encore lancé ? Ferme-le puis réessaie.",
                      "Cannot delete {nom}:\n{e}\n\nIs the game still running? Close it and try again.",
                      "{nom} を削除できません：\n{e}\n\nゲームが起動したままではありませんか？終了してからもう一度お試しください。",
                      "No se puede eliminar {nom}:\n{e}\n\n¿Sigue abierto el juego? Ciérralo y vuelve a intentarlo.",
                      "Não foi possível excluir {nom}:\n{e}\n\nO jogo ainda está aberto? Feche-o e tente de novo.",
                      "Не удалось удалить {nom}:\n{e}\n\nИгра всё ещё запущена? Закройте её и повторите.",
                      "无法删除 {nom}：\n{e}\n\n游戏是否仍在运行？请关闭后重试。"),
    "pas_notre_dll": ("Ce xinput1_4.dll n'est pas celui du randomizer : il n'est pas supprimé.",
                      "This xinput1_4.dll is not the randomizer's: it was not deleted.",
                      "この xinput1_4.dll はランダマイザーのものではないため、削除しません。",
                      "Este xinput1_4.dll no es el del randomizer: no se ha eliminado.",
                      "Este xinput1_4.dll não é o do randomizer: ele não foi excluído.",
                      "Этот xinput1_4.dll не принадлежит рандомайзеру: он не удалён.",
                      "此 xinput1_4.dll 不是随机器的文件，不会删除。"),
    "confirmer_desinstaller": ("Désinstaller la DLL du randomizer ?\n\nLe jeu redeviendra le jeu d'origine au "
                               "prochain lancement. La seed installée est conservée (elle ne sert plus à rien sans "
                               "la DLL).",
                               "Uninstall the randomizer DLL?\n\nThe game will be the original game again next "
                               "time it starts. The installed seed is kept (it does nothing without the DLL).",
                               "ランダマイザーの DLL をアンインストールしますか？\n\n次回の起動から元のゲームに戻ります。"
                               "インストール済みのシードは残ります（DLL がなければ何もしません）。",
                               "¿Desinstalar la DLL del randomizer?\n\nEl juego volverá a ser el original en el "
                               "próximo inicio. La seed instalada se conserva (sin la DLL no hace nada).",
                               "Desinstalar a DLL do randomizer?\n\nO jogo voltará a ser o original no próximo "
                               "início. A seed instalada é mantida (sem a DLL ela não faz nada).",
                               "Удалить DLL рандомайзера?\n\nПри следующем запуске игра снова станет исходной. "
                               "Установленный сид сохранится (без DLL он ни на что не влияет).",
                               "卸载随机器 DLL？\n\n下次启动时游戏将恢复为原版。已安装的种子会保留（没有 DLL 时不起作用）。"),
    "sans_randomizer": ("Le jeu se lancera sans randomizer. Pour le remettre : « Installer la DLL ».",
                        "The game will start without the randomizer. To bring it back: “Install the DLL”.",
                        "ゲームはランダマイザーなしで起動します。元に戻すには「DLLをインストール」を押してください。",
                        "El juego se iniciará sin randomizer. Para volver a ponerlo: «Instalar la DLL».",
                        "O jogo vai iniciar sem o randomizer. Para recolocá-lo: “Instalar a DLL”.",
                        "Игра запустится без рандомайзера. Чтобы вернуть его: «Установить DLL».",
                        "游戏将在没有随机器的情况下启动。要恢复：点击“安装 DLL”。"),
    "confirmer_supprimer_seed": ("Supprimer la seed installée ({graine}{armes}) ?\n\nSes fichiers restent dans le "
                                 "dossier des seeds. Sans seed, la DLL laisse le jeu tel quel.",
                                 "Remove the installed seed ({graine}{armes})?\n\nIts files stay in the seeds "
                                 "folder. Without a seed, the DLL leaves the game as it is.",
                                 "インストール済みのシード（{graine}{armes}）を削除しますか？\n\nファイルはシードのフォルダーに"
                                 "残ります。シードがなければ DLL はゲームを変更しません。",
                                 "¿Eliminar la seed instalada ({graine}{armes})?\n\nSus archivos se quedan en la "
                                 "carpeta de seeds. Sin seed, la DLL deja el juego tal cual.",
                                 "Remover a seed instalada ({graine}{armes})?\n\nOs arquivos dela continuam na "
                                 "pasta das seeds. Sem seed, a DLL deixa o jogo como está.",
                                 "Удалить установленный сид ({graine}{armes})?\n\nЕго файлы останутся в папке "
                                 "сидов. Без сида DLL не меняет игру.",
                                 "删除已安装的种子（{graine}{armes}）？\n\n其文件仍保留在种子文件夹中。没有种子时，DLL 不会改变游戏。"),
    "avec_armes": (" avec armes", " with weapons", "・武器あり", " con armas", " com armas", " с оружием", "，含武器"),
    "version_confirmer": ("Ta version de bhd.exe n'est pas celle prise en charge.\n\nLa DLL restera inactive (le jeu "
                          "ne sera pas modifié). L'installer quand même ?",
                          "Your bhd.exe version is not the supported one.\n\nThe DLL will stay inactive (the game "
                          "will not be modified). Install it anyway?",
                          "お使いの bhd.exe は対応バージョンではありません。\n\nDLL は動作しません（ゲームは変更されません）。"
                          "それでもインストールしますか？",
                          "Tu versión de bhd.exe no es la compatible.\n\nLa DLL quedará inactiva (el juego no se "
                          "modificará). ¿Instalarla de todos modos?",
                          "Sua versão do bhd.exe não é a suportada.\n\nA DLL ficará inativa (o jogo não será "
                          "modificado). Instalar mesmo assim?",
                          "Ваша версия bhd.exe не поддерживается.\n\nDLL будет неактивна (игра не изменится). "
                          "Всё равно установить?",
                          "你的 bhd.exe 版本不受支持。\n\nDLL 将保持停用（游戏不会被修改）。仍要安装吗？"),
    "dll_installee": ("DLL installée : {chemin}\nPour désinstaller : supprimer ce fichier.",
                      "DLL installed: {chemin}\nTo uninstall: delete this file.",
                      "DLL をインストールしました：{chemin}\nアンインストールするにはこのファイルを削除します。",
                      "DLL instalada: {chemin}\nPara desinstalar: elimina este archivo.",
                      "DLL instalada: {chemin}\nPara desinstalar: exclua este arquivo.",
                      "DLL установлена: {chemin}\nЧтобы удалить: удалите этот файл.",
                      "已安装 DLL：{chemin}\n卸载方法：删除此文件。"),
    "err_copier_dll": ("Impossible de copier la DLL :\n{e}\n\nLe jeu est-il encore lancé ?",
                       "Cannot copy the DLL:\n{e}\n\nIs the game still running?",
                       "DLL をコピーできません：\n{e}\n\nゲームが起動したままではありませんか？",
                       "No se puede copiar la DLL:\n{e}\n\n¿Sigue abierto el juego?",
                       "Não foi possível copiar a DLL:\n{e}\n\nO jogo ainda está aberto?",
                       "Не удалось скопировать DLL:\n{e}\n\nИгра всё ещё запущена?",
                       "无法复制 DLL：\n{e}\n\n游戏是否仍在运行？"),
    "pas_de_journal": ("Pas encore de journal : il se crée au premier lancement du jeu avec la DLL installée.",
                       "No log yet: it is created the first time the game starts with the DLL installed.",
                       "まだログがありません：DLL をインストールしてゲームを初めて起動したときに作成されます。",
                       "Todavía no hay registro: se crea la primera vez que el juego se inicia con la DLL instalada.",
                       "Ainda não há registro: ele é criado na primeira vez que o jogo inicia com a DLL instalada.",
                       "Журнала пока нет: он создаётся при первом запуске игры с установленной DLL.",
                       "还没有日志：安装 DLL 后首次启动游戏时会创建。"),
    "graine_invalide": ("La graine doit être un nombre entier positif.", "The seed must be a positive whole number.",
                        "シードは正の整数で入力してください。", "La semilla debe ser un número entero positivo.",
                        "A semente deve ser um número inteiro positivo.", "Сид должен быть целым положительным числом.",
                        "种子必须是正整数。"),
    "dossier_introuvable": ("Dossier du jeu introuvable : choisis-le, ou décoche l'installation.",
                            "Game folder not found: choose it, or untick the installation.",
                            "ゲームフォルダーが見つかりません：フォルダーを選ぶか、インストールのチェックを外してください。",
                            "No se encuentra la carpeta del juego: elígela o desmarca la instalación.",
                            "Pasta do jogo não encontrada: escolha-a ou desmarque a instalação.",
                            "Папка игры не найдена: выберите её или снимите флажок установки.",
                            "未找到游戏文件夹：请选择文件夹，或取消勾选安装。"),

    # ------------------------------------------------------------ générateur (résumé, spoiler, installation)
    "gen_resume": ("Graine {graine} — armes aléatoires : {armes}", "Seed {graine} — random weapons: {armes}",
                   "シード {graine} — 武器ランダム：{armes}", "Semilla {graine} — armas aleatorias: {armes}",
                   "Semente {graine} — armas aleatórias: {armes}", "Сид {graine} — случайное оружие: {armes}",
                   "种子 {graine} — 随机武器：{armes}"),
    "gen_oui": ("OUI", "YES", "あり", "SÍ", "SIM", "ДА", "是"),
    "gen_non": ("non", "no", "なし", "no", "não", "нет", "否"),
    "gen_compte": ("{n} objets mélangés, {m} laissés à leur place (clés et objets spéciaux{pistolet}).",
                   "{n} items shuffled, {m} left in place (keys and special items{pistolet}).",
                   "{n}個のアイテムをシャッフル、{m}個はそのまま（鍵・特殊アイテム{pistolet}）。",
                   "{n} objetos mezclados, {m} dejados en su sitio (llaves y objetos especiales{pistolet}).",
                   "{n} itens embaralhados, {m} deixados no lugar (chaves e itens especiais{pistolet}).",
                   "Перемешано предметов: {n}, оставлено на месте: {m} (ключи и особые предметы{pistolet}).",
                   "已打乱 {n} 件物品，{m} 件保持原位（钥匙和特殊物品{pistolet}）。"),
    "gen_pistolet": (", pistolet", ", handgun", "・ハンドガン", ", pistola", ", pistola", ", пистолет", "、手枪"),
    "gen_non_utilises": ("Emplacements non utilisés (valeurs fixes incomplètes) :",
                         "Unused locations (incomplete fixed values):", "未使用の配置（固定値が不完全）：",
                         "Ubicaciones no usadas (valores fijos incompletos):",
                         "Locais não usados (valores fixos incompletos):",
                         "Неиспользованные места (неполные постоянные значения):", "未使用的位置（固定值不完整）："),
    "gen_fichiers": ("\nFichiers écrits dans {dossier} : {a}, {b} et {c}\n",
                     "\nFiles written to {dossier}: {a}, {b} and {c}\n", "\n{dossier} に書き出したファイル：{a}、{b}、{c}\n",
                     "\nArchivos escritos en {dossier}: {a}, {b} y {c}\n",
                     "\nArquivos gravados em {dossier}: {a}, {b} e {c}\n",
                     "\nФайлы записаны в {dossier}: {a}, {b} и {c}\n", "\n已写入 {dossier}：{a}、{b} 和 {c}\n"),
    "gen_donnees": ("Fichier de données introuvable : {fichier}", "Data file not found: {fichier}",
                    "データファイルが見つかりません：{fichier}", "No se encuentra el archivo de datos: {fichier}",
                    "Arquivo de dados não encontrado: {fichier}", "Файл данных не найден: {fichier}",
                    "找不到数据文件：{fichier}"),
    "gen_aucun": ("Aucun emplacement relevé pour {personnage} / {difficulte} : rien à mélanger.",
                  "No surveyed locations for {personnage} / {difficulte}: nothing to shuffle.",
                  "{personnage} / {difficulte} の調査済みの配置がありません：シャッフルするものがありません。",
                  "No hay ubicaciones registradas para {personnage} / {difficulte}: nada que mezclar.",
                  "Nenhum local levantado para {personnage} / {difficulte}: nada para embaralhar.",
                  "Нет собранных мест для {personnage} / {difficulte}: перемешивать нечего.",
                  "{personnage} / {difficulte} 没有已记录的位置：没有可打乱的物品。"),
    "gen_install_impossible": ("INSTALLATION IMPOSSIBLE : dossier du jeu introuvable (bhd.exe absent). "
                               "Indique-le avec --dossier-jeu.",
                               "CANNOT INSTALL: game folder not found (no bhd.exe).",
                               "インストールできません：ゲームフォルダーが見つかりません（bhd.exe がありません）。",
                               "NO SE PUEDE INSTALAR: no se encuentra la carpeta del juego (falta bhd.exe).",
                               "IMPOSSÍVEL INSTALAR: pasta do jogo não encontrada (bhd.exe ausente).",
                               "УСТАНОВКА НЕВОЗМОЖНА: папка игры не найдена (нет bhd.exe).",
                               "无法安装：未找到游戏文件夹（缺少 bhd.exe）。"),
    "gen_installee": ("Seed {graine}{armes} installée : {chemin}", "Seed {graine}{armes} installed: {chemin}",
                      "シード {graine}{armes} をインストールしました：{chemin}", "Seed {graine}{armes} instalada: {chemin}",
                      "Seed {graine}{armes} instalada: {chemin}", "Сид {graine}{armes} установлен: {chemin}",
                      "已安装种子 {graine}{armes}：{chemin}"),
    "gen_armes": (" (armes)", " (weapons)", "（武器あり）", " (armas)", " (armas)", " (оружие)", "（含武器）"),
    "gen_remplace": ("  (remplace la seed {ancienne})", "  (replaces seed {ancienne})", "  （シード {ancienne} を置き換え）",
                     "  (sustituye a la seed {ancienne})", "  (substitui a seed {ancienne})",
                     "  (заменяет сид {ancienne})", "  （替换种子 {ancienne}）"),
    "gen_ini_autre": ("ATTENTION : randomizer.ini demande la seed « {seed} », pas {nom}.",
                      "WARNING: randomizer.ini asks for seed “{seed}”, not {nom}.",
                      "注意：randomizer.ini は {nom} ではなくシード「{seed}」を指定しています。",
                      "ATENCIÓN: randomizer.ini pide la seed «{seed}», no {nom}.",
                      "ATENÇÃO: randomizer.ini pede a seed “{seed}”, não {nom}.",
                      "ВНИМАНИЕ: randomizer.ini указывает сид «{seed}», а не {nom}.",
                      "注意：randomizer.ini 指定的种子是“{seed}”，而不是 {nom}。"),
    "gen_ini_inactif": ("ATTENTION : randomizer.ini contient Actif=0, le randomizer est désactivé.",
                        "WARNING: randomizer.ini contains Actif=0, the randomizer is disabled.",
                        "注意：randomizer.ini に Actif=0 があるため、ランダマイザーは無効です。",
                        "ATENCIÓN: randomizer.ini contiene Actif=0, el randomizer está desactivado.",
                        "ATENÇÃO: randomizer.ini contém Actif=0, o randomizer está desativado.",
                        "ВНИМАНИЕ: в randomizer.ini указано Actif=0, рандомайзер отключён.",
                        "注意：randomizer.ini 中有 Actif=0，随机器已停用。"),
    "gen_dll_absente": ("ATTENTION : xinput1_4.dll absent du dossier du jeu, la seed ne sera pas appliquée "
                        "(copie DLL\\xinput1_4.dll).",
                        "WARNING: xinput1_4.dll is missing from the game folder, the seed will not be applied "
                        "(install the DLL).",
                        "注意：ゲームフォルダーに xinput1_4.dll がないため、シードは適用されません（DLL をインストールしてください）。",
                        "ATENCIÓN: falta xinput1_4.dll en la carpeta del juego, la seed no se aplicará "
                        "(instala la DLL).",
                        "ATENÇÃO: xinput1_4.dll não está na pasta do jogo, a seed não será aplicada "
                        "(instale a DLL).",
                        "ВНИМАНИЕ: в папке игры нет xinput1_4.dll, сид не будет применён (установите DLL).",
                        "注意：游戏文件夹中缺少 xinput1_4.dll，种子不会生效（请安装 DLL）。"),
    "gen_relance": ("Relance le jeu pour que la nouvelle seed soit prise en compte.",
                    "Restart the game for the new seed to take effect.", "新しいシードを反映するにはゲームを再起動してください。",
                    "Reinicia el juego para que se aplique la nueva seed.",
                    "Reinicie o jogo para que a nova seed seja aplicada.",
                    "Перезапустите игру, чтобы новый сид вступил в силу.", "重新启动游戏以使新种子生效。"),

    # ------------------------------------------------------------ armes bonus (spoiler)
    # Les autres objets prennent leur nom officiel dans le jeu (noms_objets.py). Ces deux-là n'ont pas de nom
    # à part dans le jeu : nom officiel de l'arme + mention des munitions illimitées (anglais si le jeu n'a
    # pas la langue : portugais, russe ; « Samurai Edge » n'est pas traduit en chinois dans nos sources).
    "objet_5": ("Samurai Edge (munitions illimitées)", "Samurai Edge (unlimited ammo)", "サムライエッジ（無限弾）",
                "Samurai Edge (munición ilimitada)", "Samurai Edge (munição ilimitada)",
                "Samurai Edge (бесконечные патроны)", "Samurai Edge（无限弹药）"),
    "objet_14": ("Lance-roquettes (munitions illimitées)", "Rocket Launcher (unlimited ammo)",
                 "ロケットランチャー（無限弾）", "Lanzacohetes (munición ilimitada)", "Rocket Launcher (munição ilimitada)",
                 "Rocket Launcher (бесконечные патроны)", "火箭筒（无限弹药）"),
}


# Allemand et italien (ajoutés le 20/11/2026) : clé -> (allemand, italien)
ALLEMAND_ITALIEN = {
    'onglet_randomizer': ('Randomizer',
                          'Randomizer'),
    'onglet_spoiler': ('Spoiler',
                       'Spoiler'),
    'onglet_aide': ('Projekt unterstützen',
                    'Aiuta il progetto'),
    'onglet_installation': ('Installation',
                            'Installazione'),
    'onglet_generer': ('Seed erstellen',
                       'Genera un seed'),
    'install_etapes': ('Nur einmal:\n1.  Spielordner prüfen (er wird meist automatisch gefunden).\n2.  Auf „DLL installieren“ klicken.\n3.  Die Tabs „Seed erstellen“ und „Spoiler“ werden freigeschaltet.',
                       'Solo una volta:\n1.  Controlla la cartella del gioco (di solito viene trovata da sola).\n2.  Clicca su «Installa la DLL».\n3.  Le schede «Genera un seed» e «Spoiler» si sbloccano.'),
    'install_etape_proton': ('Auf Steam Deck / Linux: zusätzlich die Startoption unten in Steam einfügen.',
                             "Su Steam Deck / Linux: incolla anche l'opzione di avvio qui sotto in Steam."),
    'suivant_generer': ('Weiter: Seed erstellen  →',
                        'Avanti: genera un seed  →'),
    'carte_jeu': ('Spiel',
                  'Gioco'),
    'carte_partie': ('Charakter und Schwierigkeit',
                     'Personaggio e difficoltà'),
    'carte_options': ('Optionen',
                      'Opzioni'),
    'carte_fun': ('Spaß',
                  'Divertimento'),
    'note_fun': ('Optionen nur zum Spaß: Sie machen das Spiel deutlich leichter.',
                 'Opzioni solo per divertirsi: rendono il gioco molto più facile.'),
    'note_armes_bonus_fun': ('Jede angehakte Waffe ersetzt mit unendlicher Munition einen zufälligen Gegenstand. Am Boden siehst du den ursprünglichen Gegenstand, bis du ihn aufhebst.',
                             "Ogni arma spuntata, con munizioni illimitate, sostituisce un oggetto a caso. A terra vedi l'oggetto originale finché non lo raccogli."),
    'arme_bonus_samurai': ('Samurai Edge',
                           'Samurai Edge'),
    'arme_bonus_roquettes': ('Raketenwerfer',
                             'Lanciarazzi'),
    'col_lieu': ('Ort',
                 'Luogo'),
    'col_origine': ('Ursprünglicher Gegenstand',
                    'Oggetto originale'),
    'col_nouveau': ('Ersetzt durch',
                    'Sostituito da'),
    'rechercher': ('Suchen',
                   'Cerca'),
    'effacer_recherche': ('Leeren',
                          'Cancella'),
    'resultats_recherche': ('{n} Zeile(n) gefunden',
                            '{n} riga/e trovate'),
    'carte_fous': ('Für die Verrückten',
                   'Per i folli'),
    'carte_ennemis': ('Gegner',
                      'Nemici'),
    'carte_portes': ('Türen', 'Porte'),
    'partie_nouvelle': ('Neues Spiel', 'Nuova partita'),
    'note_partie_nouvelle': ('Antwort auf die Frage nach deinem Spielstil', 'Risposta alla domanda sul tuo stile di gioco'),
    'partie_ufp': ('Neues Spiel+', 'Nuova partita+'),
    'note_partie_ufp': ('Spiel schon beendet: Der Schwierigkeitsgrad wird nach Namen gewählt. Freigeschaltete unendliche Waffen werden nicht gegeben (siehe Bonuswaffen).',
                        'Gioco già finito: scegli la difficoltà per nome. Le armi infinite sbloccate non vengono date (vedi Armi bonus).'),
    'note_cle_placard_ufp': ('Bei Neues Spiel+ legt das Spiel den Kammerschlüssel schon in die Kiste.',
                             'In Nuova partita+ il gioco mette già la chiave del ripostiglio nel baule.'),
    'cle_placard': ('Kammerschlüssel von Anfang an', "Chiave del ripostiglio dall'inizio"),
    'note_cle_placard': ('Der Schlüssel zum Kostümraum liegt von Anfang an in der Kiste, wie nach dem Durchspielen. '
                         'Nur bei einem neuen Spiel (aus einem abgeschlossenen Spielstand gibt ihn das Spiel schon).',
                         "La chiave della stanza dei costumi è nel baule fin dall'inizio, come quando hai già finito "
                         "il gioco. Solo in una nuova partita (da un salvataggio di gioco finito, il gioco la dà già)."),
    'portes_aleatoires': ('Zufällige Türen', 'Porte casuali'),
    'note_portes': ('Jede Tür führt in einen anderen Raum als sonst: Das Herrenhaus wird zu einem echten Labyrinth.',
                    'Ogni porta porta a una stanza diversa dal solito: la villa diventa un vero labirinto.'),
    'carte_spoiler': ('Spoiler',
                      'Spoiler'),
    'carte_releve': ('Erfassungsmodus',
                     'Modalità rilevamento'),
    'carte_avancement': ('Fortschritt der Erfassung',
                         'Avanzamento dei rilevamenti'),
    'langue': ('Sprache',
               'Lingua'),
    'langue_auto': ('Automatisch',
                    'Automatica'),
    'parcourir': ('Durchsuchen…',
                  'Sfoglia…'),
    'installer_dll': ('DLL installieren',
                      'Installa la DLL'),
    'maj_dll': ('DLL aktualisieren',
                'Aggiorna la DLL'),
    'desinstaller_dll': ('DLL deinstallieren',
                         'Disinstalla la DLL'),
    'supprimer_seed': ('Installierten Seed entfernen',
                       'Rimuovi il seed installato'),
    'note_desinstaller': ('Die DLL zu deinstallieren genügt, um das Originalspiel zurückzubekommen.',
                          'Basta disinstallare la DLL per riavere il gioco originale.'),
    'badge_jeu_introuvable': ('●  Spiel nicht gefunden: wähle den Ordner mit bhd.exe',
                              '●  Gioco non trovato: scegli la cartella che contiene bhd.exe'),
    'badge_autre_dll': ('●  Eine andere xinput1_4.dll ist vorhanden',
                        "●  È presente un'altra xinput1_4.dll"),
    'badge_installe': ('●  Randomizer installiert',
                       '●  Randomizer installato'),
    'badge_dll_ancienne': ('●  DLL muss aktualisiert werden',
                           '●  La DLL va aggiornata'),
    'maj_disponible': ('Update v{version}',
                       'Aggiornamento v{version}'),
    'maj_confirmer': ('Version {version} ist verfügbar (du hast {actuelle}).\n\nJetzt herunterladen und installieren? Die App startet danach von selbst neu.',
                      "È disponibile la versione {version} (hai la {actuelle}).\n\nScaricarla e installarla ora? L'app si riavvierà da sola."),
    'maj_telechargement': ('Herunterladen… {pct} %',
                           'Download… {pct} %'),
    'maj_erreur': ('Das Update ist fehlgeschlagen:\n{e}\n\nDownload-Seite öffnen?',
                   "L'aggiornamento non è riuscito:\n{e}\n\nAprire la pagina di download?"),
    'maj_page': ('Version {version} ist verfügbar (du hast {actuelle}).\n\nDownload-Seite öffnen?',
                 'È disponibile la versione {version} (hai la {actuelle}).\n\nAprire la pagina di download?'),
    'badge_origine': ('●  Originalspiel (DLL nicht installiert)',
                      '●  Gioco originale (DLL non installata)'),
    'badge_version': ('●  Nicht unterstützte bhd.exe-Version: Der Randomizer bleibt inaktiv (Spiel unverändert).',
                      '●  Versione di bhd.exe non supportata: il randomizer resterà inattivo (gioco invariato).'),
    'badge_seed': ('●  Seed {graine}{armes}',
                   '●  Seed {graine}{armes}'),
    'badge_armes': (' · Waffen',
                    ' · armi'),
    'badge_aucune_seed': ('●  Kein Seed installiert',
                          '●  Nessun seed installato'),
    'proton_titre': ('Steam Deck / Linux: Startoption des Spiels',
                     'Steam Deck / Linux: opzione di avvio del gioco'),
    'proton_note': ('Das Spiel läuft unter Proton: Füge diese Option einmal in Steam ein (Eigenschaften des Spiels → Startoptionen), damit die DLL geladen wird.',
                    'Il gioco gira con Proton: incolla questa opzione una volta in Steam (Proprietà del gioco → Opzioni di avvio) perché la DLL venga caricata.'),
    'proton_dinput8': ('Auch dinput8.dll laden (für BhdTool oder einen anderen Mod, der sie nutzt)',
                       "Carica anche dinput8.dll (per BhdTool o un'altra mod che la usa)"),
    'proton_detecte': ('  · im Spielordner gefunden',
                       '  · trovata nella cartella del gioco'),
    'copier': ('Kopieren',
               'Copia'),
    'copie_ok': ('Startoption kopiert: in Steam einfügen, Eigenschaften des Spiels → Startoptionen.',
                 'Opzione di avvio copiata: incollala in Steam, Proprietà del gioco → Opzioni di avvio.'),
    'personnage': ('Charakter',
                   'Personaggio'),
    'difficulte': ('Schwierigkeit',
                   'Difficoltà'),
    'a_venir': ('demnächst',
                'in arrivo'),
    'diff_Très facile': ('Sehr leicht',
                         'Molto facile'),
    'diff_Facile': ('Leicht',
                    'Facile'),
    'diff_Normal': ('Normal',
                    'Normale'),
    'diff_Difficile': ('Schwer',
                       'Difficile'),
    'diff_Real Survival': ('Real Survival',
                           'Real Survival'),
    'armes_aleatoires': ('Zufällige Waffen',
                         'Armi casuali'),
    'note_armes': ('Die normalen Waffen des Spiels werden mit den Gegenständen gemischt. Entferne den Haken bei denen, die an ihrem Platz bleiben sollen.',
                   'Le armi normali del gioco vengono mescolate con gli oggetti. Togli la spunta a quelle che devono restare al loro posto.'),
    'arme_pistolet': ('Pistole',
                      'Pistola'),
    'arme_fusil_pompe': ('Gewehr',
                         'Fucile'),
    'arme_fusil_assaut': ('Kampfgewehr',
                          "Fucile d'assalto"),
    'arme_lance_grenades': ('Granatwerfer',
                            'Lanciagranate'),
    'arme_lance_flammes': ('Flammenwerfer',
                           'Lanciafiamme'),
    'arme_autodefense': ('Selbstverteidigungswaffe',
                         'Pistola per autodifesa'),
    'arme_lance_roquettes': ('Raketenwerfer (Spielende)',
                             'Lanciarazzi (fine del gioco)'),
    'arme_magnum': ('Magnum',
                    'Magnum'),
    'chris_uniquement': ('Nur Chris',
                         'Solo Chris'),
    'jill_uniquement': ('Nur Jill',
                        'Solo Jill'),
    'cles_aleatoires': ('Zufällige Schlüssel',
                        'Chiavi casuali'),
    'ennemis_aleatoires': ('Zufällige Gegner',
                           'Nemici casuali'),
    'armes_bonus': ('Bonuswaffen',
                    'Armi bonus'),
    'note_armes_bonus': ('Samurai Edge und Raketenwerfer mit unendlicher Munition: normalerweise freigeschaltet, wenn man das Spiel auf Normal oder Schwer in unter 5 h bzw. unter 3 h beendet.',
                         'Samurai Edge e lanciarazzi con munizioni illimitate: di norma si sbloccano finendo il gioco a Normale o Difficile in meno di 5 h e di 3 h.'),
    'aucune_arme': ('Keine Waffe angehakt: Die Waffen bleiben an ihrem Platz.',
                    'Nessuna arma spuntata: le armi restano al loro posto.'),
    'objets_visibles': ('Gegenstände am Boden sichtbar',
                        'Oggetti visibili a terra'),
    'note_objets_visibles': ('Der neue Gegenstand erscheint direkt im Raum und in der Vorschau vor dem Aufheben. Ohne Haken siehst du den ursprünglichen Gegenstand, bis du ihn aufhebst.',
                             "Il nuovo oggetto appare direttamente nella stanza e nell'anteprima prima di raccoglierlo. Senza spunta vedi l'oggetto originale finché non lo raccogli."),
    'onglet_archipelago': ('Archipelago',
                           'Archipelago'),
    'carte_archipelago': ('Archipelago  ·  demnächst',
                          'Archipelago  ·  in arrivo'),
    'ap_intro': ('Archipelago ist ein Multi-Game-Randomizer: Die Gegenstände deines Spiels können in den Spielen anderer Spieler landen (und umgekehrt), jeder in seinem eigenen Spiel, gleichzeitig. Die Unterstützung für Resident Evil HD Remaster ist in Vorbereitung: Über diesen Tab wirst du dich mit einem Archipelago-Spiel verbinden.',
                 'Archipelago è un randomizer multi-gioco: gli oggetti della tua partita possono finire nei giochi di altri giocatori (e viceversa), ognuno nel proprio gioco, contemporaneamente. Il supporto per Resident Evil HD Remaster è in preparazione: questa scheda servirà a collegarsi a una partita Archipelago.'),
    'ap_site': ('Archipelago-Website',
                'Sito di Archipelago'),
    'carte_ap_connexion': ('Verbindung',
                           'Connessione'),
    'ap_serveur': ('Server (Adresse:Port)',
                   'Server (indirizzo:porta)'),
    'ap_joueur': ('Spielername (Slot)',
                  'Nome del giocatore (slot)'),
    'ap_mot_de_passe': ('Passwort (falls das Spiel eines hat)',
                        'Password (se la partita ne ha una)'),
    'ap_connecter': ('Verbinden',
                     'Connetti'),
    'ap_etat': ('Nicht verbunden  ·  noch nicht verfügbar',
                'Non connesso  ·  non ancora disponibile'),
    'ap_deathlink': ('DeathLink (stirbt ein Spieler, sterben alle)',
                     'DeathLink (se un giocatore muore, muoiono tutti)'),
    'carte_ap_avancement': ('Was noch zu tun ist',
                            'Cosa resta da fare'),
    'ap_fait': ('erledigt',
                'fatto'),
    'ap_en_cours': ('in Arbeit',
                    'in corso'),
    'ap_a_faire': ('offen',
                   'da fare'),
    'ap_etape_releves': ('Erfassung aller Fundorte (Chris / Leicht in Arbeit)',
                         'Rilevamento di tutti i punti degli oggetti (Chris / Facile in corso)'),
    'ap_etape_cles': ('Schlüssel und Questgegenstände mit Logik (damit das Spiel schaffbar bleibt)',
                      'Chiavi e oggetti della missione con logica (perché il gioco resti completabile)'),
    'ap_etape_envoyer': ('Jeden aufgehobenen Fundort an den Server melden',
                         'Inviare al server ogni punto raccolto'),
    'ap_etape_recevoir': ('Die von anderen Spielern geschickten Gegenstände ins Inventar bekommen',
                          "Ricevere nell'inventario gli oggetti inviati dagli altri giocatori"),
    'ap_etape_monde': ('Die Archipelago-„Welt“ des Spiels (.apworld-Datei: Gegenstände, Fundorte, Regeln)',
                       'Il «mondo» Archipelago del gioco (file .apworld: oggetti, punti, regole)'),
    'ap_etape_objectif': ('Spielziel (Ende) an den Server senden',
                          'Obiettivo del gioco (finale) inviato al server'),
    'onglet_info': ('Info',
                    'Info'),
    'carte_projet': ('Projekt',
                     'Progetto'),
    'carte_auteur': ('Autor',
                     'Autore'),
    'carte_tests': ('Tests und Erfassung der Gegenstände',
                    'Test e rilevamento degli oggetti'),
    'carte_remerciements': ('Danke',
                            'Ringraziamenti'),
    'info_description': ('Mischt die Gegenstände des Herrenhauses bei jedem Durchlauf.',
                         'Mescola gli oggetti della villa a ogni partita.'),
    'lien_projet': ('Projektseite auf GitHub',
                    'Pagina del progetto su GitHub'),
    'lien_profil': ('GitHub-Profil',
                    'Profilo GitHub'),
    'info_licence': ('GPLv3-Lizenz: frei und quelloffen.',
                     'Licenza GPLv3: libero e open source.'),
    'info_fan': ('Inoffizielles Fanprojekt, nicht mit Capcom verbunden. Resident Evil ist eine Marke von Capcom.',
                 'Progetto amatoriale non ufficiale, non affiliato a Capcom. Resident Evil è un marchio di Capcom.'),
    'info_bhdtool': ('BhdTool (eleval): Raumnamen und Verbindungen und eine große Hilfe bei der Erfassung.',
                     'BhdTool (eleval): nomi e collegamenti delle stanze, e un grande aiuto per i rilevamenti.'),
    'info_inspiration': ('Inspiriert von Community-Randomizern: BioRand und dem früheren Randomizer von Benn Powell.',
                         'Ispirato ai randomizer della community: BioRand e il precedente randomizer di Benn Powell.'),
    'quitter': ('Beenden',
                'Esci'),
    'sans_logique': ('Ohne Logik',
                     'Senza logica'),
    'note_sans_logique': ('Schlüssel können überall landen: Der Durchlauf ist eventuell nicht zu schaffen.',
                          'Le chiavi possono finire ovunque: la partita potrebbe essere impossibile da finire.'),
    'arme_depart': ('Garantierte Startwaffe',
                    "Arma garantita all'inizio"),
    'note_arme_depart': ("Eine der gemischten Waffen kommt zu Spielbeginn mit ihrer Grundmunition ins Inventar. "
                         "An ihrem Fundort liegt stattdessen ein zufälliger Gegenstand. Nur bei einem neuen Spiel.",
                         "Una delle armi mescolate viene data nell'inventario all'inizio, con le sue munizioni di "
                         "base. Al suo posto ci sarà un oggetto a caso. Solo in una nuova partita."),
    'graine': ('Seed',
               'Seed'),
    'au_hasard': ('Zufällig',
                  'Casuale'),
    'note_graine': ('Gleicher Seed + gleiche Optionen = gleiches Ergebnis.',
                    'Stesso seed + stesse opzioni = stesso risultato.'),
    'generer': ('Seed erstellen',
                'Genera il seed'),
    'installer_seed_case': ('Seed im Spiel installieren',
                            'Installa il seed nel gioco'),
    'dossier_seeds': ('Seed-Ordner',
                      'Cartella dei seed'),
    'pret': ('Bereit. Wähle deine Optionen und klicke dann auf „Seed erstellen“.',
             'Pronto. Scegli le opzioni, poi clicca su «Genera il seed».'),
    'donnees_absentes': ('Datendatei {fichier} nicht gefunden: Erstellen nicht möglich.',
                         'File di dati {fichier} non trovato: impossibile generare.'),
    'generation': ('Wird erstellt…',
                   'Generazione…'),
    'erreur': ('FEHLER: {e}',
               'ERRORE: {e}'),
    'echec_generation': ('Erstellen oder Installieren fehlgeschlagen.',
                         'Generazione o installazione non riuscita.'),
    'renvoi_spoiler': ('(vollständige Liste der Änderungen: Tab „Spoiler“)',
                       '(elenco completo delle modifiche: scheda «Spoiler»)'),
    'afficher_spoiler': ('Spoiler anzeigen',
                         'Mostra lo spoiler'),
    'spoiler_aucun': ('Noch kein Seed erstellt oder installiert.',
                      'Nessun seed ancora generato o installato.'),
    'spoiler_genere': ('Zuletzt erstellter Seed',
                       'Ultimo seed generato'),
    'spoiler_installe': ('Im Spiel installierter Seed',
                         'Seed installato nel gioco'),
    'spoiler_masque': ('{titre}: Spoiler ausgeblendet. Setze den Haken, um zu sehen, welcher Gegenstand welchen ersetzt.',
                       '{titre}: spoiler nascosto. Spunta la casella per vedere quale oggetto sostituisce quale.'),
    'releve_intro': ('Der Randomizer mischt nur bereits erfasste Gegenstände. Du kannst beim Vervollständigen der Liste helfen, indem du spielst: Die DLL notiert die Gegenstände jedes besuchten Raums, ohne dein Spiel zu verändern.',
                     "Il randomizer mescola solo gli oggetti già rilevati. Puoi aiutare a completare l'elenco giocando: la DLL registra gli oggetti di ogni stanza visitata, senza modificare la tua partita."),
    'releve_case': ('Erfassungsmodus aktivieren (beim nächsten Spielstart)',
                    'Attiva la modalità rilevamento (al prossimo avvio del gioco)'),
    'etape1': ('1.  Installiere die DLL (Tab Installation) und setze oben den Haken.',
               '1.  Installa la DLL (scheda Installazione) e spunta la casella qui sopra.'),
    'releve_prevention': ('⚠  Im Erfassungsmodus sind die am Boden sichtbaren Gegenstände und ihre Vorschau deaktiviert. Um mit einem Seed zu spielen, entferne diesen Haken und starte das Spiel neu. Zum Erfassen entferne zuerst den installierten Seed.',
                          '⚠  Con la modalità rilevamento attiva, gli oggetti visibili a terra e la loro anteprima sono disattivati. Per giocare con un seed, togli questa spunta e riavvia il gioco. Per rilevare, rimuovi prima il seed installato.'),
    'alerte_releve_titre': ('Erfassungsmodus ist aktiv',
                            'Modalità rilevamento attiva'),
    'alerte_releve': ('Die am Boden sichtbaren Gegenstände (und ihre Vorschau vor dem Aufheben) sind deaktiviert, weil der Erfassungsmodus aktiv ist. Gegenstände werden erst beim Aufheben ersetzt.\n\nDeaktiviere den Erfassungsmodus, um sie zu sehen, und starte dann das Spiel neu.',
                      'Gli oggetti visibili a terra (e la loro anteprima prima di raccoglierli) sono disattivati perché la modalità rilevamento è attiva. Gli oggetti verranno sostituiti solo quando li raccogli.\n\nDisattiva la modalità rilevamento per vederli, poi riavvia il gioco.'),
    'alerte_releve_desactiver': ('Erfassungsmodus deaktivieren',
                                 'Disattiva la modalità rilevamento'),
    'alerte_releve_garder': ('Erfassungsmodus behalten',
                             'Mantieni la modalità rilevamento'),
    'alerte_releve_fait': ('Erfassungsmodus deaktiviert: Starte das Spiel neu, um die Gegenstände am Boden zu sehen.',
                           'Modalità rilevamento disattivata: riavvia il gioco per vedere gli oggetti a terra.'),
    'etape2': ('2.  Starte ein NEUES Spiel: Bereits aufgehobene Gegenstände existieren nicht mehr im Speicher.',
               '2.  Inizia una NUOVA partita: gli oggetti già raccolti non esistono più in memoria.'),
    'etape3': ('3.  Besuche Räume, ohne etwas aufzuheben; bleib in jedem etwa 2 Sekunden.',
               '3.  Visita le stanze senza raccogliere nulla; resta circa 2 secondi in ognuna.'),
    'etape4': ('4.  Schicke das Spielprotokoll (Knopf unten) und gib Charakter und Schwierigkeit an.',
               '4.  Invia il registro del gioco (pulsante qui sotto), indicando personaggio e difficoltà.'),
    'releve_saccade': ('Kleines Ruckeln (~0,3 s) beim Betreten eines Raums: Haken entfernen, um normal zu spielen.',
                       'Piccolo scatto (~0,3 s) entrando in una stanza: togli la spunta per giocare normalmente.'),
    'journal_du_jeu': ('Spielprotokoll',
                       'Registro del gioco'),
    'signaler_github': ('Auf GitHub melden / senden',
                        'Segnala / invia su GitHub'),
    'visitees': (' · +{n} besucht',
                 ' · +{n} visitate'),
    'bonus_identifiees': ('{a}/{b} identifiziert',
                          '{a}/{b} identificate'),
    'liste_a_completer': ('Liste noch unvollständig',
                          'elenco da completare'),
    'note_avancement': ('In einem neuen Spiel erfasste Räume, von {total}. Rot: vollständig · hellrot: in einem bereits laufenden Spiel besucht. Daten aus Version {version}: Deine Erfassungen erscheinen in der nächsten Version.',
                        'Stanze rilevate in una nuova partita, su {total}. Rosso: completa · rosso chiaro: visitata in una partita già iniziata. Dati della versione {version}: i tuoi rilevamenti compariranno nella prossima versione.'),
    'avancement_indispo': ('Fortschritt nicht verfügbar: {e}',
                           'Avanzamento non disponibile: {e}'),
    'choisir_dossier': ('Spielordner (der mit bhd.exe)',
                        'Cartella del gioco (quella che contiene bhd.exe)'),
    'err_ini': ('randomizer.ini kann nicht geändert werden:\n{e}',
                'Impossibile modificare randomizer.ini:\n{e}'),
    'releve_active': ('Erfassungsmodus aktiviert (beim nächsten Spielstart). In jedem neuen Raum werden die vorhandenen Gegenstände ins Spielprotokoll geschrieben (Zeilen „Releve auto“).',
                      'Modalità rilevamento attivata (al prossimo avvio del gioco). In ogni nuova stanza, gli oggetti presenti vengono scritti nel registro del gioco (righe «Releve auto»).'),
    'releve_dll_absente': ('\nAchtung: Die DLL ist nicht installiert, klicke auf „DLL installieren“.',
                           '\nAttenzione: la DLL non è installata, clicca su «Installa la DLL».'),
    'releve_desactive': ('Erfassungsmodus deaktiviert (beim nächsten Spielstart).',
                         'Modalità rilevamento disattivata (al prossimo avvio del gioco).'),
    'dll_supprimee': ('Randomizer-DLL entfernt: {chemin}',
                      'DLL del randomizer rimossa: {chemin}'),
    'seed_supprimee': ('Installierter Seed entfernt: {chemin}',
                       'Seed installato rimosso: {chemin}'),
    'err_supprimer': ('{nom} kann nicht gelöscht werden:\n{e}\n\nLäuft das Spiel noch? Schließe es und versuche es erneut.',
                      'Impossibile eliminare {nom}:\n{e}\n\nIl gioco è ancora aperto? Chiudilo e riprova.'),
    'pas_notre_dll': ('Diese xinput1_4.dll gehört nicht zum Randomizer: Sie wurde nicht gelöscht.',
                      'Questa xinput1_4.dll non è quella del randomizer: non è stata eliminata.'),
    'confirmer_desinstaller': ('Die Randomizer-DLL deinstallieren?\n\nBeim nächsten Start ist das Spiel wieder das Original. Der installierte Seed bleibt erhalten (ohne die DLL bewirkt er nichts).',
                               'Disinstallare la DLL del randomizer?\n\nAl prossimo avvio il gioco tornerà quello originale. Il seed installato viene conservato (senza la DLL non fa nulla).'),
    'sans_randomizer': ('Das Spiel startet ohne den Randomizer. Zum Zurückholen: „DLL installieren“.',
                        'Il gioco si avvierà senza il randomizer. Per riaverlo: «Installa la DLL».'),
    'confirmer_supprimer_seed': ('Den installierten Seed ({graine}{armes}) entfernen?\n\nSeine Dateien bleiben im Seed-Ordner. Ohne Seed lässt die DLL das Spiel unverändert.',
                                 "Rimuovere il seed installato ({graine}{armes})?\n\nI suoi file restano nella cartella dei seed. Senza seed, la DLL lascia il gioco com'è."),
    'avec_armes': (' mit Waffen',
                   ' con armi'),
    'version_confirmer': ('Deine bhd.exe-Version ist nicht die unterstützte.\n\nDie DLL bleibt inaktiv (das Spiel wird nicht verändert). Trotzdem installieren?',
                          'La tua versione di bhd.exe non è quella supportata.\n\nLa DLL resterà inattiva (il gioco non verrà modificato). Installarla comunque?'),
    'dll_installee': ('DLL installiert: {chemin}\nZum Deinstallieren: diese Datei löschen.',
                      'DLL installata: {chemin}\nPer disinstallarla: elimina questo file.'),
    'err_copier_dll': ('Die DLL kann nicht kopiert werden:\n{e}\n\nLäuft das Spiel noch?',
                       'Impossibile copiare la DLL:\n{e}\n\nIl gioco è ancora aperto?'),
    'pas_de_journal': ('Noch kein Protokoll: Es wird beim ersten Spielstart mit installierter DLL erstellt.',
                       'Nessun registro per ora: viene creato al primo avvio del gioco con la DLL installata.'),
    'graine_invalide': ('Der Seed muss eine positive ganze Zahl sein.',
                        'Il seed deve essere un numero intero positivo.'),
    'dossier_introuvable': ('Spielordner nicht gefunden: wähle ihn aus oder entferne den Haken bei der Installation.',
                            "Cartella del gioco non trovata: sceglila, o togli la spunta all'installazione."),
    'gen_resume': ('Seed {graine} — zufällige Waffen: {armes}',
                   'Seed {graine} — armi casuali: {armes}'),
    'gen_oui': ('JA',
                'SÌ'),
    'gen_non': ('nein',
                'no'),
    'gen_compte': ('{n} Gegenstände gemischt, {m} an ihrem Platz gelassen (Schlüssel und Spezialgegenstände{pistolet}).',
                   '{n} oggetti mescolati, {m} lasciati al loro posto (chiavi e oggetti speciali{pistolet}).'),
    'gen_pistolet': (', Pistole',
                     ', pistola'),
    'gen_non_utilises': ('Nicht genutzte Fundorte (feste Werte unvollständig):',
                         'Punti non usati (valori fissi incompleti):'),
    'gen_fichiers': ('\nDateien geschrieben in {dossier}: {a}, {b} und {c}\n',
                     '\nFile scritti in {dossier}: {a}, {b} e {c}\n'),
    'gen_donnees': ('Datendatei nicht gefunden: {fichier}',
                    'File di dati non trovato: {fichier}'),
    'gen_aucun': ('Keine erfassten Fundorte für {personnage} / {difficulte}: nichts zu mischen.',
                  'Nessun punto rilevato per {personnage} / {difficulte}: niente da mescolare.'),
    'gen_install_impossible': ('INSTALLATION NICHT MÖGLICH: Spielordner nicht gefunden (keine bhd.exe).',
                               'INSTALLAZIONE IMPOSSIBILE: cartella del gioco non trovata (nessun bhd.exe).'),
    'gen_installee': ('Seed {graine}{armes} installiert: {chemin}',
                      'Seed {graine}{armes} installato: {chemin}'),
    'gen_armes': (' (Waffen)',
                  ' (armi)'),
    'gen_remplace': ('  (ersetzt Seed {ancienne})',
                     '  (sostituisce il seed {ancienne})'),
    'gen_ini_autre': ('ACHTUNG: randomizer.ini verlangt den Seed „{seed}“, nicht {nom}.',
                      'ATTENZIONE: randomizer.ini chiede il seed «{seed}», non {nom}.'),
    'gen_ini_inactif': ('ACHTUNG: randomizer.ini enthält Actif=0, der Randomizer ist deaktiviert.',
                        'ATTENZIONE: randomizer.ini contiene Actif=0, il randomizer è disattivato.'),
    'gen_dll_absente': ('ACHTUNG: xinput1_4.dll fehlt im Spielordner, der Seed wird nicht angewendet (DLL installieren).',
                        'ATTENZIONE: xinput1_4.dll manca nella cartella del gioco, il seed non verrà applicato (installa la DLL).'),
    'gen_relance': ('Starte das Spiel neu, damit der neue Seed wirkt.',
                    'Riavvia il gioco perché il nuovo seed abbia effetto.'),
    'objet_5': ('Samurai Edge (unendliche Munition)',
                'Samurai Edge (munizioni illimitate)'),
    'objet_14': ('Raketenwerfer (unendliche Munition)',
                 'Lanciarazzi (munizioni illimitate)'),
}
ALLEMAND_ITALIEN.update({
    "couteau_aleatoire": ("Zufälliges Startmesser", "Coltello iniziale casuale"),
    "note_difficulte": (
        "Die Seeds sind für den Schwierigkeitsgrad Leicht gemacht (bisher der einzige erfasste): Wähle im Spiel "
        "denselben, sonst wird der Seed nicht angewendet.",
        "I seed sono fatti per la difficoltà Facile (l'unica rilevata per ora): scegli la stessa nel gioco, "
        "altrimenti il seed non viene applicato."),
    "note_couteau_aleatoire": (
        "Das Messer vom Anfang wird durch einen zufälligen Gegenstand ersetzt und landet woanders. Ohne „Garantierte "
        "Startwaffe“ beginnst du das Spiel eventuell ganz ohne Waffe! Nur bei einem neuen Spiel.",
        "Il coltello iniziale viene sostituito da un oggetto a caso e finisce altrove. Senza «Arma garantita "
        "all'inizio» rischi di iniziare la partita senza nessuna arma! Solo in una nuova partita."),
    "inventaire_depart": ("Startinventar", "Inventario iniziale"),
    "gen_arme_depart": ("Waffe zu Spielbeginn: {arme}", "Arma data all'inizio: {arme}"),
    "malle_aleatoire": ("Zufällige Kiste am Start", "Baule iniziale casuale"),
    "note_malle_aleatoire": (
        "Die Gegenstände in der Kiste zu Spielbeginn werden mit den anderen gemischt. Nur bei einem neuen Spiel.",
        "Gli oggetti del baule all'inizio vengono mescolati con gli altri. Solo in una nuova partita."),
    "malle_depart": ("Kiste am Start", "Baule iniziale"),
    "malle_case": ("Platz {n}", "casella {n}"),
})
for _cle, _traductions in ALLEMAND_ITALIEN.items():
    T[_cle] = T[_cle] + _traductions


def tr(cle, langue="fr", **valeurs):
    """Texte de la clé dans la langue demandée (français si la langue ou la clé manque)."""
    textes = T.get(cle)
    if textes is None:
        return cle
    i = ORDRE.index(langue) if langue in ORDRE else 0
    texte = textes[i] or textes[0]
    return texte.format(**valeurs) if valeurs else texte


class Msg:
    """Message traduit au moment de l'affichage (et non de sa création) : le journal de l'application peut ainsi
    être réaffiché dans une autre langue. Les valeurs peuvent elles-mêmes être des Msg."""

    def __init__(self, cle, *suite, **valeurs):
        self.cle, self.suite, self.valeurs = cle, suite, valeurs

    def en(self, langue):
        valeurs = {k: rendre(v, langue) for k, v in self.valeurs.items()}
        texte = tr(self.cle, langue, **valeurs) if self.cle else ""
        return texte + "".join(rendre(s, langue) for s in self.suite)


def rendre(texte, langue):
    """Texte d'un Msg dans la langue demandée ; une chaîne ordinaire est rendue telle quelle."""
    return texte.en(langue) if isinstance(texte, Msg) else str(texte)


def langue_systeme():
    """Langue du système (Windows ou Linux) si elle est disponible, sinon l'anglais."""
    import sys
    if sys.platform != "win32":
        import os
        for variable in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
            valeur = os.environ.get(variable, "")
            if valeur and valeur not in ("C", "POSIX"):
                code = valeur.split(":")[0][:2].lower()
                return code if code in LANGUES else PAR_DEFAUT
        return PAR_DEFAUT
    try:
        import ctypes
        primaire = ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF
        return {0x0C: "fr", 0x09: "en", 0x11: "ja", 0x0A: "es", 0x16: "pt", 0x19: "ru", 0x04: "zh", 0x07: "de",
                0x10: "it"}.get(
            primaire, PAR_DEFAUT)
    except Exception:
        return PAR_DEFAUT


def verifier():
    """Contrôle : chaque clé a ses 9 traductions et les mêmes {variables} dans chaque langue."""
    import string
    problemes = []
    for cle, textes in T.items():
        if len(textes) != len(ORDRE):
            problemes.append(f"{cle} : {len(textes)} traductions au lieu de {len(ORDRE)}")
            continue
        ref = {v for _, v, _, _ in string.Formatter().parse(textes[0]) if v}
        for code, texte in zip(ORDRE, textes):
            noms = {v for _, v, _, _ in string.Formatter().parse(texte) if v}
            if noms != ref:
                problemes.append(f"{cle} [{code}] : variables {sorted(noms)} au lieu de {sorted(ref)}")
    return problemes


if __name__ == "__main__":
    p = verifier()
    print("\n".join(p) if p else f"OK : {len(T)} textes × {len(ORDRE)} langues")
