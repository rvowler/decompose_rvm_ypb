from flask import Flask
import os
import psycopg2

app = Flask(__name__)

# Configuració de la base de dades
DB_HOST = os.getenv('POSTGRES_HOST', 'postgres')
DB_NAME = os.getenv('POSTGRES_DB', 'mydb')
DB_USER = os.getenv('POSTGRES_USER', 'user')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            count INTEGER NOT NULL
        )
    ''')
    cur.execute('INSERT INTO visits (count) VALUES (0) ON CONFLICT DO NOTHING')
    conn.commit()
    cur.close()
    conn.close()

# Inicialitzar la base de dades
try:
    init_db()
except Exception as e:
    print("Error inicialitzant la base de dades:", str(e))

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Incrementar el comptador
        cur.execute('UPDATE visits SET count = count + 1 WHERE id = 1')
        conn.commit()

        # Obtenir el valor actual
        cur.execute('SELECT count FROM visits WHERE id = 1')
        count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return f'Hola! Aquesta pàgina ha estat visitada {count} vegades.'

    except Exception as e:
        return str(e), 500

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return 'Healthy', 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
