from sqlalchemy import create_engine, select, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from parse import date_list, region_list, type_list, situation_list, victims_list, injured_list

engine = create_engine('mysql+mysqlconnector://ivan:0123456789@localhost/MYSQL', echo=True)
Base = declarative_base()

session = sessionmaker(bind=engine)
s = session()

class Users(Base):
    __tablename__ = 'users_table'

    id = Column(Integer, primary_key=True)
    login = Column(String(80))
    passw = Column(String(80))

class News(Base):
    __tablename__ = 'news_table'

    id = Column(Integer, primary_key=True)
    date = Column(String(80))
    region = Column(String(80))
    type = Column(String(80))
    situation = Column(String(80))
    victims = Column(String(80))
    injured = Column(String(80))

# Base.metadata.create_all(engine)

# results = s.query(News).first()
# print(results.date)

# user = Users(login='root', password='mypassword')
# s.add(user)
# s.commit()


def add_info():
    for i in range(len(date_list)):
        np = News(date=date_list[i], region=region_list[i], type=type_list[i],
                  situation=situation_list[i], victims=victims_list[i],
                  injured=injured_list[i])
        s.add(np)
    user = Users(login='root', passw='mypassword')
    s.add(user)
    s.commit()


def delete_tables():
    # Base.metadata.drop_all(bind = engine, tables = [News.__table__])
    Base.metadata.drop_all(engine)
    s.commit()

# add_info()
#
# delete_tables()


# db_result = s.query(News).all()
# for row in db_result:
#     print (row.id, row.date, row.region, row.type, row.situation, row.victims, row.injured)