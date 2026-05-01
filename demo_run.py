import asyncio
from typing import Dict, Any

from Library_api import (
    get_all_books,
    search_books,
    borrow_book,
    return_book,
    get_borrowed_books,
)


def print_line() -> None:
    print("-" * 60)


def display_books() -> None:
    print_line()
    print("AVAILABLE BOOKS IN LIMKOKWING LIBRARY")
    print_line()

    books = get_all_books()

    for book in books:
        print(f"ID: {book['id']}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Category: {book['category']}")
        print(f"Available Copies: {book['available_copies']}")
        print_line()


def display_borrowed_books() -> None:
    print_line()
    print("BORROWED BOOK RECORDS")
    print_line()

    records = get_borrowed_books()

    if len(records) == 0:
        print("No borrowed books yet.")
        return

    for record in records:
        print(f"User: {record['user_name']}")
        print(f"Book ID: {record['book_id']}")
        print(f"Book Title: {record['book_title']}")
        print(f"Borrow Date: {record['borrow_date']}")
        print(f"Due Date: {record['due_date']}")
        print(f"Return Date: {record['return_date']}")
        print_line()


async def simulate_multiple_users() -> None:
    print_line()
    print("SIMULATING MULTIPLE USERS BORROWING BOOKS")
    print_line()

    results = await asyncio.gather(
        borrow_book("Francisca", 4),
        borrow_book("Abubakar", 4),
        borrow_book("Abril", 2),
    )

    for result in results:
        print(result["message"])

        if "due_date" in result:
            print(f"Due Date: {result['due_date']}")

        print_line()


async def main_menu() -> None:
    while True:
        print("\n")
        print("WELCOME TO LIMKOKWING LIBRARY SYSTEM")
        print("1. View all books")
        print("2. Search for a book")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. View borrowed books")
        print("6. Simulate multiple users")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_books()

        elif choice == "2":
            keyword = input("Enter title, author, or category to search: ")
            results = search_books(keyword)

            print_line()
            print("SEARCH RESULTS")
            print_line()

            if len(results) == 0:
                print("No book found.")
            else:
                for book in results:
                    print(f"{book['id']} - {book['title']} by {book['author']}")
                    print(f"Category: {book['category']}")
                    print(f"Available Copies: {book['available_copies']}")
                    print_line()

        elif choice == "3":
            user_name = input("Enter your name: ")
            book_id = int(input("Enter book ID to borrow: "))

            result: Dict[str, Any] = await borrow_book(user_name, book_id)

            print_line()
            print(result["message"])

            if "due_date" in result:
                print(f"Due Date: {result['due_date']}")

        elif choice == "4":
            user_name = input("Enter your name: ")
            book_id = int(input("Enter book ID to return: "))

            result = await return_book(user_name, book_id)

            print_line()
            print(result["message"])

            if "fine" in result:
                print(f"Fine: Le {result['fine']}")

        elif choice == "5":
            display_borrowed_books()

        elif choice == "6":
            await simulate_multiple_users()

        elif choice == "7":
            print("Thank you for using Limkokwing Library System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


asyncio.run(main_menu())