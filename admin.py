import psycopg2
import db
import trainer
import datetime
def adminLogin(email, password):
    try:
        cursor = db.conn.cursor()
        query = "SELECT * FROM admins WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        admin = cursor.fetchone()
        if admin:
            print("Login successful!")
            return admin
        else:
            print("Invalid email or password.")
            return None
    except psycopg2.Error as e:
        print("Error logging in:", e)
        return None
    finally:
        cursor.close() 

def create_trainer():
    try:
        cursor = db.conn.cursor()

        # Gather trainer information from the user
        first_name = input("Enter the first name of the trainer: ")
        last_name = input("Enter the last name of the trainer: ")
        email = input("Enter the email of the trainer: ")
        password = input("Enter the password for the trainer: ")

        # Insert the trainer information into the database
        insert_query = "INSERT INTO trainers (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (first_name, last_name, email, password))
        db.conn.commit()
        print("Trainer added successfully!")

        # Query the database to fetch the newly inserted trainer's details by their email
        query = "SELECT * FROM trainers WHERE email = %s"
        cursor.execute(query, (email,))
        added_trainer = cursor.fetchone()

        return added_trainer
    except psycopg2.Error as e:
        print("Error creating trainer:", e)
        return None
    finally:
        cursor.close()
# def room_booking_management():
#     try:
#         cursor = db.conn.cursor()

#         # Fetch available rooms
#         query = "SELECT room_number FROM rooms WHERE available = TRUE"
#         cursor.execute(query)
#         available_rooms = cursor.fetchall()

#         if not available_rooms:
#             print("No rooms are currently available.")
#             return

#         print("Available Rooms:")
#         for room in available_rooms:
#             print("Room Number:", room[0])

#         room_number = int(input("Enter the room number you want to book: "))
#         # Check if the selected room is available
#         query = "SELECT available FROM rooms WHERE room_number = %s"
#         cursor.execute(query, (room_number,))
#         room_status = cursor.fetchone()

#         if not room_status or not room_status[0]:
#             print("Room is not available for booking.")
#             return

#         # Update room availability
#         update_query = "UPDATE rooms SET available = FALSE WHERE room_number = %s"
#         cursor.execute(update_query, (room_number,))
#         db.conn.commit()
#         print("Room booked successfully.")

#     except psycopg2.Error as e:
#         print("Error in room booking management:", e)

#     finally:
#         cursor.close()



def room_booking_management():
    try:
        cursor = db.conn.cursor()

        print("Room Booking Management Options:")
        print("1. Book a Room")
        print("2. Cancel a Room Booking")
        print("3. Refresh Room Bookings")
        choice = input("Enter your choice: ")

        if choice == '1':
            book_room(cursor)
        elif choice == '2':
            cancel_room_booking(cursor)
        elif choice == '3':
            refresh_room_bookings(cursor)
        else:
            print("Invalid choice!")

    except psycopg2.Error as e:
        print("Error in room booking management:", e)

    finally:
        cursor.close()


def book_room(cursor):
    try:
        # Fetch available rooms
        query = "SELECT room_number FROM rooms WHERE available = TRUE"
        cursor.execute(query)
        available_rooms = cursor.fetchall()

        if not available_rooms:
            print("No rooms are currently available.")
            return

        print("Available Rooms:")
        for room in available_rooms:
            print("Room Number:", room[0])

        room_number = int(input("Enter the room number you want to book: "))
        booking_date = input("Enter the booking date (YYYY-MM-DD): ")

        # Convert booking date to datetime object
        booking_date_obj = datetime.datetime.strptime(booking_date, '%Y-%m-%d').date()

        # Check if the booking date is in the past
        if booking_date_obj < datetime.date.today():
            print("Cannot book a room for a past date.")
            return

        # Check if the selected room is available
        query = "SELECT available FROM rooms WHERE room_number = %s"
        cursor.execute(query, (room_number,))
        room_status = cursor.fetchone()

        if not room_status or not room_status[0]:
            print("Room is not available for booking.")
            return

        # Book the room
        insert_query = "INSERT INTO admin_bookings (room_number, booking_date) VALUES (%s, %s)"
        cursor.execute(insert_query, (room_number, booking_date_obj))

        # Update room availability
        update_query = "UPDATE rooms SET available = FALSE WHERE room_number = %s"
        cursor.execute(update_query, (room_number,))
        db.conn.commit()
        print("Room booked successfully.")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error booking room:", e)


