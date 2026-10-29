
-- Create database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    status ENUM('Available', 'Issued') DEFAULT 'Available'
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- Issued books table
CREATE TABLE IF NOT EXISTS issued_books (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    student_id INT NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE DEFAULT NULL,
    status ENUM('Issued', 'Returned') DEFAULT 'Issued',

    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Sample books
INSERT INTO books (title, author) VALUES
('Wings of Fire', 'A. P. J. Abdul Kalam'),
('The Alchemist', 'Paulo Coelho'),
('Python Programming', 'Reema Thareja'),
('Database System Concepts', 'Abraham Silberschatz');

-- Sample students
INSERT INTO students (name, email) VALUES
('Rahul Sharma', 'rahul@example.com'),
('Priya Verma', 'priya@example.com'),
('Arjun Mehta', 'arjun@example.com');

-- Display tables
SELECT * FROM books;
SELECT * FROM students;
SELECT * FROM issued_books;
