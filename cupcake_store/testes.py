from cupcake_store import app, database
from cupcake_store.models import Usuario

with app.app_context():
    database.create_all()

#with app.app_context():
#    usuario = Usuario(username="Lira", email="lira@gmail.com", senha="123456")
#    usuario2 = Usuario(username="Joao", email="joao@gmail.com", senha="123456")
#    database.session.add(usuario)
#    database.session.add(usuario2)
#    database.session.commit()

#with app.app_context():
#       usuario_teste = Usuario.query.filter_by(email='g.borba@cs.up.edu.br').first()
#        print(usuario_teste.cursos)

#with app.app_context():
#    meu_post = Post(id_usuario=1, titulo="Primeiro Post", corpo="Lira voando")
#    database.session.add(meu_post)
#    database.session.commit()

# with app.app_context():
#         post_teste = Post.query.first()
#         print(post_teste.titulo)
#         print(post_teste.autor.email)
#
# with app.app_context():
#     database.drop_all()
#     database.create_all()
