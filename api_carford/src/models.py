from sqlalchemy import Enum, ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import enum



engine = create_engine('postgresql+psycopg2://sdggutzkbjtfgo:d7c2796423a179df69c61fac6b06f4820c742698a58d5bbadff85340c4a53d34@ec2-54-91-223-99.compute-1.amazonaws.com:5432/db675ubj9834se', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
bind=engine))

Base =declarative_base()
Base.query =db_session.query_property()

class NumberOfCar(str, enum.Enum):
    NAO_POSSUI = "Oportunidade de venda"
    POSSUI_1_VEICULO = 1
    POSSUI_2_VEICULOS = 2
    POSSUI_3_VEICULOS = 3


class People(Base):
    __tablename__ = 'people'
    name = Column(String(50), index=True)
    age = Column(Integer)
    cpf = Column(Integer, primary_key=True, index=True)
    phone = Column(String(12))
    email = Column(String(50), index=True)
    cars_quantity = Column(Enum(NumberOfCar))

    def __repr__ (self):
        return '<People {}'.format(self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class ColorCars(str, enum.Enum):
    AMARELO = 'amarelo'
    AZUL = 'azul'
    CINZA = 'cinza'

class ModelsCars(str, enum.Enum):
    ESCOTILHA = 'escotilha'
    SEDAN = 'sedan'
    CONVERSIVEL = 'conversível'

class Cars(Base):
    __tablename__ = 'cars'
    license_plate = Column(String(10), primary_key=True, index=True)
    color_car = Column(Enum(ColorCars))
    model_car = Column(Enum(ModelsCars))
    people_id = Column(Integer, ForeignKey('people.cpf'))

    def __repr__ (self):
        return '<Cars {}'.format(self.id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()