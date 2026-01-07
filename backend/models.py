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

    def to_dict(self):
        return {
            "id": self.id,
            "listing_source": self.listing_source,
            "listing_url": self.listing_url,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "price": float(self.price) if self.price is not None else None,
            "beds": self.beds,
            "baths": float(self.baths) if self.baths is not None else None,
            "sqft": self.sqft,
            "description": self.description,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }
    
    def to_detail_dict(self, analysis=None):
        return {
            **self.to_dict(),
            "photos": [p.to_dict() for p in (self.photos or [])],
            "analysis": analysis.to_dict() if analysis else None,
        }




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

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "photo_url": self.photo_url,
            "sort_order": self.sort_order,
        }
    
    def to_detail_dict(self, analysis=None):
        return {
            **self.to_dict(),
            "photos": [p.to_dict() for p in (self.photos or [])],
            "analysis": analysis.to_dict() if analysis else None,
        }




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
        unique=True,  # ✅ one row per property
    )

    score_total = Column(Numeric(5, 2), nullable=False)
    score_breakdown = Column(JSONB, nullable=False)
    reasons = Column(JSONB, nullable=True)

    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    property = relationship("Property", back_populates="analysis_results")

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "score_total": float(self.score_total) if self.score_total is not None else None,
            "score_breakdown": self.score_breakdown,
            "reasons": self.reasons,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }




#
#
#
# ScrapeRun
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
    error_count = Column(Integer, nullable=False, default=0)

    error_samples = Column(JSONB, nullable=True)

    max_results = Column(Integer, nullable=False, default=50)

#
#
#
# ScrapeRun
#
#
#