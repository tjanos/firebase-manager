# Contributing to Firebase Manager

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists or is planned
- Describe the feature and its use case
- Explain why it would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

### Adding Translations

To add a new language:

1. Edit `translations.py`
2. Add a new language code to the `TRANSLATIONS` dictionary
3. Translate all keys from English
4. Update the language selector in `firebase_manager.py`
5. Test all UI elements in the new language

### Testing

Before submitting:
- Test on your local machine
- Verify all features work
- Check for Python errors
- Test language switching
- Ensure no sensitive data is committed

### Security

- Never commit Service Account keys
- Never commit personal configuration files
- Report security issues privately

## Questions?

Feel free to open an issue for any questions!

---

# Közreműködés a Firebase Manager projektben

Köszönjük az érdeklődésedet! 🎉

## Hogyan Közreműködhetsz

### Hibák Jelentése

Ha hibát találsz, nyiss egy issue-t a következőkkel:
- A probléma egyértelmű leírása
- Reprodukálási lépések
- Elvárt vs valós viselkedés
- Képernyőképek, ha van
- Környezeted (OS, Python verzió, stb.)

### Funkciók Javaslása

Funkciójavaslatokat szívesen fogadunk! Kérlek:
- Ellenőrizd, hogy a funkció már létezik-e vagy tervben van
- Írd le a funkciót és használati esetét
- Magyarázd el, miért lenne hasznos

### Pull Request-ek

1. Fork-old a repository-t
2. Hozz létre új branch-et (`git checkout -b feature/amazing-feature`)
3. Végezd el a módosításokat
4. Teszteld alaposan
5. Commitold a változtatásokat (`git commit -m 'Add amazing feature'`)
6. Push-old a branch-re (`git push origin feature/amazing-feature`)
7. Nyiss Pull Request-et

### Kódstílus

- Kövesd a PEP 8-at Python kódnál
- Használj beszédes változó- és függvényneveket
- Adj hozzá kommenteket komplex logikához
- Tartsd a függvényeket fókuszáltnak és kicsinek

### Fordítások Hozzáadása

Új nyelv hozzáadásához:

1. Szerkeszd a `translations.py` fájlt
2. Adj hozzá új nyelvi kódot a `TRANSLATIONS` szótárhoz
3. Fordítsd le az összes kulcsot angolról
4. Frissítsd a nyelvválasztót a `firebase_manager.py`-ban
5. Teszteld az összes UI elemet az új nyelven

### Tesztelés

Beküldés előtt:
- Tesztelj a saját gépeden
- Ellenőrizd, hogy minden funkció működik
- Nézd át a Python hibákat
- Teszteld a nyelvváltást
- Győződj meg róla, hogy nincs érzékeny adat commitolva

### Biztonság

- Soha ne commitálj Service Account kulcsokat
- Soha ne commitálj személyes konfigurációs fájlokat
- Biztonsági problémákat privát módon jelents

## Kérdések?

Nyugodtan nyiss issue-t bármilyen kérdéssel!
