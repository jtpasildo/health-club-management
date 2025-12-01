## Jordan Pasildo
## 101288061

### Health Club Management FINAL COMP 3005 PROJECT
This project demonstrates how to interact with a PostgreSQL database using Python

### Requirements:
Python 3
PostgreSQL or pgAdmin installed and running locally
psycopg2-binary
python-dotenv

Install dependencies:
pip install -r requirements.txt

## Database Setup:
1. Create database in pgadmin

2. Run the .sql scripts in the sql/ folder in pgAdmin:
DDL.sql -> creates the tables
DML.sql -> inserts the sample data
Run the SQL scripts in the sql/ folder in pgAdmin or psql

3. Create a .env file:
PGHOST=localhost
PGPORT=(port number)
PGDATABASE=(db name)
PGUSER=postgres
PGPASSWORD=(pgAdmin password)

## How to Run:

python3 main.py

Demonstrates and prints out all the operations in action

## Video Link:
https://youtu.be/hfp04BqfF2U


