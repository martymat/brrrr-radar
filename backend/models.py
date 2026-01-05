from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from db import Base


# models



#
#
#
# Property
#
#
#
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)

    listing_source = Column(String(50), nullable=False)
    listing_url = Column(String(500), nullable=False, unique=True)

    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip = Column(String(20), nullable=False)

    price = Column(Numeric(12, 2), nullable=True)
    beds = Column(Integer, nullable=True)
    baths = Column(Numeric(4, 2), nullable=True)
    sqft = Column(Integer, nullable=True)

    description = Column(Text, nullable=True)

    scraped_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    photos = relationship(
        "PropertyPhoto",
        back_populates="property",
        cascade="all, delete-orphan",
        order_by="PropertyPhoto.sort_order",
    )

    analysis_results = relationship(
        "AnalysisResult",
        back_populates="property",
        cascade="all, delete-orphan",
    )



#
#
#
# PropertyPhoto
#
#
#
class PropertyPhoto(Base):
    __tablename__ = "property_photos"

    id = Column(Integer, primary_key=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
    )

    photo_url = Column(String(1000), nullable=False)
    sort_order = Column(Integer, nullable=False)

    # Relationship
    property = relationship("Property", back_populates="photos")



#
#
#
# AnalysisResult
#
#
#
class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
    )

    score_total = Column(Numeric(5, 2), nullable=False)

    score_breakdown = Column(JSONB, nullable=False)
    reasons = Column(JSONB, nullable=True)

    analyzed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationship
    property = relationship("Property", back_populates="analysis_results")



#
#
#
# PropertyPhoto
#
#
#
class ScrapeRun(Base):
    __tablename__ = "scrape_runs"

    id = Column(Integer, primary_key=True)

    query = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False)

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    finished_at = Column(DateTime(timezone=True), nullable=True)

    properties_found = Column(Integer, nullable=False, default=0)
    errors_count = Column(Integer, nullable=False, default=0)

    error_samples = Column(JSONB, nullable=True)