from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from conf.db.models import Model


class Video(Model):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_active = Column(Boolean, default=True)