def cancel_room_booking(cursor):
    try:
        # Fetch booked rooms and their IDs
        query = "SELECT booking_id, room_number, booking_date FROM admin_bookings"
        cursor.execute(query)
        bookings = cursor.fetchall()

        if not bookings:
            print("No room bookings found.")
            return

        print("Booked Rooms:")
        for booking in bookings:
            print("Booking ID:", booking[0])
            print("Room Number:", booking[1])
            print("Booking Date:", booking[2])
            print("-------------------------")

        booking_id = int(input("Enter the booking ID you want to cancel: "))

        # Check if the entered booking ID exists
        if booking_id not in [booking[0] for booking in bookings]:
            print("Invalid booking ID.")
            return

        # Fetch room number for the booking
        room_number_query = "SELECT room_number FROM admin_bookings WHERE booking_id = %s"
        cursor.execute(room_number_query, (booking_id,))
        room_number = cursor.fetchone()[0]

        # Delete booking from admin_bookings
        delete_query = "DELETE FROM admin_bookings WHERE booking_id = %s"
        cursor.execute(delete_query, (booking_id,))

        # Update room availability
        update_query = "UPDATE rooms SET available = TRUE WHERE room_number = %s"
        cursor.execute(update_query, (room_number,))
        db.conn.commit()
        print("Room booking canceled successfully.")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error canceling room booking:", e)

def refresh_room_bookings(cursor):
    try:
        # Get current date
        current_date = datetime.date.today()

        # Find expired bookings
        expired_bookings_query = "SELECT booking_id, room_number FROM admin_bookings WHERE booking_date < %s"
        cursor.execute(expired_bookings_query, (current_date,))
        expired_bookings = cursor.fetchall()

        if expired_bookings:
            for booking_id, room_number in expired_bookings:
                # Delete the expired booking
                delete_query = "DELETE FROM admin_bookings WHERE booking_id = %s"
                cursor.execute(delete_query, (booking_id,))

                # Update room availability
                update_query = "UPDATE rooms SET available = TRUE WHERE room_number = %s"
                cursor.execute(update_query, (room_number,))

            db.conn.commit()
            print("Expired room bookings removed successfully.")
        else:
            print("No expired room bookings found.")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error refreshing room bookings:", e)


def equipment_maintenance_monitoring():
    try:
        cursor = db.conn.cursor()
        listOfEquipment = []
        # Fetch equipment information from the database
        query = "SELECT id, equipment_name, last_maintenance_date FROM equipment"
        cursor.execute(query)
        equipment_list = cursor.fetchall()

        if not equipment_list:
            print("No equipment found.")
        else:
            print("Equipment Maintenance Monitoring")
            print("=================================")
            for equipment in equipment_list:
                equipment_id, equipment_name, last_maintenance_date = equipment
                print(f"Equipment ID: {equipment_id}")
                print(f"Equipment Name: {equipment_name}")
                print(f"Last Maintenance Date: {last_maintenance_date}")
                listOfEquipment.append(equipment_id)
                print("---------------------------------")

            # Ask if the admin wants to update maintenance date
            update_choice = input("Do you want to update the maintenance date of any equipment? (yes/no): ")
            if update_choice.lower() == 'yes':
                equipment_id_to_update = input("Enter the ID of the equipment to update maintenance date: ")
                
                # Check if the entered equipment ID exists
                if int(equipment_id_to_update) not in listOfEquipment:
                    print("Invalid equipment ID. Please enter a valid ID.")
                    return
                
                new_maintenance_date = input("Enter the new maintenance date (YYYY-MM-DD): ")

                # Update the maintenance date of the equipment
                update_query = "UPDATE equipment SET last_maintenance_date = %s WHERE id = %s"
                cursor.execute(update_query, (new_maintenance_date, equipment_id_to_update))
                db.conn.commit()
                print("Maintenance date updated successfully!")
            elif update_choice.lower() == 'no':
                print("No updates made.")
            else:
                print("Not a valid option")
    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error updating maintenance date:", e)

    finally:
        cursor.close()

def add_equipment():
    try:
        cursor = db.conn.cursor()
        equipment_name = input("Enter equipment name: ")
        last_maintenance_date = input("Enter last maintenance date (YYYY-MM-DD): ")
        # Insert equipment information into the database
        query = "INSERT INTO equipment (equipment_name, last_maintenance_date) VALUES (%s, %s)"
        cursor.execute(query, (equipment_name, last_maintenance_date))
        db.conn.commit()

        print("Equipment added successfully!")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error adding equipment:", e)

    finally:
        cursor.close()


