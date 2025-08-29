from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Date, Boolean
from datetime import date

from .base import Base, Timestamped, UUIDPrimaryKey


class TimeEntry(UUIDPrimaryKey, Timestamped, Base):
	__tablename__ = "time_entries"

	project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
	entry_date: Mapped[date] = mapped_column(Date, nullable=False)
	hours: Mapped[float] = mapped_column(Float, nullable=False)
	rate: Mapped[float] = mapped_column(Float, nullable=False)
	notes: Mapped[str | None] = mapped_column(String(1024))
	is_billed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

	project = relationship("Project", back_populates="time_entries")