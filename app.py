from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Konfiguration der Datenbank
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Definition der Modelle
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    documents = db.relationship('Document', backref='project', lazy=True)

    def __repr__(self):
        return f'<Project {self.name}>'

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(500), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
    keywords = db.Column(db.Text)
    doc_type = db.Column(db.String(50))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f'<Document {self.name}>'

@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('home.html', projects=projects)

@app.route('/search')
def search():
    query_str = request.args.get('q', '')
    doc_type = request.args.get('doc_type', '')

    from whoosh.index import open_dir
    from whoosh.qparser import MultifieldParser

    ix = open_dir("indexdir")
    parser = MultifieldParser(["content", "keywords"], schema=ix.schema)
    query = parser.parse(query_str)

    with ix.searcher() as searcher:
        results = searcher.search(query, limit=None)
        documents = []
        for result in results:
            document = Document.query.filter_by(path=result['path']).first()
            if document:
                if doc_type and document.doc_type != doc_type:
                    continue
                documents.append(document)
    return render_template('search_results.html', documents=documents, query=query_str)

if __name__ == '__main__':
    app.run(debug=True)