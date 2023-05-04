from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    importance = db.Column(db.String(20), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Note %r>' % self.id



@app.route('/')
@app.route('/notes', methods=['POST', 'GET'])
def notes():
    if request.method == 'POST':
        importance = request.form['importance']
        text = request.form['text']
        note = Note(importance=importance, text=text)
        try:
            db.session.add(note)
            db.session.commit()
            return redirect('/list')
        except:
            return 'Error'
    else:
        return render_template('notes.html')


@app.route('/list')
def list():
    lists = Note.query.order_by(Note.date.desc()).all()
    return render_template("list.html", list=lists)


if __name__ == '__main__':
    app.run(debug=True)
