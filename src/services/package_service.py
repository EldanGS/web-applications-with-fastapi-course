import datetime
from typing import Optional, List

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from data.package import Package
from data.release import Release
from data import db_session


async def release_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(Release.id))
        result = await session.execute(query)
    return result.scalar()


async def package_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(Package.id))
        result = await session.execute(query)
        return result.scalar()


async def latest_packages(limit: int = 5) -> List[Package]:
    async with db_session.create_async_session() as session:
        query = select(Release).options(
            joinedload(Release.package)
        ).order_by(Release.created_date.desc()).limit(limit)
        result = await session.execute(query)
        releases = result.scalars()

        return [r.package for r in releases]


async def get_package_by_id(package_name: str) -> Optional[Package]:
    async with db_session.create_async_session() as session:
        query = select(Package).filter(Package.id == package_name)

        result = await session.execute(query)
        package = result.scalar_one_or_none()

        return package


async def get_latest_release_for_package(package_name: str) -> Optional[
    Release]:
    async with db_session.create_async_session() as session:
        query = select(Release).filter(
            Release.package_id == package_name
        ).order_by(Release.created_date.desc())

        result = await session.execute(query)
        release = result.scalar()

        return release
