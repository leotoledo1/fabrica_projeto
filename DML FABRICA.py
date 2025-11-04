import psycopg2
from faker import Faker
import random

def inserir_empresas(cursor):
    insert_query = """
    INSERT INTO empresas (id_emp, nome) VALUES (1, 'FullTime');
    """
    cursor.execute(insert_query)


def inserir_departamentos(cursor):
    fake = Faker('pt_BR')
    for _ in range(1, 10):
        departamento = str(fake.job())
        insert_departamentos = f"""
        INSERT INTO departamentos (nome) VALUES ('{departamento}');
        """
        print(insert_departamentos)
        cursor.execute(insert_departamentos)


def inserir_dispositivos(cursor):
    dispositivos = ["Smartphone", "Tablet", "Roteador", "IoT"]
    for dispositivo in dispositivos:
        insert_dispositivos = f"""
        INSERT INTO dispositivos (nome_dispositivo) VALUES ('{dispositivo}');
        """
        print(insert_dispositivos)
        cursor.execute(insert_dispositivos)


def inserir_situacao(cursor):
    situacao = ["Inativo", "Ativo", "Suspenso"]
    for situacaos in situacao:
        insert_situacaos = f"""
        INSERT INTO situacao (situacao) VALUES ('{situacaos}');
        """
        print(insert_situacaos)
        cursor.execute(insert_situacaos)


def inserir_eventos(cursor):
    eventos = ["Nenhum", "Roaming", "Bloqueio", "Excesso de dados"]
    for eventos_especiais in eventos:
        insert_eventos_especiais = f"""
        INSERT INTO eventos_especiais (nome_eventos) VALUES ('{eventos_especiais}');
        """
        print(insert_eventos_especiais)
        cursor.execute(insert_eventos_especiais)


def inserir_alerta_excesso(cursor):
    alerta_excesso = [False, True]
    for altera_excessos in alerta_excesso:
        insert_altera_excessos = f"""
        INSERT INTO altera_excesso (nome_alerta) VALUES ('{altera_excessos}');
        """
        print(insert_altera_excessos)
        cursor.execute(insert_altera_excessos)


def inserir_cargos(cursor):
    cargos = [
        ("Vendedor", 50.0),
        ("Supervisor", 100.0),
        ("Gerente", 200.0),
        ("Tecnico", 300.0)
    ]
    for nome, limite in cargos:
        cursor.execute(f"INSERT INTO cargos (nome, limite_gigas) VALUES ('{nome}', {limite});")


def inserir_usuarios(cursor):
    fake = Faker('pt_BR')
    departamentos = [1, 2, 3, 4, 5]
    cargos = [1, 2, 3, 4]
    empresas = [1]
    for _ in range(20):
        nome = fake.name()
        nome_limpo = (
            nome.replace("Dr. ", "")
                .replace("Dra. ", "")
                .replace("Sr. ", "")
                .replace("Sra. ", "")
                .replace("Srta. ", "")
        )
        id_departamento = random.choice(departamentos)
        id_cargo = random.choice(cargos)
        id_empresa = random.choice(empresas)
        insert_usuario = f"""
        INSERT INTO usuario (nome, id_departamento, id_cargo, id_empresa)
        VALUES ('{nome_limpo}', {id_departamento}, {id_cargo}, {id_empresa});
        """
        print(insert_usuario.strip())
        cursor.execute(insert_usuario)


def inserir_log(cursor):
    fake = Faker('pt_BR')
    cursor.execute("SELECT id_usuario FROM usuario;")
    usuarios = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT id_situacao FROM situacao;")
    situacoes = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT id_alerta FROM altera_excesso;")
    alertas = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT id_evento FROM eventos_especiais;")
    eventos = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT id_dispositivo FROM dispositivos;")
    dispositivos = [r[0] for r in cursor.fetchall()]

    for _ in range(50):
        id_usuario = random.choice(usuarios)
        id_situacao = random.choice(situacoes)
        id_alerta = random.choice(alertas)
        id_evento = random.choice(eventos)
        id_dispositivo = random.choice(dispositivos)
        data_uso = fake.date_time_between(start_date="-30d", end_date="now")
        data_referencia = data_uso.date()
        consumo_gb = round(random.uniform(0.1, 5.0), 2)
        custo_total = round(consumo_gb * random.uniform(1.5, 3.5), 2)
        localizacao = fake.city()

        insert_log = """
        INSERT INTO log_uso_sim (
            id_usuario, id_situacao, id_alerta, id_evento, id_dispositivo,
            data_uso, consumo_dados_gb, custo_total, localizacao, data_referencia
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_log, (
            id_usuario, id_situacao, id_alerta, id_evento, id_dispositivo,
            data_uso, consumo_gb, custo_total, localizacao, data_referencia
        ))


try:
    conn = psycopg2.connect(
        database="ANALISE",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    print("Conectado com sucesso ao banco de dados PostgreSQL!")
    cursor = conn.cursor()

    inserir_empresas(cursor)
    inserir_departamentos(cursor)
    inserir_dispositivos(cursor)
    inserir_situacao(cursor)
    inserir_eventos(cursor)
    inserir_alerta_excesso(cursor)
    inserir_cargos(cursor)
    inserir_usuarios(cursor)
    inserir_log(cursor)

    conn.commit()
    print("comit full")
    conn.close()
    print("Conexão fechada.")

except psycopg2.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
