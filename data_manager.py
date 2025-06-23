import pickle


ARQUIVO_DADOS = 'livrosdic.pickle'

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, 'rb') as arquivo:
            dados = pickle.load(arquivo)
            return dados
    except (FileNotFoundError, EOFError):
        return {}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'wb') as arquivo:
        pickle.dump(dados, arquivo)

def get_todos_os_livros():
    dados = carregar_dados()
    return sorted(list(dados.keys()))

def get_detalhes_livro(nome_livro):
    dados = carregar_dados()
    return dados.get(nome_livro, None)

def adicionar_livro(nome, genero, autor, avaliacao, descricao):
    dados = carregar_dados()
    if nome in dados:
        print(f"Erro: Livro '{nome}' já existe.")
        return False
    
    dados[nome] = [genero, autor, str(avaliacao), descricao]
    salvar_dados(dados)
    return True

def remover_livro(nome_livro):
    dados = carregar_dados()
    if nome_livro in dados:
        dados.pop(nome_livro)
        salvar_dados(dados)
        return True
    return False

def editar_livro(nome_antigo, nome_novo, genero, autor, avaliacao, descricao):
    dados = carregar_dados()
    
    dados[nome_novo] = [genero, autor, str(avaliacao), descricao]

    if nome_antigo != nome_novo and nome_antigo in dados:
        dados.pop(nome_antigo)
    
    salvar_dados(dados)

def limpar_estante():
    salvar_dados({})