import sqlite3

conn = sqlite3.connect("quiz_bowl.db")
cursor = conn.cursor()

# Sample questions for each category
sample_questions = {
    "marketing": [
        {
            "question": "What is the primary goal of marketing?",
            "options": ["A. Increase production", "B. Maximize profits", "C. Satisfy customer needs", "D. Cut costs"],
            "answer": "C"
        },
        {
            "question": "Which of the following is a type of market segmentation?",
            "options": ["A. Demographic", "B. Symmetric", "C. Logical", "D. Theoretical"],
            "answer": "A"
        }
    ],
    "appdev": [
        {
            "question": "What language is primarily used for Android app development?",
            "options": ["A. Java", "B. Swift", "C. Python", "D. Ruby"],
            "answer": "A"
        },
        {
            "question": "What is the purpose of an IDE in app development?",
            "options": ["A. Design graphics", "B. Manage emails", "C. Write and debug code", "D. Browse the internet"],
            "answer": "C"
        }
    ],
    "analyticalthinking": [
        {
            "question": "What is the first step in solving a complex problem?",
            "options": ["A. Guessing", "B. Analyzing the situation", "C. Choosing a random solution", "D. Avoiding the issue"],
            "answer": "B"
        },
        {
            "question": "Which of the following demonstrates logical reasoning?",
            "options": ["A. Ignoring data", "B. Following emotions", "C. Using evidence to support conclusions", "D. Jumping to conclusions"],
            "answer": "C"
        }
    ],
    "database": [
        {
            "question": "Which SQL command is used to retrieve data?",
            "options": ["A. INSERT", "B. SELECT", "C. DELETE", "D. UPDATE"],
            "answer": "B"
        },
        {
            "question": "What does 'PRIMARY KEY' do in a database table?",
            "options": ["A. Deletes rows", "B. Sorts data", "C. Uniquely identifies each record", "D. Duplicates rows"],
            "answer": "C"
        }
    ],
    "stats": [
        {
            "question": "What is the mean of the data set: 2, 4, 6, 8?",
            "options": ["A. 4", "B. 5", "C. 6", "D. 10"],
            "answer": "B"
        },
        {
            "question": "Which measure is most affected by outliers?",
            "options": ["A. Mean", "B. Median", "C. Mode", "D. Range"],
            "answer": "A"
        }
    ]
}

# Insert each question into its table
for category, questions in sample_questions.items():
    for q in questions:
        cursor.execute(f"""
            INSERT INTO {category}_questions (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (q["question"], *q["options"], q["answer"]))

print("Sample questions added successfully.")

conn.commit()
conn.close()
