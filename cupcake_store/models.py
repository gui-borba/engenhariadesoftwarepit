from cupcake_store import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    # relacionamento com produtos (um usuário pode ter vários produtos)
    produtos = database.relationship('Produto', backref='autor', lazy=True)

    def contar_produtos(self):
        return len(self.produtos)

    def __repr__(self):
        return f"<Usuario {self.username}>"

class Produto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(150), nullable=False)         # antes: produto
    corpo = database.Column(database.Text, nullable=False)                 # antes: descricao
    preco = database.Column(database.Float, nullable=False, default=0.0)   # novo: preco
    foto_produto = database.Column(database.String, default='cupcake_default.jpg')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    # FK para autor (usuario)
    autor_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"<Produto {self.titulo} - R${self.preco:.2f}>"

class Venda(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    quantidade = database.Column(database.Integer, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_produto = database.Column(database.Integer, database.ForeignKey('produto.id'), nullable=False)

    usuario = database.relationship('Usuario', backref='vendas')
    produto = database.relationship('Produto')
