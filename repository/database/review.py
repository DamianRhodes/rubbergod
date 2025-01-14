from sqlalchemy import (Boolean, Column, Date, ForeignKey, Integer,
                        PrimaryKeyConstraint, String)
from sqlalchemy.orm import relationship

from repository.database import database


class Review(database.base):
    __tablename__ = "bot_review"

    id = Column(Integer, primary_key=True)
    member_ID = Column(String)
    anonym = Column(Boolean, default=True)
    subject = Column(String, ForeignKey("bot_subjects.shortcut", ondelete="CASCADE"))
    tier = Column(Integer, default=0)
    text_review = Column(String, default=None)
    date = Column(Date)
    relevance = relationship("ReviewRelevance")


class ReviewRelevance(database.base):
    __tablename__ = "bot_review_relevance"
    __table_args__ = (PrimaryKeyConstraint("review", "member_ID", name="key"),)

    member_ID = Column(String)
    vote = Column(Boolean, default=False)
    review = Column(Integer, ForeignKey("bot_review.id", ondelete="CASCADE"))


class Subject(database.base):
    __tablename__ = "bot_subjects"

    shortcut = Column(String, primary_key=True)
    reviews = relationship("Review")


class Subject_details(database.base):
    __tablename__ = "bot_subjects_details"

    shortcut = Column(String, primary_key=True)
    name = Column(String)
    credits = Column(Integer)
    semester = Column(String)
    end = Column(String)
    card = Column(String)
    year = Column(String)
    type = Column(String)
    degree = Column(String)


class Programme(database.base):
    __tablename__ = "bot_programme"

    shortcut = Column(String, primary_key=True)
    name = Column(String)
    link = Column(String)
