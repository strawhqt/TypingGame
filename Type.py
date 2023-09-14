import tkinter as tk
from random import randint
import threading
from PIL import Image, ImageTk, ImageSequence
import winsound
import time

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.canvas = tk.Canvas(self, width=1270, height=560, bg = "black")
        self.canvas.grid(row = 0, column = 0)
        self.targets = []
        self.words = []
        self.game_over = False
        self.how_long_to_create_target = 3.5
        self.bottom = 500
        self.lives = 0
        self.first_click = True
        self.difficulty_speed = {"Relaxation" : 1, "Easy" : 2, "Normal" : 3, "Hard" : 5, "Expert" : 6, "Insane" : 8}
        self.words_typed = 0;
        self.level = 1;
        self.time_played = 0

        f = open("words.txt", "r")
        self.words = f.readlines()

        self.input = tk.Entry(self, font="16", justify="center")
        self.input.grid(row = 1, column = 0, ipadx = 100, ipady = 15)

        self.counter = tk.Label(self, text = " Words Typed: " + str(self.words_typed) + "       Lives Left: " + str(10 - self.lives) + " ", font = "12")
        self.counter.grid(row = 2, column = 0)

        self.input.insert(0, "Click here to start typing")
        self.input.bind('<FocusIn>', self.on_entry_click)
        self.input.bind('<Return>', self.destroy_target)

        self.play = self.canvas.create_text(635, 250, font = ('Times New Roman', 30,  'bold'), text = "Play", fill = "white")
        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.configure(width=10)
        self.canvas.create_window(590, 300, anchor= 'center', window=self.start_button)
        self.exit_button = tk.Button(self, text="Exit", command=self.quit)
        self.exit_button.configure(width=10)
        self.canvas.create_window(680, 300, anchor='center', window=self.exit_button)

    def start(self): #start menu
        self.canvas.delete('all')

        self.start_menu = tk.Toplevel()
        self.start_menu.title("Start Menu")
        self.start_menu.geometry("{}x{}+0+0".format(main_window.winfo_screenwidth() - 800, main_window.winfo_screenheight() - 600))

        self.choose_difficulty = tk.Label(self.start_menu, text = "Choose your difficulty:")
        self.choose_difficulty.grid(row = 1, column = 0)

        self.difficulty = tk.StringVar()
        self.difficulty.set("Normal")
        self.difficulties_menu = tk.OptionMenu(self.start_menu, self.difficulty, "Relaxation", "Easy", "Normal", "Hard", "Expert", "Insane")
        self.difficulties_menu.grid(row = 1, column = 1)


        self.choose_mode = tk.Label(self.start_menu, text = "Choose your mode:")
        self.choose_mode.grid(row = 0, column = 0)

        self.start_button = tk.Button(self.start_menu, text = "Start", command = lambda: [self.start_menu.destroy(), self.create_game()])
        self.start_button.grid(row = 2, column = 3)

        self.mode = tk.StringVar()
        self.mode.set("Survival")
        self.modes_menu = tk.OptionMenu(self.start_menu, self.mode, "Practice", "Survival", "Levels", command = self.check_if_level)
        self.modes_menu.grid(row = 0, column = 1)

    def check_if_level(self, event):
        if self.mode.get() == "Levels":
            self.choose_difficulty.destroy()
            self.choose_difficulty = tk.Label(self.start_menu, text = "Choose your difficulty:", bg = "gray")
            self.choose_difficulty.grid(row = 1, column = 0)
            self.difficulties_menu.configure(state = "disabled")

    def create_game(self): #Game Starts
        self.how_long_to_create_target -= self.difficulty_speed[self.difficulty.get()] / 4
        if self.mode.get() == "Practice":
            temp = self.canvas.create_text(630, 250, font = ('Times New Roman', '30', 'bold'), text = "Practice Mode: You have infinite lives!", fill = "white")
            self.counter.destroy()
            self.counter = tk.Label(self, text = " Words Typed: " + str(self.words_typed), font = "12")
            self.counter.grid(row = 2, column = 0)
        elif self.mode.get() == "Survival":
            self.counter.destroy()
            self.counter = tk.Label(self, text=" Words Typed: " + str(self.words_typed) + "       Lives Left: " + str(10 - self.lives) + " ", font="12")
            self.counter.grid(row=2, column=0)
            temp = self.canvas.create_text(630, 250, font = ('Times New Roman', '30', 'bold'), text = "Survival Mode: Try to survive as long as possible with 10 lives!", fill = "white")
        elif self.mode.get() == "Levels":
            self.counter.destroy()
            self.counter = tk.Label(self, text=" Words Typed: " + str(self.words_typed) + "       Lives Left: " + str(10 - self.lives) + "       Level: " + str(self.level) + " ", font="12")
            self.counter.grid(row=2, column=0)
            temp = self.canvas.create_text(630, 250, font = ('Times New Roman', '30', 'bold'), text = "Levels Mode: Try to pass as many levels as you can with 10 lives!", fill = "white")

        exit_button = tk.Button(self, text = "Exit", command = self.quit)
        self.canvas.create_window(1250, 20, anchor = "center", window  = exit_button)

        if self.mode.get() == "Practice" or self.mode.get() == "Survival":
            self.diffculty_description = self.canvas.create_text(77,20, text = "     Difficulty: " + self.difficulty.get(), font = ("Times New Roman", 14, "bold"), fill = "white")

        t = threading.Timer(2.5, lambda: self.canvas.delete(temp))
        t.daemon = True
        t.start()

        t = threading.Timer(2.5, lambda: self.create_3_2_1_go("Ready"))
        t.daemon = True
        t.start()
        t = threading.Timer(3.5, lambda: self.create_3_2_1_go("Set"))
        t.daemon = True
        t.start()
        t = threading.Timer(4.5, lambda: self.create_3_2_1_go("Go!"))
        t.daemon = True
        t.start()

        t = threading.Timer(5.8, self.create_target)
        t.daemon = True
        t.start()

        t = threading.Timer(5.8, self.time_start)
        t.daemon = True
        t.start()

    def time_start(self):
        self.start_time = time.time()

    def on_entry_click(self, event):
        if self.first_click:
            self.input.delete(0, 'end')
            self.first_click = False

    def create_3_2_1_go(self, text):
        tem = self.canvas.create_text(630, 250, text = text, font = ("Times New Roman", "30", "bold"), fill = "white")
        t = threading.Timer(0.8, lambda: self.canvas.delete(tem))
        t.daemon = True
        t.start()

    def create_target(self):
        index = randint(0, len(self.words) - 1)
        if self.mode.get() == "Levels":
            t = Word(self.canvas, self.words[index], self.level)
        else:
            t = Word(self.canvas, self.words[index], self.difficulty_speed[self.difficulty.get()])
        self.targets.append(t)
        if not self.game_over:
            a_target = threading.Timer(self.how_long_to_create_target, self.create_target)
            a_target.daemon = True
            a_target.start()

    def destroy_target(self, event):
        current_word = self.input.get()
        self.input.delete(0, 'end')
        correct = False
        for n in self.targets:
            if current_word.strip() == n.text.strip():
                correct = True
                self.targets.remove(n)
                Bullet(self.canvas, n.x, n.y, n)
                self.words_typed += 1
                if self.words_typed % 10 == 0:
                    self.level += 1
                self.counter.destroy()
                if self.mode.get() == "Survival":
                    self.counter = tk.Label(self, text=" Words Typed: " + str(self.words_typed) + "       Lives Left: " + str(10 - self.lives) + " ", font="12")
                    self.counter.grid(row = 2, column = 0)

                elif self.mode.get() == "Levels":
                    self.counter = tk.Label(self, text=" Words Typed: " + str(self.words_typed) + "       Lives Left: " + str(10 - self.lives) + "       Level: " + str(self.level) + " ", font="12")

                elif self.mode.get() == "Practice":
                    self.counter.destroy()
                    self.counter = tk.Label(self, text=" Words Typed: " + str(self.words_typed), font = "12" )

                self.counter.grid(row = 2, column = 0)
                break

        if not correct:
            winsound.Beep(2500, 100)

    def lose(self):
        if self.mode.get() == "Practice":
            return
        winsound.Beep(2500, 100)
        self.lives += 1
        if self.mode.get() == "Survival" or self.mode.get() == "Levels":
            self.counter.destroy()
            if self.mode.get() == "Survival":
                self.counter = tk.Label(self, text=" Words Typed: " + str(self.words_typed) + "       Lives Left: " + str(10 - self.lives) + " ", font="12")
            elif self.mode.get() == "Levels":
                self.counter = tk.Label(self, text=" Words Typed: " + str(self.words_typed) + "       Lives Left: " + str(10 - self.lives) + "       Level: " + str(self.level) + " ", font="12")
            self.counter.grid(row=2, column=0)
            if self.lives < 10:
                return
        self.game_over = True
        self.end_time = time.time()
        self.targets.clear()

        losing_sound = "gg.wav"
        winsound.PlaySound(losing_sound, winsound.SND_FILENAME)

        self.time_played = (self.end_time - self.start_time) / 60

        self.stats = tk.Toplevel()
        self.stats.title("Stats")
        self.stats.geometry("{}x{}+0+0".format(main_window.winfo_screenwidth() - 1000, main_window.winfo_screenheight() - 550))

        game_over_message = tk.Label(self.stats, text = "   Game Over", justify = "center", font = ("Times New Roman", 25, "bold"))
        game_over_message.grid(row = 0, column = 1)
        how_many_words_typed = tk.Label(self.stats, text = "   Words Typed: " + str(self.words_typed), font = ("Times New Roman", 13))
        how_many_words_typed.grid(row = 1, column = 1)
        wpm = tk.Label(self.stats, text = "   WPM: " + str(int(self.words_typed/self.time_played)) , font = ("Times New Roman", 13))
        wpm.grid(row = 2, column = 1)
        play_again = tk.Label(self.stats, text = "   Do you want to play again?", justify = 'center', font = ('Times New Roman', 15, 'bold'))
        play_again.grid(row = 3, column = 1)
        play_again_button = tk.Button(self.stats, text = "Play Again", justify = 'center', command = lambda: [self.reset()])
        play_again_button.grid(row =4, column = 1)
        
    def reset(self):
        self.stats.destroy()
        self.game_over = False
        self.lives = 0
        self.words_typed = 0
        self.how_long_to_create_target = 3.5
        self.level = 1
        self.canvas.delete("all")
        self.input.delete(0, 'end')
        self.start()

