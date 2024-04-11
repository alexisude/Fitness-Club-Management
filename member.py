import psycopg2
import db
import datetime
import time
import random

allGoals = None
#Adds a new memeber to the database.
def register(first_name, last_name, email, password, height, weight):
    try:
        cursor = db.conn.cursor()

        # Start a transaction
        # db.conn.autocommit = False

        # Insert the new member into the database
        insert_query = "INSERT INTO members (first_name, last_name, email, password, height, weight, monthlyFeePaid) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *"
        cursor.execute(insert_query, (first_name, last_name, email, password, height, weight, False))
        registered_user = cursor.fetchone()  # Fetch the inserted row
        
        db.conn.commit()        # Commit the transaction
        
        # Reset autocommit to True
        # db.conn.autocommit = True

        print("Member added successfully!")

        # if(registered_user):
        #     registered_user = login(email, password)
        return registered_user
        # else:
        #     print("Registration Failed")
        #     return None
    except psycopg2.Error as e:
        # Rollback the transaction on error
        db.conn.rollback()
        print("Error registering member:", e)
        return None
    finally:
        # Reset autocommit to True and close cursor
        # db.conn.autocommit = True
        cursor.close()


#login to member account
def login(email, password):
    try:
        cursor = db.conn.cursor()  # Create a cursor object
        query = "SELECT * FROM members WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))  # Execute SQL query with parameters
        member = cursor.fetchone()  # Fetch the first row from the result set
        
        if member:  # If member exists (login successful)
            print("Login successful!")
            return member  # Return the member details
        else:
            return None

    except psycopg2.Error as e:
        print("Error logging in:", e)
        return None

    finally:
        cursor.close()  # Close the cursor

# Logs out the current user
def logout():
    print("Logged out successfully.")

# Profile Management (Updating personal information, fitness goals, health metrics      
def update_member_info(memberId, field, newInfo):
    try:
        cursor = db.conn.cursor()
        
        # Validate the new value based on the field
        if field in ('first_name', 'last_name', 'email', 'password'):
            # Basic validation for string fields
            if not isinstance(newInfo, str):
                print("Invalid value. Must be a string.")
                return False
        elif field in ('height', 'weight'):
            try:
                newInfo = float(newInfo)
            except ValueError:
                print("Invalid value. Must be a number.")
                return False
            if newInfo < 0:
                print("Invalid value. Must be non-negative.")
                return False
        else:
            print("Invalid field specified.")
            return False
        
        # Define the SQL query based on the field to be updated
        query = f"UPDATE members SET {field} = %s WHERE id = %s"
        
        # Execute the SQL query with the new value and member ID
        cursor.execute(query, (newInfo, memberId))
        db.conn.commit()
        return True
    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error updating member information:", e)
        return False
    finally:
        cursor.close()

def add_goal(memberId, goalType, goalValue, goalDate):
    achieved = False 
    # Validate goalValue format
    try:
        goalValue = float(goalValue)
    except ValueError:
        print("Invalid goal value! Please enter a valid number.")
        return False

    # Validate goalDate format
    try:
        datetime.datetime.strptime(goalDate, '%Y-%m-%d')
    except ValueError:
        print("Invalid goal date format! Please enter date in YYYY-MM-DD format.")
        return False

    try:
        cursor = db.conn.cursor()
        insert_query = "INSERT INTO goals (memberId, goalType, goalValue, goalDate, achieved) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (memberId, goalType, goalValue, goalDate, achieved))
        db.conn.commit()
        return True
    except psycopg2.Error as e:
        print("Error adding goal:", e)
        return False

def print_goals(memberId):
    goal_ids = []
    try:
        cursor = db.conn.cursor()
        query = "SELECT id, goalType, goalValue, goalDate, achieved FROM goals WHERE memberId = %s"
        cursor.execute(query, (memberId,))
        goals = cursor.fetchall()
        
        if goals:  # Check if goals list is not empty
            for row in goals:
                if not row[4]:  # Checking if achieved is False
                    print("Goal #", row[0])  # Print each row's goal ID
                    print("Goal Type:", row[1])
                    print("Goal Value:", row[2])
                    print("To be achieved by:", row[3])
                    print("----------------------------\n")
                    goal_ids.append(row[0])
        else:
            print("No goals found for the member.")
            
        cursor.close()
        return goal_ids
    except psycopg2.Error as e:
        print("Error fetching goals:", e)
        return None



