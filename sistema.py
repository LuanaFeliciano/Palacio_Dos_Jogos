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
    cursor.execute("SELECT * FROM jogos WHERE quantidade > 0 ORDER BY id")
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

def realizar_aluguel_jogo():
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
        print(f"A quantidade de jogos escolhida deve ser ({qtd_jogos_limite})")
        return

    quantidade_jogos = {}
    #Inserir um novo registro na tabela jogos_alugados para cada jogoe escolhido e realizar o update da quantidade
    for jogo_id in id_jogos:
        sql_select_jogo = "SELECT quantidade FROM jogos WHERE id = %s"
        valores_select_jogo = (jogo_id,)
        cursor.execute(sql_select_jogo, valores_select_jogo)
        quantidade_jogo = cursor.fetchone()
        quantidade_jogos[jogo_id] = quantidade_jogo[0]


    for jogo_id in id_jogos:
        sql_jogos_alugados = "INSERT INTO jogos_alugados (aluguel_id, jogo_id) VALUES (%s, %s)"
        valores_jogos_alugados = (aluguel_id, jogo_id,)
        cursor.execute(sql_jogos_alugados, valores_jogos_alugados)
        
        #atualizar quantidade
        quantidade_atual = quantidade_jogos[jogo_id]
        nova_quantidade = quantidade_atual - 1
        sql_update_quantidade = "UPDATE jogos SET quantidade = %s WHERE id = %s"
        valores_update_quantidade = (nova_quantidade, jogo_id)
        cursor.execute(sql_update_quantidade, valores_update_quantidade)

        conexao.commit()

    print("Aluguel cadastrado com sucesso!")

def realizar_aluguel_console():
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

def realizar_devolucao_jogo():
    #2- fazer um de realizar baixa de devolução do jogo alugado (update quantidade)
    print('\n========== Devolução de Jogo  ==========\n')
    cpf = input("Digite o CPF do cliente: ")
    listar_jogos()
    jogos_ids = input("Digite os IDs dos jogos separados por vírgula: ").split(",")

    cursor = conexao.cursor()
    #verificar se o cliente tem aluguel
    for jogo_id in jogos_ids:
        # Verificar se o cliente possui aluguéis em aberto com o jogo selecionado
        sql_select_alugueis = """
            SELECT alugueis.id AS "id do aluguel", alugueis.data_reserva, alugueis.data_entrega, alugueis.cliente_cpf,
                   jogos.titulo AS "Jogo", precos_jogos.valor AS "total"
            FROM alugueis
            JOIN jogos_alugados ON alugueis.id = jogos_alugados.aluguel_id
            JOIN jogos ON jogos_alugados.jogo_id = jogos.id
            JOIN precos_jogos ON jogos.id = precos_jogos.id
            WHERE alugueis.cliente_cpf = %s AND jogos.id = %s
        """

    valores_select_alugueis = (cpf, jogo_id,)
    cursor.execute(sql_select_alugueis, valores_select_alugueis)
    alugueis = cursor.fetchall()

    if not alugueis:
        print("Esse cliente não realizou nenhum aluguel de jogo")
        return
    
    print("\n========== Aluguéis em aberto do cliente: ==========\n")
    for aluguel in alugueis:
        print(f"ID do Aluguel: {aluguel[0]}, Data de Reserva: {aluguel[1]}, Data de Entrega: {aluguel[2]}, CPF do Cliente: {aluguel[3]}")
        print(f"Jogo: {aluguel[4]}, Valor Total: {aluguel[5]}")

    aluguel_id = input("Digite o ID do aluguel que deseja devolver o jogo: ")

        # Verificar se o jogo está associado ao aluguel selecionado
    sql_select_jogo_alugado = "SELECT * FROM jogos_alugados WHERE aluguel_id = %s AND jogo_id = %s"
    valores_select_jogo_alugado = (aluguel_id, jogo_id,)
    cursor.execute(sql_select_jogo_alugado, valores_select_jogo_alugado)
    jogo_alugado = cursor.fetchone()

    if jogo_alugado is None:
        print("ID de jogo inválido para o aluguel selecionado.")
        return
    
    # Atualizar a quantidade do jogo na tabela de jogos
    sql_select_jogo = "SELECT quantidade FROM jogos WHERE id = %s"
    valores_select_jogo = (jogo_id,)
    cursor.execute(sql_select_jogo, valores_select_jogo)
    quantidade_atual = cursor.fetchone()[0]

    nova_quantidade = quantidade_atual + 1

    sql_update_quantidade = "UPDATE jogos SET quantidade = %s WHERE id = %s"
    valores_update_quantidade = (nova_quantidade, jogo_id)
    cursor.execute(sql_update_quantidade, valores_update_quantidade)

    conexao.commit()
    print("Devolução realizada com sucesso")

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
    print("8 - Realizar devolução de jogo")
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
        realizar_aluguel_jogo()
    elif opcao == "7":
        realizar_aluguel_console()
    elif opcao == "8":
        realizar_devolucao_jogo()                    
    elif opcao == "0":
        break