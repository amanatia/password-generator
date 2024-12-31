import random
from tkinter import * 
from tkinter import messagebox
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters= random.randint(8, 10) 
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
   
    letters_password = (random.choices(letters, k=nr_letters))
    symbols_password = (random.choices(symbols, k=nr_symbols))
    numbers_password = (random.choices(numbers, k= nr_numbers))
    
    password_list = letters_password + symbols_password + numbers_password
    random.shuffle(password_list)
    
    # Instead of all of this: 
    '''FinalPassword = ""

    for char in password_list:
        FinalPassword = FinalPassword + char'''
        
    # We can use this:
    password = "".join(password_list)
    
    password_entry.insert(0, password)
    
    pyperclip.copy(password) # this copies the password right away
                             # without you having to do anything    

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    new_data = {
        website:{
            "email": email,
            "password": password,
        }
    }
    
    if len(website)==0 or len(password) == 0:  
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:   
        try:                     
            with open("output.json", "r") as file:
                #Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("output.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            #Updating old data
            data.update(new_data)      
            
            with open("output.json", "w") as file:
                #Saving updated data
                json.dump(data, file, indent=4)
        finally:               
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            
   
            
            
# ---------------------------- SEARCH WEBSITE ------------------------------- #
def find_password():
    
    website = website_entry.get()
    
    try:
        with open("output.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Info", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Info", message="No details for the website")
    
    
      

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=400, height=400)

lock = PhotoImage(file="logo.png")
canvas.create_image(200, 200, image= lock)
canvas.grid(column=1, row=0)

website_label = Label(text="Website", font=("Arial", 10, "bold"))
website_label.grid(column=0, row=1)
website_entry = Entry(width=40)
website_entry.grid(column=1, row=1,columnspan=2)

email_label = Label(text="Email/Username", font=("Arial", 10, "bold"))
email_label.grid(column=0, row=2)
email_entry = Entry(width=40)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "amanda@gmail.com") #inserts text at the given index

password_label = Label(text="Password", font=("Arial", 10, "bold"))
password_label.grid(column=0, row=3)
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3)
password = password_entry.get()

generate = Button(text="Generate Password", command=generate_password)
generate.grid(column=2, row=3)

search = Button(text="Search", width=13,  command=find_password)
search.grid(column=2, row=1)

add = Button(text="Add", width=40, command=save)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()