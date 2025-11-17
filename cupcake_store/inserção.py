# atualizar_descricoes.py
from cupcake_store import app, database
from cupcake_store.models import Produto  # ajuste conforme sua estrutura

# Dicionário: título → nova descrição
descricoes_atualizadas = {
    "Cupcake de Amora": "Explosão de suculência selvagem! Massa fofinha de baunilha recheada com geleia fresca de amora, coberta por buttercream roxo vibrante e amoras frescas. Um deleite ácido-doce que conquista o paladar!",

    "Cupcake de Oreo": "Clássico irresistível com twist! Base de chocolate úmido misturada com pedaços crocantes de Oreo, recheio cremoso de baunilha, topped com ganache de chocolate e mini Oreos. Perfeito para os viciados em biscoito!",

    "Cupcake de Coco": "Viagem tropical em cada mordida! Massa leve de coco ralado, recheio de brigadeiro de coco cremoso, finalizado com glacê de coco neve e flocos torrados. Frescor e doçura que remetem ao paraíso!",

    "Baunilha": "Simplesmente perfeito e atemporal! Massa macia de baunilha pura, recheio surpresa de creme de baunilha, coberta por buttercream suave e sprinkles coloridos. O conforto clássico que nunca sai de moda!",

    "Cupcake de Chantily Rosa": "Sonho romântico em forma de doce! Massa delicada de baunilha tingida de rosa, recheio de chantily leve, topped com nuvens de chantily rosa e confeitos brilhantes. Ideal para festas e corações apaixonados!",

    "Cupcake de Morango": "Frescor vermelho e vibrante! Massa fofinha com pedaços de morango fresco, recheio de geleia natural, coberta por frosting de morango cremoso e morangos inteiros. Uma explosão juicy que grita verão!",

    "Cupcake de Chocolate": "Indulgência pura para chocólatras! Massa rica de cacau intenso, recheio de ganache derretido, topped com buttercream de chocolate belga e raspas crocantes. Decadência que derrete na boca!",

    "Cupcake de Doce de Leite": "Carinho argentino em miniatura! Massa macia de baunilha, recheio generoso de doce de leite cremoso, coberta por glacê de doce de leite e fios dourados. Doçura viciante que abraça a alma!"
}

with app.app_context():
    atualizados = 0
    nao_encontrados = []

    for titulo, nova_descricao in descricoes_atualizadas.items():
        produto = Produto.query.filter_by(titulo=titulo).first()
        if produto:
            produto.corpo = nova_descricao
            atualizados += 1
        else:
            nao_encontrados.append(titulo)

    if atualizados > 0:
        database.session.commit()
        print(f"✅ {atualizados} descrições atualizadas com sucesso!")
    else:
        print("Nenhum produto foi atualizado.")

    if nao_encontrados:
        print(f"⚠️ Não encontrados: {', '.join(nao_encontrados)}")