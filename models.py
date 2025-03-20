from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Donor(Base):
    __tablename__ = 'donors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    
    donations = relationship("Donation", back_populates="donor")
    
    def get_donations(self):
        return [donation for donation in self.donations]
    
    def total_donated(self):
        total = sum(donation.amount for donation in self.donations)
        return total
    
    def campaigns_supported(self):
        campaigns = set(donation.campaign for donation in self.donations)
        return list(campaigns)


class Campaign(Base):
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    goal_amount = Column(Float)
    current_amount = Column(Float, default=0.0)
    organization = Column(String)
    
    donations = relationship("Donation", back_populates="campaign")
    
    def progress_percentage(self):
        if self.goal_amount == 0:
            return 0
        return round((self.current_amount / self.goal_amount) * 100, 2)
    
    def update_amount(self, donation_amount):
        self.current_amount += donation_amount
    
    def get_donors(self):
        donors = set(donation.donor for donation in self.donations)
        return list(donors)
    
    def get_donations(self):
        return [donation for donation in self.donations]


class Donation(Base):
    __tablename__ = 'donations'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.now)
    
    donor_id = Column(Integer, ForeignKey('donors.id'))
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    
    donor = relationship("Donor", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")