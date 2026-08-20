# Bond practice database

`bond_sports.db` is a generated SQLite database containing the practice
`bookings`, `users`, and `courts` tables. The binary database is intentionally
ignored by Git; `setup_bookings.sql` is the reproducible source of truth.

To rebuild or reset it, delete `bond_sports.db` and execute `setup_bookings.sql` with SQLite. The setup script is idempotent, so it can also be executed again to restore the four sample rows.

Run command to create the db and tables from setup_bookings.sql file:

 python -c 'import sqlite3, pathlib; db=sqlite3.connect("database/bond_sports.db"); db.executescript(pathlib.Path("database/setup_bookings.sql").read_text()); db.commit(); db.close()'


python -c "import sqlite3; db=sqlite3.connect('database/bond_sports.db'); print(*db.execute('SELECT * FROM bookings'), sep='\n'); db.close()"

specifc query:


python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT * FROM bookings WHERE user_id = ? AND status = ?", (5, "confirmed")), sep="\n"); db.close()'



SELECT id, status
FROM bookings;

python -c "import sqlite3; db=sqlite3.connect('database/bond_sports.db'); print(*db.execute('SELECT id, status FROM bookings'), sep='\n'); db.close()"



python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT * FROM bookings WHERE status = ? AND price > ? ", ("confirmed", 100)), sep="\n"); db.close()'

#All bookings where the status is either cancelled OR pending.

python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT * FROM bookings WHERE status = ? OR status = ? ", ("pending", "cancelled")), sep="\n"); db.close()'


Find all bookings, ordered by price from highest to lowest.
python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT price FROM bookings ORDER BY price DESC"), sep="\n"); db.close()'

#from highest to lowest
python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT price FROM bookings ORDER BY price ASC"), sep="\n"); db.close()'


Which email address belongs to booking 101?
Need to do join !!!

SELECT
    b.id,
    u.email,
    b.status
FROM bookings b
JOIN users u
    ON b.user_id = u.id;

python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT bookings.id, bookings.user_id, users.email FROM bookings JOIN users ON bookings.user_id == users.id WHERE bookings.id = ? ", (101,)), sep="\n"); db.close()'


SELECT
    b.id,
    u.email,
    b.price
FROM bookings b
JOIN users u
    ON b.user_id = u.id
WHERE b.status = 'confirmed';



python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT b.id, b.price, u.email FROM bookings AS b JOIN users AS u ON b.user_id == u.id WHERE b.status = ? ", ("confirmed",)), sep="\n"); db.close()'

#join 3 tables bookings,users,courts
return
booking id
user email
court name
status
price

SELECT
    b.id,
    u.email,
    c.name,
    b.status,
    b.price
FROM bookings AS b
JOIN users AS u
    ON b.user_id = u.id
JOIN courts AS c
    ON b.court_id = c.id;


python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT b.id, u.email, c.name, b.status, b.price FROM bookings AS b JOIN users AS u ON b.user_id == u.id JOIN courts AS c ON b.court_id == c.id"), sep="\n"); db.close()'


GROUP BY / HAVING


How many bookings does each user have?

We use:

SELECT
    user_id,
    COUNT(*) AS booking_count
FROM bookings
GROUP BY user_id;


python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT bookings.user_id, COUNT(*) AS booking_count FROM bookings GROUP BY bookings.user_id"), sep="\n"); db.close()'

#Show only users with more than 1 booking.

SELECT
    user_id,
    COUNT(*) AS booking_count
FROM bookings
GROUP BY user_id;
WHERE booking_account > 1

python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT bookings.user_id, COUNT(*) AS booking_count FROM bookings GROUP BY bookings.user_id HAVING COUNT(*) > ? ", (1,)), sep="\n"); db.close()'

python -c 'import sqlite3; db=sqlite3.connect("database/bond_sports.db"); print(*db.execute("SELECT bookings.user_id, COUNT(*) AS booking_count FROM bookings GROUP BY bookings.user_id HAVING COUNT(*) > ?", (1,)), sep="\n"); db.close()'
