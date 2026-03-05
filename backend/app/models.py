#backend/app/models.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, BigInteger, Integer, ForeignKey, UniqueConstraint, func
from pgvector.sqlalchemy import Vector
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    storage_path: Mapped[str] = mapped_column(String, nullable=False)
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class EmbeddingModel(Base):
    __tablename__ = "embedding_models"
    __table_args__ = (UniqueConstraint("provider","name","pretrained",name="uq_embedding_models"),)
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    pretrained: Mapped[str] = mapped_column(String, nullable=False)
    dim: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
class Embedding(Base):
    __tablename__ = "embeddings"
    __table_args__ = (UniqueConstraint("asset_id","model_id",name="uq_asset_model"),)
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    model_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("embedding_models.id", ondelete="RESTRICT"), nullable=False)
    vector: Mapped[list[float]] = mapped_column(Vector(512), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True),server_default=func.now(), nullable=False)