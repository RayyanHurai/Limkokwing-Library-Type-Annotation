import asyncio
from datetime import date, timedelta
from typing import Dict, List, Optional, Any


# -----------------------------
# LIMKOKWING LIBRARY DATA
# -----------------------------

books: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Python Basics",
        "author": "A. Coker",
        "category": "Programming",
        "available_copies": 3,
    },
    {
        "id": 2,
        "title": "Networking Essentials",
        "author": "J. Kamara",
        "category": "Technology",
        "available_copies": 2,
    },
    {
        "id": 3,
        "title": "Database Systems",
        "author": "M. Conteh",
        "category": "Information Systems",
        "available_copies": 4,
    },
    {
        "id": 4,
        "title": "Object-Oriented Programming",
        "author": "S. Bangura",
        "category": "Programming",
        "available_copies": 1,
    },
    {
        "id": 5,
        "title": "Web Development Guide",
        "author": "F. Kabina",
        "category": "Web Design",
        "available_copies": 2,
    },
]


borrowed_books: List[Dict[str, Any]] = []


# This lock helps to protect the borrow and return process
# when many users access the system at the same time.
library_lock: asyncio.Lock = asyncio.Lock()


# -----------------------------
# ENDPOINT SIMULATION FUNCTIONS
# -----------------------------

def get_all_books() -> List[Dict[str, Any]]:
    """
    Simulates GET /books
    Returns all books in the library.
    """
    return books


def search_books(keyword: str) -> List[Dict[str, Any]]:
    """
    Simulates GET /books/search
    Searches books by title, author, or category.
    """
    keyword = keyword.lower()

    results: List[Dict[str, Any]] = []

    for book in books:
        title = str(book["title"]).lower()
        author = str(book["author"]).lower()
        category = str(book["category"]).lower()

        if keyword in title or keyword in author or keyword in category:
            results.append(book)

    return results


def find_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    """
    Finds one book using its ID.
    Returns the book if found, otherwise returns None.
    """
    for book in books:
        if book["id"] == book_id:
            return book

    return None


async def borrow_book(user_name: str, book_id: int) -> Dict[str, Any]:
    """
    Simulates POST /borrow
    Allows a user to borrow a book if copies are available.
    Uses async/await to show multiple users accessing the system.
    """

    async with library_lock:
        await asyncio.sleep(1)

        book = find_book_by_id(book_id)

        if book is None:
            return {
                "status": "failed",
                "message": f"Book with ID {book_id} was not found.",
            }

        if int(book["available_copies"]) <= 0:
            return {
                "status": "failed",
                "message": f"Sorry {user_name}, '{book['title']}' is currently not available.",
            }

        book["available_copies"] = int(book["available_copies"]) - 1

        borrow_record: Dict[str, Any] = {
            "user_name": user_name,
            "book_id": book_id,
            "book_title": book["title"],
            "borrow_date": date.today(),
            "due_date": date.today() + timedelta(days=7),
            "return_date": None,
        }

        borrowed_books.append(borrow_record)

        return {
            "status": "success",
            "message": f"{user_name} successfully borrowed '{book['title']}'.",
            "due_date": borrow_record["due_date"],
        }


async def return_book(user_name: str, book_id: int) -> Dict[str, Any]:
    """
    Simulates POST /return
    Allows a user to return a borrowed book.
    """

    async with library_lock:
        await asyncio.sleep(1)

        book = find_book_by_id(book_id)

        if book is None:
            return {
                "status": "failed",
                "message": f"Book with ID {book_id} was not found.",
            }

        for record in borrowed_books:
            if (
                record["user_name"].lower() == user_name.lower()
                and record["book_id"] == book_id
                and record["return_date"] is None
            ):
                record["return_date"] = date.today()
                book["available_copies"] = int(book["available_copies"]) + 1

                fine = calculate_fine(record["due_date"], record["return_date"])

                return {
                    "status": "success",
                    "message": f"{user_name} successfully returned '{book['title']}'.",
                    "fine": fine,
                }

        return {
            "status": "failed",
            "message": f"No active borrow record found for {user_name} and book ID {book_id}.",
        }


def calculate_fine(due_date: date, return_date: date) -> int:
    """
    Calculates fine for overdue books.
    The fine is 100 Leones per overdue day.
    """

    if return_date <= due_date:
        return 0

    overdue_days: int = (return_date - due_date).days
    fine: int = overdue_days * 100

    return fine


def get_borrowed_books() -> List[Dict[str, Any]]:
    """
    Simulates GET /borrowed-books
    Returns all borrowed book records.
    """
    return borrowed_books