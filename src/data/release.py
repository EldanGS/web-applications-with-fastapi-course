import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from data.modelbase import SqlAlchemyBase


class Release(SqlAlchemyBase):
    __tablename__ = "releases"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # Versions
    major_ver: int = sa.Column(sa.BigInteger, index=True)
    minor_ver: int = sa.Column(sa.BigInteger, index=True)
    build_ver: int = sa.Column(sa.BigInteger, index=True)

    created_date: datetime.datetime = sa.Column(sa.DateTime,
                                                default=datetime.datetime.now,
                                                index=True)
    comment: str = sa.Column(sa.String)
    url: str = sa.Column(sa.String)
    size: int = sa.Column(sa.BigInteger)

    # Package relationship
    package_id: str = sa.Column(sa.String, sa.ForeignKey("packages.id"))
    package = orm.relationship('Package')

    @property
    def version_text(self):
        return f"{self.major_ver}.{self.minor_ver}.{self.build_ver}"
