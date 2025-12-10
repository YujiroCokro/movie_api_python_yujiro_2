from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS
from flask_compress import Compress

DB_HOST = "mysql-movies"
DB_PORT = 3306
DB_USER = "react_daniel"
DB_PASSWORD = "ubaya"
DB_NAME = "react_daniel"  

app = Flask(__name__)
CORS(app)
Compress(app)

def get_db_conn():
    return mysql.connector.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME
    )

@app.get("/movies")
def get_movies():
    sql = "SELECT id, title, year, poster_url FROM movies LIMIT 50;"
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        data = [dict(zip(cols, row)) for row in cur.fetchall()]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            cur.close(); conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
