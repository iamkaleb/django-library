import sqlite3
from django.shortcuts import redirect, reverse, render
from libraryapp.models import Book
from ..connection import Connection
from django.contrib.auth.decorators import login_required

@login_required
def book_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                b.id,
                b.title,
                b.isbn,
                b.author,
                b.year_published,
                b.librarian_id,
                b.location_id
            from libraryapp_book b
            """)

            all_books = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                book = Book()
                book.id = row['id']
                book.title = row['title']
                book.isbn = row['isbn']
                book.author = row['author']
                book.year_published = row['year_published']
                book.librarian_id = row['librarian_id']
                book.location_id = row['location_id']

                all_books.append(book)

        template = 'books/list.html'
        context = {
            'all_books': all_books
        }

        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_book
            (
                title, author, isbn,
                year_published, librarian_id, location_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['author'],
                form_data['isbn'], form_data['year_published'],
                request.user.librarian.id, form_data["location"]))

        return redirect(reverse('libraryapp:books'))    