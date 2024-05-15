import os
from flask import Flask, render_template, request, redirect, flash, session;
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mateusSena'

@app.route('/')
def index():
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    if conect_BD.is_connected():
        cursur = conect_BD.cursor()
        cursur.execute("SELECT produtos.*, vendedor.nome AS nome_vendedor FROM produtos JOIN vendedor ON produtos.vendedor_id = vendedor.id;")
        produtosBD = cursur.fetchall()
        cursur.close()
        conect_BD.close()
        return render_template('home.html', produtos=produtosBD)
    
@app.route('/vendedorPremium')
def vendedorPremium():
    if 'vendedor' in session:
        conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    if conect_BD.is_connected():
        cursur = conect_BD.cursor()
        cursur.execute("SELECT produtos.*, vendedor.nome AS nome_vendedor, vendedor.telefone AS telefone_vendedor FROM produtos JOIN vendedor ON produtos.vendedor_id = vendedor.id;")
        produtosBD = cursur.fetchall()
        cursur.close()
        conect_BD.close()
        return render_template('vendedorPremium.html', produtos=produtosBD)

@app.route('/sair')
def sair():
    session.clear()
    return redirect('/')

@app.route('/loginVendedor')
def loginVendedor():
    return render_template('loginVendedor.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro.html')

@app.route('/perfilVendedor') 
def perfilVendedor():
    if 'vendedor' in session:
        conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
        email = session['vendedor']
    if conect_BD.is_connected():
        cursur = conect_BD.cursor()
        cursur.execute("select * from vendedor where email=%s;", (email,))
        vendedoresBD = cursur.fetchone()
        nome = vendedoresBD[2]
        foto = vendedoresBD[4]
        cursur = conect_BD.cursor()
        cursur.execute("select * from produtos where vendedor_id=%s", (vendedoresBD[0],))
        produtos = cursur.fetchall() 
        cursur.close()
        conect_BD.close()
        return render_template('vendedor.html', foto=foto, nome=nome, email=email, produtos=produtos)
    else:
        return redirect('/loginVendedor')            
    
@app.route('/acessoVendedor', methods=['POST'])
def acessoVendedor():
    email = request.form.get('emailvendedor')
    senha = request.form.get('senhavendedor')
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    if conect_BD.is_connected():
        cursur = conect_BD.cursor()
        cursur.execute("select * from vendedor where email=%s and senha=%s;", (email, senha))
        vendedoresBD = cursur.fetchone()
        cursur.close()
        conect_BD.close()
        if vendedoresBD:
            session['vendedor'] = email
            return redirect('/perfilVendedor')
        else: 
            flash('Email ou senha incorretos')
            return redirect('/loginVendedor') 
    
@app.route('/enviarFoto', methods=['POST'])
def enviarFoto():
    foto = request.files.get('foto')
    emailUsuario = request.form.get('emailUsuario')
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    nome_arquivo = f"Foto_perfil_{emailUsuario}.{foto.filename.split('.')[-1]}"
    foto.save(os.path.join('static/fotoperfil', nome_arquivo))
    cursur = conect_BD.cursor()
    cursur.execute("select * from vendedor where email=%s;", (emailUsuario,))
    vendedoresBD = cursur.fetchone()
    cursur.execute("update vendedor set foto=%s where id=%s;", (nome_arquivo, vendedoresBD[0],))
    conect_BD.commit()
    cursur.close()
    conect_BD.close()
    return redirect('/perfilVendedor')

@app.route('/novo_produto', methods=['POST'])
def novo_produto():
    foto = request.files.get("foto")
    nome_produto = request.form.get("nome")
    preco = request.form.get("preco")
    descricao = request.form.get("descricao")
    emailUsuario = request.form.get("emailUsuario")
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    if conect_BD.is_connected():
        nome_arquivo = f"foto_produto{session['vendedor']}_{nome_produto}.{foto.filename.split('.')[-1]}"
        foto.save(os.path.join('static/produtos', nome_arquivo))
        cursur = conect_BD.cursor()
        cursur.execute("select * from vendedor where email=%s;", (emailUsuario,))
        vendedoresBD = cursur.fetchone()
        id = vendedoresBD[0]
        cursur.execute("insert into produtos (nome_produto, imagem, descricao, preco, vendedor_id) values (%s, %s, %s, %s, %s);", (nome_produto, nome_arquivo, descricao, preco, id))
        conect_BD.commit()
        cursur.close()
        conect_BD.close()
    return redirect('/perfilVendedor')

