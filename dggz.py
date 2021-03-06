from flask import Flask, url_for, request
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext import admin
from flask.ext.sqlalchemy import SQLAlchemy
import os
import os.path as op


# Create App	
app = Flask(__name__)


# create boxes on bio page


def makeCheckers(rows):
    rows = int(rows)
    row=[]
    col=[]
    cnt=0
    for i in range(rows):
        col=[]
        for t in range(rows):
            cnt += 1
            col.append('box '+str(cnt))
        row.insert(i, col)
    return row
        

# Create secret key 
app.config['SECRET_KEY'] = '123456790'

# Create db
app.config['DATABASE_FILE'] = 'dggz_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#db models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    email = db.Column(db.Unicode(64))
    tmppass = db.Column(db.Unicode(64))

    def __unicode__(self):
        return self.name
		
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(64))
    content = db.Column(db.UnicodeText)

    def __unicode__(self):
        return self.name
		
# admin models

class CustomView(ModelView):
	pass
	"""
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'
 	"""

class UserAdmin(CustomView):
    column_searchable_list = ('name',)
    column_filters = ('name', 'email', 'tmppass')

# Create custom admin views

cnt = 0

class BioView(BaseView):
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        """"
        This is a work around that must be fixed!!
        """
        global cnt
        cnt += 1
        if cnt != 1:
            boxesper = request.args['boxesper']
        else:
            boxesper = 3
        return self.render('bio.html',test=makeCheckers(boxesper))

class TestDropView1(BaseView):
    @expose('/')
    def index(self):
        return self.render('test1.html')
	
class TestDropView2(BaseView):
    @expose('/')
    def index(self):
        return self.render('test2.html')
		
# Flask views

@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'
    
@app.route('/bio')
def testrun():
    return 'the script actually ran'
	
# Create admin interface

admin = Admin(app, base_template='layout.html', name='DGGZ')

# Add views

admin.add_view(TestDropView1(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(TestDropView2(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(BioView(name='Bio', endpoint='bio'))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(CustomView(Page, db.session))

# Create db with data

def build_dggz_db():
   
    db.drop_all()
    db.create_all()

    first_names = [
        'Deriv', 'Eddie', 'Jack', 'Carl', 'Leonardo', 'Bill', 'Bettie', 'Kim',
        'Jessica', 'Thomas', 'Honey', 'John', 'Bill', 'Prince', 'Teddy', 'Saraha', 'Barbi',
        'Steve', 'William', 'Bobby', 'Chris', 'Lisa', 'Benjamin', 'Coutney', 'Alex'
    ]
    last_names = [
        'Diggs', 'Murphy', 'Ripper', 'Seagan', 'DaVinci', 'Murry', 'Davis', 'Kardasian',
        'Alba', 'Edison', 'Booboo', 'Kennedy', 'Clinton', 'Nelson', 'Riley', 'Conners',
        'Bush', 'Martin', 'Tell', 'Brown', 'Brown', 'Love', 'Button', 'Cox', 'Alexander'
    ]

    for i in range(len(first_names)):
        user = User()
        user.name = first_names[i] + " " + last_names[i]
        user.email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
        tmppass_first = ""
        tmppass_last = ""
        for t in range(3):
            if first_names[i].lower()[t] != "":
                tmppass_first += first_names[i].lower()[t]
            else:
                tmppass_first += "x"
            if last_names[i].lower()[t] != "":
                tmppass_last += last_names[i].lower()[t]
            else:
                tmppass_last += "x"
        user.tmppass = tmppass_first + tmppass_last
        db.session.add(user)

    sample_text = [
        {
            'title': "Some more data 1",
            'content': "Data data data data data data data data data data. Data data data data data data data \
						data data data. Data data data data data data data data data data. Data data data data \
						data data data data data data. Data data data data data data data data data data. Data \
						data data data data data data data data data."
        },
        {
            'title': "Some more data 2",
            'content': "Data data data data data data data data data data. Data data data data data data data \
						data data data. Data data data data data data data data data data. Data data data data \
						data data data data data data. Data data data data data data data data data data. Data \
						data data data data data data data data data."
        },
        {
            'title': "Some more data 3",
            'content': "Data data data data data data data data data data. Data data data data data data data \
						data data data. Data data data data data data data data data data. Data data data data \
						data data data data data data. Data data data data data data data data data data. Data \
						data data data data data data data data data."
        }
    ]

    for entry in sample_text:
        page = Page()
        page.title = entry['title']
        page.content = entry['content']
        db.session.add(page)

    db.session.commit()
    return

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_dggz_db()

    # Start app
    app.debug = True
    app.run()