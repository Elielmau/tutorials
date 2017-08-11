# Import the database object (db) from the main application module
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created    = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified   = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Define a chore model: contains the chores to be completed by the kids
class Chore(Base):

    __tablename__ = 'chore'

    #  Title: short description of the chore
    title =db.Column(db.Text, nullable=False)

    # Owner: Name of the responsible of the chore
    owner =db.Column(db.Text, nullable=False)

    # Status: 0: Completed, 1: Pending
    status =db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, title, owner, status):
        self.title = title
        self.owner = owner
        self.status = status

    def __repr__(self):
        return '<Chore %r>' % self.title