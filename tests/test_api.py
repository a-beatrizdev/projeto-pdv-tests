from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.cliente import Cliente


def test_listar_produtos_retorna_200(cliente):

    resposta = cliente.get("/produtos/")
    

    # 200 = ok, a página carregou sem erro

    assert resposta.status_code == 200


# Teste a tela de produtos em login 
def test_listagem_produtos_sem_login():
    from fastapi.testclient import TestClient
    from app.main import app

    cliente_sem_login = TestClient(app)

    resposta = cliente_sem_login.get("/produtos/")

    assert resposta.status_code == 401 


# Teste pagína lista o produto criado com sucesso!
def test_verificar_produtos_criado_com_sucesso(cliente, db_session_test):
    
    categoria = Categoria(nome="Bonés")
    db_session_test.add(categoria)
    db_session_test.commit()

    #criar produto
    produto = Produto(nome="Boné Aba Reta", preco=129.90, estoque_atual=50, categoria_id=categoria.id)
    db_session_test.add(produto)
    db_session_test.commit()

    resposta = cliente.get("/produtos")

    # Testar se existe o Boné na listagem de produtos
    assert "Boné Aba Reta" in resposta.text  


    #Testar a busca retorna somente os produtos filtrados
def test_listar_produtos_filtrado_por_busca (cliente, db_session_test):

    produto = Produto (nome="Camisa Nike", preco=99.90, estoque_atual=500)
    produto1 = Produto (nome="Caneca Harry Potter", preco=99.90, estoque_atual = 500 )
    db_session_test.add(produto)    
    db_session_test.add(produto1)    
    db_session_test.commit()

    resposta = cliente.get("/produtos", params={"busca": "Harry"})

    assert "Caneca Harry Potter" in resposta.text
    assert "Camisa Nike" not in resposta.text

#Exercicio verificar se a busca da rota cliente funciona.
def test_listar_clientes_filtrado_por_busca(cliente, db_session_test):

    cliente1 = Cliente(nome="Yasmim")
    cliente2 = Cliente( nome="Alana")
    db_session_test.add(cliente1)
    db_session_test.add(cliente2)
    db_session_test.commit()

    resposta = cliente.get("/clientes", params={"busca": "Alana"})

    assert "Alana" in resposta.text
    assert "Yasmim" not in resposta.text

# Test criar produto com sucesso na rota de produtos/novo 
def test_criar_produto_com_sucesso(cliente):

    resposta = cliente.post(
        "/produtos/novo",
        data={"nome": "Celular 14x", "preco": "2000.00", "estoque_atual": "20"}, 
        follow_redirects=False
    )

    # Testar
    assert resposta.status_code == 302
    assert resposta.headers["location"] == "/produtos?criado=ok"

    # Buscar as informações do HTML
    resposta_lista = cliente.get("/produtos")
    assert "Celular 14x" in resposta_lista.text 

# Teste editar um produto novo 
def test_editar_produto_atualiza_campos(cliente, db_session_test):
    # Criar um produto novo no banco. 
    produto = Produto(nome="Nome antigo", preco=20.0, estoque_atual=32)
    db_session_test.add(produto)
    db_session_test.commit()

    resposta = cliente.post(
        f"/produtos/{produto.id}/editar",
        data={"nome": "Nome novo", "preco": "30.0", "estoque_atual": "6"},
        follow_redirects=False
    )

    assert resposta.status_code == 302

    buscar_produto = db_session_test.query(Produto).filter(Produto.id == produto.id).first()
    assert buscar_produto.nome == "Nome novo"


