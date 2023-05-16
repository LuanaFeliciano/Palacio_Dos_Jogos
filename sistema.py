import mysql.connector
import datetime
#Cadastrar Cliente
def cadastrar_cliente():
    print('\n========== Cadastro dos Clientes ==========\n')
    nome = input("Digite o nome do cliente: ")
    cpf = input("Digite o cpf do cliente: ")
    contato = input("Digite o telefone do cliente: ")
    cursor = conexao.cursor()
    sql = "INSERT INTO clientes (cpf,nome,contato) VALUES (%s, %s, %s)"
    valores = (cpf,nome,contato,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Cliente cadastrado com sucesso!")

#Cadastrar Jogo
def cadastrar_jogo():
    print('\n========== Cadastro dos Jogos ==========\n')
    titulo = input("Digite o titulo do jogo: ")
    plataforma = input("Digite a plataforma do jogo: ")
    genero = input("Digite o genero do jogo: ")
    quantidade = input("Digite a quantidade: ")

    cursor = conexao.cursor()
    sql = "INSERT INTO jogos (titulo,plataforma,genero,quantidade) VALUES (%s, %s, %s, %s)"
    valores = (titulo,plataforma,genero,quantidade,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Jogo cadastrado com sucesso!")

#Cadastrar Console
def cadastrar_console():
    print('\n========== Cadastro dos Consoles ==========\n')
    nome = input("Digite o nome do console: ")
    quantidade = input("Digite a quantidade: ")

    cursor = conexao.cursor()
    sql = "INSERT INTO consoles (nome,quantidade) VALUES (%s, %s)"
    valores = (nome,quantidade,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Console cadastrado com sucesso!")

def cadastrar_preco_jogo():
    print('\n========== Cadastro Tabela de Preços dos Jogos ==========\n')
    plataforma = input("A plataforma dos jogos: ")
    quantidade = input("Digite a quantidade de jogos: ")
    duracao_dias = input("Digite a duração em dias: ")
    preco = input("Digite o preço: ")

    cursor = conexao.cursor()
    sql = "INSERT INTO precos_jogos (plataforma_jogo,qtd_jogos,duracao_dias,valor) VALUES (%s, %s, %s, %s)"
    valores = (plataforma,quantidade,duracao_dias,preco,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Preço cadastrado com sucesso!")

def cadastrar_preco_console():
    print('\n========== Cadastro Tabela de Preços dos Consoles ==========\n')
    console = input("Nome do Console: ")
    duracao_horas = input("Digite a duração em horas: ")
    valor = input("Digite o preço: ")

    cursor = conexao.cursor()
    sql = "INSERT INTO precos_consoles (console,duracao_horas,valor) VALUES (%s, %s, %s)"
    valores = (console,duracao_horas,valor,)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Preço cadastrado com sucesso!")

def listar_tabela_precos():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM precos_jogos ORDER BY id")
    precos_jogos = cursor.fetchall()
    if not precos_jogos:
        print("Não existem preços de jogos cadastrados!")
    else:
        for precos_jogo in precos_jogos:
            print(f"ID: {precos_jogo[0]}, Plataforma: {precos_jogo[1]}, Quantidade de Jogos:{precos_jogo[2]}, Dias: {precos_jogo[3]}, Valor: {precos_jogo[4]}")

def listar_tabela_precos_consoles():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM precos_consoles ORDER BY id")
    precos_consoles = cursor.fetchall()
    if not precos_consoles:
        print("Não existem preços de consoles cadastrados!")
    else:
        for precos_console in precos_consoles:
            print(f"ID: {precos_console[0]}, Console: {precos_console[1]}, Horas:{precos_console[2]}, Valor: {precos_console[3]}")

def listar_jogos():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM jogos ORDER BY id")
    jogos = cursor.fetchall()
    if not jogos:
        print("Não existem jogos cadastrados!")
    else:
        for jogo in jogos:
            print(f"ID: {jogo[0]}, Título: {jogo[1]}, Plataforma:{jogo[2]}, gênero: {jogo[3]}, quantidade: {jogo[4]}")   

def listar_consoles():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM consoles ORDER BY id")
    consoles = cursor.fetchall()
    if not consoles:
        print("Não existem jogos cadastrados!")
    else:
        for console in consoles:
            print(f"ID: {console[0]}, Nome: {console[1]}")    

def cadastrar_aluguel_jogo():
    print('\n========== Cadastrando Aluguel de Jogo  ==========\n')

    cpf = input("Digite o cpf do cliente: ")
    print("Escolha qual forma de aluguel o cliente deseja: \n")
    listar_tabela_precos()

    preco_id = input("ID da forma de aluguel escolhida: ")
    #verificar se o ID da tabela preço escolhida é válido
    cursor = conexao.cursor()
    sql = "SELECT * FROM precos_jogos WHERE id = %s"
    valores = (preco_id,)
    cursor.execute(sql, valores)
    preco_jogo = cursor.fetchone()

    if preco_jogo is None:
        print("ID de preço da forma de aluguel inválido")
        return
    
    qtd_jogos_limite = preco_jogo[2]
    duracao_dias = preco_jogo[3]
    data_entrega = datetime.datetime.now() + datetime.timedelta(days=duracao_dias)

    #Inserir um novo registro na tabela alugueis
    cursor = conexao.cursor()
    sql = "INSERT INTO alugueis (data_entrega, cliente_cpf, preco_jogo_id) VALUES (%s, %s, %s)"
    valores = (data_entrega, cpf, preco_id,)
    cursor.execute(sql, valores)
    conexao.commit()
    aluguel_id = cursor.lastrowid

    print("Escolha os jogos para alugar: \n")
    listar_jogos()
    id_jogos = input().split(",") #['1', '2', '3', '4']

    if len(id_jogos) > qtd_jogos_limite:
        print(f"A quantidade de jogos deve ser ({qtd_jogos_limite})")
        return

    #Inserir um novo registro na tabela jogos_alugados para cada jogoe escolhido
    for jogo_id in id_jogos:
        sql_jogos_alugados = "INSERT INTO jogos_alugados (aluguel_id, jogo_id) VALUES (%s, %s)"
        valores_jogos_alugados = (aluguel_id, jogo_id,)
        cursor.execute(sql_jogos_alugados, valores_jogos_alugados)
        conexao.commit()

    print("Aluguel cadastrado com sucesso!")

def cadastrar_aluguel_console():
    print('\n========== Cadastrando Aluguel de Console  ==========\n')

    cpf = input("Digite o cpf do cliente: ")
    print("Escolha qual forma de aluguel o cliente deseja: \n")
    listar_tabela_precos_consoles()

    preco_id = input("ID da forma de aluguel escolhida: ")
    #verificar se o ID da tabela preço escolhida é válido
    cursor = conexao.cursor()
    sql = "SELECT * FROM precos_consoles WHERE id = %s"
    valores = (preco_id,)
    cursor.execute(sql, valores)
    preco_console = cursor.fetchone()

    if preco_console is None:
        print("ID de preço da forma de aluguel inválido")
        return
    
    duracao_horas = preco_console[2]
    currentDateAndTime = datetime.datetime.now()

    horarioFinal = currentDateAndTime + datetime.timedelta(hours=duracao_horas)

    #Inserir um novo registro na tabela alugueis
    cursor = conexao.cursor()
    sql = "INSERT INTO alugueis (data_entrega, cliente_cpf, preco_console_id) VALUES (%s, %s, %s)"
    valores = (horarioFinal, cpf, preco_id,)
    cursor.execute(sql, valores)
    conexao.commit()
    aluguel_id = cursor.lastrowid

    print("\nEscolha os consoles para alugar:")
    listar_consoles()
    id_consoles = input().split(",") #['1', '2', '3', '4']

    #Inserir um novo registro na tabela jogos_alugados para cada jogoe escolhido
    for console_id in id_consoles:
        sql_consoles_alugados = "INSERT INTO consoles_alugados (aluguel_id, console_id) VALUES (%s, %s)"
        valores_consoles_alugados = (aluguel_id, console_id,)
        cursor.execute(sql_consoles_alugados, valores_consoles_alugados)
        conexao.commit()

    print("Aluguel cadastrado com sucesso!")

# Cria uma conexão com o banco de dados
try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="palacioJogos"
    )
    cursor = conexao.cursor()
except:
    print("Erro ao conectar com o banco de dados")
    exit()



while True:
    print("\nEscolha uma opção: ")
    print("1 - Cadastrar Cliente")
    print("2 - Cadastrar jogo")
    print("3 - Cadastrar console")
    print("4 - Cadastrar preços de jogos")
    print("5 - Cadastrar preços de consoles")
    print("6 - Realizar um aluguel de jogo")
    print("7 - Realizar um aluguel de console")
    print("0 - Sair")

    opcao = input("Opção escolhida: ")
    
    if opcao == "1":
        cadastrar_cliente()
    elif opcao == "2":
        cadastrar_jogo()
    elif opcao == "3":
        cadastrar_console()
    elif opcao == "4":
        cadastrar_preco_jogo()
    elif opcao == "5":
        cadastrar_preco_console()
    elif opcao == "6":
        cadastrar_aluguel_jogo()
    elif opcao == "7":
        cadastrar_aluguel_console()                
    elif opcao == "0":
        break
