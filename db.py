import psycopg2

# Establish connection parameters
conn_params = {
    "host": "localhost",  # Database host
    "database": "Fitness Club Management",  # Database name
    "user": "postgres",  # Database username
    "password": "postgres"  # Database password
}

# Global variable for database connection
conn = None

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(**conn_params)  # Establish a connection
    print("Connected to the database db!")

except psycopg2.Error as e:
    print("Error while connecting to PostgreSQL:", e)

def close_connection():
    conn.close()