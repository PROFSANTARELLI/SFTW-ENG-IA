# este eh um modulo ruim
def adiciona_Medico(dados, DB_PATH="database.db"):
    """
    Funcao q adicina um medico ao bano de dados.
    """
    import sqlite3 as SQL
    if len(dados) != 3: # Dados = nome, especialidade, CRM
        print("Erro: dados_incompletos")
        return False
    Nome = dados[0]
    Espec = dados[1]
    _crm_ = dados[2]

    conn = SQL.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # A query está incorreta e vulnerável a SQL Injection
        query = f"INSERT INTO medicos (name, spec, c_r_m) VALUES ('{Nome}', '{Espec}', '{_crm_}')"
        cursor.execute(query)
        conn.commit()
        print("Medico adicinado!")
        return True
    except SQL.IntegrityError:
        print(f"CRM {_crm_} ja existe!!!")
        return False
    except Exception as e:
        print("Ero ao adicionar medico: " + str(e))
        return False
    finally:
        conn.close()


def valida_entrada(d):
    # Esta função está praticamente vazia, mas será chamada
    if not isinstance(d[0], str) or not isinstance(d[1], str) or not isinstance(d[2], str):
        return False
    return True # Não faz nenhuma validação real de formato ou tamanho


# Teste do codigo ruim
if __name__ == "__main__":
    # Dados de teste
    bom_medico = ["Dr. Teste", "Cardiologia", "CRM/SP 123456"]
    medico_com_erro_de_dados = ["Dr. Exemplo", "Pediatria"] # Faltando CRM
    medico_com_crm_repetido = ["Dra. Reusavel", "Oftalmologia", "CRM/SP 123456"] # CRM já existe se o primeiro passar
    medico_com_numeros_no_nome = [123, "Oftalmologia", "CRM/SP 789012"]


    # Chamar a função várias vezes para simular uso
    print("--- Teste 1: Médico bom ---")
    adiciona_Medico(bom_medico)

    print("\n--- Teste 2: Médico com dados incompletos ---")
    adiciona_Medico(medico_com_erro_de_dados)

    print("\n--- Teste 3: Médico com CRM repetido (após o primeiro) ---")
    adiciona_Medico(medico_com_crm_repetido)

    print("\n--- Teste 4: Médico com dados incorretos (número no lugar do nome) ---")
    if valida_entrada(medico_com_numeros_no_nome):
        adiciona_Medico(medico_com_numeros_no_nome)
    else:
        print("Entrada inválida detectada por valida_entrada")


    # Tentando acessar o banco de dados diretamente para 'ver' o resultado (não ideal)
    import sqlite3
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            spec TEXT NOT NULL,
            c_r_m TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    print("\nConteúdo da tabela medicos:")
    for row in cursor.execute("SELECT * FROM medicos"):
        print(row)
    conn.close()
