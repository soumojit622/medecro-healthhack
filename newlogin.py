# Import necessary modules for GUI development and file operations
from tkinter import *  # Importing all functions from tkinter for GUI
import os  # Importing os module to interact with the operating system

# Function to destroy all child widgets of a parent widget


def destroyPackWidget(parent):
    # Loop through and destroy each packed widget
    for e in parent.pack_slaves():
        e.destroy()

# Function to display the registration screen


def register():
    global root, register_screen

    # Clear the root window before displaying registration screen
    destroyPackWidget(root)

    register_screen = root  # Use root as the registration screen
    register_screen.title("Register")  # Set the title of the window
    register_screen.geometry("300x250")  # Set the window dimensions

    # Define global variables to store user input
    global username
    global password
    global username_entry
    global password_entry

    # Initialize the variables for username and password
    username = StringVar()
    password = StringVar()

    # Display instructions and input fields for username and password
    Label(register_screen, text="Please enter the details below", bg="blue").pack()
    Label(register_screen, text="").pack()  # Spacer
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    # Hide password input
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()  # Spacer
    # Button to trigger user registration
    Button(register_screen, text="Register", width=10,
           height=1, bg="blue", command=register_user).pack()

# Function to display the login screen


def login():
    global login_screen
    login_screen = Toplevel(login_screen)  # Create a new window for login
    login_screen.title("Login")  # Set the title of the window
    login_screen.geometry("300x250")  # Set the window dimensions

    # Display instructions and input fields for username and password
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()  # Spacer

    # Define global variables to store user input for login
    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()

    # Define input fields for login
    global username_login_entry
    global password_login_entry
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()  # Spacer
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(
        login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()  # Spacer
    # Button to trigger login verification
    Button(login_screen, text="Login", width=10,
           height=1, command=login_verify).pack()

# Function to handle a successful registration event


def btnSucess_Click():
    global root
    # Clear the root window after successful registration
    destroyPackWidget(root)

# Function to handle user registration


def register_user():
    global root, username, password
    username_info = username.get()  # Get username input
    password_info = password.get()  # Get password input

    # Print the user details for debugging purposes
    print("abc", username_info, password_info, "xyz")

    # Save the username and password to a file
    # Open a file with the username as the filename
    file = open(username_info, "w")
    file.write(username_info + "\n")  # Write the username
    file.write(password_info)  # Write the password
    file.close()  # Close the file

    # Clear the input fields
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    # Display success message and button to proceed
    Label(root, text="Registration Success",
          fg="green", font=("calibri", 11)).pack()
    Button(root, text="Click Here to proceed", command=btnSucess_Click).pack()

# Function to verify login credentials


def login_verify():
    username1 = username_verify.get()  # Get entered username
    password1 = password_verify.get()  # Get entered password
    username_login_entry.delete(0, END)  # Clear username field
    password_login_entry.delete(0, END)  # Clear password field

    list_of_files = os.listdir()  # List all files in the directory
    if username1 in list_of_files:  # Check if the username file exists
        file1 = open(username1, "r")  # Open the username file
        verify = file1.read().splitlines()  # Read the file content line by line
        if password1 in verify:  # Check if the password matches
            login_sucess()  # Call success function
        else:
            password_not_recognised()  # Handle incorrect password
    else:
        user_not_found()  # Handle user not found case

# Popup window for successful login


def login_sucess():
    global login_success_screen
    # Create a new window for login success
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")  # Set the title
    login_success_screen.geometry("150x100")  # Set dimensions
    Label(login_success_screen, text="Login Success").pack()  # Display message
    Button(login_success_screen, text="OK",
           command=delete_login_success).pack()

# Popup window for incorrect password


def password_not_recognised():
    global password_not_recog_screen
    # Create a new window for incorrect password
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100")
    # Display error message
    Label(password_not_recog_screen, text="Invalid Password").pack()
    Button(password_not_recog_screen, text="OK",
           command=delete_password_not_recognised).pack()

# Popup window for user not found


def user_not_found():
    global user_not_found_screen
    # Create a new window for user not found
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("150x100")
    # Display error message
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK",
           command=delete_user_not_found_screen).pack()

# Function to close login success popup


def delete_login_success():
    login_success_screen.destroy()

# Function to close password not recognized popup


def delete_password_not_recognised():
    password_not_recog_screen.destroy()

# Function to close user not found popup


def delete_user_not_found_screen():
    user_not_found_screen.destroy()

# Function to display the main account screen


def main_account_screen(frmmain):
    main_screen = frmmain  # Use the passed frame as the main window

    # Set up the window size and title
    main_screen.geometry("300x250")
    main_screen.title("Account Login")

    # Display the title and buttons for login and registration
    Label(main_screen, text="Select Your Choice", bg="blue",
          width="300", height="2", font=("Calibri", 13)).pack()
    Label(main_screen, text="").pack()  # Spacer
    Button(main_screen, text="Login", height="2",
           width="30", command=login).pack()  # Login button
    Label(main_screen, text="").pack()  # Spacer
    Button(main_screen, text="Register", height="2", width="30",
           command=register).pack()  # Register button


# Start the application by initializing the main window
root = Tk()  # Create the root window
main_account_screen(root)  # Call the main screen
root.mainloop()  # Run the Tkinter main loop to keep the window open
