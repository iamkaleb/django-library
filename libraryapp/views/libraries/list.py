import sqlite3
from django.shortcuts import redirect, reverse, render
from libraryapp.models import Library, Book
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def list_libraries(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_library
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                li.id,
                li.title,
                li.address,
                b.id book_id,
                b.title book_title,
                b.author,
                b.year_published,
                b.isbn
            FROM libraryapp_library li
            JOIN libraryapp_book b ON li.id = b.location_id
            """)

            dataset = db_cursor.fetchall()

            all_libraries = {}

            for (library, book) in dataset:
                if library.id not in all_libraries:
                    all_libraries[library.id] = library
                    all_libraries[library.id].books.append(book)

                else:
                    all_libraries[library.id].books.append(book)

        template_name = 'libraries/list.html'

        context = {
            'all_libraries': all_libraries
        }

        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_library
            (
                title, address
            )
            VALUES (?, ?)
            """,
            (form_data['title'], form_data['address']))

        return redirect(reverse('libraryapp:libraries')) 

def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["id"]
    library.title = _row["title"]
    library.address = _row["address"]

    # Note: You are adding a blank books list to the library object
    # This list will be populated later (see below)
    library.books = []

    book = Book()
    book.id = _row["book_id"]
    book.title = _row["book_title"]
    book.author = _row["author"]
    book.isbn = _row["isbn"]
    book.year_published = _row["year_published"]

    # Return a tuple containing the library and the
    # book built from the data in the current row of
    # the data set
    return (library, book,)