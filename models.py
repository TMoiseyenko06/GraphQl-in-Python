from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer,String,Float,ForeignKey

class Item(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    price: Mapped[float] = mapped_column(Float,nullable=False)
    category: Mapped[str] = mapped_column(String(32),nullable=False)

