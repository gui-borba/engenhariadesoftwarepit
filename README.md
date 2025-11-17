# Loja de Cupcakes - Vitrine Virtual

Uma loja virtual completa e charmosa de cupcakes feita com **Flask** (Python).  
Perfeita para portfólio, MVP ou até mesmo para colocar no ar e vender de verdade!

<img width="1888" height="891" alt="image" src="https://github.com/user-attachments/assets/c54bed58-e222-4f4d-a280-8fb0536bee9d" />



## Funcionalidades

- Cadastro e login de usuários (senhas criptografadas com Bcrypt)  
- Criação de cupcakes com nome, descrição, preço e foto  
- Vitrine pública com todos os produtos  
- Carrinho de compras (session)  
- Finalização de compra com registro de vendas  
- Perfil do usuário com foto e edição   
- Upload seguro de imagens com redimensionamento automático  

## Tecnologias Utilizadas

- Python
- Flask
- SQLite
- Bootstrap 5.0
- HTML
- CSS

## Como rodar o projeto localmente

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/loja-cupcakes.git
cd loja-cupcakes

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate    # Linux/Mac
# ou
venv\Scripts\activate       # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a aplicação
python run.py
# ou
flask run
Acesse: http://localhost:5000
