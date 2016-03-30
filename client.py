import socket
import tkinter as tk
from tkinter import messagebox


class Login:
    def __init__(self, main):
        self.main = main

        self.user_lab = tk.Label(text="Username: ")
        self.pass_lab = tk.Label(text="Password: ")
        self.ip_lab = tk.Label(text="Server IP: ")

        self.user_entry = tk.Entry()
        self.pass_entry = tk.Entry(show="\u2022")
        self.ip_entry = tk.Entry()

        self.signup_but = tk.Button(text="Sign up", command=self.signup)
        self.login_but = tk.Button(text="Login", command=self.login)

    def draw(self):
        self.user_lab.grid(column=0, row=0)
        self.pass_lab.grid(column=0, row=1)
        self.ip_lab.grid(column=0, row=2)

        self.user_entry.grid(column=1, row=0, columnspan=3)
        self.pass_entry.grid(column=1, row=1, columnspan=3)
        self.ip_entry.grid(column=1, row=2, columnspan=3)

        self.signup_but.grid(column=0, row=3, columnspan=3)
        self.login_but.grid(column=2, row=3)

    def undraw(self):
        self.user_lab.grid_forget()
        self.pass_lab.grid_forget()
        self.ip_lab.grid_forget()

        self.user_entry.grid_forget()
        self.pass_entry.grid_forget()
        self.ip_entry.grid_forget()

        self.signup_but.grid_forget()
        self.login_but.grid_forget()

    def connect(self):
        host = self.ip_entry.get()
        try:
            if host:
                self.main.s.connect((host, 54321))
            else:
                self.main.s.connect(self.main.server)
            return True

        except ConnectionRefusedError:
            self.main.popup("warning", "Could not connect to supplied server.\nIs the server running?")
            return False

        except OSError as e:
            if str(e) == "[WinError 10051] A socket operation was attempted to an unreachable network":
                self.main.popup("warning", "Could not connect to supplied server.\nIs the server running?")
                return False
            return True

    # Signup
    def signup(self):
        user = self.user_entry.get()
        passw = self.pass_entry.get()

        if not user or not passw:
            self.main.popup("warning", "Username or password fields blank.")
            return

        if self.connect():
            try:
                self.main.s.send("#signup:{}:{}".format(user, passw).encode('utf-8'))
                reply = self.main.s.recv(1024)
                reply = reply.decode('utf-8')
                print(reply)
                if not reply:
                    self.main.popup("warning", "Server did not respond!")
                if reply == "#signedup":
                    self.main.popup("info", "Registered successfully, please log in.")
                split = reply.split(':')
                if split[0] == "#error":
                    if split[1] == "conflict":
                        self.main.popup("warning", "That username is already in use.")
            except Exception as e:
                print(e)

    # Login
    def login(self):
        user = self.user_entry.get()
        passw = self.pass_entry.get()

        if not user or not passw:
            self.main.popup("warning", "Username or password fields blank.")
            return

        if self.connect():
            try:
                self.main.s.send("#login:{}:{}".format(user, passw).encode('utf-8'))
                reply = self.main.s.recv(1024)
                reply = reply.decode('utf-8')
                print(reply)
                if not reply:
                    self.main.popup("warning", "Server did not respond!")

                if reply == "#loggedin":
                    self.undraw()
                    self.main.user = user
                    self.main.current_window = self.main.game
                    self.main.current_window.draw()
                    self.main.current_window.update()

                split = reply.split(':')
                if split[0] == "#error":
                    if split[1] == "badlogin":
                        self.main.popup("warning", "That account doesn't exist.")

            except Exception as e:
                print(e)


