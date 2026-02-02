from src.repository.queries import QueriesRepository
from src.model.model import Usuario

def teste_criar_usuario(session):

    repo = QueriesRepository(session)

    usuario = Usuario(
        nome="João Mendes",
        email="joao@email.com",
        senha="1234Jbl#",
        ativo=True,
        admin=False

    )

    usuario_criado = repo.criar_usuario(usuario)

    assert usuario_criado.id is not None
    assert usuario_criado.email == "joao@email.com"


def teste_buscar_usuario(session):

    repo = QueriesRepository(session)
    usuario = Usuario(
        nome="Maria",
        email="maria@email.com",
        senha="senha123"
    )

    repo.criar_usuario(usuario)
    usuario = repo.buscar_email("maria@email.com")

    assert usuario is not None
    assert usuario.email == "maria@email.com"
