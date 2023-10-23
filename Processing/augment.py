from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Augment(Base):
    __tablename__ = 'augment'

    id = Column(Integer, primary_key = True)
    augment_id= Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    rarity = Column(Integer, nullable=False)
    placement = Column(Integer, nullable=False)
    stage_picked = Column(String(250), nullable=False)
    winrate = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, augment_id, name, rarity, placement, stage_picked, winrate, trace_id):
        self.augment_id = augment_id
        self.name = name
        self.rarity = rarity
        self.placement = placement
        self.stage_picked = stage_picked
        self.winrate = winrate
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        
        dict = {}
        dict['id'] = self.id
        dict['augment_id'] = self.augment_id
        dict['name'] = self.name
        dict['rarity'] = self.rarity
        dict['placement'] = self.placement
        dict['stage_picked'] = self.stage_picked
        dict['winrate'] = self.winrate
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created

        return dict