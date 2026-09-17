import json


def load_library(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_library(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def find_book(books, search_text):
    clean_search = search_text.strip().lower()
    for book_id in books:
        if book_id.lower() == clean_search:
            return book_id
    return None


def display_books(books):
    print("BOOK CATALOGUE")
    print("-" * 60)
    for bid, book in books.items():
        if book["available"]:
            avail_text = "AVAILABLE"
        else:
            avail_text = "ON LOAN"
        print(f"{bid} | {book['title']} | {book['category']} | {avail_text}")


def display_loans(loans, books):
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        bid = loan["book_id"]
        borrower = loan["borrower"]
        title = books[bid]["title"]
        print(f"{bid} | {title} | Borrower: {borrower}")


def library_statistics(books):
    total = len(books)
    available = 0
    for b in books.values():
        if b["available"]:
            available += 1
    borrowed = total - available
    return total, available, borrowed


def main():
    sample_data = {
        "library": {
            "name": "Sample Library",
            "branch": "Main",
            "year": 2026
        },
        "categories": ["Science", "History", "Fiction"],
        "books": {
            "B1001": {"title": "Sample Book One", "category": "Fiction", "available": True},
            "B1002": {"title": "Sample Book Two", "category": "Science", "available": False}
        },
        "loans": [
            {"book_id": "B1002", "borrower": "Test User"}
        ]
    }
    lib_info = sample_data["library"]
    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {lib_info['name']}")
    print(f"Branch: {lib_info['branch']}")
    print(f"Year: {lib_info['year']}")
    print(f"Categories: {', '.join(sample_data['categories'])}")

    display_books(sample_data["books"])
    display_loans(sample_data["loans"], sample_data["books"])

    print("STATISTICS")
    print("-" * 60)
    total, avail, bor = library_statistics(sample_data["books"])
    print(f"Total books: {total}")
    print(f"Available: {avail}")
    print(f"Borrowed: {bor}")


if __name__ == "__main__":
    main()