def printAchevivements(memberId):
    goal_ids = []
    try:
        cursor = db.conn.cursor()
        query = "SELECT id, goalType, goalValue, goalDate, achieved FROM goals WHERE memberId = %s"
        cursor.execute(query, (memberId,))
        goals = cursor.fetchall()
        
        if goals:  # Check if goals list is not empty
            for row in goals:
                if row[4]:  # Checking if achieved is False
                    print("Goal #", row[0])  # Print each row's goal ID
                    print("Goal Type:", row[1])
                    print("Goal Value:", row[2])
                    print("Achieved on:", row[3])
                    print("----------------------------\n")
                    goal_ids.append(row[0])
        else:
            print("No goals found for the member.")
            
        cursor.close()
        return goal_ids
    except psycopg2.Error as e:
        print("Error fetching goals:", e)
        return None



def update_goal(memberId, goal_id, field, newInfo):
    try:
        cursor = db.conn.cursor()
      
        # Validate newInfo based on the field
        if field == 'goalType':
            # Basic validation for goalType field
            if not isinstance(newInfo, str):
                print("Invalid value. Must be a string.")
                return False
        elif field == 'goalValue':
            try:
                newInfo = float(newInfo)
            except ValueError:
                print("Invalid value. Must be a number.")
                return False
            if newInfo < 0:
                print("Invalid value. Must be non-negative.")
                return False
        elif field == 'achieved':
            if newInfo.lower() not in ['true', 'false']:
                print("Invalid value. Must be 'true' or 'false'.")
                return False
            newInfo = newInfo.lower() == 'true'  # Convert input to boolean
            if newInfo:  # If achieved is set to True
                # Update the goal date to the current date
                newInfo_date = datetime.datetime.now().strftime('%Y-%m-%d')
                # Update the goal date field
                cursor.execute("UPDATE goals SET goalDate = %s WHERE id = %s AND memberId = %s", (newInfo_date, goal_id, memberId))
                db.conn.commit()
        elif field == 'goalDate':
            try:
                datetime.datetime.strptime(newInfo, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format! Please enter date in YYYY-MM-DD format.")
                return False
        else:
            print("Invalid field specified.")
            return False
        
        # Define the SQL query based on the field to be updated
        query = f"UPDATE goals SET {field} = %s WHERE id = %s AND memberId = %s"
        
        # Execute the SQL query with the new value, goal ID, and member ID
        cursor.execute(query, (newInfo, goal_id, memberId))
        db.conn.commit()
        return True
    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error updating goal:", e)
        return False
    finally:
        cursor.close()


def bookSession(member_id, session_id):
    try:
        cursor = db.conn.cursor()

        # Check if the session is a personal training session or a group session
        query = "SELECT sessionType FROM sessions WHERE id = %s"
        cursor.execute(query, (session_id,))
        session_type = cursor.fetchone()[0]

        # Check if the session is already booked
        if session_type == "Personal Training":
            query = "SELECT * FROM trainingSessionParticipants WHERE sessionId = %s"
            cursor.execute(query, (session_id,))
            existing_session = cursor.fetchone()
            if existing_session:
                print("This personal training session is already booked.")
                return False

        # If the session is not already booked, book the session
        insert_query = "INSERT INTO trainingSessionParticipants (memberId, sessionId) VALUES (%s, %s)"
        cursor.execute(insert_query, (member_id, session_id))
        db.conn.commit()
        print("Session booked successfully!")
        return True

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error booking session:", e)
        return False

    finally:
        cursor.close()

def printAvailableSessions(member_id):
    try:
        cursor = db.conn.cursor()

        # Fetch all available sessions
        query = "SELECT id, sessionDate, sessionTime, roomNumber, sessionType FROM sessions"
        cursor.execute(query)
        available_sessions = cursor.fetchall()

        available_session_ids = []  # List to store IDs of available sessions

        # Check if any personal training session has been booked by the member
        query = "SELECT sessionId FROM trainingSessionParticipants WHERE memberId = %s"
        cursor.execute(query, (member_id,))
        booked_sessions = [row[0] for row in cursor.fetchall()]

        # Print available sessions for the user to choose
        print("Available Sessions:")
        for session in available_sessions:
            session_id = session[0]
            session_date = session[1]
            session_time = session[2]
            room_number = session[3]
            session_type = session[4]

            # Check if the session is already booked
            if session_id in booked_sessions:
                continue

            # Print the session details
            print("Session ID:", session_id)
            print("Date:", session_date)
            print("Time:", session_time)
            print("Room Number:", room_number)
            print("Session Type:", session_type)
            print("--------------------------")
            available_session_ids.append(session_id)

        return available_session_ids

    except psycopg2.Error as e:
        print("Error fetching available sessions:", e)
        return None

    finally:
        cursor.close()



def viewBookedSessions(member_id):
    try:
        cursor = db.conn.cursor()
        query = "SELECT sessions.id, sessions.sessionType, sessions.sessionDate, sessions.sessionTime \
                 FROM sessions \
                 INNER JOIN trainingSessionParticipants \
                 ON sessions.id = trainingSessionParticipants.sessionId \
                 WHERE trainingSessionParticipants.memberId = %s"
        cursor.execute(query, (member_id,))
        sessions = cursor.fetchall()
        yourSessions = []
        if sessions:
            print("Your booked sessions:")
            for session in sessions:
                print("Session ID:", session[0])
                print("Session Type:", session[1])
                print("Date:", session[2])
                print("Time:", session[3])
                print("--------------------------")
                yourSessions.append(session[0])
                return yourSessions
        else:
            print("You have no booked sessions.")
        
    except psycopg2.Error as e:
        print("Error fetching booked sessions:", e)
        
    finally:
        cursor.close()


def rescheduleSession(member_id, session_id):
    try:
        cursor = db.conn.cursor()
        new_session_date = input("Enter the new session date (YYYY-MM-DD): ")
        new_session_time = input("Enter the new session time (HH:MM:SS): ")

        # Check if the trainer is available for the new session time
        check_query = "SELECT COUNT(*) FROM sessions WHERE trainerId = (SELECT trainerId FROM sessions WHERE id = %s) AND sessionDate = %s AND sessionTime = %s"
        cursor.execute(check_query, (session_id, new_session_date, new_session_time))
        session_count = cursor.fetchone()[0]

        if session_count == 0:
            print("Trainer is not available for the new session time.")
            return False

        # Insert a new session with the updated date and time
        insert_query = "INSERT INTO sessions (trainerId, roomNumber, sessionType, sessionDate, sessionTime) VALUES ((SELECT trainerId FROM sessions WHERE id = %s), (SELECT roomNumber FROM sessions WHERE id = %s), (SELECT sessionType FROM sessions WHERE id = %s), %s, %s) RETURNING id"
        cursor.execute(insert_query, (session_id, session_id, session_id, new_session_date, new_session_time))
        new_session_id = cursor.fetchone()[0]

        # Update the trainingSessionParticipants table
        update_participant_query = "UPDATE trainingSessionParticipants SET sessionId = %s WHERE memberId = %s AND sessionId = %s"
        cursor.execute(update_participant_query, (new_session_id, member_id, session_id))

        # Remove the session from the trainingSessionParticipants table for the old session
        delete_participant_query = "DELETE FROM trainingSessionParticipants WHERE memberId = %s AND sessionId = %s"
        cursor.execute(delete_participant_query, (member_id, session_id))

        db.conn.commit()
        print("Session rescheduled successfully!")
        return True
        
    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error rescheduling session:", e)
        return False
    
    finally:
        cursor.close()
def cancelSession(member_id, session_id):
    try:
        cursor = db.conn.cursor()
        delete_query = "DELETE FROM trainingSessionParticipants WHERE memberId = %s AND sessionId = %s"
        cursor.execute(delete_query, (member_id, session_id))
        db.conn.commit()
        print("Session canceled successfully!")
        
    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error canceling session:", e)
        
    finally:
        cursor.close()

def printMemberNotifications(member_id):
    try:
        cursor = db.conn.cursor()

        # Fetch notifications for the member
        query = "SELECT * FROM memberNotifications WHERE member_id = %s"
        cursor.execute(query, (member_id,))
        memberNotifications = cursor.fetchall()

        # Print member notifications
        print("Member Notifications:")
        if memberNotifications:
            for notification in memberNotifications:
                print(notification[2])  
        else:
            print("No notifications for the member.")

    except psycopg2.Error as e:
        print("Error fetching member notifications:", e)

    finally:
        cursor.close()

def createRoutine(member_id, routine_details):
    try:
        cursor = db.conn.cursor()
        insert_query = "INSERT INTO exerciseRoutine (memberId, routineDetails) VALUES (%s, %s)"
        cursor.execute(insert_query, (member_id, routine_details))
        db.conn.commit()
        print("Exercise routine created successfully!")
    except psycopg2.Error as e:
        print("Error creating exercise routine:", e)
    finally:
        cursor.close()

def printRoutines(member_id):
    try:
        cursor = db.conn.cursor()
        
        # Fetch existing exercise routines for the member
        query = "SELECT id, routineDetails FROM exerciseRoutine WHERE memberId = %s"
        cursor.execute(query, (member_id,))
        routines = cursor.fetchall()
        
        # Display existing exercise routines for selection
        if not routines:
            print("You have no existing exercise routines.")
        else:
            print("Existing Exercise Routines:")
            for routine in routines:
                print("Routine ID:", routine[0])
                print("Details:", routine[1])
                print("--------------------------")
       
    except psycopg2.Error as e:
        print("Error printing exercise routines:", e)
    finally:
        cursor.close()

def modifyRoutine(member_id):
    try:
        cursor = db.conn.cursor()
        
        # Fetch existing exercise routines for the member
        query = "SELECT id, routineDetails FROM exerciseRoutine WHERE memberId = %s"
        cursor.execute(query, (member_id,))
        routines = cursor.fetchall()
        
        # Display existing exercise routines for selection
        if not routines:
            print("You have no existing exercise routines to modify.")
        else:
            printRoutines(member_id)

            routine_id = input("Enter the ID of the routine you want to modify: ")
            new_details = input("Enter the updated details for the exercise routine: ")
            
            # Update the exercise routine
            update_query = "UPDATE exerciseRoutine SET routineDetails = %s WHERE id = %s AND memberId = %s"
            cursor.execute(update_query, (new_details, routine_id, member_id))
            db.conn.commit()
            print("Exercise routine updated successfully.")
        
    except psycopg2.Error as e:
        print("Error modifying exercise routine:", e)
    finally:
        cursor.close()

def display_dashboard(member_id):
    try:
        cursor = db.conn.cursor()
        
        # Fetch member details
        query = "SELECT first_name, last_name, height, weight FROM members WHERE id = %s"
        cursor.execute(query, (member_id,))
        member_details = cursor.fetchone()
        if member_details:
            first_name, last_name, height, weight = member_details
            print("\n")
            print(f"{first_name}'s Dashboard")
            print("------------------------------")
            printRoutines(member_id)
            print("\nFitness Achievements:")
            printAchevivements(member_id)
            print("\nHealth Metrics:")
            print(f"Height: {height} cm")
            print(f"Weight: {weight} kg")
            print("------------------------------\n")
        else:
            print("Member not found.")
            
    except psycopg2.Error as e:
        print("Error displaying dashboard:", e)
    finally:
        cursor.close()


def get_heart_rate():
    return 60 + int(time.time() % 100)


def start_timer():
    # Prompt the user to enter the timer duration
    while True:
        timer_duration = input("Enter the timer duration in seconds: ")
        if timer_duration.isdigit():
            timer_duration = int(timer_duration)
            break
        else:
            print("Invalid input! Please enter a valid number.")

    # Start the timer
    start_time = time.time()
    end_time = start_time + timer_duration

    # Print the timer as it counts down
    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        remaining_time = end_time - time.time()
        print(f"Elapsed time: {elapsed_time:.2f} seconds | Remaining time: {remaining_time:.2f} seconds", end="\r")
        time.sleep(0.1)  # Update the timer every 0.1 second

    # Timer finished
    print("Timer finished!")



def calculate_bmi(member_id):
    try:
        cursor = db.conn.cursor()
        
        # Fetch member's weight from the database
        cursor.execute("SELECT weight FROM members WHERE id = %s", (member_id,))
        weight_kg = cursor.fetchone()[0]
        
        cursor.execute("SELECT weight FROM members WHERE id = %s", (member_id,))
        height_m = cursor.fetchone()[0]
        

        bmi = weight_kg / (height_m ** 2)
        return bmi
    
    except (psycopg2.Error, Exception) as error:
        print("Error calculating BMI:", error)
        return None
    
    finally:
       cursor.close()

def workout_menu(member_id):
    while True:
        print("Workout and Health tracking Options:")
        print("1. Track Heart Rate")
        print("2. Measure Blood Pressure")
        print("3. Calculate BMI")
        print("4. Start Workout Timer")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            # Track heart rate
            heart_rate = get_heart_rate()
            print(f"Heart Rate: {heart_rate} BPM")

        elif choice == '2':
            # Measure blood pressure
            print("Please put on the blood pressure cuff.")
            time.sleep(2)  # Simulating putting on the cuff
            blood_pressure = measure_blood_pressure()
            print(f"Blood Pressure: {blood_pressure}")

        elif choice == '3':
            # Calculate BMI
            bmi = calculate_bmi(member_id)
            if bmi is not None:
                print(f"Your BMI is: {bmi:.2f}")

        elif choice == '4':
            # Start workout timer
            start_timer()

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")



def measure_blood_pressure():
    systolic = random.randint(90, 150)  
    diastolic = random.randint(60, 100)  
    return f"{systolic}/{diastolic} mmHg"