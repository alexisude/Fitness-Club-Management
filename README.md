# Fitness-Club-Management-Project README

This project interacts with a PostgreSQL database containing all tables needed for the running of the app. This project is a software application designed to streamline the operations of a health and fitness club. It provides functionalities for both members and administrators to manage various aspects of the club efficiently.

# Video Link: https://www.youtube.com/watch?v=klCxkkQeeTU

# Steps to Run the Project:
1. **Install Required Dependencies:**
   - Make sure you have Python installed on your system.
   - Install the psycopg2 package using pip:
     ```
     pip install psycopg2
     ```
2. **Set Up the Database:**
   - Ensure you have PostgreSQL installed on your system.
   - Create a database named "Fitness Club Management" and set up the necessary tables using the DDL and DML files in the sql folder. Use the Query tool and upload the DDL.sql file or copy paste into the file and run then do the same for the DML.sql

3. **Compile and Run the Application:**
   - Save the provided Python files (main.py, member.py, trainer.py, admin.py, db.py) in  the same directory.
   - change the connection parameters in db.py to the parmaeters of your postgres server (user and password)
   - Open a terminal or command prompt and navigate to the directory containing the python files.
   - Run the script using Python python main.py

4. **Interact with the Application:**  
  - Once the application runs, you will be prompted to choose your role: member, trainer, or admin.
  - Members can register directly within the application. Trainers and admins need to use credentials provided in the DML.sql file.
  - Available commands include:
      - Registration: New members can register by providing their details.
      - Login: Members, trainers, and admins can log in using their credentials.
      - Member Actions: Members can book sessions, track health metrics, and pay fees.
      - Trainer Actions: Trainers can manage sessions and view member details.
      - Admin Actions: Admins can manage trainers, rooms, equipment, session bookings, and collect fees.
  - Follow the prompts to execute the desired commands.

5. **Exiting the Application:**
   - To exit the application, there is an option depending what part of the program you are on, if just starting simply click 4 to exit.
   - Or, press Ctrl + C in the terminal to terminate the script.

## Important Note:
Before running the application, Ensure that your PostgreSQL server is running and accessible with the connection parameters provided in db.py.
- Review and modify the connection parameters in db.py if necessary to match your PostgreSQL configuration.
"# Fitness-Club-Management" 
