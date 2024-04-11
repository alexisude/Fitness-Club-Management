import member
import trainer
import admin
import datetime
# Variable to keep track of the current user
currentUser = None
currTrainer = None
currAdmin = None
# Main loop
while True:
    if currentUser is None:
        print("\nWho are you?")
        print("1. Trainer")
        print("2. Member")
        print("3. Admin")
        print("4. Exit")
        userInput = input("Please enter your choice: ")

        if userInput == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            currTrainer = trainer.trainerLogin(email, password)
            if currTrainer:
                print("Welcome,", currTrainer[1])
                # Now perform trainer-specific operations
                while True:
                    print("Trainer Operations:")
                    print("1. Create Session")
                    print("2. Member Profile Viewing")
                    print("3. View Schedule")
                    print("4. Notifications")
                    print("5. Update Session")
                    print("6. Cancel Session")
                    print("7. Refresh Sessions")
                    print("8. Logout")
                    trainerChoice = input("Please enter your choice: ")

                    if trainerChoice == '1':
                        try:
                            rooms = trainer.print_available_rooms()
                            room_number = input("Enter room number: ")
                            if int(room_number) not in rooms:
                                print("This room number does not exist or isnt available")
                            else:
                                session_type = input("Enter session type: ")
                                session_date = input("Enter session date (YYYY-MM-DD): ")
                                session_time = input("Enter session time (HH:MM): ")
                                trainer.createSession(currTrainer[0], room_number, session_type, session_date, session_time)
                        except Exception as e:
                            print("Error:", e)

                    elif trainerChoice == '2':
                        try:
                            member_name = input("Enter member's first name or full name: ")
                            trainer.viewMember(member_name)
                        except Exception as e:
                            print("Error:", e)
                    elif trainerChoice == '3':
                        trainer.viewSchedule(currTrainer[0])
                    elif trainerChoice == '4':
                        trainer.printTrainerNotifications(currTrainer[0])
                    elif trainerChoice == '5':
                        ids = trainer.viewSchedule(currTrainer[0])
                        print(ids)
                        sessionid = input("Enter the ID of the session you want to update: ")
                        if int(sessionid) not in ids:
                            print("This session dooes not exist")
                        else:
                            trainer.updateSession(sessionid)
                    elif trainerChoice == '6':
                        ids = trainer.viewSchedule(currTrainer[0])
                        print(ids)
                        sessionid = input("Enter the ID of the session you want to update: ")
                        if int(sessionid) not in ids:
                            print("This session dooes not exist")
                        else:
                            trainer.cancelSession(sessionid)
                    elif trainerChoice == '7':
                        trainer.refreshSessions()
                    elif trainerChoice == '8':
                        currTrainer = None
                        print("Logged out successfully.")
                        break 

                    else:
                        print("Invalid choice. Please enter a number between 1 and 7.")
            else:
                print("Trainer login failed.")

        elif userInput == '2':
            # Handle member operations
            print("1. Member Login")
            print("2. Member Registration")
            print("3. Back")
            member_choice = input("Please enter your choice: ")
            
            if member_choice == '1':
                # Perform member login
                email = input("Please enter your email: ")
                password = input("Please enter your password: ")
                currentUser = member.login(email, password)
                if currentUser:
                    print("Welcome Back!", currentUser[1])
                    print("--------------------------------------")
                else:
                    print("Invalid email or password.")
                
            elif member_choice == '2':
                # Perform member registration
                first_name = input("Please enter your first name: ")
                last_name = input("Please enter your last name: ")
                try:
                    height = float(input("Please enter your current height or guess: "))
                except ValueError:
                    print("Invalid input! Please enter a valid height.")
                try:
                    weight = float(input("Please enter current weight or guess: "))
                except ValueError:
                    print("Invalid input! Please enter a valid weight.")
                email = input("Please enter your email: ")
                password = input("Please enter your password: ")
                confirmPass= input("Please enter your password again: ")
                
                
                while (password != confirmPass):
                    password = input("Please enter your password: ")
                    confirmPass= input("Please enter your password again: ")
                currentUser = member.register(first_name, last_name, email, password, height, weight)
                
                if currentUser != None:
                    print("Welcome new member, good luck in your fitness journey")
                    currentUser =  member.login(email, password)# Simulate logged in user
                    print("--------------------------------------")
                else:
                    print("Registration failed. Please try again.")
                    print("--------------------------------------")
            
            elif member_choice == '3':
                pass  # Go back to main options

            else:
                print("Invalid choice. Please enter a number between 1 and 3.")

        elif userInput == '3':
            # Handle admin operations
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            currAdmin = admin.adminLogin(email, password)
            if currAdmin:
                print("Welcome, Admin")
                # Now perform trainer-specific operations
                while True:
                    admin_input = input("Enter the admin operation you want to perform \n1. Room Booking Management\n2. Equipment Maintenance Monitoring\n3. Add Equipment\n4. Class Schedule Updating \n5. View all Sessions\n6. Billing and Payment Processing \n7. Add Staff(Trainer)\n8. Refresh sessions \n9. LogOut \nEnter Choice: ")
            
                    if admin_input == '1':
                        admin.room_booking_management()
                    elif admin_input == '2':
                        admin.equipment_maintenance_monitoring()
                    elif admin_input == '3':
                        #add equipment
                        admin.add_equipment()
                    elif admin_input == '4':
                        #class Schedule Updating
                        admin.update_session()
                    elif admin_input == '5':
                        admin.print_all_sessions()
                    elif admin_input == '6':
                        admin.collect_monthly_fees()
                    elif admin_input == '7':
                        admin.create_trainer()
                    elif admin_input == '8':
                        trainer.refreshSessions()
                    elif admin_input == '9':
                        currAdmin = None
                        print("logged out sucessfully")
                        break
                    else:
                        print("Invalid admin operation.")

        elif userInput == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    else:
        # After login or registration, prompt member for further actions
        # print("Welcome, {}!".format(currentUser["first_name"]))
        print("What would you like to do?")
        print("1. Profile Management")
        print("2. Dashboard Display")
        print("3. Schedule Management")
        print("4. Create or modify an exercise routine")
        print("5. Workout Features")
        print("6. Notifications")
        print("7. Logout")
        user_input = input("Please enter your choice: ")
        
        if user_input == '1':
            while True:
                # Perform profile management actions
                
                print("What would you like to update?")
                print("1. First Name")
                print("2. Last Name")
                print("3. Email")
                print("4. Password")
                print("5. Height")
                print("6. Weight")
                print("7. Create fitness goals")
                print("8. Update fitness goals")
                print("9. Back")
                profile_input = input("Please enter your choice: ")

                if profile_input == '1':
                    # Update first name
                    new_first_name = input("Please enter your new first name: ")
                    # Call function to update first name
                    if member.update_member_info(currentUser[0], 'first_name', new_first_name):
                        print("First name updated successfully!")
                        print("--------------------------------------\n")

                elif profile_input == '2':
                    # Update last name
                    new_last_name = input("Please enter your new last name: ")
                    # Call function to update last name
                    if member.update_member_info(currentUser[0], 'last_name', new_last_name):
                        print("Last name updated successfully!")
                        print("--------------------------------------\n")

                elif profile_input == '3':
                    # Update email
                    new_email = input("Please enter your new email: ")
                    # Call function to update email
                    if member.update_member_info(currentUser[0], 'email', new_email):
                        print("Email updated successfully!")
                        print("--------------------------------------\n")

                elif profile_input == '4':
                    # Update password
                    new_password = input("Please enter your new password: ")
                    # Call function to update password
                    if member.update_member_info(currentUser[0], 'password', new_password):
                        print("Password updated successfully!")
                        print("--------------------------------------\n")

                elif profile_input == '5':
                    try:
                        new_height = float(input("Please enter your new height: "))
                        # Call function to update height
                        if member.update_member_info(currentUser[0], 'height', new_height):
                            print("Height updated successfully!")
                            print("--------------------------------------\n")
                    except ValueError:
                        print("Invalid input! Please enter a valid height.")
                elif profile_input == '6':
                    try:
                        new_weight = float(input("Please enter your new weight: "))
                        # Call function to update weight
                        if member.update_member_info(currentUser[0], 'weight', new_weight):
                            print("Weight updated successfully!")
                            print("--------------------------------------\n")
                    except ValueError:
                        print("Invalid input! Please enter a valid weight.")

                elif profile_input == '7':
                    goal_type = input("Enter goal type (e.g., weight, BMI, etc.): ")
                    try:
                        goal_value = float(input("Enter goal value: "))
                    except ValueError:
                        print("Invalid input! Please enter a valid number.")
                    goal_date = input("Enter goal deadline (YYYY-MM-DD): ")

                    # Call function to add goal to the database
                    if member.add_goal(int(currentUser[0]), goal_type, goal_value, goal_date):
                        print("Goal created successfully!")
                        print("--------------------------------------\n")
                    else:
                        print("Try again!")
                        print("--------------------------------------\n")

                elif profile_input == '8':
                    
                    print("What goal do you want to update?")
                    allGoals = member.print_goals(currentUser[0])
                    if (len(allGoals) != 0):
                        goal_num = input("Enter goal number: ")

                    
                        if int(goal_num) not in allGoals:
                            print("Invalid goal number! Please enter a valid goal number.")
                        else:
                            field = input("What field do you want to update?\n1. Goal Type\n2. Goal Value\n3. When goal is to be achieved\n4. Completed?\nEnter choice: ")

                            if field not in ['1', '2', '3', '4']:
                                print("Invalid choice. Please enter a number between 1 and 4.")
                            else:
                                if field == '1':
                                    field_name = 'goalType'
                                    new_value = input("Enter the new goal type: ")
                                elif field == '2':
                                    field_name = 'goalValue'
                                    try:
                                        new_value = float(input("Enter the new goal value: "))
                                    except ValueError:
                                        print("Invalid input! Please enter a valid number.")
                                elif field == '4':
                                    field_name = 'achieved'
                                    new_value = input("Enter the new goal value (True or False): ")
                                    if new_value.lower() not in ['true', 'false']:
                                        print("Invalid input! Please enter True or False.")
                                        break
                                else:
                                    field_name = 'goalDate'
                                    try:
                                        new_value = input("Enter the new deadline for the goal (YYYY-MM-DD): ")
                                    except ValueError:
                                        print("Invalid input! Please enter a valid date.")

                                # Call the update_goal function
                                if member.update_goal(currentUser[0], int(goal_num), field_name, new_value):
                                    print("Goal updated successfully!")
                                    print("--------------------------------------\n")
                                else:
                                    print("Failed to update goal.")

                elif profile_input == '9':
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 8.")


        elif user_input == '2':
            print(currentUser)
            member.display_dashboard(currentUser[0])

        elif user_input == '3':
            # Perform schedule management actions
            while True:
                print("Schedule Management:")
                print("1. Book Session")
                print("2. View Booked Sessions")
                print("3. Reschedule Session")
                print("4. Cancel Session")
                print("5. Back to Main Menu")
                schedule_choice = input("Please enter your choice: ")

                if schedule_choice == '1':
                    # Book Session
                    availabe = member.printAvailableSessions(currentUser[0])
                    if(availabe == []):
                        print("There are no available sessions to book")
                        break
                    session_id = input("Enter the ID of the session you want to book: ")
                   
                    if int(session_id) not in availabe:
                        print("This booking does not exist or is not availabe to you")
                    else:
                        booked = member.bookSession(currentUser[0], session_id)
                    
                elif schedule_choice == '2':
                    print("Your Sessions:")
                    member.viewBookedSessions(currentUser[0])
                elif schedule_choice == '3':
                    print("Your Sessions:")
                    value = member.viewBookedSessions(currentUser[0])

                    if(value == []):
                        # print("You have no sessions booked")
                        break
                    session_id = input("Enter the ID of the session you want to reschedule: ")
                    if int(session_id) not in value:
                        print("You never booked this")
                    else:
                        member.rescheduleSession(currentUser[0], session_id)
                elif schedule_choice == '4':
                    # Cancel Session
                    print("Your Sessions:")
                    value = member.viewBookedSessions(currentUser[0])
                    if(value == []):
                        # print("You have no sessions booked")
                        break
                    session_id = input("Enter the ID of the session you want to cancel: ")
                    
                    if int(session_id) not in value:
                        print("You never booked this")
                    else:
                        member.cancelSession(currentUser[0], session_id)

                elif schedule_choice == '5':
                    break  # Go back to the main menu

                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")

        elif user_input == '4':
            #. Create or modify an exercise routine"
            while True:
                print("1. Create a new exercise routine")
                print("2. Modify an existing exercise routine")
                print("3. Back")
                routine_choice = input("Please enter your choice: ")
                
                if routine_choice == '1':
                    # Create a new exercise routine
                    routine_details = input("Enter the details of the new exercise routine: ")
                    member.createRoutine(currentUser[0] , routine_details)
                    
                elif routine_choice == '2':
                    # Modify an existing exercise routine
                    member.modifyRoutine(currentUser[0])
                    
                elif routine_choice == '3':
                    break 
                    
                else:
                    print("Invalid choice. Please enter a valid option.")
        
        elif user_input == '5':
            member.workout_menu(currentUser[0])
        elif user_input == '6':
            member.printMemberNotifications(currentUser[0])

        elif user_input == '7':
            currentUser = None
            print("Logged out successfully.")

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