class Letters:
    def __init__(self, main):
        self.main = main

        self.alph = list("abcdefghijklmnopqrstuvwxyz".upper())
        self.guessed = []
        self.buttons = dict()
        for i in range(0, 26):
            self.buttons[i] = tk.Button(state="disabled", text=self.alph[i], width=2, command=lambda x=i: self.click(x))

    def draw(self):
        for but in self.buttons:
            self.buttons[but].grid(row=3, column=but)

    def undraw(self):
        for but in self.buttons:
            self.buttons[but].grid_forget()

    def activate(self):
        for but in self.buttons:
            self.buttons[but].configure(state="active")

    def disable(self):
        for but in self.buttons:
            self.buttons[but].configure(state="disabled")

    def click(self, id):
        self.buttons[id].configure(state="disabled")
        self.guessed.append(self.alph[id].lower())
        if self.alph[id].lower() in self.main.game.word:
            disp = " ".join([char if char in self.guessed else "_" for char in self.main.game.word])
            self.main.game.word_lab.configure(text=disp.upper())
            if "".join(self.main.game.word) == disp.replace(" ", ""):
                self.main.popup("info", "Correct!")
                self.disable()
                try:
                    self.main.s.send("#finished:{}".format(self.main.user).encode('utf-8'))
                    reply = self.main.s.recv(1024)
                    reply = reply.decode('utf-8')
                    print(reply)
                    if not reply:
                        self.main.popup("warning", "Server did not respond!")
                    split = reply.split(':')
                    if split[0] == "#winner":
                        self.main.popup("info", "{} won that round!".format(split[1]))
                except Exception as e:
                    print(e)
        else:
            if self.main.game.tries - 1 < 0:
                self.main.popup("info", "You've lost!")
                self.main.game.lost = True
                self.disable()
            else:
                self.main.game.tries -= 1
        self.main.game.hangman.configure(image=self.main.game.photos[9-self.main.game.tries])
        self.main.game.hangman.image = self.main.game.photos[9-self.main.game.tries]


class Game:
    def __init__(self, main):
        self.main = main
        self.tries = 9
        self.lost = False
        self.word = ""

        # Pictures
        self.photos = dict()
        for i in range(0, 10):
            self.photos[i] = tk.PhotoImage(file="images/{}.gif".format(i))

        self.hangman = tk.Label(image=self.photos[0])
        self.hangman.image = self.photos[0]

        self.word_lab = tk.Label(text="Waiting for word...")
        self.letters = Letters(main)

        self.counter_lab = tk.Label(text=45)

    def draw(self):
        self.counter_lab.grid(column=0, row=0, columnspan=26)
        self.hangman.grid(column=0, row=1, columnspan=26)
        self.word_lab.grid(column=0, row=2, columnspan=26)
        self.letters.draw()

    def undraw(self):
        self.counter_lab.grid_forget()
        self.hangman.grid_forget()
        self.word_lab.grid_forget()
        self.letters.undraw()

    def update(self):
        try:
            self.main.s.send("#gettime".encode('utf-8'))
            reply = self.main.s.recv(1024)
            counter = reply.decode('utf-8')
            print(counter)
            if not counter:
                self.main.popup("warning", "Server did not respond!")
            if counter.isdigit():
                self.counter_lab.configure(text=str(int(counter)-1))
                if self.lost and int(counter) == 1:
                    try:
                        self.main.s.send("#lost".encode('utf-8'))
                        reply = self.main.s.recv(1024)
                        reply = reply.decode('utf-8')
                        print(reply)
                        if not reply:
                            self.main.popup("warning", "Server did not respond!")
                        split = reply.split(':')
                        if split[0] == "#winner":
                            self.main.popup("info", "{} won that round!".format(split[1]))
                    except Exception as e:
                        print(e)

                if int(counter) == 45:
                    print("getting word")
                    self.main.s.send("#getword".encode('utf-8'))
                    reply = self.main.s.recv(1024)
                    self.word = reply.decode('utf-8')
                    if not self.word:
                        self.main.popup("warning", "Server did not respond!")
                    else:
                        self.word_lab.configure(text="_ " * len(self.word))
                        self.letters.activate()
                        self.letters.guessed = []
                elif int(counter) > 45:
                    self.word_lab.configure(text="Waiting for word...")
                    self.hangman.configure(image=self.photos[0])
                    self.hangman.image = self.photos[0]
                    self.letters.disable()
                    self.tries = 9
        except Exception as e:
            print(e)

        finally:
            self.main.root.after(1000, self.update)


class App:
    def __init__(self):
        # App
        self.root = tk.Tk()
        self.root.title("C'mon boys")

        # Networking
        self.s = socket.socket()
        self.s.settimeout(2)
        self.server = (socket.gethostname(), 54321)
        self.current_window = ''

        # UI declare
        self.login = Login(self)
        self.game = Game(self)

        # Build app
        self.current_window = self.login
        self.current_window.draw()

        self.root.mainloop()

    @staticmethod
    def popup(box, msg):
        if box == "info":
            messagebox.showinfo("Information", msg)
        if box == "warning":
            messagebox.showwarning("Warning", msg)
        if box == "error":
            messagebox.showerror("Error", msg)


app = App()
