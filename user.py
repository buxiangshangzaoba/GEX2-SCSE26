from admin import find_book, load_library, save_library


def books_in_category(books, category):
    clean_cat = category.strip().lower()
    result_ids = []
    for book_id, book in books.items():
        if book["category"].lower() == clean_cat:
            result_ids.append(book_id)
    return result_ids


def search_by_title(books, search_text):
    clean_text = search_text.strip().lower()
    matches = []
    for book_id, book in books.items():
        if clean_text in book["title"].lower():
            matches.append(book_id)
    return matches


def borrow_book(books, loans, search_text, borrower):
    if not borrower.strip():
        return "EMPTY_NAME"

    real_book_id = find_book(books, search_text)
    if real_book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[real_book_id]
    if not book["available"]:
        return "NOT_AVAILABLE"

    book["available"] = False
    loans.append({
        "book_id": real_book_id,
        "borrower": borrower
    })
    return "OK"


def return_book(books, loans, book_title, borrower):
    if not borrower.strip():
        return "EMPTY_NAME"

    real_book_id = find_book(books, book_title)
    if real_book_id is None:
        return "BOOK_NOT_FOUND"

    loan_index = None
    for idx, loan in enumerate(loans):
        if loan["book_id"] == real_book_id:
            loan_index = idx
            break

    if loan_index is None:
        return "NOT_ON_LOAN"

    del loans[loan_index]
    books[real_book_id]["available"] = True
    return "OK"


def main():
    filename = "library.json"
    try:
        lib_data = load_library(filename)
    except FileNotFoundError:
        lib_data = {
            "library": {"name": "Local Library", "branch": "Main", "year": 2026},
            "categories": ["Fiction", "Science"],
            "books": {},
            "loans": []
        }

    books = lib_data["books"]
    loans = lib_data["loans"]

    print("LIBRARY USER SYSTEM")
    while True:
        print("\n==== MENU ====")
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow book")
        print("4. Return book")
        print("5. Exit")
        user_input = input("Please select an option: ")

        if user_input == "1":
            text = input("Enter title keyword: ")
            res = search_by_title(books, text)
            print("Matching book ids:", res)
        elif user_input == "2":
            cat = input("Enter category: ")
            res = books_in_category(books, cat)
            print("Books in category:", res)
        elif user_input == "3":
            bid_text = input("Enter book id: ")
            name = input("Enter borrower name: ")
            ret = borrow_book(books, loans, bid_text, name)
            print(ret)
        elif user_input == "4":
            bid_text = input("Enter book id: ")
            name = input("Enter borrower name: ")
            ret = return_book(books, loans, bid_text, name)
            print(ret)
        elif user_input == "5":
            lib_data["books"] = books
            lib_data["loans"] = loans
            save_library(lib_data, filename)
            print("Exiting...")
            break
        else:
            print("Invalid selection, try again.")


if __name__ == "__main__":
    main()
