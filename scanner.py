import os
from datetime import datetime
from app import app, db, Project, Document
import spacy
from rake_nltk import Rake

# Laden des deutschen Sprachmodells für spaCy
nlp = spacy.load('de_core_news_sm')

def extract_keywords(text):
    rake_nltk_var = Rake(language='german')
    rake_nltk_var.extract_keywords_from_text(text)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    keywords = keyword_extracted[:10]  # Begrenzen auf die Top 10 Keywords
    return keywords

def extract_content(file_path):
    text = ''
    if file_path.endswith('.pdf'):
        from PyPDF2 import PdfReader
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            print(f'Fehler beim Extrahieren von {file_path}: {e}')
    # Weitere Dateitypen können hier hinzugefügt werden

    keywords = extract_keywords(text)
    return text, keywords

def scan_files(root_directory):
    with app.app_context():
        for dirpath, dirnames, filenames in os.walk(root_directory):
            relative_path = os.path.relpath(dirpath, root_directory)
            path_parts = relative_path.split(os.sep)
            if len(path_parts) >= 1:
                module_name = path_parts[0]
            else:
                continue

            project = Project.query.filter_by(name=module_name).first()
            if not project:
                project = Project(name=module_name)
                db.session.add(project)
                db.session.commit()

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                stat = os.stat(file_path)
                created = datetime.fromtimestamp(stat.st_ctime)
                modified = datetime.fromtimestamp(stat.st_mtime)

                # Dokumenttyp bestimmen
                if 'vorlesung' in filename.lower():
                    doc_type = 'Vorlesung'
                elif 'übung' in filename.lower() or 'uebung' in filename.lower():
                    doc_type = 'Übung'
                else:
                    doc_type = 'Sonstiges'

                content, keywords = extract_content(file_path)
                keywords_str = ','.join(keywords)

                document = Document.query.filter_by(path=file_path).first()
                if not document:
                    document = Document(
                        name=filename,
                        path=file_path,
                        created_at=created,
                        modified_at=modified,
                        keywords=keywords_str,
                        doc_type=doc_type,
                        project_id=project.id
                    )
                    db.session.add(document)
                else:
                    document.modified_at = modified
                    document.keywords = keywords_str
                    document.doc_type = doc_type
                db.session.commit()

def index_files():
    from whoosh.index import create_in, open_dir
    from whoosh.fields import Schema, TEXT, ID
    import os

    # Schema definieren
    schema = Schema(
        path=ID(unique=True, stored=True),
        content=TEXT,
        project=TEXT,
        keywords=TEXT
    )

    index_dir = "indexdir"
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        ix = create_in(index_dir, schema)
    else:
        ix = open_dir(index_dir)

    writer = ix.writer()
    with app.app_context():
        for document in Document.query.all():
            content, _ = extract_content(document.path)
            writer.update_document(
                path=document.path,
                content=content,
                project=document.project.name,
                keywords=document.keywords
            )
    writer.commit()

if __name__ == "__main__":
    root_directory = '/home/aaron/projects/test-data/Semester'  # Ersetzen Sie diesen Pfad entsprechend
    scan_files(root_directory)
    index_files()