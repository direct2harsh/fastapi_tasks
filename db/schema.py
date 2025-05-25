
from sqlalchemy import Column, String,DateTime
from db.connection import DeclarativeBase
# from sqlalchemy.sql import func
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Tasks(DeclarativeBase):
    __tablename__ ="tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String,nullable=False)
    description = Column(String,nullable=True)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),index=True)
    updated_at = Column(DateTime(timezone=True),)
    # email = Column(String,unique=True)    # For alembic test
