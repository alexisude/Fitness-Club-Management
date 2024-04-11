import psycopg2
import db
import datetime
from datetime import datetime
def trainerLogin(email, password):
    try:
        cursor = db.conn.cursor()
        query = "SELECT * FROM trainers WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        trainer = cursor.fetchone()
        if trainer:
            print("Login successful!")
            return trainer
        else:
            print("Invalid email or password.")
            return None
    except psycopg2.Error as e:
        print("Error logging in:", e)
        return None
    finally:
        cursor.close() 

def refreshSessions():
    try:
        cursor = db.conn.cursor()

        # Get current date and time
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        # Get session IDs of passed sessions
        passed_sessions_query = "SELECT id FROM sessions WHERE sessionDate < %s OR (sessionDate = %s AND sessionTime < %s)"
        cursor.execute(passed_sessions_query, (current_date, current_date, current_time))
        passed_sessions = cursor.fetchall()

        if passed_sessions:
            # Remove passed sessions from trainingSessionParticipants
            delete_training_participants_query = "DELETE FROM trainingSessionParticipants WHERE sessionId IN %s"
            cursor.execute(delete_training_participants_query, (tuple(passed_sessions),))

            # Remove passed sessions from groupClassParticipants
            delete_group_participants_query = "DELETE FROM groupClassParticipants WHERE sessionId IN %s"
            cursor.execute(delete_group_participants_query, (tuple(passed_sessions),))

            # Remove passed sessions from sessions
            delete_sessions_query = "DELETE FROM sessions WHERE id IN %s"
            cursor.execute(delete_sessions_query, (tuple(passed_sessions),))

            # Update room availability for passed sessions
            update_rooms_query = "UPDATE rooms SET available = TRUE WHERE room_number IN (SELECT roomNumber FROM sessions)"
            cursor.execute(update_rooms_query)

            db.conn.commit()
            print("Passed sessions removed successfully!")
        else:
            print("No sessions to remove.")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error refreshing sessions:", e)

    finally:
        cursor.close()

def createSession(trainer_id, room_number, session_type, session_date, session_time):
    try:
        cursor = db.conn.cursor()

        session_datetime = datetime.strptime(session_date + " " + session_time, '%Y-%m-%d %H:%M')

        # Get current date and time
        current_datetime = datetime.now()

        # Compare just the dates
        if session_datetime.date() < current_datetime.date():
            print("Cannot schedule session for a past date.")
            return False
        elif session_datetime.date() == current_datetime.date():
            # If the dates are the same, compare the times
            if session_datetime.time() < current_datetime.time():
                print("Cannot schedule session for a past time on the current date.")
                return False

        # Check if the room is available
        check_room_query = "SELECT available FROM rooms WHERE room_number = %s"
        cursor.execute(check_room_query, (room_number,))
        room_available = cursor.fetchone()

        if not room_available or not room_available[0]:
            print("Room is not available.")
            return False

        # Check if the trainer already has a session scheduled for the given date and time
        check_query = "SELECT COUNT(*) FROM sessions WHERE trainerId = %s AND sessionDate = %s AND sessionTime = %s"
        cursor.execute(check_query, (trainer_id, session_date, session_time))
        session_count = cursor.fetchone()[0]

        if session_count > 0:
            print("Trainer already has a session scheduled at that date and time.")
            return False

        # If the trainer doesn't have a session, insert the new session into the database
        insert_query = "INSERT INTO sessions (trainerId, roomNumber, sessionType, sessionDate, sessionTime) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (trainer_id, room_number, session_type, session_date, session_time))
        db.conn.commit()
        print("Session scheduled successfully!")

        # Update room availability
        update_query = "UPDATE rooms SET available = FALSE WHERE room_number = %s"
        cursor.execute(update_query, (room_number,))
        db.conn.commit()

        return True

    except psycopg2.Error as e:
        print("Error in scheduling session:", e)
        return False

    finally:
        cursor.close()
        
def print_available_rooms():
    arr = []
    try:
        cursor = db.conn.cursor()

        # Fetch available room numbers
        query = "SELECT room_number FROM rooms WHERE available = TRUE"
        cursor.execute(query)
        available_rooms = cursor.fetchall()
        # print(available_rooms)
        if not available_rooms:
            print("No rooms are currently available.")
        else:
            print("Available Rooms:")
            for room in available_rooms:
                print("Room #", room[0])
                arr.append(room[0])
        return arr
    except psycopg2.Error as e:
        print("Error fetching available rooms:", e)

    finally:
        cursor.close()

def cancelSession(session_id):
    try:
        cursor = db.conn.cursor()

        # Delete session from the sessions table
        
        # Delete session from the trainingSessionParticipants table
        delete_training_participants_query = "DELETE FROM trainingSessionParticipants WHERE sessionId = %s"
        cursor.execute(delete_training_participants_query, (session_id,))

        # Delete session from the groupClassParticipants table
        delete_group_participants_query = "DELETE FROM groupClassParticipants WHERE sessionId = %s"
        cursor.execute(delete_group_participants_query, (session_id,))
        old_room_query = "SELECT roomNumber FROM sessions WHERE id = %s"
        cursor.execute(old_room_query, (session_id,))
        old_room_number = cursor.fetchone()[0]
        print(old_room_number)
        # Update availability of old room
        update_old_room_query = "UPDATE rooms SET available = TRUE WHERE room_number = %s"
        cursor.execute(update_old_room_query, (old_room_number,))

        delete_session_query = "DELETE FROM sessions WHERE id = %s"
        cursor.execute(delete_session_query, (session_id,))

        db.conn.commit()
        print("Session canceled successfully!")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error canceling session:", e)

    finally:
        cursor.close()

