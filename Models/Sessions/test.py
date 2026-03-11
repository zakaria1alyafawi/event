import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from datetime import datetime
from Models.Configuration import Configuration
from Models.Session import DatabaseSession
from Models.Users.AddUser import AddUsers
from Models.Sessions.AddSessions import AddSessions
from Models.Sessions.RetrieveSessions import RetrieveSessions
from Models.Sessions.UpdateSessions import UpdateSessions
from Models.Sessions.DeleteSessions import DeleteSessions
# from Models.Sessions.Sessions import StatusEnum

# Step 1: Initialize database configuration
config = Configuration(
    user="postgres",  # Replace with your database username
    password="1234",  # Replace with your database password
    host="localhost",  # Replace with your database host
    port="5432",  # Replace with your database port
    database="ASR"  # Replace with your database name
)

# Step 2: Initialize database session
db_session = DatabaseSession(config)

# Step 3: Create database if it doesn't exist
db_session.create_database_if_not_exists()

# Step 4: Get a session
session = db_session.get_session()

# Testing CRUD operations
try:

    # --- INSERT SESSION ---
    print("Inserting a new record into Sessions table...")
    session_adder = AddSessions(session)
    start_time = datetime.now()
    new_session = session_adder.add(
        UserID=1,
        StartTime=start_time,
        EndTime=None,
        Token="dsfasdfasdfasdfasdfas",
        Status=1,
        Created_at=datetime.now()
    )
    print(f"Inserted Session: {new_session}")

    # # --- SELECTION ---
    # print("Retrieving all session records...")
    # session_retriever = RetrieveSessions(session)
    # all_sessions = session_retriever.get_all()
    # print(f"All Sessions: {all_sessions}")

    # print(f"Retrieving session record with ID={new_session.SessionID}...")
    # retrieved_session = session_retriever.get_by_id(record_id=new_session.SessionID)
    # print(f"Retrieved Session: {retrieved_session}")

    # print("Retrieving sessions by User ID...")
    # sessions_by_model = session_retriever.get_by_user_id(user_id=1)

    # # --- UPDATING ---
    # print(f"Updating session record with ID={new_session.SessionID}...")
    # session_updater = UpdateSessions(session)
    # updated_session = session_updater.update(
    #     SessionID=new_session.SessionID,
    #     EndTime=datetime.now(),
    # )
    # print(f"Updated Session: {updated_session}")

    # # --- DELETION ---
    # print(f"Deleting session record with ID={new_session.SessionID}...")
    # session_deleter = DeleteSessions(session)
    # success = session_deleter.delete(SessionID=new_session.SessionID)
    # print(f"Deletion Successful: {success}")

    # print("Retrieving all session records after deletion...")
    # all_sessions_after_deletion = session_retriever.get_all()
    # print(f"All Sessions After Deletion: {all_sessions_after_deletion}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.close()
    print("Session closed.")
