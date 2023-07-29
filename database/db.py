from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


from models.user import User
from models.product import Product

class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def create_user(self, user_data):
        session = self.Session()
        try:
            user = User(**user_data)
            session.add(user)
            session.commit()
            return user
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_users(self):
        session = self.Session()
        try:
            users = session.query(User).all()
            return users
        except SQLAlchemyError as e:
            raise e
        finally:
            session.close()

    # def get_products(self):
    #     session = self.Session()
    #     try:
    #         products = session.query(Product).all()
    #         return products
    #     except SQLAlchemyError as e:
    #         raise e
    #     finally:
    #         session.close()

    # def login(self, email):
    #     session = self.Session()
    #     try:
    #         user = session.query(User).filter_by(email=email).first()
    #         return user
    #     except SQLAlchemyError as e:
    #         raise e
    #     finally:
    #         session.close()
