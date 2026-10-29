
function showMessage(action) {
    alert(action + " feature selected!");

    switch (action) {
        case "Add Book":
            addBook();
            break;

        case "Issue Book":
            issueBook();
            break;

        case "Return Book":
            returnBook();
            break;

        case "View Books":
            viewBooks();
            break;

        default:
            alert("Invalid action!");
    }
}

function addBook() {
    const title = prompt("Enter book title:");

    if (title === null) return;

    if (title.trim() === "") {
        alert("Book title cannot be empty!");
        return;
    }

    const author = prompt("Enter author name:");

    if (author === null) return;

    if (author.trim() === "") {
        alert("Author name cannot be empty!");
        return;
    }

    alert(
        "Book details entered successfully!\n" +
        "Title: " + title + "\n" +
        "Author: " + author +
        "\n\nConnect the Flask backend to save this book permanently."
    );
}

function issueBook() {
    const student = prompt("Enter student name:");

    if (student === null) return;

    if (student.trim() === "") {
        alert("Student name cannot be empty!");
        return;
    }

    const book = prompt("Enter book title to issue:");

    if (book === null) return;

    if (book.trim() === "") {
        alert("Book title cannot be empty!");
        return;
    }

    alert(
        "Issue details entered!\n" +
        "Student: " + student +
        "\nBook: " + book +
        "\n\nConnect the Flask backend to record the issue."
    );
}

function returnBook() {
    const book = prompt("Enter book title to return:");

    if (book === null) return;

    if (book.trim() === "") {
        alert("Book title cannot be empty!");
        return;
    }

    alert(
        "Return request entered for: " + book +
        "\n\nConnect the Flask backend to update the return record."
    );
}

function viewBooks() {
    alert(
        "Book List\n\n" +
        "Your book list will appear here after connecting MySQL."
    );
}
