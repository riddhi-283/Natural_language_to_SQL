from flask import Flask, render_template, request, jsonify, send_file
import mysql.connector
import pandas as pd
from mysql.connector import Error
from dotenv import load_dotenv
import os
import google.generativeai as genai
import io

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

app = Flask(__name__)

# Function to get response from Gemini API
def get_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to execute the SQL query
def execute_query(user, password, host, database, query):
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]
            conn.close()
            return result, column_names
    except Error as e:
        return f"Error: {e}", []

# Function to fetch table and column information
def fetch_db_schema(user, password, host, database):
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (database,))
            tables = cursor.fetchall()
            schema_info = []
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = cursor.fetchall()
                column_info = [column[0] for column in columns]
                schema_info.append((table_name, column_info))
            conn.close()
            return schema_info
    except Error as e:
        return f"Error: {e}"

# Function to generate prompt based on schema
def generate_prompt(schema_info):
    prompt = "You are an expert in converting questions to SQL Query in multiple languages. The SQL database has the following tables:\n"
    for table, columns in schema_info:
        prompt += f"Table {table} with columns {', '.join(columns)}.\n"
    prompt += "\nFor example, if the question is in English: 'Which t-shirts have discounts on them?' then the SQL command will be something like this: SELECT t_shirts.* FROM t_shirts INNER JOIN discounts ON t_shirts.id = discounts.t_shirt_id.\n"
    prompt += "If the question is in another language, first translate it to English and then convert it to the corresponding SQL query. Also, the SQL code should not have ``` in beginning or end and sql word in output."
    return prompt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    user = request.form['user']
    password = request.form['password']
    host = request.form['host']
    database = request.form['database']
    question = request.form['question']

    if user and password and host and database and question:
        schema_info = fetch_db_schema(user, password, host, database)
        if isinstance(schema_info, str):
            return jsonify({"error": schema_info})
        else:
            prompt = generate_prompt(schema_info)
            sql_query = get_response(question, [prompt])
            result, column_names = execute_query(user, password, host, database, sql_query)
            if isinstance(result, str):
                return jsonify({"error": result})
            else:
                df = pd.DataFrame(result, columns=column_names)
                csv = df.to_csv(index=False).encode('utf-8')
                return jsonify({
                    "sql_query": sql_query,
                    "result": df.to_dict(orient='records'),
                    "columns": column_names,
                    "csv": csv.decode('utf-8')
                })
    else:
        return jsonify({"error": "Please provide all the details."})

@app.route('/download', methods=['POST'])
def download():
    csv_data = request.form['csv_data']
    return send_file(
        io.BytesIO(csv_data.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='query_results.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
