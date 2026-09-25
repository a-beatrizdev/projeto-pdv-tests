from app.models.produto import Produto
from app.models.movimentacao import Movimentacao
from app.models.categoria import Categoria
from app.models.venda import Venda


# Test criar movimentação com sucesso
def test_criar_movimentacao_com_sucesso(cliente, db_session_test):

    produto = Produto(
        nome="Caderno",
        preco=20.0,
        estoque_atual=10
    )

    db_session_test.add(produto)
    db_session_test.commit()

    resposta = cliente.post(
        "/movimentacoes/nova",
        data={
            "produto_id": produto.id,
            "tipo": "saida",
            "quantidade": "3",
            "preco_unitario": "20.0",
            "observacao": "Saida"
        },
        follow_redirects=False
    )

    assert resposta.status_code == 302

    buscar_produto = db_session_test.query(Produto).filter(
        Produto.id == produto.id
    ).first()

    assert buscar_produto.estoque_atual == 7

    movimentacao = db_session_test.query(Movimentacao).first()

    assert movimentacao is not None
    assert movimentacao.quantidade == 3


# Teste criar categoria com sucesso
def test_criar_categoria_com_sucesso(cliente, db_session_test):

    resposta = cliente.post(
        "/categorias/nova",
        data={"nome": "Eletrônicos"},
        follow_redirects=False
    )

    assert resposta.status_code == 302
    assert resposta.headers["location"] == "/categorias?criado=ok"

    categoria = db_session_test.query(Categoria).filter(
        Categoria.nome == "Eletrônicos"
    ).first()

    assert categoria is not None
    assert categoria.nome == "Eletrônicos"


# Teste não permitir categoria duplicada
def test_criar_categoria_duplicada(cliente, db_session_test):

    categoria = Categoria(nome="Eletrônicos")

    db_session_test.add(categoria)
    db_session_test.commit()

    resposta = cliente.post(
        "/categorias/nova",
        data={"nome": "Eletrônicos"},
        follow_redirects=False
    )

    assert resposta.status_code == 400
    assert "Já existe uma categoria com este nome." in resposta.text


# Test criar venda com sucesso
def test_criar_venda_com_sucesso(cliente, db_session_test):

    produto = Produto(
        nome="Caderno",
        preco=20.0,
        estoque_atual=10
    )

    db_session_test.add(produto)
    db_session_test.commit()

    resposta = cliente.post(
        "/pdv/finalizar",
        data={
            "carrinho_json": '[{"produto_id": %d, "nome": "Caderno", "preco": 20.0, "quantidade": 2}]' % produto.id,
            "cliente_id": "0",
            "observacao": "Venda"
        },
        follow_redirects=False
    )

    assert resposta.status_code == 302

    buscar_venda = db_session_test.query(Venda).first()

    assert buscar_venda is not None
    assert buscar_venda.total_bruto == 40.0
    assert buscar_venda.total_liquido == 40.0


from app.models.usuarios import Usuario


# Test editar usuario com sucesso
def test_editar_usuario_com_sucesso(cliente, db_session_test):

    usuario = Usuario(
        nome="Usuario",
        email="usuario@gmail.com",
        senha_hash="123456",
        role="operador"
    )

    db_session_test.add(usuario)
    db_session_test.commit()

    resposta = cliente.post(
        f"/usuarios/{usuario.id}/editar",
        data={
            "nome": "Usuario Teste",
            "email": "usuario@gmail.com",
            "role": "admin"
        },
        follow_redirects=False
    )

    assert resposta.status_code == 302

    buscar_usuario = db_session_test.query(Usuario).filter(
        Usuario.id == usuario.id
    ).first()

    assert buscar_usuario.nome == "Usuario Teste"
    assert buscar_usuario.role == "admin"

