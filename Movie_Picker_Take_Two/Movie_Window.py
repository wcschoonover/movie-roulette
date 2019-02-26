import tkinter as tk
from random import *
from tkinter import messagebox, font, StringVar
import mysql.connector



# ---Lists---
GENRES = [
    "Action",
    "Childhood",
    "Comedy",
    "Drama",
    "Horror",
    "Teen",
    "Thriller"
]


# ---Definitions
root = tk.Tk()
v_genre = tk.StringVar()
v_genre.set("Initialize")

v_stored_movie_id = tk.StringVar()

v_classic = tk.IntVar()
v_classic.set(1)


v_unwatched_movies_text: StringVar = tk.StringVar()
v_unwatched_movies_text.set('')

movieDB = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

#catch if connection fails

cursor = movieDB.cursor()








# ---window definitions---
root.title("90s Movie Dice")
root.geometry("400x400")


# ---Labels---
banner = tk.Label(text="Choose Movie Options Below", font=("Times New Roman", 20))
banner.grid(row=0, columnspan=2)

genre_label = tk.Label(text="Choose a Genre", font=("Helvetica", 14))
genre_label.grid(row=1, column=0, sticky=tk.W)

classic_label = tk.Label(text="Classic or Deep Cut?", font=("Helvetica", 14))
classic_label.grid(row=1, column=1, sticky=tk.W)

movie_name_label = tk.Label(text="Movie", font=("Helvetica", 14))
movie_name_label.grid(row=11, column=0)

year_label = tk.Label(text="Year", font=("Helvetica", 14))
year_label.grid(row=11, column=1)

unwatched_movies_remaining_label = tk.Label(textvariable = v_unwatched_movies_text, font=("Helvetica", 10))
unwatched_movies_remaining_label.grid(row=9, column=0)

# ---button method definitions---
def get_movie():
    # clear current movie value
    movie_name.delete(1.0, 3.0)
    movie_year.delete(1.0, 3.0)

    # declare str variables
    chosen_genre = v_genre.get()
    chosen_classic_bool = str(v_classic.get())

    # get all data into a tuple
    movie_id_query = 'SELECT movie_id,movie_name,movie_year FROM movies.movie_list WHERE movie_genre = \'' + chosen_genre + '\' AND classic_bool = ' + chosen_classic_bool + ' AND viewed_bool = 0;'
    cursor.execute(movie_id_query)
    random_choice_tuple = choice(cursor.fetchall())

    # catch for queries returning no records and exit

    # store id for later use
    v_stored_movie_id.set(str(random_choice_tuple[0]))

    # insert values from tuple
    movie_name.insert(tk.INSERT, random_choice_tuple[1])
    movie_year.insert(tk.INSERT, random_choice_tuple[2])

    cursor.reset()


def mark_movie_as_watched():
    print("stored_movie_id = " + v_stored_movie_id.get())
    update_watched_query = 'UPDATE movies.movie_list SET viewed_bool = 1 WHERE movie_id = ' + v_stored_movie_id.get() + ';'
    print(update_watched_query)
    cursor.execute(update_watched_query)
    movieDB.commit()
    messagebox.showinfo("Movie watched", "Movie has been marked as watched and will no longer appear in dice rolls.")

    cursor.reset()


def validate_choices():
    if v_genre.get() not in GENRES:
        messagebox.showinfo("Choose all options", "Choose all options above to continue")
        root.mainloop()


def set_unwatched_movies_remaining_label():
    unwatched_movie_count_query = 'SELECT COUNT(movie_id) FROM movies.movie_list WHERE viewed_bool = 0 AND movie_genre = \'' + v_genre.get() + '\';'
    unwatched_movies_remaining_count = ''
    cursor.execute(unwatched_movie_count_query)
    unwatched_movies_remaining_count = cursor.fetchone() #returns a tuple, so you have to convert back to int
    unwatched_movies_remaining_count = unwatched_movies_remaining_count[0]
    cursor.reset()

    if unwatched_movies_remaining_count == '':
        return
    elif unwatched_movies_remaining_count == 0:
        v_unwatched_movies_text.set('No unwatched movies remaining in this genre!')
    elif unwatched_movies_remaining_count == 1:
        v_unwatched_movies_text.set('One movie remaining in this genre!')
    else:
        v_unwatched_movies_text.set(str(unwatched_movies_remaining_count) + ' movies remaining in this genre.')




# ---Text Boxes---
movie_name = tk.Text(root, height=1, width=20)
movie_name.grid(row=12, column=0)
movie_name.insert(tk.INSERT, " ")


movie_year = tk.Text(root, height=1, width=10)
movie_year.grid(row=12, column=1)
movie_year.insert(tk.INSERT, " ")



# ---Radiobuttons---
for var in range(7):
    genre_button = tk.Radiobutton(root,
                                  variable=v_genre,
                                  text=GENRES[var],
                                  value=GENRES[var],
                                  command=lambda: [v_genre.get(), set_unwatched_movies_remaining_label()]
                                  )
    genre_button.grid(row=var + 2, column=0, sticky=tk.W)

classic_button = tk.Radiobutton(root, variable=v_classic,
                                text="Classic",
                                value=1,
                                command=lambda: print(v_classic.get()))
classic_button.grid(row=2, column=1, sticky=tk.W)

deep_cut_button = tk.Radiobutton(root,
                                 variable=v_classic,
                                 text="Deep Cut",
                                 value=0, command=lambda: print(v_classic.get()))
deep_cut_button.grid(row=3, column=1, sticky=tk.W)






# ---Buttons---
dice_button = tk.Button(root, text="Roll the Nostalgia Dice", command=lambda: [validate_choices(), get_movie()])
  # add method call that will query the db
dice_button.grid(row=10, columnspan=2)

choose_button = tk.Button(root, text="Choose this movie", command=mark_movie_as_watched)
choose_button.grid(row=13, column=0)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=13, column=1)



# ---Text fields---

root.mainloop()
