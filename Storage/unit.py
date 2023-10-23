from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime
import uuid

class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key = True)
    unit_id = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    buy_cost = Column(Integer, nullable=False)
    sell_cost = Column(Integer, nullable=False)
    rarity = Column(Integer, nullable=False)
    ability_name = Column(String(100), nullable=False)
    stars = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, unit_id, name, buy_cost, sell_cost, rarity, ability_name, stars, trace_id):
        self.unit_id = unit_id
        self.name = name
        self.buy_cost = buy_cost
        self.sell_cost = sell_cost
        self.rarity = rarity
        self.stars = stars
        self.ability_name = ability_name
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        dict = {}
        dict['id'] = self.id
        dict['unit_id'] = self.unit_id
        dict['name'] = self.name
        dict['buy_cost'] = self.buy_cost
        dict['sell_cost'] = self.sell_cost
        dict['rarity'] = self.rarity
        dict['ability_name'] = self.ability_name
        dict['stars'] = self.stars
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created

        return dict