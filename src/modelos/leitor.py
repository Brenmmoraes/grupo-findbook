
class Leitor:
    def __init__(self, idLeitor, nome, email="", contacto="", morada="", cartaoCidadao=""):
        self.idLeitor = idLeitor
        self.nome = nome
        self.email = email
        self.contacto = contacto
        self.morada = morada
        self.cartaoCidadao = cartaoCidadao
        self.historicoEmprestimos = []
        self.emprestimosAtivos = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome do leitor não pode estar vazio.")
        self._nome = valor.strip()

    def para_dicionario(self):
        return {
            "idLeitor": self.idLeitor,
            "nome": self.nome,
            "email": self.email
        }

    @classmethod
    def de_dicionario(cls, dados):
        return cls(
            idLeitor=dados["idLeitor"],
            nome=dados["nome"],
            email=dados["email"]
        )

