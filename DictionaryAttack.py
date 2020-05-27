'''
Created on Apr 26, 2020

@author: lukeh
'''
import hashlib
import time
import itertools as it
import tkinter
import matplotlib.pyplot as plt

#Creates the program window
root = tkinter.Tk()
root.title("Dictionary Attack - HW13")
root.geometry("800x500")
root.configure(background="grey")

#Makes a label prompting user to enter password
password_label = tkinter.Label(root, text="Enter in your password", font=("Helvetica", 14), bg="grey")
password_label.place(rely=0.1, relx=0.38)

#Makes an entry box for the password
password_entry = tkinter.Entry(root)
password_entry.place(x=335, y=100)

#Makes a label for the solved password
solved_password = tkinter.Label(root, text="", bg="grey", font=("Helvetica", 12))
solved_password.place(x=285, y=200)

#Makes a label for the hash algorithm type
hash_type = tkinter.Label(root, text="", bg="grey", font=("Helvetica", 12))
hash_type.place(x=200, y=275)

#Makes a label for the dictionary size
dict_size = tkinter.Label(root, text="", bg="grey", font=("Helvetica", 12))
dict_size.place(x=200, y=320)

#Makes a label for the number of guesses
num_guess = tkinter.Label(root, text="", bg="grey", font=("Helvetica", 12))
num_guess.place(x=450, y=275)

#Makes a label for the time it took to solve
time_taken = tkinter.Label(root, text="", bg="grey", font=("Helvetica", 12))
time_taken.place(x=450, y=320)

#Creates array of lengths and times for different password to display graphically
pswrd_lengths = []
times_taken = []

#Crates the plot to display data graphically
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(pswrd_lengths, times_taken, "bo")
plt.xlabel("Length of Password")
plt.ylabel("Time to Solve in Seconds")
fig.canvas.draw()

#Two helper functions for each button command
def pushed_256():
    main(0)

def pushed_512():
    main(1)

#Main function, tracks time, reads dictionary file, encodes password, configures labels to print final info, and updates the plot
def main(hash_algorithm):
    start = time.time()
    user_password = password_entry.get()
    password_length = len(user_password)
    
    if hash_algorithm == 0:
        temp = hashlib.sha256(user_password.encode("ascii"))
        encoded_password = temp.hexdigest()
        hash_is = "SHA-256"
    else:
        temp = hashlib.sha512(user_password.encode("ascii"))
        encoded_password = temp.hexdigest()
        hash_is ="SHA-512"
        
    file = open("Dictionary.txt", "r")
    dictionary = file.readlines()
    dictionary_size = len(dictionary)
    for i in range(len(dictionary)):
        dictionary[i] = dictionary[i].rstrip("\n")
    file.close()
    
    vals = find_password(dictionary, hash_algorithm, password_length, encoded_password)
    
    #if the password can't be found, stop the function
    if vals == 0:
        return
    
    cracked_password = vals[0]
    num_guesses = vals[1]
    
    end = time.time()
    run_time = end-start
    
    solved_password.configure(text="Your password is: " + cracked_password)
    
    hash_type.configure(text="Hash type: " + hash_is)
    
    dict_size.configure(text="Dictionary size: " + str(dictionary_size))
    
    num_guess.configure(text="Number of guesses: " + str(num_guesses))
    
    time_taken.configure(text="Time taken: " + str(run_time))
    
    pswrd_lengths.append(password_length)
    times_taken.append(run_time)
    
    ax.clear()
    line1, = ax.plot(pswrd_lengths, times_taken, "bo")
    plt.xlabel("Length of Password")
    plt.ylabel("Time to Solve in Seconds")
    fig.canvas.draw()

#Helper function for main, creates combinations of passwords from the dictionary and compares hashes
def find_password(dict_list, hash_algorithm, pwrd_len, encoded_password):
    try:
        num_guesses = 0
        for i in range(len(dict_list)):
            combos = list(it.combinations(dict_list, i))
            for j in range(len(combos)):
                word = ""
                for k in range(len(combos[j])):
                    word = word + combos[j][k]
                if len(word) == pwrd_len:
                    if hash_algorithm == 0:
                        check_hash = hashlib.sha256(word.encode("ascii")).hexdigest()
                    else:
                        check_hash = hashlib.sha512(word.encode("ascii")).hexdigest()
                    num_guesses = num_guesses + 1
                    if check_hash == encoded_password:
                        return(word, num_guesses)
    #If the password can't be found, return 0 
    except MemoryError:
        solved_password.configure(text="Could not find")
        return(0)

#Makes the button to run the password under SHA-256
button_256 = tkinter.Button(root, text="SHA-256", command=pushed_256)
button_256.place(x=325, y=150)

#Makes the button to run the password under SHA-512
button_512 = tkinter.Button(root, text="SHA-512", command=pushed_512)
button_512.place(x=412, y=150)

#Runs the program window
root.mainloop()