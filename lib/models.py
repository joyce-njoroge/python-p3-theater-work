from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    character_name = Column(String)
    auditions = relationship("Audition", backref="role")

    def __repr__(self):
        return f"<Role(id={self.id}, character_name={self.character_name})>"
    
    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        for audition in self.auditions:
            if audition.hired:
                return audition
        return "no actor has been hired for this role"

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) < 2:
            return "no actor has been hired for understudy for this role"
        return hired_auditions[1]

class Audition(Base):
    __tablename__ = "auditions"
    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", backref=backref("auditions", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Audition(id={self.id}, actor={self.actor}, location={self.location}, phone={self.phone}, hired={self.hired}, role_id={self.role_id})>"

    def call_back(self):
        self.hired = True