class Bullet:
    def __init__(self, canvas, x, y, target):
        self.canvas = canvas
        self.x = x
        self.y = 600
        self.end = y;
        self.target = target;
        if target.speed >= 6 and target.speed < 8:
            self.when_explode = 40
        elif target.speed >= 8:
            self.when_explode = 80
        else:
            self.when_explode = 10
        self.img = tk.PhotoImage(file = "bullet.png")
        self.canvas.create_image
        self.draw()
        t = threading.Timer(0.0001, self.move)
        t.daemon = True
        t.start()

    def draw(self):
        self.bullet = self.canvas.create_image(self.x, self.y, image = self.img)

    def move(self):
        self.canvas.delete(self.bullet)
        self.y -= 10
        self.draw()
        if self.y <= self.end + self.when_explode:
            self.canvas.delete(self.bullet)
            self.explode_target(self.x,self.y)
            self.target.erase()
        else:
            t = threading.Timer(0.0001, self.move)
            t.daemon = True
            t.start()

    def explode_target(self, x, y):

        explosion_image = Image.open(r"explosion.gif")
        sequence = [ImageTk.PhotoImage(img)
                    for img in ImageSequence.Iterator(
                explosion_image)]
        image = self.canvas.create_image(x, y, image=sequence[0])

        def animate(counter):
            if counter == 5:
                self.canvas.delete(image)
                return
            self.canvas.itemconfig(image, image=sequence[counter])
            self.canvas.after(100, lambda: animate((counter + 1)))

        animate(1)

