"""
Translations for Firebase Manager
Fordítások a Firebase Manager-hez
"""

TRANSLATIONS = {
    "en": {
        # Window title
        "window_title": "Firebase Manager",
        
        # Top bar - Login
        "login_btn": "🔐 Login",
        "login_help_btn": "❓",
        "logout_btn": "🚪 Logout",
        
        # Top bar - Keys
        "key_label": "Key:",
        "no_key": "No key",
        "add_key_btn": "➕",
        "use_key_btn": "🔑 Login with Key",
        "key_help_btn": "❓ Key Help",
        
        # Folder selection
        "project_folder_label": "Firebase project folder:",
        "browse_btn": "📁 Browse",
        "check_btn": "✓ Check",
        "folder_placeholder": "Select a folder...",
        
        # Project selection
        "project_label": "Project:",
        "refresh_btn": "🔄 Refresh",
        "loading": "Loading...",
        "no_project": "No project",
        
        # Status messages
        "status_no_project": "✗ No Firebase project",
        "status_select_folder": "⚠️ Select a folder",
        "status_project_found": "✅ Firebase project found",
        "status_logged_in": "Logged in",
        
        # Action buttons
        "deploy_btn": "🚀 Deploy",
        "build_deploy_btn": "🔨 Build + Deploy",
        "serve_btn": "👁️ Serve (Local)",
        "stop_btn": "⏹️ Stop",
        "rollback_btn": "🔄 Rollback",
        "actions_help_btn": "❓ Help",
        
        # Log window
        "output_label": "Output:",
        "sysinfo_btn": "ℹ️ System Info",
        
        # Messages
        "select_folder_msg": "⚠️ Select a folder!\n",
        "project_found_msg": "✅ Firebase project found!\n",
        "folder_msg": "📁 Folder: {}\n\n",
        "no_firebase_json": "❌ firebase.json not found in this folder!\n",
        "tips_title": "💡 Tips:\n",
        "tip_1": "  1. Select another folder with the 'Browse' button\n",
        "tip_2": "  2. Or run 'firebase init' command in the folder\n",
        
        # Login messages
        "login_starting": "🔐 Starting Firebase login...\n",
        "login_external_window": "⚠️ An external terminal window will open.\n",
        "login_instruction": "⚠️ Log in there, then close that window.\n\n",
        "login_completed": "\n✓ Login process completed.\n",
        "login_checking": "💡 Checking status...\n",
        
        # Key login messages
        "key_auth": "🔑 Authenticating with key file: {}...\n",
        "key_success": "✅ Successfully authenticated with key file!\n",
        "key_active": "💡 Active key: {}\n",
        "key_error": "❌ Authentication error.\n",
        "key_check": "⚠️ Check if the key file is valid.\n",
        "key_not_found": "❌ Key file not found: {}\n",
        
        # Logout messages
        "logout_starting": "🚪 Firebase logout...\n\n",
        "logout_success": "\n✓ Successfully logged out!\n",
        "logout_tip": "💡 You can now log in with another account using the Login button.\n",
        "logout_failed": "\n✗ Logout failed (code: {})\n",
        
        # Key management
        "no_key_selected": "⚠️ No key selected!\n",
        "use_add_key": "💡 Use the '➕ Add Key' button.\n",
        "key_added": "✅ {}\n",
        "key_location": "📁 Key location: keys/{}\n",
        "key_add_error": "❌ {}\n",
        
        # Rollback
        "rollback_starting": "🔄 Starting rollback to version: {}...\n",
        "rollback_warning": "⚠️ This will restore the live site to the selected version.\n\n",
        "rollback_no_project": "❌ No Firebase project selected!\n",
        "rollback_project": "📋 Project: {}\n",
        "rollback_command": "🔄 Command: {}\n\n",
        "rollback_success": "\n✅ Rollback successful!\n",
        "rollback_restored": "💡 The live site has been restored to the selected version.\n",
        "rollback_failed": "\n❌ Rollback failed (code: {})\n",
        "rollback_try_console": "💡 Try from Firebase Console.\n",
        
        # Deploy messages
        "deploy_starting": "🚀 Starting deploy...\n\n",
        "build_starting": "🔨 Starting build...\n\n",
        "deploy_after_build": "\n🚀 Starting deploy...\n\n",
        "serve_starting": "👁️ Starting local server...\n",
        "serve_info": "⚠️ Server running in background. Open: http://localhost:5000\n\n",
        "processes_stopped": "\n⏹️ Processes stopped.\n",
        
        # Help dialogs
        "help_key_title": "Help - Service Account Key",
        "help_key_header": "🔑 How to get a Service Account key?",
        "help_login_title": "Help - Browser Login",
        "help_login_header": "🔐 How does Browser Login work?",
        "help_actions_title": "Help - Firebase Operations",
        "help_actions_header": "🚀 Firebase Operations - Help",
        "close_btn": "Close",
        
        # Folder selection dialog
        "folder_select_title": "Select Folder",
        "folder_select_header": "Select folder:",
        "recent_folders": "📁 Recent folders:",
        "browse_new_folder": "📂 Browse new folder...",
        
        # Rollback dialog
        "rollback_dialog_title": "🔄 Rollback - Version Restore",
        "rollback_dialog_header": "Select a version to restore:",
        "rollback_loading": "Loading versions...",
        "rollback_no_versions": "No versions found or error occurred.",
        "rollback_version_id": "Version ID",
        "rollback_date": "Date",
        "rollback_status": "Status",
        "rollback_select": "Select",
        "rollback_selected": "✓ Selected",
        "rollback_execute": "🔄 Execute Rollback",
        "rollback_console": "🌐 Firebase Console",
        "rollback_no_selection": "No selection",
        "rollback_select_version": "Select a version for rollback!",
        "rollback_confirm_title": "Rollback Confirmation",
        "rollback_confirm_msg": "Are you sure you want to restore this version?\n\nRelease ID: {}\n\nThis will go live immediately!",
        
        # System info
        "sysinfo_checking": "🔍 Checking system information...\n\n",
        "sysinfo_os": "💻 Operating System: {} {}",
        "sysinfo_platform": "📦 Platform: {}",
        "sysinfo_python": "🐍 Python: {}",
        "sysinfo_nodejs": "✅ Node.js: {}",
        "sysinfo_nodejs_missing": "❌ Node.js: Not installed",
        "sysinfo_npm": "✅ npm: {}",
        "sysinfo_npm_missing": "❌ npm: Not installed",
        "sysinfo_firebase": "✅ Firebase CLI: {}",
        "sysinfo_firebase_missing": "❌ Firebase CLI: Not installed",
        "sysinfo_python_modules": "📚 Python modules:",
        "sysinfo_module_installed": "  ✅ {}: {}",
        "sysinfo_module_missing": "  ❌ {}: Not installed",
        "sysinfo_working_dir": "📁 Working directory: {}",
        "sysinfo_firebase_json_found": "✅ firebase.json: Found",
        "sysinfo_firebase_json_missing": "❌ firebase.json: Not found",
        "sysinfo_firebaserc_found": "✅ .firebaserc: Found",
        "sysinfo_firebaserc_missing": "❌ .firebaserc: Not found",
        "sysinfo_current_project": "📋 Current project: {}",
        "sysinfo_active_key": "🔑 Active JSON key: {}",
        "sysinfo_rest_available": "✅ REST API functions: Available",
        "sysinfo_no_key": "⚠️ No active JSON key",
        "sysinfo_rest_unavailable": "❌ REST API functions: Not available",
        
        # Prerequisites warning
        "prereq_missing_title": "Missing Components",
        "prereq_missing_msg": "The following components are missing:\n\n{}\n\nInstall them for proper functionality!\n\nDetails in the log window.",
        "prereq_warning": "⚠️ Missing components:\n\n{}\n\n",
        "prereq_install_guide": "📋 Installation guide:\n\n",
        "prereq_nodejs": "• Node.js: https://nodejs.org/\n",
        "prereq_npm": "• npm: Usually installed with Node.js\n",
        "prereq_firebase": "• Firebase CLI: npm install -g firebase-tools\n",
        "prereq_python": "• Python modules: pip install -r requirements.txt\n",
        "prereq_run_in_folder": "  (Run the command in the program folder!)\n",
        "prereq_final_warning": "\n⚠️ The application will not work properly without these components!",
        
        # JSON key requirement
        "json_key_required_title": "JSON Key Required",
        "json_key_required_msg": "The Rollback function requires logging in with a Service Account JSON key!\n\n1. Get a JSON key from Firebase Console\n2. Add it with the '🔑 Add Key' button\n3. Select the key and click '🔑 Login with Key'\n\nThen you can use the Rollback function.",
        
        # Help content - Service Account Key
        "help_key_content": """
1. Go to Firebase Console:
   https://console.firebase.google.com

2. Select your project from the list

3. Click the gear icon in the top left corner
   (Project Settings)

4. Select the "Service Accounts" tab

5. Click the "Generate new private key" button

6. A confirmation window will appear
   → Click the "Generate key" button

7. A JSON file will be downloaded
   (e.g. my-project-firebase-adminsdk-xxxxx.json)

8. Save this file in a secure location!
   ⚠️ DO NOT share it with anyone, it grants full access!

9. In the application, click the "🔑 Login with Key" button

10. Select the downloaded JSON file

✅ Done! You are now automatically logged in,
   without opening a browser!

💡 Tip: This method is ideal for CI/CD pipelines
   and automated deployments.
""",
        
        # Help content - Browser Login
        "help_login_content": """
Browser Login is the traditional Firebase CLI
login method.

🔐 How does it work?

1. Click the "🔐 Login" button

2. A new CMD (command line) window will open

3. Firebase CLI will start in that window

4. Your browser will automatically open

5. Log in with your Google account
   (Select the appropriate account)

6. Grant Firebase CLI access

7. The browser will show: "Success! You're logged in."

8. The CMD window will show: "Press any key to continue..."

9. Press any key to close the CMD window

10. The application will automatically update the status

✅ Done! You are now logged in!

📌 When to use this method?

• First time login
• Personal use
• When you want to switch to another Google account
• During development

⚠️ Note:

This method is interactive, so it's not suitable for automation
or CI/CD pipelines. For that, use the Service Account
key (🔑 Login with Key button).
""",
        
        # Help content - Actions
        "help_actions_content": """
🚀 DEPLOY

What it does:
• Uploads your application to Firebase
• Runs the 'firebase deploy' command
• Uploads all services (Hosting, Functions, Firestore, etc.)

When to use:
• When you're done with changes
• When you want to update your live website
• Full deploy for all Firebase services

Output:
• You see live in the log window what's happening
• Deploy URL appears
• Success or failure status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔨 BUILD + DEPLOY

What it does:
1. First runs the 'npm run build' command
2. This compiles/builds your application
   (React, Vue, Angular, etc.)
3. Then automatically runs 'firebase deploy'

When to use:
• When you have a build step (React, Vue, Angular)
• When you want to ensure a fresh build is uploaded
• For automated workflow

Advantage:
• You won't forget the build step
• Everything done with one click
• Ensures you upload the latest version

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👁️ SERVE (LOCAL)

What it does:
• Starts a local development server
• Runs the 'firebase serve' command
• Usually available at http://localhost:5000

When to use:
• Before testing, to see if it works
• During local development
• Before going live, test locally

Important:
• Server runs in the background
• Use the Stop button to stop it
• Doesn't upload anything to Firebase, only local

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏹️ STOP

What it does:
• Stops all running background processes
• Mainly stops the 'firebase serve' server
• Interrupts running commands

When to use:
• When you're done with local testing
• When you want to stop the serve server
• If something is stuck and you want to interrupt it

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 ROLLBACK

What it does:
• Restores your website to a previous version
• Opens Firebase Console
• There you can select which version to restore

When to use:
• If something broke in the new deploy
• If you need to quickly restore to a working version
• In case of emergency

Important:
• Firebase automatically stores all versions
• Rollback goes live immediately
• Doesn't delete previous versions
• You can restore to a newer version anytime

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 RECOMMENDED WORKFLOW:

1. 👁️ Serve (Local) - Local testing
2. Check in browser (localhost:5000)
3. ⏹️ Stop - Stop server
4. 🔨 Build + Deploy - Compile and upload
5. ✅ Done! Your app is live!

⚠️ Note:
Buttons are only active when you're logged in
and have a valid Firebase project selected.
""",
    },
    
    "hu": {
        # Ablak cím
        "window_title": "Firebase Manager",
        
        # Felső sáv - Login
        "login_btn": "🔐 Login",
        "login_help_btn": "❓",
        "logout_btn": "🚪 Logout",
        
        # Felső sáv - Kulcsok
        "key_label": "Kulcs:",
        "no_key": "Nincs kulcs",
        "add_key_btn": "➕",
        "use_key_btn": "🔑 Bejelentkezés",
        "key_help_btn": "❓ Kulcs súgó",
        
        # Mappa választó
        "project_folder_label": "Firebase projekt mappa:",
        "browse_btn": "📁 Tallózás",
        "check_btn": "✓ Ellenőrzés",
        "folder_placeholder": "Válassz egy mappát...",
        
        # Projekt választó
        "project_label": "Projekt:",
        "refresh_btn": "🔄 Frissítés",
        "loading": "Betöltés...",
        "no_project": "Nincs projekt",
        
        # Státusz üzenetek
        "status_no_project": "✗ Nincs Firebase projekt",
        "status_select_folder": "⚠️ Válassz egy mappát",
        "status_project_found": "✅ Firebase projekt megtalálva",
        "status_logged_in": "Bejelentkezve",
        
        # Művelet gombok
        "deploy_btn": "🚀 Deploy",
        "build_deploy_btn": "🔨 Build + Deploy",
        "serve_btn": "👁️ Serve (Local)",
        "stop_btn": "⏹️ Stop",
        "rollback_btn": "🔄 Rollback",
        "actions_help_btn": "❓ Súgó",
        
        # Log ablak
        "output_label": "Kimenet:",
        "sysinfo_btn": "ℹ️ Rendszerinfó",
        
        # Üzenetek
        "select_folder_msg": "⚠️ Válassz egy mappát!\n",
        "project_found_msg": "✅ Firebase projekt megtalálva!\n",
        "folder_msg": "📁 Mappa: {}\n\n",
        "no_firebase_json": "❌ Nem található firebase.json ebben a mappában!\n",
        "tips_title": "💡 Tippek:\n",
        "tip_1": "  1. Válassz egy másik mappát a 'Tallózás' gombbal\n",
        "tip_2": "  2. Vagy futtasd a 'firebase init' parancsot a mappában\n",
        
        # Login üzenetek
        "login_starting": "🔐 Firebase bejelentkezés indítása...\n",
        "login_external_window": "⚠️ Egy külső terminál ablak fog megnyílni.\n",
        "login_instruction": "⚠️ Jelentkezz be ott, majd zárd be azt az ablakot.\n\n",
        "login_completed": "\n✓ A bejelentkezési folyamat lezajlott.\n",
        "login_checking": "💡 Ellenőrzöm az állapotot...\n",
        
        # Kulcsos login üzenetek
        "key_auth": "🔑 Hitelesítés kulcsfájllal: {}...\n",
        "key_success": "✅ Sikeres hitelesítés kulcsfájllal!\n",
        "key_active": "💡 Aktív kulcs: {}\n",
        "key_error": "❌ Hiba a hitelesítés során.\n",
        "key_check": "⚠️ Ellenőrizd, hogy a kulcsfájl érvényes-e.\n",
        "key_not_found": "❌ A kulcsfájl nem található: {}\n",
        
        # Logout üzenetek
        "logout_starting": "🚪 Firebase kijelentkezés...\n\n",
        "logout_success": "\n✓ Sikeres kijelentkezés!\n",
        "logout_tip": "💡 Most bejelentkezhetsz másik fiókkal a Login gombbal.\n",
        "logout_failed": "\n✗ Kijelentkezés sikertelen (kód: {})\n",
        
        # Kulcs kezelés
        "no_key_selected": "⚠️ Nincs kiválasztott kulcs!\n",
        "use_add_key": "💡 Használd a '➕' gombot.\n",
        "key_added": "✅ {}\n",
        "key_location": "📁 Kulcs helye: keys/{}\n",
        "key_add_error": "❌ {}\n",
        
        # Rollback
        "rollback_starting": "🔄 Rollback indítása a verzióra: {}...\n",
        "rollback_warning": "⚠️ Ez visszaállítja az éles oldalt a kiválasztott verzióra.\n\n",
        "rollback_no_project": "❌ Nincs kiválasztva Firebase projekt!\n",
        "rollback_project": "📋 Projekt: {}\n",
        "rollback_command": "🔄 Parancs: {}\n\n",
        "rollback_success": "\n✅ Rollback sikeres!\n",
        "rollback_restored": "💡 Az éles oldal visszaállt a kiválasztott verzióra.\n",
        "rollback_failed": "\n❌ Rollback sikertelen (kód: {})\n",
        "rollback_try_console": "💡 Próbáld meg a Firebase Console-ból.\n",
        
        # Deploy üzenetek
        "deploy_starting": "🚀 Deploy indítása...\n\n",
        "build_starting": "🔨 Build indítása...\n\n",
        "deploy_after_build": "\n🚀 Deploy indítása...\n\n",
        "serve_starting": "👁️ Helyi szerver indítása...\n",
        "serve_info": "⚠️ A szerver a háttérben fut. Nyisd meg: http://localhost:5000\n\n",
        "processes_stopped": "\n⏹️ Folyamatok leállítva.\n",
        
        # Súgó ablakok
        "help_key_title": "Súgó - Service Account kulcs",
        "help_key_header": "🔑 Hogyan szerezz Service Account kulcsot?",
        "help_login_title": "Súgó - Browser Login",
        "help_login_header": "🔐 Hogyan működik a Browser Login?",
        "help_actions_title": "Súgó - Firebase Műveletek",
        "help_actions_header": "🚀 Firebase Műveletek - Súgó",
        "close_btn": "Bezárás",
        
        # Mappa választó dialógus
        "folder_select_title": "Mappa választás",
        "folder_select_header": "Válassz mappát:",
        "recent_folders": "📁 Legutóbbi mappák:",
        "browse_new_folder": "📂 Új mappa tallózása...",
        
        # Rollback dialógus
        "rollback_dialog_title": "🔄 Rollback - Verzió visszaállítás",
        "rollback_dialog_header": "Válassz egy verziót a visszaállításhoz:",
        "rollback_loading": "Verziók betöltése...",
        "rollback_no_versions": "Nem találhatók verziók vagy hiba történt.",
        "rollback_version_id": "Verzió ID",
        "rollback_date": "Dátum",
        "rollback_status": "Státusz",
        "rollback_select": "Kiválaszt",
        "rollback_selected": "✓ Kiválasztva",
        "rollback_execute": "🔄 Rollback végrehajtása",
        "rollback_console": "🌐 Firebase Console",
        "rollback_no_selection": "Nincs kiválasztva",
        "rollback_select_version": "Válassz ki egy verziót a rollback-hez!",
        "rollback_confirm_title": "Rollback megerősítés",
        "rollback_confirm_msg": "Biztosan visszaállítod ezt a verziót?\n\nRelease ID: {}\n\nEz azonnal élesbe kerül!",
        
        # Rendszerinfó
        "sysinfo_checking": "🔍 Rendszerinformációk ellenőrzése...\n\n",
        "sysinfo_os": "💻 Operációs rendszer: {} {}",
        "sysinfo_platform": "📦 Platform: {}",
        "sysinfo_python": "🐍 Python: {}",
        "sysinfo_nodejs": "✅ Node.js: {}",
        "sysinfo_nodejs_missing": "❌ Node.js: Nem telepítve",
        "sysinfo_npm": "✅ npm: {}",
        "sysinfo_npm_missing": "❌ npm: Nem telepítve",
        "sysinfo_firebase": "✅ Firebase CLI: {}",
        "sysinfo_firebase_missing": "❌ Firebase CLI: Nem telepítve",
        "sysinfo_python_modules": "📚 Python modulok:",
        "sysinfo_module_installed": "  ✅ {}: {}",
        "sysinfo_module_missing": "  ❌ {}: Nincs telepítve",
        "sysinfo_working_dir": "📁 Munkakönyvtár: {}",
        "sysinfo_firebase_json_found": "✅ firebase.json: Megtalálva",
        "sysinfo_firebase_json_missing": "❌ firebase.json: Nem található",
        "sysinfo_firebaserc_found": "✅ .firebaserc: Megtalálva",
        "sysinfo_firebaserc_missing": "❌ .firebaserc: Nem található",
        "sysinfo_current_project": "📋 Aktuális projekt: {}",
        "sysinfo_active_key": "🔑 Aktív JSON kulcs: {}",
        "sysinfo_rest_available": "✅ REST API funkciók: Elérhetők",
        "sysinfo_no_key": "⚠️ Nincs aktív JSON kulcs",
        "sysinfo_rest_unavailable": "❌ REST API funkciók: Nem elérhetők",
        
        # Előfeltételek figyelmeztetés
        "prereq_missing_title": "Hiányzó komponensek",
        "prereq_missing_msg": "A következő komponensek hiányoznak:\n\n{}\n\nTelepítsd őket a megfelelő működéshez!\n\nRészletek a log ablakban.",
        "prereq_warning": "⚠️ Hiányzó komponensek:\n\n{}\n\n",
        "prereq_install_guide": "📋 Telepítési útmutató:\n\n",
        "prereq_nodejs": "• Node.js: https://nodejs.org/\n",
        "prereq_npm": "• npm: Általában a Node.js-sel együtt települ\n",
        "prereq_firebase": "• Firebase CLI: npm install -g firebase-tools\n",
        "prereq_python": "• Python modulok: pip install -r requirements.txt\n",
        "prereq_run_in_folder": "  (Futtasd a parancsot a program mappájában!)\n",
        "prereq_final_warning": "\n⚠️ Az alkalmazás nem fog megfelelően működni ezen komponensek nélkül!",
        
        # JSON kulcs szükséges
        "json_key_required_title": "JSON kulcs szükséges",
        "json_key_required_msg": "A Rollback funkció használatához Service Account JSON kulccsal kell bejelentkezned!\n\n1. Szerezz be egy JSON kulcsot a Firebase Console-ból\n2. Add hozzá a '🔑 Kulcs hozzáadása' gombbal\n3. Válaszd ki a kulcsot és kattints a '🔑 Bejelentkezés' gombra\n\nEzután használhatod a Rollback funkciót.",
        
        # Súgó tartalom - Service Account Kulcs
        "help_key_content": """
1. Menj a Firebase Console-ba:
   https://console.firebase.google.com

2. Válaszd ki a projektedet a listából

3. Kattints a bal felső sarokban a fogaskerék ikonra
   (Project Settings)

4. Válaszd a "Service Accounts" fület

5. Kattints a "Generate new private key" gombra

6. Egy megerősítő ablak jelenik meg
   → Kattints a "Generate key" gombra

7. Letöltődik egy JSON fájl
   (pl. my-project-firebase-adminsdk-xxxxx.json)

8. Mentsd el biztonságos helyre ezt a fájlt!
   ⚠️ NE oszd meg senkivel, ez teljes hozzáférést ad!

9. Az alkalmazásban kattints a "🔑 Bejelentkezés" gombra

10. Válaszd ki a letöltött JSON fájlt

✅ Kész! Most már automatikusan be vagy jelentkezve,
   böngésző megnyitása nélkül!

💡 Tipp: Ez a módszer ideális CI/CD pipeline-okhoz
   és automatizált deploy-okhoz.
""",
        
        # Súgó tartalom - Browser Login
        "help_login_content": """
A Browser Login (böngészős bejelentkezés) a Firebase CLI 
hagyományos bejelentkezési módja.

🔐 Hogyan működik?

1. Kattints a "🔐 Login" gombra

2. Megnyílik egy új CMD (parancssori) ablak

3. A Firebase CLI elindul ebben az ablakban

4. Automatikusan megnyílik a böngésződ

5. Jelentkezz be a Google fiókoddal
   (Válaszd ki a megfelelő fiókot)

6. Engedélyezd a Firebase CLI hozzáférést

7. A böngészőben megjelenik: "Success! You're logged in."

8. A CMD ablakban megjelenik: "Press any key to continue..."

9. Nyomj egy billentyűt a CMD ablak bezárásához

10. Az alkalmazás automatikusan frissíti az állapotot

✅ Kész! Most már be vagy jelentkezve!

📌 Mikor használd ezt a módszert?

• Első bejelentkezéskor
• Személyes használatra
• Amikor másik Google fiókra szeretnél váltani
• Fejlesztés közben

⚠️ Megjegyzés:

Ez a módszer interaktív, ezért nem alkalmas automatizálásra
vagy CI/CD pipeline-okhoz. Arra használd a Service Account
kulcsot (🔑 Bejelentkezés gomb).
""",
        
        # Súgó tartalom - Műveletek
        "help_actions_content": """
🚀 DEPLOY

Mit csinál:
• Feltölti az alkalmazásodat a Firebase-re
• Futtatja a 'firebase deploy' parancsot
• Minden szolgáltatást feltölt (Hosting, Functions, Firestore, stb.)

Mikor használd:
• Amikor kész vagy a változtatásokkal
• Amikor frissíteni akarod az élő weboldaladat
• Teljes deploy minden Firebase szolgáltatáshoz

Kimenet:
• Látod élőben a log ablakban, mi történik
• Megjelenik a deploy URL
• Sikeres vagy sikertelen státusz

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔨 BUILD + DEPLOY

Mit csinál:
1. Először lefuttatja az 'npm run build' parancsot
2. Ez lefordítja/összeállítja az alkalmazásodat
   (React, Vue, Angular, stb.)
3. Majd automatikusan futtatja a 'firebase deploy' parancsot

Mikor használd:
• Amikor van build lépésed (React, Vue, Angular)
• Amikor biztosan friss build-et akarsz feltölteni
• Automatizált workflow-hoz

Előny:
• Nem felejted el a build-et
• Egy kattintással mindent megcsinál
• Biztos, hogy a legfrissebb verziót töltöd fel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👁️ SERVE (LOCAL)

Mit csinál:
• Elindít egy helyi fejlesztői szervert
• Futtatja a 'firebase serve' parancsot
• Általában a http://localhost:5000 címen érhető el

Mikor használd:
• Tesztelés előtt, hogy megnézd, működik-e
• Helyi fejlesztés közben
• Mielőtt élesbe tennéd, kipróbálod lokálisan

Fontos:
• A szerver a háttérben fut
• Használd a Stop gombot a leállításhoz
• Nem tölt fel semmit a Firebase-re, csak helyi

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏹️ STOP

Mit csinál:
• Leállítja az összes futó háttérfolyamatot
• Főleg a 'firebase serve' szervert állítja le
• Megszakítja a futó parancsokat

Mikor használd:
• Amikor befejezted a helyi tesztelést
• Amikor le akarod állítani a serve szervert
• Ha valami elakadt és meg akarod szakítani

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 ROLLBACK

Mit csinál:
• Visszaállítja a weboldaladat egy korábbi verzióra
• Megnyitja a Firebase Console-t
• Ott kiválaszthatod, melyik verzióra állj vissza

Mikor használd:
• Ha az új deploy-nál valami elromlott
• Ha gyorsan vissza kell állni működő verzióra
• Vészhelyzet esetén

Fontos:
• A Firebase automatikusan tárolja az összes verziót
• A rollback azonnal élesbe kerül
• Nem törli a korábbi verziókat
• Bármikor visszaállhatsz újabb verzióra

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 AJÁNLOTT MUNKAFOLYAMAT:

1. 👁️ Serve (Local) - Helyi tesztelés
2. Ellenőrzés a böngészőben (localhost:5000)
3. ⏹️ Stop - Szerver leállítása
4. 🔨 Build + Deploy - Fordítás és feltöltés
5. ✅ Kész! Az alkalmazásod élő!

⚠️ Megjegyzés:
A gombok csak akkor aktívak, ha be vagy jelentkezve
és van érvényes Firebase projekt kiválasztva.
""",
    }
}


def get_text(key: str, lang: str = "en") -> str:
    """Get translated text by key"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
