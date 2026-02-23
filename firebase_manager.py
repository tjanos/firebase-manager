"""
Firebase Manager - Desktop GUI for Firebase CLI
Multi-language support (English/Hungarian)
"""
import customtkinter as ctk
import subprocess
import json
import threading
import os
import shutil
import platform
from typing import Optional, Callable
from pathlib import Path
from tkinter import filedialog, messagebox
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
from translations import get_text, TRANSLATIONS


class ConfigManager:
    """Konfiguráció kezelése"""
    
    def __init__(self, config_file: str = "app_config.json"):
        self.config_file = Path(__file__).parent / config_file
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Betölti a konfigurációt"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Alapértelmezett konfiguráció"""
        return {
            "last_project_folder": "",
            "last_selected_key": "",
            "language": "en",  # Default language
            "window_size": {
                "width": 900,
                "height": 650
            },
            "recent_folders": []
        }
    
    def save_config(self):
        """Elmenti a konfigurációt"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Konfig mentési hiba: {e}")
    
    def set_last_folder(self, folder: str):
        """Beállítja az utolsó mappát"""
        self.config["last_project_folder"] = folder
        
        # Hozzáadja a recent folders listához
        if folder and folder not in self.config["recent_folders"]:
            self.config["recent_folders"].insert(0, folder)
            # Csak az utolsó 5-öt tartjuk
            self.config["recent_folders"] = self.config["recent_folders"][:5]
        
        self.save_config()
    
    def get_last_folder(self) -> str:
        """Visszaadja az utolsó mappát"""
        return self.config.get("last_project_folder", "")
    
    def set_last_key(self, key: str):
        """Beállítja az utolsó kulcsot"""
        self.config["last_selected_key"] = key
        self.save_config()
    
    def get_last_key(self) -> str:
        """Visszaadja az utolsó kulcsot"""
        return self.config.get("last_selected_key", "")
    
    def get_recent_folders(self) -> list[str]:
        """Visszaadja a legutóbbi mappákat"""
        return self.config.get("recent_folders", [])
    
    def set_window_size(self, width: int, height: int):
        """Beállítja az ablak méretét"""
        self.config["window_size"] = {"width": width, "height": height}
        self.save_config()
    
    def get_window_size(self) -> tuple[int, int]:
        """Visszaadja az ablak méretét"""
        size = self.config.get("window_size", {"width": 900, "height": 650})
        return size["width"], size["height"]
    
    def set_language(self, lang: str):
        """Beállítja a nyelvet"""
        self.config["language"] = lang
        self.save_config()
    
    def get_language(self) -> str:
        """Visszaadja a nyelvet"""
        return self.config.get("language", "en")


class FirebaseAPI:
    """Firebase CLI műveletek kezelése"""
    
    def __init__(self, working_dir: Optional[str] = None):
        self.current_project: Optional[str] = None
        self.running_processes = []
        self.working_dir = working_dir or os.getcwd()
        self.keys_dir = Path(__file__).parent / "keys"
        self.platform = platform.system()  # 'Windows', 'Darwin' (Mac), 'Linux'
        
        # Létrehozzuk a keys mappát, ha nem létezik
        self.keys_dir.mkdir(exist_ok=True)
    
    def check_prerequisites(self) -> tuple[bool, list[str]]:
        """Ellenőrzi, hogy a szükséges eszközök és Python modulok telepítve vannak-e"""
        missing = []
        
        # Node.js ellenőrzés
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                timeout=5,
                shell=True if self.platform == "Windows" else False
            )
            if result.returncode != 0:
                missing.append("Node.js")
        except:
            missing.append("Node.js")
        
        # npm ellenőrzés
        try:
            result = subprocess.run(
                ["npm", "--version"],
                capture_output=True,
                timeout=5,
                shell=True if self.platform == "Windows" else False
            )
            if result.returncode != 0:
                missing.append("npm")
        except:
            missing.append("npm")
        
        # Firebase CLI ellenőrzés
        try:
            result = subprocess.run(
                ["firebase", "--version"],
                capture_output=True,
                timeout=5,
                shell=True if self.platform == "Windows" else False
            )
            if result.returncode != 0:
                missing.append("Firebase CLI")
        except:
            missing.append("Firebase CLI")
        
        # Python modulok ellenőrzése
        python_modules = {
            "customtkinter": "CustomTkinter (GUI)",
            "google.auth": "Google Auth (REST API)",
            "google.oauth2.service_account": "Google Service Account (REST API)",
            "requests": "Requests (HTTP)"
        }
        
        for module_name, display_name in python_modules.items():
            try:
                __import__(module_name)
            except ImportError:
                missing.append(f"Python modul: {display_name}")
        
        return len(missing) == 0, missing
    
    def get_available_keys(self) -> list[str]:
        """Visszaadja az elérhető kulcsfájlok listáját"""
        if not self.keys_dir.exists():
            return []
        
        json_files = list(self.keys_dir.glob("*.json"))
        return [f.name for f in json_files]
    
    def copy_key_to_keys_dir(self, source_path: str) -> tuple[bool, str]:
        """Átmásol egy kulcsfájlt a keys mappába"""
        try:
            source = Path(source_path)
            if not source.exists():
                return False, "A fájl nem található"
            
            if not source.suffix == ".json":
                return False, "Csak JSON fájlokat lehet hozzáadni"
            
            destination = self.keys_dir / source.name
            
            # Ha már létezik, kérdezzük meg
            if destination.exists():
                return False, f"A '{source.name}' már létezik a keys mappában"
            
            shutil.copy2(source, destination)
            return True, f"Kulcs hozzáadva: {source.name}"
            
        except Exception as e:
            return False, f"Hiba: {str(e)}"
    
    def set_working_dir(self, path: str):
        """Beállítja a munkakönyvtárat"""
        self.working_dir = path
    
    def check_firebase_project(self) -> bool:
        """Ellenőrzi, hogy van-e firebase.json a mappában"""
        firebase_json = Path(self.working_dir) / "firebase.json"
        return firebase_json.exists()
    
    def check_login_status(self) -> tuple[bool, str, Optional[str]]:
        """Ellenőrzi, hogy be van-e jelentkezve a felhasználó és visszaadja az email-t"""
        try:
            # Próbáljuk meg lekérni a projekteket - ez a legmegbízhatóbb módszer
            result = subprocess.run(
                ["firebase", "projects:list"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10,
                cwd=self.working_dir,
                encoding='utf-8',
                errors='replace'
            )
            
            # Ha sikeres, akkor be van jelentkezve
            if result.returncode == 0 and "Error" not in result.stdout:
                # Próbáljuk meg lekérni az email címet
                login_result = subprocess.run(
                    ["firebase", "login:list"],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=5,
                    cwd=self.working_dir,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if login_result.returncode == 0 and login_result.stdout:
                    lines = login_result.stdout.split('\n')
                    for line in lines:
                        if '@' in line:
                            email = line.strip().split()[0]
                            return True, "Bejelentkezve", email
                
                return True, "Bejelentkezve", None
            else:
                return False, "Nincs bejelentkezve", None
                
        except Exception as e:
            return False, f"Hiba: {str(e)}", None
    
    def login(self, callback: Callable[[str, bool], None]):
        """Firebase bejelentkezés indítása egy új konzolablakban"""
        def run():
            try:
                callback("🔐 Firebase bejelentkezés indítása...\n", False)
                callback("⚠️ Egy külső terminál ablak fog megnyílni.\n", False)
                callback("⚠️ Jelentkezz be ott, majd zárd be azt az ablakot.\n\n", False)
                
                # Platform-specifikus parancs
                if self.platform == "Windows":
                    # Windows: új CMD ablak
                    command = "start /wait cmd /c firebase login && pause"
                elif self.platform == "Darwin":
                    # macOS: új Terminal ablak
                    command = 'osascript -e \'tell application "Terminal" to do script "firebase login && read -p \\"Press Enter to close...\\"";\''
                else:
                    # Linux: próbáljuk meg különböző terminálokat
                    # Először gnome-terminal, aztán xterm
                    command = 'gnome-terminal -- bash -c "firebase login; read -p \\"Press Enter to close...\\""'
                
                process = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.working_dir
                )
                
                callback(f"\n✓ A bejelentkezési folyamat lezajlott.\n", False)
                callback(f"💡 Ellenőrzöm az állapotot...\n", True)
                
            except Exception as e:
                callback(f"\n✗ Hiba: {str(e)}\n", True)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def login_with_key(self, key_name: str, callback: Callable[[str, bool], None]):
        """Bejelentkezés JSON kulcsfájllal - nem nyit böngészőt!"""
        def run():
            try:
                key_path = self.keys_dir / key_name
                
                # Ellenőrizzük, létezik-e a fájl
                if not key_path.exists():
                    callback(f"❌ A kulcsfájl nem található: {key_name}\n", True)
                    return
                
                callback(f"🔑 Hitelesítés kulcsfájllal: {key_name}...\n", False)
                
                # Beállítjuk a környezeti változót
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(key_path)
                
                # Teszteljük, hogy működik-e
                result = subprocess.run(
                    ["firebase", "projects:list"],
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.working_dir,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if result.returncode == 0:
                    callback("✅ Sikeres hitelesítés kulcsfájllal!\n", False)
                    callback(f"💡 Aktív kulcs: {key_name}\n", True)
                else:
                    callback(f"❌ Hiba a hitelesítés során.\n", False)
                    callback(f"⚠️ Ellenőrizd, hogy a kulcsfájl érvényes-e.\n", True)
                    
            except Exception as e:
                callback(f"❌ Váratlan hiba: {str(e)}\n", True)
        
        threading.Thread(target=run, daemon=True).start()
    
    def logout(self, callback: Callable[[str, bool], None]):
        """Firebase kijelentkezés"""
        def run():
            try:
                callback("🚪 Firebase kijelentkezés...\n\n", False)
                
                process = subprocess.Popen(
                    ["firebase", "logout"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=True,
                    bufsize=1,
                    cwd=self.working_dir,
                    encoding='utf-8',
                    errors='replace'
                )
                
                output_lines = []
                for line in process.stdout:
                    output_lines.append(line)
                    callback(line, False)
                
                process.wait()
                
                if process.returncode == 0:
                    callback(f"\n✓ Sikeres kijelentkezés!\n", False)
                    callback(f"💡 Most bejelentkezhetsz másik fiókkal a Login gombbal.\n", True)
                else:
                    callback(f"\n✗ Kijelentkezés sikertelen (kód: {process.returncode})\n", True)
                
            except Exception as e:
                callback(f"\n✗ Hiba: {str(e)}\n", True)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def get_projects(self) -> list[dict]:
        """Lekéri az elérhető Firebase projekteket"""
        try:
            result = subprocess.run(
                ["firebase", "projects:list", "--json"],
                capture_output=True,
                text=True,
                shell=True,
                timeout=15,
                cwd=self.working_dir,
                encoding='utf-8',
                errors='replace'  # Unicode hibák kezelése
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("result", [])
            return []
        except Exception as e:
            print(f"Projekt lekérési hiba: {e}")
            return []
    
    def get_current_project(self) -> Optional[str]:
        """Lekéri az aktuális projektet a .firebaserc-ből"""
        try:
            firebaserc_path = Path(self.working_dir) / ".firebaserc"
            if firebaserc_path.exists():
                with open(firebaserc_path, 'r') as f:
                    config = json.load(f)
                    return config.get("projects", {}).get("default")
        except Exception as e:
            print(f"Projekt olvasási hiba: {e}")
        return None
    
    def run_command_async(self, command: list[str], callback: Callable[[str, bool], None]):
        """Parancs futtatása háttérszálon élő kimenettel"""
        def run():
            try:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=True,
                    bufsize=1,
                    cwd=self.working_dir,
                    encoding='utf-8',
                    errors='replace'  # Unicode hibák kezelése
                )
                
                self.running_processes.append(process)
                
                for line in process.stdout:
                    callback(line, False)
                
                process.wait()
                success = process.returncode == 0
                
                if process in self.running_processes:
                    self.running_processes.remove(process)
                
                callback(f"\n{'✓ Sikeres' if success else '✗ Sikertelen'} (kód: {process.returncode})", True)
                
            except Exception as e:
                callback(f"\n✗ Hiba: {str(e)}", True)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def get_hosting_releases(self, project_id: str) -> tuple[bool, list[dict]]:
        """Lekéri a Firebase Hosting korábbi verzióit explicit projekt megadással"""
        try:
            # Ellenőrizzük, hogy van-e érvényes projekt
            if not project_id or project_id == "Betöltés..." or project_id == "Nincs projekt":
                print(f"❌ Érvénytelen projekt ID: {project_id}")
                return False, []
            
            # Windows-on a string parancs sokkal stabilabb shell=True mellett
            cmd = f'firebase hosting:releases:list --project {project_id} --json'
            print(f"🔍 Verziók lekérése: {cmd}")
            print(f"📁 Munkakönyvtár: {self.working_dir}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,  # Windows-on mindenképp True kell
                cwd=self.working_dir,
                encoding='utf-8',
                errors='replace',
                timeout=15
            )
            
            print(f"📊 Return code: {result.returncode}")
            
            if result.returncode == 0 and result.stdout:
                print(f"✅ Sikeres válasz, stdout hossza: {len(result.stdout)}")
                try:
                    data = json.loads(result.stdout)
                    # A CLI kimenete lehet 'result' kulcs alatt, vagy direktben a lista
                    if isinstance(data, dict) and 'result' in data:
                        print(f"📋 Verziók száma: {len(data['result'])}")
                        return True, data['result']
                    elif isinstance(data, list):
                        print(f"📋 Verziók száma: {len(data)}")
                        return True, data
                    else:
                        print(f"⚠️ Ismeretlen JSON struktúra: {type(data)}")
                        return False, []
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parse hiba: {e}")
                    print(f"📄 Stdout tartalom: {result.stdout[:200]}")
                    return False, []
            else:
                # Ha hiba van, írjuk ki a konzolra a valós okot (debug)
                print(f"❌ Sikertelen parancs")
                if result.stderr:
                    print(f"🔴 STDERR: {result.stderr}")
                if result.stdout:
                    print(f"📄 STDOUT: {result.stdout[:200]}")
                return False, []
                
        except Exception as e:
            print(f"❌ Váratlan hiba: {e}")
            import traceback
            traceback.print_exc()
            return False, []
    
    def _try_text_releases(self, project_id: str) -> tuple[bool, list[dict]]:
        """Próbálja meg szöveges formátumban lekérni"""
        try:
            cmd = f'firebase hosting:releases:list --project {project_id}'
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                cwd=self.working_dir,
                encoding='utf-8',
                errors='replace',
                timeout=15
            )
            
            if result.returncode == 0 and result.stdout:
                # Szöveges kimenet feldolgozása
                releases = []
                lines = result.stdout.split('\n')
                
                for line in lines:
                    # Keressük a verzió sorokat
                    if line.strip() and not line.startswith('─') and not line.startswith('Release'):
                        parts = line.split()
                        if len(parts) >= 2:
                            releases.append({
                                'name': parts[0],
                                'createTime': ' '.join(parts[1:3]) if len(parts) > 2 else 'N/A',
                                'status': 'DEPLOYED'
                            })
                
                return len(releases) > 0, releases
            
            return False, []
        except:
            return False, []
    
    def rollback_to_version(self, version_name: str, callback: Callable[[str, bool], None]):
        """Visszaállítja az éles weboldalt a megadott verzióra"""
        def run():
            try:
                callback(f"🔄 Rollback indítása a verzióra: {version_name}...\n", False)
                callback("⚠️ Ez visszaállítja az éles oldalt a kiválasztott verzióra.\n\n", False)
                
                # Projekt ID lekérése
                project_id = self.get_current_project() or ""
                
                if not project_id or project_id in ["Betöltés...", "Nincs projekt"]:
                    callback("❌ Nincs kiválasztva Firebase projekt!\n", True)
                    return
                
                # A HELYES PARANCS: hosting:releases:rollback
                # Ez visszaállítja az éles (production) verziót
                cmd = f'firebase hosting:releases:rollback {version_name} --project {project_id}'
                
                callback(f"📋 Projekt: {project_id}\n", False)
                callback(f"🔄 Parancs: {cmd}\n\n", False)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    shell=True,
                    bufsize=1,
                    cwd=self.working_dir,
                    encoding='utf-8',
                    errors='replace'
                )
                
                self.running_processes.append(process)
                
                for line in process.stdout:
                    callback(line, False)
                
                process.wait()
                success = process.returncode == 0
                
                if process in self.running_processes:
                    self.running_processes.remove(process)
                
                if success:
                    callback(f"\n✅ Rollback sikeres!\n", True)
                    callback(f"💡 Az éles oldal visszaállt a kiválasztott verzióra.\n", True)
                else:
                    callback(f"\n❌ Rollback sikertelen (kód: {process.returncode})\n", True)
                    callback(f"💡 Próbáld meg a Firebase Console-ból.\n", True)
                
            except Exception as e:
                callback(f"\n❌ Hiba: {str(e)}\n", True)
        
        threading.Thread(target=run, daemon=True).start()
    
    def get_hosting_url(self, project_id: str) -> str:
        """Visszaadja a Firebase Console Hosting URL-jét"""
        if project_id and project_id not in ["Betöltés...", "Nincs projekt"]:
            return f"https://console.firebase.google.com/project/{project_id}/hosting/sites"
        return "https://console.firebase.google.com"
    
    def get_credentials_from_env(self):
        """Lekéri a hitelesítési adatokat a környezeti változóból"""
        creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_path or not os.path.exists(creds_path):
            return None
        
        try:
            credentials = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            return credentials
        except Exception as e:
            print(f"❌ Hitelesítési hiba: {e}")
            return None
    
    def get_access_token(self) -> Optional[str]:
        """Lekér egy access tokent.
        
        Sorrend:
          1. firebase login (böngészős bejelentkezés) tárolt tokenje
          2. Service Account JSON kulcs (GOOGLE_APPLICATION_CREDENTIALS)
        """
        # 1. Firebase böngészős login tárolt tokenje
        try:
            home = Path.home()
            config_paths = [
                home / ".config" / "configstore" / "firebase-tools.json",
                home / "AppData" / "Roaming" / "Configstore" / "firebase-tools.json",
            ]
            for cfg_path in config_paths:
                if cfg_path.exists():
                    with open(cfg_path, 'r', encoding='utf-8') as f:
                        cfg = json.load(f)
                    tokens = cfg.get("tokens", {})
                    # A firebase-tools refresh tokennel dolgozik
                    refresh_token = tokens.get("refresh_token")
                    access_token = tokens.get("access_token")
                    if access_token:
                        print(f"✅ Firebase böngészős token megtalálva: {cfg_path}")
                        return access_token
                    # Ha van refresh token, frissítsük
                    if refresh_token:
                        new_token = self._refresh_firebase_token(refresh_token)
                        if new_token:
                            return new_token
        except Exception as e:
            print(f"⚠️ Firebase config olvasási hiba: {e}")

        # 2. Service Account JSON kulcs
        credentials = self.get_credentials_from_env()
        if credentials:
            try:
                credentials.refresh(Request())
                print("✅ Service Account token lekérve")
                return credentials.token
            except Exception as e:
                print(f"❌ Service Account token hiba: {e}")

        print("❌ Nincs elérhető token (sem firebase login, sem JSON kulcs)")
        return None

    def _refresh_firebase_token(self, refresh_token: str) -> Optional[str]:
        """Frissíti a Firebase CLI access tokent a Google OAuth2 endpointtal"""
        try:
            import urllib.request
            import urllib.parse
            # Google OAuth2 token refresh endpoint (ezt használja a firebase-tools is)
            url = "https://oauth2.googleapis.com/token"
            data = urllib.parse.urlencode({
                "client_id": "563584335869-fgrhgmd47bqnekij5i8b5pr03ho849e6.apps.googleusercontent.com",
                "client_secret": "j9iVZfS8kkCEFUPaAeJV0sAi",
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }).encode('utf-8')
            req = urllib.request.Request(url, data=data, method="POST")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                token = result.get("access_token")
                if token:
                    print("✅ Firebase token sikeresen frissítve")
                return token
        except Exception as e:
            print(f"⚠️ Token frissítési hiba: {e}")
            return None
    
    def get_hosting_releases_rest(self, project_id: str) -> tuple[bool, list[dict]]:
        """Lekéri a Firebase Hosting verzióit REST API-val (JSON kulcs szükséges)"""
        try:
            if not project_id or project_id in ["Betöltés...", "Nincs projekt"]:
                print(f"❌ Érvénytelen projekt ID: {project_id}")
                return False, []
            
            # Access token lekérése
            access_token = self.get_access_token()
            if not access_token:
                print("❌ Nincs érvényes JSON kulcs beállítva!")
                return False, []
            
            print(f"🔍 REST API hívás: Firebase Hosting Releases")
            print(f"📋 Projekt: {project_id}")
            
            # Firebase Hosting API endpoint
            # Először lekérjük a site-okat
            sites_url = f"https://firebasehosting.googleapis.com/v1beta1/projects/{project_id}/sites"
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Sites lekérése
            sites_response = requests.get(sites_url, headers=headers, timeout=10)
            
            if sites_response.status_code != 200:
                print(f"❌ Sites lekérési hiba: {sites_response.status_code}")
                print(f"📄 Válasz: {sites_response.text}")
                return False, []
            
            sites_data = sites_response.json()
            sites = sites_data.get('sites', [])
            
            if not sites:
                print("⚠️ Nincs hosting site a projektben")
                return False, []
            
            # Az első site releases-eit kérjük le
            site_name = sites[0]['name']  # pl: projects/PROJECT_ID/sites/SITE_ID
            print(f"🌐 Site: {site_name}")
            
            # Releases lekérése
            releases_url = f"https://firebasehosting.googleapis.com/v1beta1/{site_name}/releases"
            releases_response = requests.get(releases_url, headers=headers, timeout=10)
            
            if releases_response.status_code != 200:
                print(f"❌ Releases lekérési hiba: {releases_response.status_code}")
                print(f"📄 Válasz: {releases_response.text}")
                return False, []
            
            releases_data = releases_response.json()
            releases = releases_data.get('releases', [])
            
            print(f"✅ Sikeresen lekérve {len(releases)} verzió")
            
            return True, releases
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Hálózati hiba: {e}")
            return False, []
        except Exception as e:
            print(f"❌ Váratlan hiba: {e}")
            import traceback
            traceback.print_exc()
            return False, []
    
    def rollback_to_version_rest(self, project_id: str, release_name: str, callback: Callable[[str, bool], None]):
        """Visszaállítja a megadott verziót REST API-val"""
        def run():
            try:
                callback(f"🔄 Rollback indítása...\n", False)
                callback(f"📋 Projekt: {project_id}\n", False)
                callback(f"📦 Verzió: {release_name}\n\n", False)
                
                # Access token lekérése
                access_token = self.get_access_token()
                if not access_token:
                    callback("❌ Nincs érvényes JSON kulcs beállítva!\n", True)
                    return
                
                # Site lekérése
                sites_url = f"https://firebasehosting.googleapis.com/v1beta1/projects/{project_id}/sites"
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                
                sites_response = requests.get(sites_url, headers=headers, timeout=10)
                if sites_response.status_code != 200:
                    callback(f"❌ Site lekérési hiba: {sites_response.status_code}\n", True)
                    return
                
                sites_data = sites_response.json()
                sites = sites_data.get('sites', [])
                
                if not sites:
                    callback("❌ Nincs hosting site a projektben\n", True)
                    return
                
                site_name = sites[0]['name']
                callback(f"🌐 Site: {site_name}\n", False)
                
                # Rollback végrehajtása - új release létrehozása a régi verzióval
                # A release_name formátuma: projects/PROJECT/sites/SITE/releases/RELEASE_ID
                # Ebből kinyerjük a version-t
                callback("🔄 Verzió információk lekérése...\n", False)
                
                release_url = f"https://firebasehosting.googleapis.com/v1beta1/{release_name}"
                release_response = requests.get(release_url, headers=headers, timeout=10)
                
                if release_response.status_code != 200:
                    callback(f"❌ Release lekérési hiba: {release_response.status_code}\n", True)
                    return
                
                release_data = release_response.json()
                version_name = release_data.get('version', {}).get('name')
                
                if not version_name:
                    callback("❌ Nem található verzió információ\n", True)
                    return
                
                callback(f"📦 Verzió név: {version_name}\n", False)
                callback("🚀 Új release létrehozása ezzel a verzióval...\n", False)
                
                # Új release létrehozása
                create_release_url = f"https://firebasehosting.googleapis.com/v1beta1/{site_name}/releases?versionName={version_name}"
                
                create_response = requests.post(create_release_url, headers=headers, timeout=30)
                
                if create_response.status_code in [200, 201]:
                    callback("\n✅ Rollback sikeres!\n", True)
                    callback("💡 Az éles oldal visszaállt a kiválasztott verzióra.\n", True)
                else:
                    callback(f"\n❌ Rollback sikertelen: {create_response.status_code}\n", True)
                    callback(f"📄 Válasz: {create_response.text}\n", True)
                
            except Exception as e:
                callback(f"\n❌ Hiba: {str(e)}\n", True)
                import traceback
                traceback.print_exc()
        
        threading.Thread(target=run, daemon=True).start()
    
    def has_json_key_active(self) -> bool:
        """Ellenőrzi, hogy van-e aktív JSON kulcs"""
        creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        return creds_path is not None and os.path.exists(creds_path)
    
    def stop_all_processes(self):
        """Leállítja az összes futó folyamatot"""
        for process in self.running_processes:
            try:
                process.terminate()
            except:
                pass
        self.running_processes.clear()



class FirebaseManagerApp(ctk.CTk):
    """Fő alkalmazás ablak"""
    
    def __init__(self):
        super().__init__()
        
        self.api = FirebaseAPI()
        self.config = ConfigManager()  # Konfiguráció kezelő
        self.current_lang = self.config.get_language()  # Nyelv betöltése
        
        self.title(get_text("window_title", self.current_lang))
        
        # Ablak méret betöltése
        width, height = self.config.get_window_size()
        self.geometry(f"{width}x{height}")
        
        # Színséma
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        
        # Utolsó mappa betöltése
        last_folder = self.config.get_last_folder()
        if last_folder and Path(last_folder).exists():
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, last_folder)
            self.check_firebase_project()
        else:
            self.check_firebase_project()
        
        self.refresh_keys()  # Kulcsok betöltése
        
        # Utolsó kulcs kiválasztása
        last_key = self.config.get_last_key()
        if last_key:
            keys = self.api.get_available_keys()
            if last_key in keys:
                self.key_combo.set(last_key)
        
        # Előfeltételek ellenőrzése
        self.check_prerequisites()
        
        # Ablak bezáráskor
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """UI elemek létrehozása"""
        # Nyelvválasztó sáv (legfelül)
        lang_bar = ctk.CTkFrame(self, height=40)
        lang_bar.pack(fill="x", padx=10, pady=(10, 0))
        
        ctk.CTkLabel(lang_bar, text="🌐", font=("Arial", 16)).pack(side="left", padx=(10, 5))
        
        self.lang_combo = ctk.CTkComboBox(
            lang_bar,
            values=["English", "Magyar"],
            width=120,
            height=28,
            state="readonly",
            command=self.change_language
        )
        self.lang_combo.pack(side="left", padx=5, pady=5)
        self.lang_combo.set("English" if self.current_lang == "en" else "Magyar")
        
        # Felső vezérlő sáv
        top_bar = ctk.CTkFrame(self, height=70)
        top_bar.pack(fill="x", padx=10, pady=10)
        
        # Bal oldal - Login gombok
        left_frame = ctk.CTkFrame(top_bar)
        left_frame.pack(side="left", padx=10, pady=10)
        
        self.login_btn = ctk.CTkButton(
            left_frame,
            text=get_text("login_btn", self.current_lang),
            command=self.do_login,
            width=90,
            height=32,
            fg_color="#ff9800"
        )
        self.login_btn.pack(side="left", padx=3)
        
        self.login_help_btn = ctk.CTkButton(
            left_frame,
            text=get_text("login_help_btn", self.current_lang),
            command=self.show_login_help,
            width=35,
            height=32,
            fg_color="#607d8b"
        )
        self.login_help_btn.pack(side="left", padx=3)
        
        # Jobb oldal - Kulcs kezelő
        right_frame = ctk.CTkFrame(top_bar)
        right_frame.pack(side="right", padx=10, pady=10)
        
        ctk.CTkLabel(right_frame, text=get_text("key_label", self.current_lang), font=("Arial", 10)).pack(side="left", padx=3)
        
        self.key_combo = ctk.CTkComboBox(
            right_frame,
            values=[get_text("no_key", self.current_lang)],
            width=150,
            height=32,
            state="readonly"
        )
        self.key_combo.pack(side="left", padx=3)
        
        self.add_key_btn = ctk.CTkButton(
            right_frame,
            text=get_text("add_key_btn", self.current_lang),
            command=self.add_key,
            width=40,
            height=32,
            fg_color="#4caf50"
        )
        self.add_key_btn.pack(side="left", padx=3)
        
        self.use_key_btn = ctk.CTkButton(
            right_frame,
            text=get_text("use_key_btn", self.current_lang),
            command=self.use_selected_key,
            width=120,
            height=32,
            fg_color="#2196f3"
        )
        self.use_key_btn.pack(side="left", padx=3)
        
        self.help_btn = ctk.CTkButton(
            right_frame,
            text=get_text("key_help_btn", self.current_lang),
            command=self.show_help,
            width=110,
            height=32,
            fg_color="#607d8b"
        )
        self.help_btn.pack(side="left", padx=3)
        
        # Mappa választó
        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(folder_frame, text=get_text("project_folder_label", self.current_lang), font=("Arial", 12, "bold")).pack(side="left", padx=10)
        
        self.folder_entry = ctk.CTkEntry(
            folder_frame,
            width=500,
            placeholder_text=get_text("folder_placeholder", self.current_lang)
        )
        self.folder_entry.pack(side="left", padx=10, pady=10)
        self.folder_entry.insert(0, os.getcwd())
        
        self.browse_btn = ctk.CTkButton(
            folder_frame,
            text=get_text("browse_btn", self.current_lang),
            command=self.browse_folder,
            width=120
        )
        self.browse_btn.pack(side="left", padx=5)
        
        self.check_btn = ctk.CTkButton(
            folder_frame,
            text=get_text("check_btn", self.current_lang),
            command=self.check_firebase_project,
            width=120,
            fg_color="green"
        )
        self.check_btn.pack(side="left", padx=5)
        
        # Projekt választó
        project_frame = ctk.CTkFrame(self)
        project_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(project_frame, text=get_text("project_label", self.current_lang)).pack(side="left", padx=10)
        
        self.project_combo = ctk.CTkComboBox(
            project_frame,
            values=[get_text("loading", self.current_lang)],
            width=300,
            state="readonly"
        )
        self.project_combo.pack(side="left", padx=10, pady=10)
        
        self.refresh_btn = ctk.CTkButton(
            project_frame,
            text=get_text("refresh_btn", self.current_lang),
            command=self.refresh_projects,
            width=100
        )
        self.refresh_btn.pack(side="left", padx=5)
        
        # Első elválasztó vonal
        separator_frame1 = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_frame1.pack(fill="x", padx=20, pady=(10, 5))
        
        # Firebase projekt állapot szöveg
        self.firebase_status_frame = ctk.CTkFrame(self)
        self.firebase_status_frame.pack(fill="x", padx=10, pady=5)
        
        self.firebase_status_label = ctk.CTkLabel(
            self.firebase_status_frame,
            text=get_text("status_no_project", self.current_lang),
            font=("Arial", 12),
            text_color="red"
        )
        self.firebase_status_label.pack(pady=5)
        
        # Második elválasztó vonal
        separator_frame2 = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_frame2.pack(fill="x", padx=20, pady=(5, 10))
        
        # Műveletek
        actions_frame = ctk.CTkFrame(self)
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        self.deploy_btn = ctk.CTkButton(
            actions_frame,
            text=get_text("deploy_btn", self.current_lang),
            command=self.deploy,
            width=150,
            height=40,
            state="disabled"
        )
        self.deploy_btn.pack(side="left", padx=10, pady=10)
        
        self.build_deploy_btn = ctk.CTkButton(
            actions_frame,
            text=get_text("build_deploy_btn", self.current_lang),
            command=self.build_and_deploy,
            width=150,
            height=40,
            state="disabled"
        )
        self.build_deploy_btn.pack(side="left", padx=10, pady=10)
        
        self.serve_btn = ctk.CTkButton(
            actions_frame,
            text=get_text("serve_btn", self.current_lang),
            command=self.serve_local,
            width=150,
            height=40,
            state="disabled"
        )
        self.serve_btn.pack(side="left", padx=10, pady=10)
        
        self.stop_btn = ctk.CTkButton(
            actions_frame,
            text=get_text("stop_btn", self.current_lang),
            command=self.stop_processes,
            width=100,
            height=40,
            fg_color="#e53935"
        )
        self.stop_btn.pack(side="left", padx=10, pady=10)
        
        # Rollback gomb
        self.rollback_btn = ctk.CTkButton(
            actions_frame,
            text=get_text("rollback_btn", self.current_lang),
            command=self.show_rollback_dialog,
            width=120,
            height=40,
            fg_color="#ff6f00",
            state="disabled"
        )
        self.rollback_btn.pack(side="left", padx=10, pady=10)
        
        # Műveletek súgó gomb - jobbra igazítva
        self.actions_help_btn = ctk.CTkButton(
            actions_frame,
            text=get_text("actions_help_btn", self.current_lang),
            command=self.show_actions_help,
            width=80,
            height=40,
            fg_color="#607d8b"
        )
        self.actions_help_btn.pack(side="right", padx=10, pady=10)
        
        # Log ablak
        log_frame = ctk.CTkFrame(self)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(log_frame, text=get_text("output_label", self.current_lang), font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.log_text = ctk.CTkTextbox(log_frame, wrap="word", font=("Consolas", 11))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        
        # Alsó sáv: Rendszerinfó (bal) és Logout (jobb)
        bottom_bar = ctk.CTkFrame(log_frame)
        bottom_bar.pack(fill="x", padx=10, pady=5)
        
        # Rendszerinfó gomb bal oldalon
        self.sysinfo_btn = ctk.CTkButton(
            bottom_bar,
            text=get_text("sysinfo_btn", self.current_lang),
            command=self.show_system_info,
            width=130,
            height=35,
            fg_color="#607d8b"
        )
        self.sysinfo_btn.pack(side="left")
        
        # Logout gomb jobb oldalon
        self.logout_btn = ctk.CTkButton(
            bottom_bar,
            text=get_text("logout_btn", self.current_lang),
            command=self.do_logout,
            width=100,
            height=35,
            fg_color="#e53935",
            state="disabled"
        )
        self.logout_btn.pack(side="right")
    
    def browse_folder(self):
        """Mappa tallózó megnyitása"""
        # Legutóbbi mappák menü
        recent_folders = self.config.get_recent_folders()
        
        if recent_folders:
            # Popup menü a legutóbbi mappákkal
            menu_window = ctk.CTkToplevel(self)
            menu_window.title("Mappa választás")
            menu_window.geometry("500x300")
            menu_window.transient(self)
            menu_window.grab_set()
            
            ctk.CTkLabel(
                menu_window,
                text="Válassz mappát:",
                font=("Arial", 14, "bold")
            ).pack(pady=10)
            
            # Legutóbbi mappák
            if recent_folders:
                ctk.CTkLabel(
                    menu_window,
                    text="📁 Legutóbbi mappák:",
                    font=("Arial", 12)
                ).pack(pady=5)
                
                for folder in recent_folders:
                    if Path(folder).exists():
                        btn = ctk.CTkButton(
                            menu_window,
                            text=folder,
                            command=lambda f=folder: self.select_folder(f, menu_window),
                            width=450,
                            anchor="w"
                        )
                        btn.pack(pady=2, padx=20)
            
            # Tallózás gomb
            ctk.CTkButton(
                menu_window,
                text="📂 Új mappa tallózása...",
                command=lambda: self.browse_new_folder(menu_window),
                width=450,
                height=40,
                fg_color="#1e88e5"
            ).pack(pady=20, padx=20)
        else:
            # Nincs legutóbbi mappa, egyből tallózás
            self.browse_new_folder(None)
    
    def select_folder(self, folder: str, window):
        """Kiválaszt egy mappát"""
        self.folder_entry.delete(0, "end")
        self.folder_entry.insert(0, folder)
        window.destroy()
        self.check_firebase_project()
    
    def browse_new_folder(self, window):
        """Új mappa tallózása"""
        if window:
            window.destroy()
        
        folder = filedialog.askdirectory(
            title="Válassz Firebase projekt mappát",
            initialdir=self.folder_entry.get() or os.getcwd()
        )
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.check_firebase_project()
    
    def check_firebase_project(self):
        """Ellenőrzi, hogy érvényes Firebase projekt-e"""
        folder = self.folder_entry.get()
        if not folder:
            self.log_text.delete("1.0", "end")
            self.log(get_text("select_folder_msg", self.current_lang))
            self.firebase_status_label.configure(text=get_text("status_select_folder", self.current_lang), text_color="orange")
            return
        
        self.api.set_working_dir(folder)
        
        # Mappa mentése a konfigba
        self.config.set_last_folder(folder)
        
        if self.api.check_firebase_project():
            self.log_text.delete("1.0", "end")
            self.log(get_text("project_found_msg", self.current_lang))
            self.log(get_text("folder_msg", self.current_lang).format(folder))
            self.firebase_status_label.configure(text=get_text("status_project_found", self.current_lang), text_color="green")
            
            # Gombok engedélyezése
            self.deploy_btn.configure(state="normal")
            self.build_deploy_btn.configure(state="normal")
            self.serve_btn.configure(state="normal")
            self.rollback_btn.configure(state="normal")
            
            # Állapot ellenőrzés
            self.check_status()
        else:
            self.log_text.delete("1.0", "end")
            self.log(get_text("no_firebase_json", self.current_lang))
            self.log(get_text("folder_msg", self.current_lang).format(folder))
            self.log(get_text("tips_title", self.current_lang))
            self.log(get_text("tip_1", self.current_lang))
            self.log(get_text("tip_2", self.current_lang))
            self.firebase_status_label.configure(text=get_text("status_no_project", self.current_lang), text_color="red")
            
            # Gombok tiltása
            self.deploy_btn.configure(state="disabled")
            self.build_deploy_btn.configure(state="disabled")
            self.serve_btn.configure(state="disabled")
            self.rollback_btn.configure(state="disabled")
    
    def check_status(self):
        """Bejelentkezési állapot ellenőrzése"""
        def check():
            is_logged_in, message, email = self.api.check_login_status()
            self.after(0, lambda: self.update_status(is_logged_in, message, email))
            if is_logged_in:
                self.after(0, self.refresh_projects)
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_status(self, is_logged_in: bool, message: str, email: Optional[str]):
        """Állapot frissítése"""
        # Frissítjük a Firebase projekt állapot szöveget
        if is_logged_in:
            if email:
                self.firebase_status_label.configure(
                    text=f"✅ Firebase projekt megtalálva | 👤 {email}", 
                    text_color="green"
                )
            else:
                self.firebase_status_label.configure(
                    text=f"✅ Firebase projekt megtalálva | ✓ {message}", 
                    text_color="green"
                )
        
        # Login/Logout gombok kezelése
        if is_logged_in:
            self.login_btn.configure(text="✓ OK", fg_color="green", state="disabled")
            self.logout_btn.configure(state="normal")
        else:
            self.login_btn.configure(text="🔐 Login", fg_color="#ff9800", state="normal")
            self.logout_btn.configure(state="disabled")
        
        # Rollback gomb kezelése - csak JSON kulccsal aktív
        if self.api.has_json_key_active():
            self.rollback_btn.configure(state="normal", fg_color="#ff6f00")
        else:
            self.rollback_btn.configure(state="disabled", fg_color="gray")
    
    def do_login(self):
        """Firebase login indítása"""
        self.log_text.delete("1.0", "end")
        
        def login_callback(output: str, is_final: bool):
            self.log(output, is_final)
            if is_final:
                # Mindig frissítjük az állapotot login után
                self.after(1000, self.check_status)
        
        self.api.login(login_callback)
    
    def do_key_login(self):
        """Firebase login kulcsfájllal - DEPRECATED, használd az add_key-t"""
        self.add_key()
    
    def refresh_keys(self):
        """Frissíti a kulcsok listáját"""
        keys = self.api.get_available_keys()
        if keys:
            self.key_combo.configure(values=keys)
            self.key_combo.set(keys[0])
        else:
            self.key_combo.configure(values=[get_text("no_key", self.current_lang)])
            self.key_combo.set(get_text("no_key", self.current_lang))
    
    def add_key(self):
        """Új kulcs hozzáadása"""
        # Fájl választó megnyitása
        key_file = filedialog.askopenfilename(
            title="Válassz Service Account kulcsfájlt",
            filetypes=[("JSON fájlok", "*.json"), ("Minden fájl", "*.*")],
            initialdir=self.folder_entry.get() or os.getcwd()
        )
        
        if key_file:
            success, message = self.api.copy_key_to_keys_dir(key_file)
            
            self.log_text.delete("1.0", "end")
            if success:
                self.log(f"✅ {message}\n")
                self.log(f"📁 Kulcs helye: keys/{Path(key_file).name}\n")
                self.refresh_keys()
            else:
                self.log(f"❌ {message}\n")
    
    def use_selected_key(self):
        """A kiválasztott kulcs használata"""
        selected_key = self.key_combo.get()
        
        if selected_key == get_text("no_key", self.current_lang):
            self.log_text.delete("1.0", "end")
            self.log(get_text("no_key_selected", self.current_lang))
            self.log(get_text("use_add_key", self.current_lang))
            return
        
        # Kulcs mentése a konfigba
        self.config.set_last_key(selected_key)
        
        self.log_text.delete("1.0", "end")
        
        def key_login_callback(output: str, is_final: bool):
            self.log(output, is_final)
            if is_final:
                # Frissítjük az állapotot
                self.after(1000, self.check_status)
        
        self.api.login_with_key(selected_key, key_login_callback)
    
    def do_logout(self):
        """Firebase logout indítása"""
        self.log_text.delete("1.0", "end")
        
        def logout_callback(output: str, is_final: bool):
            self.log(output, is_final)
            if is_final:
                # Mindig frissítjük az állapotot logout után
                # Töröljük a környezeti változót is
                if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
                    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
                    self.log("\n🔑 Service Account kulcs törölve.\n")
                self.after(500, self.check_status)
        
        self.api.logout(logout_callback)
    
    def show_system_info(self):
        """Rendszerinformációk megjelenítése"""
        self.log_text.delete("1.0", "end")
        self.log("🔍 Rendszerinformációk ellenőrzése...\n\n")
        
        def check_versions():
            info = []
            
            # Operációs rendszer
            info.append(f"💻 Operációs rendszer: {platform.system()} {platform.release()}")
            info.append(f"📦 Platform: {platform.platform()}")
            info.append("")
            
            # Python verzió
            info.append(f"🐍 Python: {platform.python_version()}")
            info.append("")
            
            # Node.js verzió
            try:
                result = subprocess.run(
                    ["node", "--version"],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    info.append(f"✅ Node.js: {version}")
                else:
                    info.append("❌ Node.js: Nem telepítve")
            except:
                info.append("❌ Node.js: Nem telepítve")
            
            # npm verzió
            try:
                result = subprocess.run(
                    ["npm", "--version"],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    info.append(f"✅ npm: {version}")
                else:
                    info.append("❌ npm: Nem telepítve")
            except:
                info.append("❌ npm: Nem telepítve")
            
            # Firebase CLI verzió
            try:
                result = subprocess.run(
                    ["firebase", "--version"],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    info.append(f"✅ Firebase CLI: {version}")
                else:
                    info.append("❌ Firebase CLI: Nem telepítve")
            except:
                info.append("❌ Firebase CLI: Nem telepítve")
            
            info.append("")
            info.append("📚 Python modulok:")
            
            # Python modulok ellenőrzése
            modules = {
                "customtkinter": "CustomTkinter",
                "google.auth": "Google Auth",
                "google.oauth2.service_account": "Google Service Account",
                "requests": "Requests"
            }
            
            for module_name, display_name in modules.items():
                try:
                    mod = __import__(module_name)
                    # Verzió lekérése, ha van
                    version = getattr(mod, "__version__", "telepítve")
                    info.append(f"  ✅ {display_name}: {version}")
                except ImportError:
                    info.append(f"  ❌ {display_name}: Nincs telepítve")
            
            info.append("")
            
            # Firebase projekt info
            if self.api.working_dir:
                info.append(f"📁 Munkakönyvtár: {self.api.working_dir}")
                
                firebase_json = Path(self.api.working_dir) / "firebase.json"
                if firebase_json.exists():
                    info.append("✅ firebase.json: Megtalálva")
                else:
                    info.append("❌ firebase.json: Nem található")
                
                firebaserc = Path(self.api.working_dir) / ".firebaserc"
                if firebaserc.exists():
                    info.append("✅ .firebaserc: Megtalálva")
                    current_project = self.api.get_current_project()
                    if current_project:
                        info.append(f"📋 Aktuális projekt: {current_project}")
                else:
                    info.append("❌ .firebaserc: Nem található")
            
            info.append("")
            
            # JSON kulcs státusz
            if self.api.has_json_key_active():
                key_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'N/A')
                key_name = Path(key_path).name if key_path != 'N/A' else 'N/A'
                info.append(f"🔑 Aktív JSON kulcs: {key_name}")
                info.append("✅ REST API funkciók: Elérhetők")
            else:
                info.append("⚠️ Nincs aktív JSON kulcs")
                info.append("❌ REST API funkciók: Nem elérhetők")
            
            # Kiírás
            self.after(0, lambda: self.log("\n".join(info) + "\n"))
        
        # Háttérszálon futtatjuk
        threading.Thread(target=check_versions, daemon=True).start()
    
    def show_help(self):
        """Súgó ablak megjelenítése"""
        help_window = ctk.CTkToplevel(self)
        help_window.title(get_text("help_key_title", self.current_lang))
        help_window.geometry("600x400")
        help_window.transient(self)
        help_window.grab_set()
        
        # Fejléc
        header = ctk.CTkLabel(
            help_window,
            text=get_text("help_key_header", self.current_lang),
            font=("Arial", 18, "bold")
        )
        header.pack(pady=20)
        
        # Szöveg doboz az útmutatóval
        help_text = ctk.CTkTextbox(
            help_window,
            wrap="word",
            font=("Arial", 12),
            fg_color=("#f0f0f0", "#2b2b2b")
        )
        help_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Útmutató szöveg
        help_text.insert("1.0", get_text("help_key_content", self.current_lang))
        help_text.configure(state="disabled")  # Csak olvasható
        
        # Bezárás gomb
        close_btn = ctk.CTkButton(
            help_window,
            text=get_text("close_btn", self.current_lang),
            command=help_window.destroy,
            width=120,
            height=35
        )
        close_btn.pack(pady=15)
    
    def show_login_help(self):
        """Login súgó ablak megjelenítése"""
        help_window = ctk.CTkToplevel(self)
        help_window.title(get_text("help_login_title", self.current_lang))
        help_window.geometry("600x400")
        help_window.transient(self)
        help_window.grab_set()
        
        # Fejléc
        header = ctk.CTkLabel(
            help_window,
            text=get_text("help_login_header", self.current_lang),
            font=("Arial", 18, "bold")
        )
        header.pack(pady=20)
        
        # Szöveg doboz az útmutatóval
        help_text = ctk.CTkTextbox(
            help_window,
            wrap="word",
            font=("Arial", 12),
            fg_color=("#f0f0f0", "#2b2b2b")
        )
        help_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Útmutató szöveg
        help_text.insert("1.0", get_text("help_login_content", self.current_lang))
        help_text.configure(state="disabled")  # Csak olvasható
        
        # Bezárás gomb
        close_btn = ctk.CTkButton(
            help_window,
            text=get_text("close_btn", self.current_lang),
            command=help_window.destroy,
            width=120,
            height=35
        )
        close_btn.pack(pady=15)
    
    def show_actions_help(self):
        """Műveletek súgó ablak megjelenítése"""
        help_window = ctk.CTkToplevel(self)
        help_window.title(get_text("help_actions_title", self.current_lang))
        help_window.geometry("650x500")
        help_window.transient(self)
        help_window.grab_set()
        
        # Fejléc
        header = ctk.CTkLabel(
            help_window,
            text=get_text("help_actions_header", self.current_lang),
            font=("Arial", 18, "bold")
        )
        header.pack(pady=20)
        
        # Szöveg doboz az útmutatóval
        help_text = ctk.CTkTextbox(
            help_window,
            wrap="word",
            font=("Arial", 11),
            fg_color=("#f0f0f0", "#2b2b2b")
        )
        help_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Útmutató szöveg
        help_text.insert("1.0", get_text("help_actions_content", self.current_lang))
        help_text.configure(state="disabled")  # Csak olvasható
        
        # Bezárás gomb
        close_btn = ctk.CTkButton(
            help_window,
            text=get_text("close_btn", self.current_lang),
            command=help_window.destroy,
            width=120,
            height=35
        )
        close_btn.pack(pady=15)
    
    def refresh_projects(self):
        """Projektek frissítése"""
        def fetch():
            projects = self.api.get_projects()
            current = self.api.get_current_project()
            self.after(0, lambda: self.update_projects(projects, current))
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def update_projects(self, projects: list[dict], current: Optional[str]):
        """Projekt lista frissítése"""
        if projects:
            project_names = [p.get("projectId", p.get("id", "")) for p in projects]
            self.project_combo.configure(values=project_names)
            if current and current in project_names:
                self.project_combo.set(current)
            elif project_names:
                self.project_combo.set(project_names[0])
        else:
            self.project_combo.configure(values=[get_text("no_project", self.current_lang)])
    
    def log(self, message: str, is_final: bool = False):
        """Üzenet hozzáadása a loghoz"""
        self.log_text.insert("end", message)
        self.log_text.see("end")
    
    def deploy(self):
        """Firebase deploy futtatása"""
        self.log_text.delete("1.0", "end")
        self.log(get_text("deploy_starting", self.current_lang))
        self.api.run_command_async(["firebase", "deploy"], self.log)
    
    def build_and_deploy(self):
        """Build + Deploy futtatása"""
        self.log_text.delete("1.0", "end")
        self.log(get_text("build_starting", self.current_lang))
        
        def build_then_deploy(output: str, is_final: bool):
            self.log(output, is_final)
            if is_final and "✓ Sikeres" in output:
                self.log(get_text("deploy_after_build", self.current_lang))
                self.api.run_command_async(["firebase", "deploy"], self.log)
        
        self.api.run_command_async(["npm", "run", "build"], build_then_deploy)
    
    def serve_local(self):
        """Helyi szerver indítása"""
        self.log_text.delete("1.0", "end")
        self.log(get_text("serve_starting", self.current_lang))
        self.log(get_text("serve_info", self.current_lang))
        self.api.run_command_async(["firebase", "serve"], self.log)
    
    def stop_processes(self):
        """Leállítja a futó folyamatokat"""
        self.api.stop_all_processes()
        self.log(get_text("processes_stopped", self.current_lang))
    
    def show_rollback_dialog(self):
        """Rollback párbeszédablak megjelenítése verziólistával (REST API - JSON kulcs szükséges)"""
        # Ellenőrizzük, hogy van-e aktív JSON kulcs
        if not self.api.has_json_key_active():
            messagebox.showwarning(
                get_text("json_key_required_title", self.current_lang),
                get_text("json_key_required_msg", self.current_lang)
            )
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(get_text("rollback_dialog_title", self.current_lang))
        dialog.geometry("1000x650")
        dialog.transient(self)
        dialog.grab_set()
        
        # Fejléc
        header = ctk.CTkLabel(
            dialog,
            text=get_text("rollback_dialog_header", self.current_lang),
            font=("Arial", 16, "bold")
        )
        header.pack(pady=15)
        
        # Info
        info_text = "🔑 Authenticated with JSON key - Using REST API" if self.current_lang == "en" else "🔑 JSON kulccsal hitelesítve - REST API használatban"
        info = ctk.CTkLabel(
            dialog,
            text=info_text,
            font=("Arial", 11),
            text_color="green"
        )
        info.pack(pady=5)
        
        # Figyelmeztetés
        warning_text = "⚠️ WARNING: Selected version will go live immediately!" if self.current_lang == "en" else "⚠️ FIGYELEM: A kiválasztott verzió azonnal élesbe kerül!"
        warning = ctk.CTkLabel(
            dialog,
            text=warning_text,
            font=("Arial", 12, "bold"),
            text_color="orange"
        )
        warning.pack(pady=10)
        
        # Betöltés állapot
        loading_text = "📋 Loading versions via REST API..." if self.current_lang == "en" else "📋 Verziók betöltése REST API-val..."
        loading_label = ctk.CTkLabel(
            dialog,
            text=loading_text,
            font=("Arial", 12)
        )
        loading_label.pack(pady=10)
        
        # Verziók táblázat frame
        table_frame = ctk.CTkScrollableFrame(dialog, height=350)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Kiválasztott verzió
        selected_version = {"name": None, "button": None}
        
        def load_versions():
            """Verziók betöltése REST API-val háttérszálon"""
            # Lekérjük, mi van éppen kiválasztva a UI-on
            current_selected_project = self.project_combo.get()
            
            # REST API hívás
            success, releases = self.api.get_hosting_releases_rest(current_selected_project)
            
            def update_ui():
                loading_label.configure(text="")
                
                if not success or not releases:
                    error_msg = (
                        "❌ Failed to load versions.\n\n"
                        "Possible causes:\n"
                        "• No deployed versions yet\n"
                        "• JSON key doesn't have proper permissions\n"
                        "• Network error\n\n"
                        "💡 Solution:\n"
                        "1. Check that JSON key has 'Firebase Hosting Admin' permission\n"
                        "2. Check console output for details\n"
                        "3. Use Firebase Console: click the button below!"
                    ) if self.current_lang == "en" else (
                        "❌ Nem sikerült betölteni a verziókat.\n\n"
                        "Lehetséges okok:\n"
                        "• Nincs még deploy-olt verzió\n"
                        "• A JSON kulcs nem rendelkezik megfelelő jogosultságokkal\n"
                        "• Hálózati hiba\n\n"
                        "💡 Megoldás:\n"
                        "1. Ellenőrizd, hogy a JSON kulcs 'Firebase Hosting Admin' jogosultsággal rendelkezik\n"
                        "2. Nézd meg a konzol kimenetét a részletekért\n"
                        "3. Használd a Firebase Console-t: kattints a gombra alul!"
                    )
                    no_data_label = ctk.CTkLabel(
                        table_frame,
                        text=error_msg,
                        font=("Arial", 11),
                        text_color="orange",
                        justify="left"
                    )
                    no_data_label.pack(pady=20)
                    return
                
                # Táblázat fejléc
                header_frame = ctk.CTkFrame(table_frame)
                header_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(header_frame, text=get_text("rollback_version_id", self.current_lang), font=("Arial", 11, "bold"), width=200).pack(side="left", padx=5)
                ctk.CTkLabel(header_frame, text=get_text("rollback_date", self.current_lang), font=("Arial", 11, "bold"), width=150).pack(side="left", padx=5)
                type_text = "Type" if self.current_lang == "en" else "Típus"
                message_text = "Message" if self.current_lang == "en" else "Üzenet"
                ctk.CTkLabel(header_frame, text=type_text, font=("Arial", 11, "bold"), width=100).pack(side="left", padx=5)
                ctk.CTkLabel(header_frame, text=message_text, font=("Arial", 11, "bold"), width=250).pack(side="left", padx=5)
                ctk.CTkLabel(header_frame, text="", font=("Arial", 11, "bold"), width=120).pack(side="left", padx=5)
                
                # Verziók listázása
                for idx, release in enumerate(releases[:15]):  # Első 15 verzió
                    # Release name: projects/PROJECT/sites/SITE/releases/RELEASE_ID
                    release_name = release.get('name', f'Release {idx+1}')
                    release_id = release_name.split('/')[-1] if '/' in release_name else release_name
                    
                    # Időbélyeg
                    create_time = release.get('version', {}).get('createTime', release.get('createTime', 'N/A'))
                    
                    # Dátum formázása
                    try:
                        from datetime import datetime
                        if 'T' in str(create_time):
                            dt = datetime.fromisoformat(str(create_time).replace('Z', '+00:00'))
                            date_str = dt.strftime('%Y-%m-%d %H:%M')
                        else:
                            date_str = str(create_time)[:16]
                    except:
                        date_str = str(create_time)[:16]
                    
                    # Típus
                    release_type = release.get('type', 'DEPLOY')
                    
                    # Üzenet
                    message = release.get('message', release.get('version', {}).get('labels', {}).get('message', '-'))
                    if len(message) > 35:
                        message = message[:32] + "..."
                    
                    # Verzió sor
                    row_frame = ctk.CTkFrame(table_frame)
                    row_frame.pack(fill="x", pady=2)
                    
                    ctk.CTkLabel(row_frame, text=release_id[:28], width=200, anchor="w", font=("Arial", 10)).pack(side="left", padx=5)
                    ctk.CTkLabel(row_frame, text=date_str, width=150, anchor="w").pack(side="left", padx=5)
                    
                    type_color = "green" if release_type == "DEPLOY" else "orange"
                    ctk.CTkLabel(row_frame, text=release_type, width=100, anchor="w", text_color=type_color).pack(side="left", padx=5)
                    ctk.CTkLabel(row_frame, text=message, width=250, anchor="w", font=("Arial", 9)).pack(side="left", padx=5)
                    
                    # Kiválasztás gomb
                    def make_select_callback(r_name, r_id, btn_ref):
                        def callback():
                            # Előző gomb visszaállítása
                            if selected_version["button"]:
                                selected_version["button"].configure(fg_color="#1e88e5", text=get_text("rollback_select", self.current_lang))
                            # Új gomb kijelölése
                            btn_ref.configure(fg_color="green", text=get_text("rollback_selected", self.current_lang))
                            selected_version["name"] = r_name
                            selected_version["id"] = r_id
                            selected_version["button"] = btn_ref
                        return callback
                    
                    select_btn = ctk.CTkButton(
                        row_frame,
                        text=get_text("rollback_select", self.current_lang),
                        width=120,
                        height=28,
                        fg_color="#1e88e5"
                    )
                    select_btn.configure(command=make_select_callback(release_name, release_id, select_btn))
                    select_btn.pack(side="left", padx=5)
            
            dialog.after(0, update_ui)
        
        # Verziók betöltése háttérszálon
        threading.Thread(target=load_versions, daemon=True).start()
        
        # Alsó gombok
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=20)
        
        def do_rollback():
            if not selected_version.get("name"):
                messagebox.showwarning(
                    get_text("rollback_no_selection", self.current_lang),
                    get_text("rollback_select_version", self.current_lang)
                )
                return
            
            # Megerősítés
            confirm = messagebox.askyesno(
                get_text("rollback_confirm_title", self.current_lang),
                get_text("rollback_confirm_msg", self.current_lang).format(selected_version.get('id', 'N/A'))
            )
            
            if confirm:
                dialog.destroy()
                self.log_text.delete("1.0", "end")
                
                def rollback_callback(output: str, is_final: bool):
                    self.log(output, is_final)
                
                # REST API rollback
                current_project = self.project_combo.get()
                self.api.rollback_to_version_rest(current_project, selected_version["name"], rollback_callback)
        
        rollback_btn = ctk.CTkButton(
            button_frame,
            text=get_text("rollback_execute", self.current_lang),
            command=do_rollback,
            width=200,
            height=40,
            fg_color="#ff6f00"
        )
        rollback_btn.pack(side="left", padx=10)
        
        console_btn = ctk.CTkButton(
            button_frame,
            text=get_text("rollback_console", self.current_lang),
            command=lambda: self.open_firebase_console(),
            width=180,
            height=40,
            fg_color="#1e88e5"
        )
        console_btn.pack(side="left", padx=10)
        
        close_btn = ctk.CTkButton(
            button_frame,
            text=get_text("close_btn", self.current_lang),
            command=dialog.destroy,
            width=120,
            height=40
        )
        close_btn.pack(side="left", padx=10)
    
    def open_firebase_console(self):
        """Megnyitja a Firebase Console-t a böngészőben"""
        import webbrowser
        webbrowser.open("https://console.firebase.google.com/")
        self.log_text.delete("1.0", "end")
        self.log("🌐 Firebase Console megnyitva a böngészőben.\n")
        self.log("📍 Navigálj: Hosting → Release history → Rollback\n")
    
    def on_closing(self):
        """Ablak bezáráskor"""
        # Ablak méret mentése
        width = self.winfo_width()
        height = self.winfo_height()
        self.config.set_window_size(width, height)
        
        # Folyamatok leállítása
        self.api.stop_all_processes()
        self.destroy()
    
    def change_language(self, choice):
        """Nyelv váltása"""
        new_lang = "en" if choice == "English" else "hu"
        if new_lang != self.current_lang:
            self.current_lang = new_lang
            self.config.set_language(new_lang)
            
            # Újraindítás üzenet
            messagebox.showinfo(
                "Language Changed" if new_lang == "en" else "Nyelv megváltoztatva",
                "Please restart the application to apply the language change.\n\nKérlek indítsd újra az alkalmazást a nyelv alkalmazásához." if new_lang == "en" else "Kérlek indítsd újra az alkalmazást a nyelv alkalmazásához.\n\nPlease restart the application to apply the language change."
            )
    
    def check_prerequisites(self):
        """Ellenőrzi a szükséges eszközöket"""
        def check():
            all_ok, missing = self.api.check_prerequisites()
            if not all_ok:
                self.after(0, lambda: self.show_prerequisites_warning(missing))
        
        threading.Thread(target=check, daemon=True).start()
    
    def show_prerequisites_warning(self, missing: list[str]):
        """Figyelmeztetés megjelenítése a hiányzó eszközökről"""
        missing_str = "\n".join([f"  • {item}" for item in missing])
        message = get_text("prereq_warning", self.current_lang).format(missing_str)
        
        # Telepítési útmutatók
        install_guide = get_text("prereq_install_guide", self.current_lang)
        
        if "Node.js" in missing_str:
            install_guide += get_text("prereq_nodejs", self.current_lang)
        if "npm" in missing_str:
            install_guide += get_text("prereq_npm", self.current_lang)
        if "Firebase CLI" in missing_str:
            install_guide += get_text("prereq_firebase", self.current_lang)
        if "Python modul" in missing_str or "Python module" in missing_str:
            install_guide += get_text("prereq_python", self.current_lang)
            install_guide += get_text("prereq_run_in_folder", self.current_lang)
        
        install_guide += get_text("prereq_final_warning", self.current_lang)
        
        self.log_text.delete("1.0", "end")
        self.log(message)
        self.log(install_guide)
        
        # Popup figyelmeztetés is
        messagebox.showwarning(
            get_text("prereq_missing_title", self.current_lang),
            get_text("prereq_missing_msg", self.current_lang).format(missing_str)
        )


if __name__ == "__main__":
    app = FirebaseManagerApp()
    app.mainloop()
