# Requirements:
# ● Create the dictionary: Begin with creating a dictionary where the keys are tuples of book titles and authors, and the values are genres.
# ● Add a New Book: Add a new entry to the dictionary with a tuple containing the title and author of the new book, and set its genre.
# ● Retrieve and Print Book Information: Retrieve and print the genre of a book given its title and author.


books = {
    ("Broken April", "Ismail Kadare"): "Fiction",
    ("Bethoven and the french revolution", "Fan Noli"): "Biography",
    ("Highland Lute", "Gjergj Fishta"): "Poem",
}


new_book = ("Harry Potter and the sorceres's Stone", "J. K.Rowling")
books[new_book] = "Novel"

book_to_find = ("Bethoven and the french revolution", "Fan Noli")
genre = books.get(book_to_find, "Book not found")

print(f"The genre of '{book_to_find[0]}' by {book_to_find[1]} is: {genre}")