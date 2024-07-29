from sqlalchemy import Column, Integer, String, Text
from public_api.database import Base

class Meme(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    image_url = Column(String)