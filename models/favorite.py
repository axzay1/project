from connection.connection import Base, engine
from sqlalchemy import Column, Integer, ForeignKey

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

# Create the table
Base.metadata.create_all(engine)
