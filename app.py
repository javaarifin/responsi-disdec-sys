from flask import Flask, jsonify
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

# Konfigurasi koneksi ke YugabyteDB
def get_db_connection():
    conn = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="yugabyte",
        user="yugabyte",
        password="yugabyte"
    )
    return conn

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Selamat datang di API Responsi DisDec. Akses /api/buku atau /api/anggota"})

# Endpoint untuk mengambil data tabel 1
@app.route('/api/buku', methods=['GET'])
def get_buku():
    try:
        conn = get_db_connection()
        cur = conn.cursor(row_factory=dict_row)
        cur.execute("SELECT * FROM buku;")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint untuk mengambil data tabel 2
@app.route('/api/anggota', methods=['GET'])
def get_anggota():
    try:
        conn = get_db_connection()
        cur = conn.cursor(row_factory=dict_row)
        cur.execute("SELECT * FROM anggota;")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Berjalan di port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)