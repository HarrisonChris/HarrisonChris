from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey

from .base import Base, Timestamped, UUIDPrimaryKey


class InvoiceItem(UUIDPrimaryKey, Timestamped, Base):
	__tablename__ = "invoice_items"

	invoice_id: Mapped[str] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
	description: Mapped[str] = mapped_column(String(512), nullable=False)
	hours: Mapped[float] = mapped_column(Float, nullable=False)
	rate: Mapped[float] = mapped_column(Float, nullable=False)
	amount: Mapped[float] = mapped_column(Float, nullable=False)

	invoice = relationship("Invoice", back_populates="items")