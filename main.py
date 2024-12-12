import mysql.connector
from mysql.connector import Error
import re

#MySQL connection
connection_params = {

    'host': 'localhost',
    'database': 'new_database5',
    'user': 'new_username5',
    'password': 'new_password5'
}


def ensure_table_exists():
    try:
        # Establish connection
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()

            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {connection_params['database']}")
            conn.commit()

            # Switch to the newly created database
            cursor.execute(f"USE {connection_params['database']}")

            # Create table if not exists
            create_table_query = """
            CREATE TABLE IF NOT EXISTS USER (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                address VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            conn.commit()

            print("Table 'USER' is ensured to exist or created.")
    except Error as e:
        print(f"Error: {e}")

# Helper function for valid email using regex
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Helper function for valid phone number (numeric only and at least 10 digits)
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10

def main():
    ensure_table_exists()

    while True:
        print("Choose an operation: ")
        print("1. Create a new record")
        print("2. Read records")
        print("3. Update a record")
        print("4. Delete a record")
        print("5. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            create_record()
        elif choice == "2":
            read_records()
        elif choice == "3":
            update_record()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")

def create_record():
    name = input("Enter Name: ").strip()
    while not name:
        print("Please enter a valid Name.")
        name = input("Enter Name: ").strip()

    email = input("Enter Email: ").strip()
    while not email or not is_valid_email(email):
        print("Please enter a valid Email (e.g., example@example.com).")
        email = input("Enter Email: ").strip()

    phone = input("Enter Phone (minimum 10 digits): ").strip()
    while not is_valid_phone(phone):
        print("Please enter a valid Phone number (numeric, at least 10 digits).")
        phone = input("Enter Phone: ").strip()

    address = input("Enter Address: ").strip()
    while not address:
        print("Please enter a valid Address.")
        address = input("Enter Address: ").strip()

    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            query = """
            INSERT INTO USER (name, email, phone, address) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, phone, address))
            conn.commit()
            print("Record inserted successfully.")
    except Error as e:
        print(f"Error: {e}")

def read_records():
    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM USER"
            cursor.execute(query)
            rows = cursor.fetchall()
            print(f"{'Id':<5} {'Name':<20} {'Email':<25} {'Phone':<15} {'Address':<30} {'Created At':<20}")
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<25} {row[3]:<15} {row[4]:<30} {row[5]:<20}")
    except Error as e:
        print(f"Error: {e}")

def update_record():
    record_id = input("Enter the ID of the person to update:").strip()
    while not record_id.isdigit():
        print("Please enter a valid ID.")
        record_id = input("Enter the ID of the person to update:").strip()
    record_id = int(record_id)

    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            select_query = "SELECT * FROM USER WHERE id = %s"
            cursor.execute(select_query, (record_id,))
            row = cursor.fetchone()

            if not row:
                print(f"No record found with ID: {record_id}")
                return

            new_name = input("Enter new Name: ").strip()
            new_email = input("Enter new Email: ").strip()
            while not is_valid_email(new_email):
                print("Please enter a valid Email.")
                new_email = input("Enter new Email: ").strip()

            new_phone = input("Enter new Phone: ").strip()
            while not is_valid_phone(new_phone):
                print("Please enter a valid Phone number.")
                new_phone = input("Enter new Phone: ").strip()

            new_address = input("Enter new Address: ").strip()

            update_query = """
            UPDATE USER SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s
            """
            cursor.execute(update_query, (new_name, new_email, new_phone, new_address, record_id))
            conn.commit()
            if cursor.rowcount > 0:
                print("Record updated successfully.")
            else:
                print("No records updated.")
    except Error as e:
        print(f"Error: {e}")

def delete_record():
    record_id = input("Enter the ID of the person to delete:").strip()
    while not record_id.isdigit():
        print("Please enter a valid ID.")
        record_id = input("Enter the ID of the person to delete:").strip()
    record_id = int(record_id)

    try:
        with mysql.connector.connect(**connection_params) as conn:
            cursor = conn.cursor()
            delete_query = "DELETE FROM USER WHERE id = %s"
            cursor.execute(delete_query, (record_id,))
            conn.commit()

            if cursor.rowcount > 0:
                print("Record deleted successfully.")
            else:
                print("No records deleted.")
    except Error as e:
        print(f"Error: {e}")

# Run the main function
if __name__ == "__main__":
    main()