# doc-joerg
py# Dokumentenmanagement-System

Ein Prototyp für ein Dokumentenmanagement- und Projektverfolgungssystem.

## Installation

1. **Erstellen und aktivieren Sie ein virtuelles Python-Umfeld:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Für Unix/MacOS
   # Oder für Windows
   venv\Scripts\activate
   ```

2. **Installieren Sie alle erforderlichen Pakete:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Installieren Sie das deutsche Sprachmodell für spaCy:**

   ```bash
   python -m spacy download de_core_news_sm
   ```

4. **Initialisieren Sie die Datenbank mit Flask-Migrate:**

   - Setzen Sie die Umgebungsvariable:

     - Unix/MacOS:

       ```bash
       export FLASK_APP=app.py
       ```

     - Windows:

       ```bash
       set FLASK_APP=app.py
       ```

   - Führen Sie die Migrationen durch:

     ```bash
     flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade
     ```

5. **Passen Sie den Pfad in `scanner.py` an:**

   - Öffnen Sie `scanner.py` und ersetzen Sie `'/Pfad/zu/Ihren/Dateien'` durch den tatsächlichen Pfad zu Ihrem Dateiverzeichnis:

     ```python
     root_directory = '/Pfad/zu/Ihren/Dateien'  # Ersetzen Sie diesen Pfad entsprechend
     ```

6. **Führen Sie `scanner.py` aus, um die Dateien zu scannen und den Index zu erstellen:**

   ```bash
   python scanner.py
   ```

   - Dies erstellt die Datenbankeinträge und den Whoosh-Index.

7. **Starten Sie die Flask-Anwendung:**

   ```bash
   python app.py
   ```

8. **Öffnen Sie die Anwendung in Ihrem Browser:**

   - Navigieren Sie zu `http://127.0.0.1:5000/`

9. **Testen Sie die Suchfunktion:**

   - Verwenden Sie das Suchfeld, um nach Themen oder Schlagworten zu suchen.