def print_all_sessions():
    session_ids = []
    try:
        cursor = db.conn.cursor()
        query = "SELECT id, trainerId, roomNumber, sessionType, sessionDate, sessionTime FROM sessions"
        cursor.execute(query)
        sessions = cursor.fetchall()

        if sessions:
            print("All Sessions:")
            for session in sessions:
                session_id = session[0]
                session_ids.append(session_id)
                trainer_id = session[1]
                room_number = session[2]
                session_type = session[3]
                session_date = session[4]
                session_time = session[5]

                print(f"Session ID: {session_id}")
                print(f"Trainer ID: {trainer_id}")
                print(f"Room Number: {room_number}")
                print(f"Session Type: {session_type}")
                print(f"Session Date: {session_date}")
                print(f"Session Time: {session_time}")
                print("--------------------------")

        else:
            print("No sessions found.")

        return session_ids

    except psycopg2.Error as e:
        print("Error fetching sessions:", e)
        return []

    finally:
        cursor.close()

def update_session():
    try:
        cursor = db.conn.cursor()
        ids = print_all_sessions()
        # Get session ID from the user
        session_id = input("Enter the ID of the session to update: ")
        if len(ids) == 0:
            print("There are no sessions to update.")
            return False
        
        # Check if the session exists
        query = "SELECT * FROM sessions WHERE id = %s"
        cursor.execute(query, (session_id,))
        session = cursor.fetchone()
        if not session:
            print("Session not found.")
            return False

        # Get the field to update from the user
        print("Choose the field to update:")
        print("1. Room Number")
        print("2. Session Date")
        print("3. Session Time")
        choice = input("Enter your choice: ")

        # Validate user choice
        if choice not in ['1', '2', '3']:
            print("Invalid choice.")
            return False

        field = ""
        new_value = ""

        # Get the new value based on the selected field
        if choice == '1':
            field = 'roomNumber'
            rooms = trainer.print_available_rooms()
            new_value = input("Enter the new room number: ")
            if int(new_value) not in rooms:
                print("This room number does not exist or isn't available")
        elif choice == '2':
            field = 'sessionDate'
            new_value = input("Enter the new session date (YYYY-MM-DD): ")
        elif choice == '3':
            field = 'sessionTime'
            new_value = input("Enter the new session time (HH:MM): ")

        # Check if updating room number and verify room availability
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
        
        # Define the SQL query based on the field to be updated
        query = f"UPDATE sessions SET {field} = %s WHERE id = %s"

        # Execute the SQL query with the new value and session ID
        cursor.execute(query, (new_value, session_id))
        db.conn.commit()
        print("Session updated successfully!")

        # Send notifications to members and the trainer
        send_notifications(session_id, field, new_value)

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

        # Get the trainer ID for the session
        trainer_query = "SELECT trainerId FROM sessions WHERE id = %s"
        cursor.execute(trainer_query, (session_id,))
        trainer_id = cursor.fetchone()[0]

        # Insert notification for trainer
        insert_trainer_notification_query = "INSERT INTO trainerNotifications (trainer_id, message) VALUES (%s, %s)"
        cursor.execute(insert_trainer_notification_query, (trainer_id, message))

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

def collect_monthly_fees():
    try:
        cursor = db.conn.cursor()

        # Fetch all members who have not paid their monthly fees
        query = "SELECT id, first_name, last_name FROM members WHERE id NOT IN (SELECT member_id FROM payments WHERE EXTRACT(YEAR FROM payment_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND EXTRACT(MONTH FROM payment_date) = EXTRACT(MONTH FROM CURRENT_DATE))"
        cursor.execute(query)
        unpaid_members = cursor.fetchall()

        if not unpaid_members:
            print("All members have paid their monthly fees.")
        else:
            print("Unpaid Members:")
            for member in unpaid_members:
                print(f"ID: {member[0]}, Name: {member[1]} {member[2]}")

            # Prompt admin to select a member to collect fees
            member_id = input("Enter the ID of the member to collect monthly fees from: ")

            # Validate member ID
            if not member_id.isdigit() or int(member_id) not in [member[0] for member in unpaid_members]:
                print("Invalid member ID. Please enter a valid ID from the list.")
                return

            # Prompt for amount
            amount = input("Enter the amount to collect: ")

            # Validate amount
            try:
                amount = float(amount)
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
                return

            # Record the payment in the payments table
            insert_query = "INSERT INTO payments (member_id, amount, payment_date) VALUES (%s, %s, CURRENT_DATE)"
            cursor.execute(insert_query, (member_id, amount))
            db.conn.commit()
            print("Monthly fees collected successfully.")

    except psycopg2.Error as e:
        db.conn.rollback()
        print("Error collecting monthly fees:", e)

    finally:
        cursor.close()


