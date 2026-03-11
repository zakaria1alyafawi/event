import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime
from Models.Configuration import Configuration
from Models.Session import DatabaseSession
# from Models.Users.AddUser import AddUsers
from Models.Users.RetrieveUsers import RetrieveUsers
# from Models.Users.UpdateUser import UpdateUsers
# from Models.Users.DeleteUser import DeleteUser
# from Models.Users.Users import StatusEnum
# from Models.UserType.UserType import UserTypeEnum\n\nfrom Models.Companies import CompaniesModel\nfrom Models.Sessions import Session\nfrom Models.Events import EventsModel\nfrom Models.UserRoles import UserRolesModel

# Step 1: Initialize database configuration
config = Configuration(
    user="postgres",  # Replace with your database username
    password="1234",  # Replace with your database password
    host="localhost",  # Replace with your database host
    port="5432",  # Replace with your database port
    database="vision"  # Replace with your database name
)

# Step 2: Initialize database session
db_session = DatabaseSession(config)

# Step 3: Create database if it doesn't exist
db_session.create_database_if_not_exists()

# Step 4: Get a session
session = db_session.get_session()

# Testing CRUD operations
try:
    # # --- INSERTION ---
    # print("Inserting a new record into Users table...")
    # adder = AddUsers(session)
    # created_at = datetime.now()
    # new_record = adder.add(
    #     FirstName="TestDataSource",
    #     LastName="zakaria",
    #     Phone="558",
    #     Email="zha@gmail.com",
    #     Password="8567",
    #     Type=UserTypeEnum.Tenant.value,  # Make sure this references a valid UserType TypeID
    #     TenantID=1,
    #     Status=StatusEnum.ACTIVE,
    #     Created_at=created_at,
    #     Created_by=1
    # )
    # print(f"Inserted Record: {new_record}")

    # --- SELECTION ---
    print("Retrieving all records...")
    retriever = RetrieveUsers(session)
    all_records = retriever.validate_login(email="zakariaaalyafawi@gmail.com", plain_password="Abcdef@12345")
    # all_records = retriever.get_by_id(1)
    from API.utils.encryption import PasswordHasher

    pw = "Abcdef@12345"
    h1 = PasswordHasher.hash_password(pw)
    h2 = PasswordHasher.hash_password(pw)

    print(h1)
    print(h2)
    print("Are they different? →", h1 != h2)          # True
    print("But verify works?  →", PasswordHasher.verify_password(pw, h1))   # True
    print("And also on h2?   →", PasswordHasher.verify_password(pw, h2))   # True
    print(f"All Records: {all_records}")

    # retriever = RetrieveUsers(session)
    # # retrieved_record = retriever.get_by_id(1)
    # retrieved_record = retriever.(4)
    
    # print(f"Retrieved Record: {retrieved_record}")

    # # # --- UPDATING ---
    # # print(f"Updating record with ID={2}...")
    # updater = UpdateUsers(session)
    # updated_record = updater.update(
    #     UserID=1,
    #     FirstName="fayez",
    #     Status=StatusEnum.INACTIVE,
    #     Updated_by=2
    # )
    # print(f"Updated Record: {updated_record}")

    # # --- DELETION ---
    # print(f"Deleting record with ID={2}...")
    # deleter = DeleteUser(session)
    # success = deleter.delete(DataSourceID=2)
    # print(f"Deletion Successful: {success}")

    # print("Retrieving all records after deletion...")
    # all_records_after_deletion = retriever.get_all()
    # print(f"All Records After Deletion: {all_records_after_deletion}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.close()
    print("Session closed.")
