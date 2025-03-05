from sqlalchemy import String, Float, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class PriceItem(Base):
    vendor: Mapped[str] = mapped_column(String(64), nullable=True)
    number: Mapped[str] = mapped_column(String, nullable=True)
    search_vendor: Mapped[str] = mapped_column(String, nullable=True)
    search_number: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(20, 2), nullable=True)
    count: Mapped[int] = mapped_column(Integer, nullable=True)

