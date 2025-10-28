MISSÃO FINAL: 0,25 + BÔNUS DE 0,25 SE COMPLETO 100%

Missão integrar o aplicativo "Gerenciador de Tarefas" com as ferramentas modernas que um engenheiro de software utiliza diariamente: VS Code para desenvolvimento e GitHub (com GitHub Actions) para versionamento de código e CI/CD.

1. Configuração Inicial do Projeto e Ambiente (VS Code)
1.1 Criar a Estrutura de Pastas
Abra o terminal (ou o terminal integrado do VS Code) e crie a estrutura do projeto:
code
Bash
1.2 Abrir o Projeto no VS Code
Agora, abra a pasta simple_task_manager no VS Code.
File > Open Folder... e selecione a pasta simple_task_manager.
1.3 Criar um Ambiente Virtual
É crucial usar um ambiente virtual para gerenciar as dependências do seu projeto Python.
No terminal integrado do VS Code (Ctrl + ou View > Terminal):
code
Bash
python -m venv venv
Isso criará uma pasta venv com seu ambiente virtual.
1.4 Ativar o Ambiente Virtual
Windows:
code
Bash
.\venv\Scripts\activate
macOS/Linux:
code
Bash
source venv/bin/activate
Você verá (venv) no início da linha de comando, indicando que o ambiente está ativo.
1.5 Instalar Dependências
Com o ambiente virtual ativo, instale as bibliotecas necessárias:
code
Bash
pip install fastapi uvicorn jinja2
# Opcional, para o linter que usaremos no CI:
pip install flake8
1.6 Criar o Arquivo requirements.txt
Para que o GitHub Actions e outras pessoas possam replicar seu ambiente, crie o arquivo requirements.txt:
code
Bash
pip freeze > requirements.txt```
Isso listará todas as bibliotecas instaladas no seu ambiente virtual.

### **2. Implementação do Código do Aplicativo**

Agora, crie os arquivos conforme detalhado no meu exemplo anterior. Certifique-se de que os nomes e a estrutura das pastas correspondam.

#### **2.1 `database.py`**
(Copie e cole o conteúdo fornecido anteriormente neste arquivo)

```python
# simple_task_manager/database.py
import sqlite3

DATABASE_NAME = "tasks.db"

def init_db():
    """
    Inicializa o banco de dados e cria a tabela 'tasks' se ela não existir.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("Banco de dados inicializado ou já existe.")

def create_task(description: str):
    """
    Cria uma nova tarefa no banco de dados.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description) VALUES (?)", (description,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {"id": task_id, "description": description, "completed": False}

def get_tasks():
    """
    Retorna todas as tarefas do banco de dados.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, completed FROM tasks ORDER BY id DESC")
    tasks = []
    for row in cursor.fetchall():
        tasks.append({"id": row[0], "description": row[1], "completed": bool(row[2])})
    conn.close()
    return tasks

def update_task_status(task_id: int, completed: bool):
    """
    Atualiza o status 'completed' de uma tarefa específica.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
    conn.commit()
    conn.close()
    
def delete_task(task_id: int):
    """
    Exclui uma tarefa do banco de dados.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
init_db()
