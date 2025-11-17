# Cupcake Store – Virtual Cupcake Shop

A beautiful, fully functional online cupcake store built with **Flask** (Python).

<img width="1888" height="891" alt="image" src="https://github.com/user-attachments/assets/c54bed58-e222-4f4d-a280-8fb0536bee9d" />



## Features

- User registration & login (passwords hashed with Bcrypt)
- Create cupcakes with title, description, price and photo
- Public product showcase
- Shopping cart (session-based)
- Checkout with order history
- User profile with photo upload and editing
- 100% responsive design (Bootstrap 5)
- Secure image upload with automatic resizing

## Tech Stack

- Python
- Flask
- SQLite
- Bootstrap 5.0
- HTML
- CSS

## How to Run Locally

# 1. Clone the repo
git clone https://github.com/your-username/cupcake-store.git
cd cupcake-store

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux/Mac
# or
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
flask run
# or
python run.py

Acess: http://localhost:5000


## Project Structure

cupcake_store/
│
├── app/
│   ├── __init__.py 
│   ├── models.py  
│   ├── forms.py 
│   ├── routes.py 
│   ├── templates/ 
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── produto.html
│   │   ├── carrinho.html
│   │   ├── perfil.html
│   │   ├── editarperfil.html
│   │   ├── criarproduto.html
│   │   ├── login.html
│   │   ├── contato.html
│   │   ├── usuarios.html
│   │   └── navbar.html
│   │
│   └── static/                   # Arquivos estáticos
│       ├── css/
│       │   └── main.css
│       ├── cupcakes/
│       └── fotos_perfil/
│
├── migrations/                   # (criado automaticamente pelo Flask-Migrate)
│
├── instance/                     # Banco SQLite + arquivos de instância
│   └── cupcake_store.db
│
├── scripts/                      # Scripts auxiliares
│   └── update_descriptions.py    # (antigo inserção.py, renomeado em inglês)
│
├── tests/                        # Testes unitários (futuro)
│   └── test_basico.py
│
├── .gitignore
├── main.py
├── requirements.txt
