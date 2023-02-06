from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, Enum
from db_home.references import Size, Status


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    email = Column(String(32), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    orders = relationship('Order', back_populates='user')

    def __str__(self):
        return f'User {self.email}'


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    quantity = Column(Integer, nullable=False)
    order_status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    pizza_size = Column(Enum(Size), default=Size.SMALL, nullable=False)

    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f'Order {self.id}'
