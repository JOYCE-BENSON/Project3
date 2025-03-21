<<<<<<< HEAD
# Project3
=======
#GiveConnect

GiveConnect is a command-line application that connects donors with charitable causes. The platform allows users to create donor profiles and browse various charitable causes.

##Features

- User registration and login
- Browse to see charitable campaigns
- Make donations to the campaigns
- Track donation history
- View profile 

#Installation

1. Install dependencies:
 using the command 
pipenv install
```

2. Run the application:
```
python main.py
```

## Database Structure

The application uses SQLAlchemy ORM with the following models:

- **Donor**: Represents users who can donate to campaigns
- **Campaign**: Represents charitable causes that accept donations
- **Donation**: Represents individual donations made by donors to campaigns

## To run the .db
to open the database run command sqlite3 giveconnect.db to the terminal

## How you can use the application

1. Register a new account or login with an existing account
2. Browse available campaigns
3. Make donations to campaigns of your choice
4. View your donation history and profile statistics

## Project Structure
My structure for Project3 
```
giveconnect/
├── README.md
├── Pipfile
├── main.py
├── models.py
└── cli.py
```

## The requirements to run this project

- Python 
- SQLAlchemy
