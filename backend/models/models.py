from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Folder(Base):
    __tablename__ = "folders"

    folder_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Paper(Base):
    __tablename__ = "papers"

    paper_id = Column(Integer, primary_key=True)
    folder_id = Column(Integer, ForeignKey("folders.folder_id"), nullable=True)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    content_hash = Column(String, nullable=False) 
    filename = Column(String, nullable=False)
    name = Column(String, nullable=True)
    objective = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    methodology = Column(Text, nullable=True)
    dataset = Column(Text, nullable=True)
    main_findings = Column(Text, nullable=True)
    limitations = Column(Text, nullable=True)


class Authors(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class PaperAuthors(Base):
    __tablename__ = "paper_authors"

    paper_id = Column(Integer, ForeignKey("papers.paper_id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.author_id"), primary_key=True)
    associated_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class PaperContent(Base):
    __tablename__ = "paper_content"

    paper_id = Column(Integer, ForeignKey("papers.paper_id"), primary_key=True)
    content = Column(Text, nullable=False)
