import re

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from app.core.db import Base

url_pattern = r'^https?://(?:[a-z0-9-]+\.)*[a-z0-9-]+(?:/.*)?$'


class ParsingData(Base):
    __tablename__ = "parsing_data"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    url = Column(String(250), unique=True, nullable=False)
    xpath = Column(String(250), nullable=False)

    @validates("url")
    def validate_url(self, key, url):
        pattern = re.compile(url_pattern)
        if pattern.match(url) is None:
            raise ValueError("failed url validation")
        return url

    def __repr__(self):
        return f"ParsingData({self.name})"
