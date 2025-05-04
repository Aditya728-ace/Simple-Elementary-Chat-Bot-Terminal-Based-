import google.generativeai as genai
import os
import sqlite3

genai.configure(api_key='AIzaSyBlk-AzukxmjqorlZD-q18Jq-A-bfmeHqQ')

def init_db():
    conn = sqlite3.connect('searches.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def store_search(query, conn):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO searches (query) VALUES (?)', (query,))
    conn.commit()

def get_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    conn = init_db() 

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        store_search(user_input, conn)

        response = get_response(user_input)
        print(f"Chatbot: {response}")
    
    conn.close() 
