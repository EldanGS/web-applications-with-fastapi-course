import datetime
from typing import Optional, List

from sqlalchemy.orm import joinedload

from data.package import Package
from data.release import Release
from data import db_session


def release_count() -> int:
    with db_session.create_session() as session:
        return session.query(Release).count()


def package_count() -> int:
    with db_session.create_session() as session:
        return session.query(Package).count()


def latest_packages(limit: int = 5) -> List[Package]:
    with db_session.create_session() as session:
        releases = session.query(Release).options(
            joinedload(Release.package)
        ).order_by(Release.created_date.desc()).limit(limit).all()

        return [r.package for r in releases]


def get_package_by_id(package_name: str) -> Optional[Package]:
    with db_session.create_session() as session:
        package = session.query(Package).filter(Package.id == package_name).first()
        return package


def get_latest_release_for_package(package_name: str) -> Optional[Release]:
    with db_session.create_session() as session:
        release = session.query(Release).filter(
            Release.package_id == package_name
        ).order_by(Release.created_date.desc()).first()

        return release
