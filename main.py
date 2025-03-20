from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Donor, Campaign, Donation
from cli import CLI

def create_sample_data(session):
    if session.query(Donor).count() == 0:
        donors = [
            Donor(name="Joyce Benson", email="bensonjoyce25@gmail.com", password="Joyce@16"),
            Donor(name="Ladasha Benson", email="Ladasha18@gmail.com", password="Ladasha@2020")
        ]
        session.add_all(donors)
        session.commit()
    
    if session.query(Campaign).count() == 0:
        campaigns = [
            Campaign(
                name="Save the Oceans", 
                description="Help clean up ocean pollution and protect marine life",
                goal_amount=10000.0,
                current_amount=2500.0,
                organization="Ocean Conservation Inc."
            ),
            Campaign(
                name="Feed the Hungry", 
                description="Provide meals to those in need in our community",
                goal_amount=5000.0,
                current_amount=1200.0,
                organization="Food Bank Foundation"
            ),
            Campaign(
                name="Emergency Relief", 
                description="Support victims of recent natural disasters",
                goal_amount=15000.0,
                current_amount=3000.0,
                organization="Relief Organization"
            )
        ]
        session.add_all(campaigns)
        session.commit()

def main():
    
    engine = create_engine('sqlite:///giveconnect.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    create_sample_data(session)
    
    print("=" * 60)
    
    cli = CLI(session)
    cli.start()

if __name__ == "__main__":
    main()