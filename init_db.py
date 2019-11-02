from main import db, Fighter, Votes, User

db.create_all()

john = Fighter(name="John Cena")
rock = Fighter(name="The Rock")

db.session.add(john)
db.session.add(rock)

db.session.commit()
