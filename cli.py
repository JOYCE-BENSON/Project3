from models import Donor, Campaign, Donation
import getpass
from datetime import datetime
import re

class CLI:
    def __init__(self, session):
        self.session = session
        self.current_user = None
    
    def start(self):
        self.main_menu()
    
    def main_menu(self):
        while True:
            print("\n----- MAIN MENU -----")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                print("Thank you for using GiveConnect. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def login(self):
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")
        
        donor = self.session.query(Donor).filter_by(email=email).first()
        
        if donor and donor.password == password:
            self.current_user = donor
            print(f"Welcome back, {donor.name}!")
            self.donor_menu()
        else:
            print("Invalid email or password.")
    
    def register(self):
        name = input("Enter your name: ")
    
        while True:
            email = input("Enter your email: ")
            if "@" not in email or "." not in email.split("@")[-1]:
                print("Invalid email format. Please try again.")
                continue
                
            existing_user = self.session.query(Donor).filter_by(email=email).first()
            if existing_user:
                print("Email already exists. Please use a different email.")
                continue
            
            break
        
        password = getpass.getpass("Enter your password: ")
        confirm_password = getpass.getpass("Confirm your password: ")
        
        if password != confirm_password:
            print("Passwords do not match.")
            return
        
        new_donor = Donor(name=name, email=email, password=password)
        self.session.add(new_donor)
        self.session.commit()
        
        print("Registration successful! You can now login.")
    
    def donor_menu(self):
        while True:
            print("\n----- DONOR MENU -----")
            print(f"Logged in as: {self.current_user.name}")
            print("1. Browse Campaigns")
            print("2. Make a Donation")
            print("3. View Donation History")
            print("4. View Profile")
            print("5. Logout")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                self.browse_campaigns()
            elif choice == "2":
                self.make_donation()
            elif choice == "3":
                self.view_donation_history()
            elif choice == "4":
                self.view_profile()
            elif choice == "5":
                self.current_user = None
                print("Logged out successfully.")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def browse_campaigns(self):
        campaigns = self.session.query(Campaign).all()
        
        if not campaigns:
            print("No campaigns available at the moment.")
            return
        
        print("\n----- AVAILABLE CAMPAIGNS -----")
        for idx, campaign in enumerate(campaigns, 1):
            progress = campaign.progress_percentage()
            print(f"{idx}. {campaign.name} - {campaign.organization}")
            print(f"   Description: {campaign.description}")
            print(f"   Goal: ${campaign.goal_amount:.2f} | Raised: ${campaign.current_amount:.2f}")
    
    def view_campaign_details(self, campaign):
        print(f"\n----- CAMPAIGN DETAILS: {campaign.name} -----")
        print(f"Organization: {campaign.organization}")
        print(f"Description: {campaign.description}")
        print(f"Goal Amount: ${campaign.goal_amount:.2f}")
        print(f"Current Amount: ${campaign.current_amount:.2f}")
        
        print("\n1. Make a Donation to this Campaign")
        print("2. Go Back")
        
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            self.donate_to_campaign(campaign)
    
    def make_donation(self):
        campaigns = self.session.query(Campaign).all()
        
        if not campaigns:
            print("No campaigns available at the moment.")
            return
        
        print("\n----- SELECT A CAMPAIGN TO DONATE -----")
        for idx, campaign in enumerate(campaigns, 1):
            print(f"{idx}. {campaign.name} - {campaign.organization}")
        
        while True:
            choice = input("Enter campaign number: ")
    
    def donate_to_campaign(self, campaign):
        print(f"\nDonating to: {campaign.name}")
        
        while True:
            amount_str = input("Enter donation amount (KSHs): ")
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Donation amount must be greater than zero.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        confirm = input(f"Confirm donation of {amount:.2f} to {campaign.name}? (y/n): ")
        
        if confirm.lower() == 'y':
            donation = Donation(
                amount=amount,
                donor=self.current_user,
                campaign=campaign,
                date=datetime.now()
            )
            
            campaign.update_amount(amount)
            
            self.session.add(donation)
            self.session.commit()
    
    def view_donation_history(self):
        donations = self.current_user.get_donations()
        
        if not donations:
            print("You haven't made any donations yet.")
            return
        
        print("\n----- YOUR DONATION HISTORY -----")
        total = 0

        for idx, donation in enumerate(donations, 1):
            total += donation.amount
            date_str = donation.date.isoformat(sep=" ", timespec="minutes")
            print(f"{idx}. {donation.amount:.2f} to {donation.campaign.name} on {date_str}")

        print(f"\nTotal donations: ${total:.2f}")
        input("Press Enter to continue...")

    def view_profile(self):
        donor = self.current_user
        donations = donor.get_donations()
        campaigns = donor.campaigns_supported()
        total_donated = donor.total_donated()

        print(f"\n----- PROFILE: {donor.name} -----")
        print(f"Email: {donor.email}")
        print(f"Total Donations: ${total_donated:.2f}")
        print(f"Campaigns Supported: {len(campaigns)}")

        print("\n1. Change Password")
        print("2. Delete Account")
        print("3. Go Back")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            self.change_password()
        elif choice == "2":
            self.delete_account()
    
    def change_password(self):
        current_password = getpass.getpass("Enter current password: ")
        
        if current_password != self.current_user.password:
            print("Incorrect password.")
            return
        
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("Passwords do not match.")
            return
        
        self.current_user.password = new_password
        self.session.commit()
        
        print("Password has been changed.")
    
    def delete_account(self):
        confirm = input("Are you sure you want to delete your account? (y/n): ")
        
        if confirm.lower() != 'y':
            print("Account has not been deleted.")
            return
        
        password = getpass.getpass("Enter your password to confirm: ")
        
        if password != self.current_user.password:
            print("Incorrect password.")
            return
        
        self.session.delete(self.current_user)
        self.session.commit()
        
        print("Account deleted successfully.")
        self.current_user = None
        self.main_menu()
