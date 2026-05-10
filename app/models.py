from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


class Ticket(Base):

    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String)
    message = Column(Text)
    product = Column(String)
    sentiment = Column(String)
    category = Column(String)
    suggested_reply = Column(Text)
    order_value = Column(Float)