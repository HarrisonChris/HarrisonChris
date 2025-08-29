from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float

from .base import Base, Timestamped, UUIDPrimaryKey


class Client(UUIDPrimaryKey, Timestamped, Base):
	__tablename__ = "clients"

	name: Mapped[str] = mapped_column(String(255), nullable=False)
	email: Mapped[str | None] = mapped_column(String(255))
	phone: Mapped[str | None] = mapped_column(String(64))
	default_hourly_rate: Mapped[float | None] = mapped_column(Float)

	projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")
	invoices = relationship("Invoice", back_populates="client")