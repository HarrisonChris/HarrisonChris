from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Date, Enum
from datetime import date
import enum

from .base import Base, Timestamped, UUIDPrimaryKey


class InvoiceStatus(str, enum.Enum):
	DRAFT = "DRAFT"
	SENT = "SENT"
	PAID = "PAID"
	VOID = "VOID"


class Invoice(UUIDPrimaryKey, Timestamped, Base):
	__tablename__ = "invoices"

	client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False)
	invoice_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
	issue_date: Mapped[date] = mapped_column(Date, nullable=False)
	due_date: Mapped[date] = mapped_column(Date, nullable=False)
	total_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
	status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False)

	client = relationship("Client", back_populates="invoices")
	items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")