@app.route('/cadastroVendedor', methods=['POST'])
def cadastroVendedor():
    email = request.form.get('emailVendedor')
    nome = request.form.get('nomeVendedor') 
    senha = request.form.get('senhaVendedor')
    telefone = request.form.get('telefoneVendedor')
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    if conect_BD.is_connected():
        cursur = conect_BD.cursor()
        cursur.execute("select * from vendedor where email = %s;", (email,))
        vendedor_existente = cursur.fetchone()
        if vendedor_existente:
            flash('Este e-mail já está cadastrado. Por favor, escolha outro.')
        else:
            cursur.execute("insert into vendedor (email,nome,senha,telefone) values (%s, %s, %s, %s);", (email, nome, senha, telefone))  
            conect_BD.commit()
            cursur.close()
            conect_BD.close()    
            flash(f'{nome} cadastrado com sucesso!!')
    return redirect('/loginVendedor')

@app.route('/apagar_conta', methods=['POST'])
def apagar_conta():
    emailUsuario = request.form.get("emailUsuario")
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    cursur = conect_BD.cursor()
    cursur.execute("select * from vendedor where email=%s;", (emailUsuario,))
    vendedoresBD = cursur.fetchone()
    id = vendedoresBD[0]
    cursur.execute("delete from vendedor where id=%s;", (id,))                
    conect_BD.commit()
    cursur.close()
    conect_BD.close()    
    return redirect('/')

@app.route("/novaSenha", methods=['POST']) 
def novaSenha():
    novaSenha = request.form.get('novaSenha')
    emailUsuario = request.form.get('emailUsuario') 
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    cursur = conect_BD.cursor()
    cursur.execute("select * from vendedor where email=%s;", (emailUsuario,))
    vendedoresBD = cursur.fetchone()
    cursur.execute("update vendedor set senha=%s where id=%s;", (novaSenha, vendedoresBD[0]))
    conect_BD.commit()
    cursur.close()
    conect_BD.close()
    flash(f'Senha alterada com sucesso, a nova senha é {novaSenha}')
    return redirect('/perfilVendedor')    

@app.route('/editar_produto', methods=['POST'])
def editar_produto():
    nome = request.form.get('editar_nome')
    preco = request.form.get('editar_preco')
    descricao = request.form.get('editar_descricao')
    emailUsuario = request.form.get('emailUsuario')
    nomeAntigo = request.form.get('nomeAntigo')
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    cursur = conect_BD.cursor()
    cursur.execute("select * from vendedor where email=%s;", (emailUsuario,))
    vendedoresBD = cursur.fetchone()
    print('TESTE')
    print(vendedoresBD[0])
    cursur.execute("update produtos set nome_produto=%s, preco=%s, descricao=%s where nome_produto=%s and vendedor_id=%s;",(nome, preco, descricao, nomeAntigo, vendedoresBD[0]))
    conect_BD.commit()
    cursur.close()
    conect_BD.close()
    return redirect('/perfilVendedor')  

@app.route('/excluir_produto', methods=['POST'])
def excluir_produto():  
    conect_BD = mysql.connector.connect(host='localhost', database='vendedores', user='root', password='')
    emailUsuario = request.form.get('emailUsuario')
    nomeProduto = request.form.get('nomeProduto')
    listnomeProdutos = nomeProduto.split(",")
    arquivo = listnomeProdutos[2]
    nome = listnomeProdutos[1]
    novoArquivo = arquivo.replace("'","").strip()
    novoNome = nome.replace("'", "").strip()
    cursur = conect_BD.cursor()
    cursur.execute("select * from vendedor where email=%s;", (emailUsuario,))
    vendedoresBD = cursur.fetchone() 
    id = vendedoresBD[0]
    os.remove(f"static/produtos/{novoArquivo}")
    cursur.execute("delete from produtos where nome_produto=%s and vendedor_id=%s;", (novoNome, id))
    conect_BD.commit()
    cursur.close()  
    conect_BD.close()                        
    return redirect('/perfilVendedor')

if __name__ in '__main__':
    app.run(debug=True)
