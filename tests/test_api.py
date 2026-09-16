from app.models.produto import Produto 
from app.models.categoria import Categoria 


def test_listar_produtos_retorna_200(cliente):

    resposta = cliente.get("/produtos/")

    # 200 = ok, a página carregou sem erro.

    assert resposta.status_code == 200
    
