from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

class ItemForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=100), validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=1, max=200), validators.DataRequired()])

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        new_item = Item(name=form.name.data, description=form.description.data)
        db.session.add(new_item)
        db.session.commit()
        flash('Item created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)
    form = ItemForm(request.form, obj=item)
    if request.method == 'POST' and form.validate():
        item.name = form.name.data
        item.description = form.description.data
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('update.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/detail/<int:id>')
def detail(id):
    item = Item.query.get_or_404(id)
    return render_template('detail.html', item=item)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
