from sqlalchemy import func, and_
from .models import HwFirmware

def get_latest_firmware_entries(session):
    subq = (
        session.query(
            HwFirmware.serialHex,
            HwFirmware.goldImg,
            func.max(HwFirmware.datetime).label('latest_datetime')
        )
        .group_by(HwFirmware.serialHex, HwFirmware.goldImg)
        .subquery()
    )

    query = (
        session.query(HwFirmware)
        .join(
            subq,
            and_(
                HwFirmware.serialHex == subq.c.serialHex,
                HwFirmware.goldImg == subq.c.goldImg,
                HwFirmware.datetime == subq.c.latest_datetime
            )
        )
    )
    return query.all()
