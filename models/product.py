

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    cost = Column(Float)
    description = Column(String)
    type = Column(String(50))
    created_by = Column(String(100))
    image = Column(String)
    color = Column(String)
    size = Column(String)
    is_printed = Column(Boolean)

    def __init__(self, name, cost, description, type, created_by, image, color, size, is_printed):
        self.name = name
        self.cost = cost
        self.description = description
        self.type = type
        self.created_by = created_by
        self.image = image
        self.color = color
        self.size = size
        self.is_printed = is_printed

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, cost={self.cost})>"