def updateSession(session_id):
    try:
        cursor = db.conn.cursor()

        # Ask which field to update
        print("Which field would you like to update?")
        print("1. Room Number")
        print("2. Session Date")
        print("3. Session Time")
        choice = input("Enter your choice: ")

        if choice == '1':
            field = 'roomNumber'
            rooms = print_available_rooms()
            new_value = input("Enter the new room number: ")
            if int(new_value) not in rooms:
                print("This room number does not exist or isnt available")
                return False
        elif choice == '2':
            field = 'sessionDate'
            new_value = input("Enter the new session date (YYYY-MM-DD): ")
        elif choice == '3':
            field = 'sessionTime'
            new_value = input("Enter the new session time (HH:MM:SS): ")
        else:
            print("Invalid choice!")
            return False

        if field == 'roomNumber':
            # Get the current room number
            old_room_query = "SELECT roomNumber FROM sessions WHERE id = %s"
            cursor.execute(old_room_query, (session_id,))
            old_room_number = cursor.fetchone()[0]

            # Update availability of old room
            update_old_room_query = "UPDATE rooms SET available = TRUE WHERE room_number = %s"
            cursor.execute(update_old_room_query, (old_room_number,))

            # Check room availability
            room_query = "SELECT available FROM rooms WHERE room_number = %s"
            cursor.execute(room_query, (new_value,))
            room_available = cursor.fetchone()[0]

            if not room_available:
                print("Room is not available for booking.")
                return False

            # Update room availability
            update_room_query = "UPDATE rooms SET available = FALSE WHERE room_number = %s"
            cursor.execute(update_room_query, (new_value,))

        # Update the session
        update_query = f"UPDATE sessions SET {field} = %s WHERE id = %s"
        cursor.execute(update_query, (new_value, session_id))
        send_notifications(session_id, field, new_value)
        db.conn.commit()
        print("Session updated successfully!")
        
        return True

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error updating session:", e)
        return False

    finally:
        cursor.close()


def send_notifications(session_id, field, new_value):
    try:
        cursor = db.conn.cursor()

        # Construct notification message based on the updated field
        message = f"Session {session_id } has been updated. {field.capitalize()} changed to {new_value}."

        # Get member IDs registered for the session
        member_query = "SELECT memberId FROM trainingSessionParticipants WHERE sessionId = %s"
        cursor.execute(member_query, (session_id,))
        member_ids = cursor.fetchall()

        # Insert notification for each member
        for member_id in member_ids:
            insert_member_notification_query = "INSERT INTO memberNotifications (member_id, message) VALUES (%s, %s)"
            cursor.execute(insert_member_notification_query, (member_id, message))

        db.conn.commit()
        print("Notifications sent successfully!")

    except psycopg2.Error as e:
            db.conn.rollback()
            print("Error sending notifications:", e)

    finally:
        cursor.close()


def viewSchedule(trainer_id):
    listofSessions = []
    try:
        cursor = db.conn.cursor()
        query = "SELECT * FROM sessions WHERE trainerId = %s"
        cursor.execute(query, (trainer_id,))
        sessions = cursor.fetchall()
        
        if sessions:
            print("Your Sessions:")
            for session in sessions:
                print(f"Session ID: {session[0]}")
                print(f"Room Number: {session[2]}")
                print(f"Session Type: {session[3]}")
                print(f"Session Date: {session[4]}")
                print(f"Session Time: {session[5]}")
                listofSessions.append(session[0])
                print("--------------------------")
        else:
            print("You have no scheduled sessions.")
        return listofSessions
    except psycopg2.Error as e:
        print("Error fetching sessions:", e)
    
    finally:
        cursor.close()

def viewMember(member_name):
    try:
        cursor = db.conn.cursor()

        # Split the input into first name and last name
        names = member_name.split()
        if len(names) == 1:
            first_name = names[0]
            last_name = ""
        else:
            first_name = names[0]
            last_name = names[-1]

        # Check if member_name matches either first_name or last_name ILIKE so case doesn't matter
        query = "SELECT first_name, last_name, email FROM members WHERE first_name ILIKE %s AND last_name ILIKE %s"
        cursor.execute(query, (f'%{first_name}%', f'%{last_name}%'))
        members = cursor.fetchall()

        if members:
            print("Members found:")
            for member in members:
                print("Name:", member[0], member[1])
                print("Email:", member[2])
                print()  # Empty line for better readability
        else:
            print("No members found.")

    except psycopg2.Error as e:
        print("Error during member profile viewing:", e)

    finally:
        cursor.close()

def printTrainerNotifications(trainer_id):
    try:
        cursor = db.conn.cursor()

        # Fetch notifications for the trainer
        query = "SELECT * FROM trainerNotifications WHERE trainer_id = %s"
        cursor.execute(query, (trainer_id,))
        trainerNotifications = cursor.fetchall()

        # Print trainer notifications
        print("Trainer Notifications:")
        if trainerNotifications:
            for notification in trainerNotifications:
                print(notification[2], notification[3]) 

            # Empty out notifications after viewing
            delete_query = "DELETE FROM trainerNotifications WHERE trainer_id = %s"
            cursor.execute(delete_query, (trainer_id,))
            db.conn.commit()
            print("Notifications emptied out.")
        else:
            print("No notifications for the trainer.")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error fetching or deleting trainer notifications:", e)

    finally:
        cursor.close()
