from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Books.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

# class Customers(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     city =  db.Column(db.String(50), nullable=False)

#     def __init__(self, name, age, city):
#         self.name = name
#         self.age = age
#         self.city = city


# class Loans(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     customers_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('Books.id'), nullable=False)
#     loan_date = db.Column(db.Date, nullable=False)
#     return_date = db.Column(db.Date, nullable=False)

#     def __init__(self, customers_id, book_id, loan_date, return_date):
#         self.customers_id = customers_id
#         self.book_id = book_id
#         self.loan_date = loan_date
#         self.return_date = return_date
        

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, name, author, published_year, type):
        self.name = name
        self.author = author
        self.published_year = published_year
        self.type = type


@app.route("/")
def home():
    return  render_template('index.html') 


######## show books data ########
@app.route("/data/<ind>")
@app.route("/data/")
def books_data(ind =-1):
    # one book
    if int(ind) > -1:
        book=Books.query.get(int(ind))
        return render_template('data.html',book=book) 
    # all books
    return render_template('data_all.html',books= Books.query.all()) 


######## add a book ########
@app.route("/add_book/", methods=['POST','GET'])
def add_book():
    request_data = request.get_json()
    name= request_data["name"]
    author= request_data["author"]
    published_year= request_data["published_year"]
    type= request_data["type"]
 
 
    newbook= Books(name, author, published_year, type)
    db.session.add (newbook)
    db.session.commit()
    return "a new book added"

######## delete a book ########
@app.route("/delete/<ind>", methods=['DELETE','GET'])
def delete_book(ind=-1):
        book=Books.query.get(int(ind))
        if book:
            db.session.delete(book)
            db.session.commit()
            return f"book delete {book.name}"
        return f"no such book"


######## update a book ########
@app.route("/update/<ind>", methods=['PUT'])
def update_book(ind=-1):
    if int(ind) > -1:
        data = request.json
        uname = (data["name"])
        book=Books.query.get(int(ind))
        if book:
            book.name=uname
            db.session.commit()
            return "book update"
        return "no such book to update"


######## add Customers ########
# @app.route("/add_Customers/", methods=['POST'])
# def add_Customers():
#     request_data = request.get_json()
#     name= request_data["name"]
 
#     newCustomers= Customers(name)
#     db.session.add (newCustomers)
#     db.session.commit()
#     return "a new rcord was create"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

