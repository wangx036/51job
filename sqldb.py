# -*- coding: UTF-8 -*-

# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime,INTEGER,Float


# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class job(Base):
    # 表的名字:
    __tablename__ = 'job'

    # 表的结构:
    id = Column(INTEGER, primary_key=True)
    name = Column(String(40))
    salaryname=Column(String(20))
    lng=Column(Float(10))
    lat=Column(Float(10))
    comment=Column(String(2000))
    createdate=Column(DateTime)
    coid=Column(INTEGER)
    coname=Column(String(40))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/51job')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

