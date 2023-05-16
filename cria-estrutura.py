#PALÁCIO DOS JOGOS - ALUGUEL DE JOGOS e LAN-HOUSE DE CONSOLES
import mysql.connector

def cria_estrutura(sql, conexao, tabela):
    try:
        conexao.execute(sql)
    except mysql.connector.Error as err:
        print("Erro ao criar tabela: ", tabela)
        print("Mensagem de erro: ", err)
        exit()

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

#cadastro do cliente
cria_estrutura("CREATE TABLE clientes (cpf VARCHAR(11) NOT NULL, nome VARCHAR(100) NOT NULL, contato VARCHAR(11) NOT NULL, PRIMARY KEY (cpf))", cursor, "CLIENTES")

#cadastro dos jogos
cria_estrutura("CREATE TABLE jogos (id INT NOT NULL AUTO_INCREMENT, titulo VARCHAR(50) NOT NULL, plataforma VARCHAR(50) NOT NULL,genero VARCHAR(50) NOT NULL,quantidade INT NOT NULL, PRIMARY KEY (id))", cursor, "JOGOS")
#cadastro dos consoles
cria_estrutura("CREATE TABLE consoles (id INT NOT NULL AUTO_INCREMENT, nome VARCHAR(50) NOT NULL,quantidade INT NOT NULL, PRIMARY KEY (id))", cursor, "CONSOLES")

#CRIAR TABELA DE PRECOS PRA JOGOS E PARA OS CONSOLES
cria_estrutura("CREATE TABLE precos_jogos (id INT NOT NULL AUTO_INCREMENT, plataforma_jogo VARCHAR(20) NOT NULL, qtd_jogos INT NOT NULL, duracao_dias INT NOT NULL, valor DECIMAL(7,2) NOT NULL, PRIMARY KEY (id))", cursor, "PREÇOS_JOGOS")
cria_estrutura("CREATE TABLE precos_consoles (id INT NOT NULL AUTO_INCREMENT,console VARCHAR(20) NOT NULL, duracao_horas INT NOT NULL, valor DECIMAL(7,2) NOT NULL, PRIMARY KEY (id))", cursor, "PREÇOS_CONSOLES")

# tabela para cadastrar o aluguel do cliente
cria_estrutura("CREATE TABLE alugueis (id INT NOT NULL AUTO_INCREMENT, data_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP, data_entrega DATETIME, cliente_cpf VARCHAR(11) NOT NULL, preco_jogo_id INT, preco_console_id INT, FOREIGN KEY (cliente_cpf) REFERENCES clientes(cpf), FOREIGN KEY (preco_jogo_id) REFERENCES precos_jogos(id), FOREIGN KEY (preco_console_id) REFERENCES precos_consoles(id), PRIMARY KEY (id))", cursor, "ALUGUEIS")

# Criação da tabela de jogos alugados
cria_estrutura("CREATE TABLE jogos_alugados (id INT NOT NULL AUTO_INCREMENT, aluguel_id INT NOT NULL, jogo_id INT NOT NULL, PRIMARY KEY (id), FOREIGN KEY (aluguel_id) REFERENCES alugueis(id), FOREIGN KEY (jogo_id) REFERENCES jogos(id))", cursor, "JOGOS_ALUGADOS")

# Criação da tabela de consoles alugados
cria_estrutura("CREATE TABLE consoles_alugados (id INT NOT NULL AUTO_INCREMENT, aluguel_id INT NOT NULL, console_id INT NOT NULL, PRIMARY KEY (id), FOREIGN KEY (aluguel_id) REFERENCES alugueis(id), FOREIGN KEY (console_id) REFERENCES consoles(id))", cursor, "CONSOLES_ALUGADOS")


print("*******************************")
print("*ESTRUTURA CRIADA COM SUCESSO!*")
print("*******************************")