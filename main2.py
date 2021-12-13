from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    password_letters = [choice(letters) for items in range(randint(8, 10))]
    password_symbols = [choice(symbols) for sym in range(randint(2, 4))]
    password_numbers = [choice(numbers) for num in range(randint(2, 4))]
    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Rob's Password Manager")
window.config(padx=50, pady=50)

# main image
canvas = Canvas(width=200, height=200)
logo_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_png)
canvas.grid(column=1, row=0)

# labels for website, email and password
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# entry boxes for website, email and password

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_entry = Entry(width=39)
email_entry.insert(END, "rpether@hotmail.co.nz")
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# buttons for add and generate password
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
        }
    }
    # message box check input
    if password == "" or email == "" or website == "":
        messagebox.showinfo(title="Oops", message="Please make sure there aren't any empty fields")
    else:
        try:
            with open("password.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("password.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("password.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            # message box confirm input
            messagebox.showinfo(title=None, message="Your details have been saved")

def find_password():
    try:
        website = website_entry.get()
        with open("password.json", "r") as data_file:
            info = json.load(data_file)
        email = info[website]["email"]
        password = info[website]["password"]
        messagebox.showinfo(title=f"{website}", message=f"Email: {email} \n Password: {password}")
    except (KeyError, FileNotFoundError):
        messagebox.showinfo(title=f"{website} not found", message=f"There are no emails and passwords matching {website}")


search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1)

generate_button = Button(text="Generate Password", command=password_generator)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