class Word:
    def __init__(self, canvas, text, speed):
        self.x = randint(95, 1100)
        self.y = 10
        self.speed = speed
        if self.speed > 5:
            self.timer_delay = 0.03
        else:
            self.timer_delay = 0.1
        self.canvas = canvas
        self.text = text
        self.colors = ["red", "green", "white", "yellow", "orange"]
        self.condition = True
        self.draw(self.colors[randint(0,len(self.colors)-1)])
        t = threading.Timer(self.timer_delay, lambda : self.move(self.colors[randint(0,len(self.colors)-1)]))
        t.daemon = True
        t.start()

    def move(self, color):
        self.canvas.delete(self.w)
        self.y += self.speed
        self.draw(color)
        if self.y < 550 and self.condition and not app.game_over:
            t = threading.Timer(self.timer_delay, lambda : self.move(color))
            t.daemon = True
            t.start()
        elif not self.condition:
            self.canvas.delete(self.w)
        elif self.y >= 550:
            self.canvas.delete(self.w)
            app.lose()

    def draw(self, color):
        self.w = self.canvas.create_text(self.x, self.y, text=self.text, font="16", fill = color)

    def erase(self):
        self.condition = False

main_window = tk.Tk()
main_window.state("zoomed")
main_window.title("Typing Game")
main_window.geometry("{}x{}+0+0".format(main_window.winfo_screenwidth(), main_window.winfo_screenheight()))
app = App(main_window)
main_window.mainloop()

