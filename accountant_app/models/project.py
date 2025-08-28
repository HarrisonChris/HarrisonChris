from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Boolean

from .base import Base, Timestamped, UUIDPrimaryKey


class Project(UUIDPrimaryKey, Timestamped, Base):
	__tablename__ = "projects"

	client_id: Mapped[str] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
	name: Mapped[str] = mapped_column(String(255), nullable=False)
	hourly_rate: Mapped[float | None] = mapped_column(Float)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

	client = relationship("Client", back_populates="projects")
	time_entries = relationship("TimeEntry", back_populates="project", cascade="all, delete-orphan")