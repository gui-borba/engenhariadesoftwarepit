import flask_login
from flask import render_template, redirect, url_for, flash, request, abort, url_for, current_app, session
from cupcake_store import app, database, bcrypt
from cupcake_store.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarProduto
from cupcake_store.models import Usuario, Produto
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from decimal import Decimal

@app.route('/')
def home():
    produtos = Produto.query.order_by(Produto.id.desc()).all()
    return render_template('home.html', produtos=produtos)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. Email ou senha incorretos.', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

def salvar_imagem_perfil(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def salvar_imagem_produto(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/cupcakes', nome_arquivo)
    # redimensiona mantendo proporção, dimensões maiores para produto
    tamanho = (600, 600)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route('/produto/criar', methods=['GET', 'POST'])
@login_required
def criar_produto():
    form = FormCriarProduto()
    if form.validate_on_submit():
        nome_imagem = None
        if form.foto_produto.data:
            nome_imagem = salvar_imagem_produto(form.foto_produto.data)
        else:
            nome_imagem = 'cupcake_default.jpg'
        produto = Produto(
            titulo=form.titulo.data,
            corpo=form.corpo.data,
            preco=float(form.preco.data),
            foto_produto=nome_imagem,
            autor=current_user
        )
        database.session.add(produto)
        database.session.commit()
        flash('Produto criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarproduto.html', form=form)

@app.route('/produto/<int:produto_id>', methods=['GET', 'POST'])
def exibir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    # se autor, permite edição em outra rota; aqui apenas exibimos
    return render_template('produto.html', produto=produto)

@app.route('/adicionar_carrinho/<int:produto_id>', methods=['POST'])
@login_required
def adicionar_carrinho(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    quantidade = int(request.form.get('quantidade', 1))
    cart = session.get('cart', {})
    # armazenar como strings para serialização em session
    item = cart.get(str(produto_id), {'titulo': produto.titulo, 'preco': produto.preco, 'quantidade': 0, 'foto': produto.foto_produto})
    item['quantidade'] = item.get('quantidade', 0) + quantidade
    cart[str(produto_id)] = item
    session['cart'] = cart
    flash(f'Adicionado {quantidade} x {produto.titulo} ao carrinho.', 'alert-success')
    return redirect(url_for('home'))

@app.route('/carrinho')
@login_required
def ver_carrinho():
    cart = session.get('cart', {})
    total = 0.0
    for k, item in cart.items():
        total += float(item['preco']) * int(item['quantidade'])
    return render_template('carrinho.html', cart=cart, total=total)

@app.route('/remover_carrinho/<produto_id>')
def remover_carrinho(produto_id):
    cart = session.get('cart', {})
    if produto_id in cart:
        del cart[produto_id]
        session['cart'] = cart
        flash('Item removido do carrinho.', 'alert-info')
    return redirect(url_for('ver_carrinho'))

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem_perfil(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return  render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/finalizar_compra', methods=['POST'])
@login_required
def finalizar_compra():
    cart = session.get('cart', {})

    if not cart:
        flash('Seu carrinho está vazio!', 'alert-warning')
        return redirect(url_for('ver_carrinho'))

    from cupcake_store.models import Venda

    # Salvar cada item como uma Venda separada
    for produto_id, item in cart.items():
        venda = Venda(
            quantidade=item['quantidade'],
            id_usuario=current_user.id,
            id_produto=int(produto_id)
        )
        database.session.add(venda)

    database.session.commit()

    # limpar carrinho
    session['cart'] = {}

    flash('Compra realizada com sucesso! Obrigado pela preferência 😊', 'alert-success')
    return redirect(url_for('home'))