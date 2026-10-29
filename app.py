
from flask import Flask, render_template, request, jsonify
from database import get_connection

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Get all books
@app.route("/api/books", methods=["GET"])
def get_books():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(books)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add a new book
@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()
    author = data.get("author", "").strip()

    if not title or not author:
        return jsonify({
            "error": "Book title and author are required"
        }), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO books (title, author) VALUES (%s, %s)",
            (title, author)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Book added successfully"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Dashboard statistics
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM books WHERE status = 'Available'"
        )
        available_books = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM books WHERE status = 'Issued'"
        )
        issued_books = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "total_books": total_books,
            "available_books": available_books,
            "issued_books": issued_books,
            "total_students": total_students
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Issue a book
@app.route("/api/issue", methods=["POST"])
def issue_book():
    data = request.get_json(silent=True) or {}

    book_id = data.get("book_id")
    student_id = data.get("student_id")

    if not book_id or not student_id:
        return jsonify({
            "error": "Book ID and student ID are required"
        }), 400

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT status FROM books WHERE book_id = %s",
            (book_id,)
        )
        book = cursor.fetchone()

        if book is None:
            return jsonify({"error": "Book not found"}), 404

        if book[0] != "Available":
            return jsonify({
                "error": "Book is not available"
            }), 400

        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (student_id,)
        )

        if cursor.fetchone() is None:
            return jsonify({"error": "Student not found"}), 404

        cursor.execute(
            """
            INSERT INTO issued_books (book_id, student_id, issue_date, status)
            VALUES (%s, %s, CURDATE(), 'Issued')
            """,
            (book_id, student_id)
        )

        cursor.execute(
            "UPDATE books SET status = 'Issued' WHERE book_id = %s",
            (book_id,)
        )

        conn.commit()

        return jsonify({
            "message": "Book issued successfully"
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


# Return a book
@app.route("/api/return/<int:issue_id>", methods=["POST"])
def return_book(issue_id):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT book_id FROM issued_books
            WHERE issue_id = %s AND status = 'Issued'
            """,
            (issue_id,)
        )

        record = cursor.fetchone()

        if record is None:
            return jsonify({
                "error": "Active issue record not found"
            }), 404

        book_id = record[0]

        cursor.execute(
            """
            UPDATE issued_books
            SET status = 'Returned', return_date = CURDATE()
            WHERE issue_id = %s
            """,
            (issue_id,)
        )

        cursor.execute(
            "UPDATE books SET status = 'Available' WHERE book_id = %s",
            (book_id,)
        )

        conn.commit()

        return jsonify({
            "message": "Book returned successfully"
        })

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
