import os
import time
import mysql.connector
import redis
from flask import Flask, jsonify

app = Flask(__name__)

# Configurações obtidas das variáveis de ambiente
DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')
DB_NAME = os.getenv('DB_NAME', 'minhabase')
REDIS_HOST = os.getenv('REDIS_HOST', 'cache')

# Conexão com o Redis
cache_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def get_db_connection():
    """Tenta conectar ao MySQL com retry caso o banco ainda esteja inicializando."""
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
            )
            return conn
        except mysql.connector.Error:
            retries -= 1
            time.sleep(2)
    raise Exception('Não foi possível conectar ao banco de dados MySQL.')


@app.route('/')
def index():
    # 1. Atualiza o contador de acessos no Redis (Cache)
    visitas = cache_client.incr('contador_visitas')

    # 2. Registra o evento de acesso no MySQL (Banco de Dados)
    conn = get_db_connection()
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS acessos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute('INSERT INTO acessos () VALUES ()')
    conn.commit()

    # Busca o total de acessos gravados no banco
    cursor.execute('SELECT COUNT(*) FROM acessos')
    total_db = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        'mensagem': 'Aplicação Python rodando com sucesso!',
        'visitas_em_cache_redis': visitas,
        'registros_no_mysql': total_db,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)