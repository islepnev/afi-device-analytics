from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

Base = declarative_base()

class HwFirmware(Base):
    __tablename__ = 'hw_firmware'

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    revision = Column(Integer)
    fw_maj = Column(Integer)
    fw_min = Column(Integer)
    git_hash = Column(String(40))
    base_name = Column(String(40), nullable=False)
    pcb_name = Column(String(20))
    path = Column(Text, nullable=False)
    fromHost = Column(Text, nullable=False)
    goldImg = Column(Boolean, nullable=False)
    serialHex = Column(String, nullable=False)
