import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect("quiz_bowl.db")
cursor = conn.cursor()

# Define your course categories
categories = ["marketing", "appdev", "analyticalthinking", "database", "stats"]

# Create a table for each category
for category in categories:
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {category}_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        );
    """)

print("Database and tables created successfully!")

# Save changes and close
conn.commit()
conn.close()
