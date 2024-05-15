const btnapagar_conta = document.querySelector(".apagar_conta");
const modal_apagarConta = document.querySelector("#modal_apagarConta");
const cancelarApagarConta = document.querySelector("#cancelarApagarConta")
const btnEscolha_formulario_senha = document.querySelector("#escolha_formulario_senha");
const btnEscolha_formulario_produtos = document.querySelector("#escolha_formulario_produtos");
const formulario_produtos = document.querySelector("#formulario_produtos")
const produtos = document.querySelector("#produtos");
const formulario_senha = document.querySelector("#formulario_senha");
const titulo = document.querySelector("#titulo");
const botaoCancelar = document.querySelector('#cancelar-edicao');
var botaoEditar = document.querySelectorAll("#Editar");
const editarProduto = document.querySelector("#editar-produto");
 
btnapagar_conta.addEventListener("click", ()=>{
    modal_apagarConta.style.display = 'block';
})

cancelarApagarConta.addEventListener("click", ()=>{
    modal_apagarConta.style.display = 'none';
})

btnEscolha_formulario_senha.addEventListener("click", ()=>{
    produtos.style.display = 'none';
    formulario_produtos.style.display = 'none';
    editarProduto.style.display = 'none';
    formulario_senha.style.display = 'flex';
    titulo.textContent = "Alterar Senha";
})

btnEscolha_formulario_produtos.addEventListener("click", ()=>{
    if (produtos.style.display !== 'none') {
        produtos.style.display = 'none';
        editarProduto.style.display = 'none';
        formulario_produtos.style.display = 'flex';
        formulario_senha.style.display = 'none';
        titulo.textContent = 'Enviar Carros'
        btnEscolha_formulario_produtos.textContent = 'Meus Produtos';
    }else{
        produtos.style.display = 'flex';
        formulario_produtos.style.display = 'none';
        editarProduto.style.display = 'none';
        formulario_senha.style.display = 'none';
        titulo.textContent = 'Meus Carros'
        btnEscolha_formulario_produtos.textContent = 'Enviar Carros';
    }
})

const formNovasenha = document.querySelector("#formMudarSenha");
const novasenha = document.querySelector("#novaSenha");
const repetir = document.querySelector("#repetirNovaSenha");
const msgerro = document.querySelector("#errosenha");

formNovasenha.addEventListener("submit", (e)=>{
    if(novasenha.value !== repetir.value){
        msgerro.textContent = "As senha não são iguais";
        e.preventDefault();
        return false;
    }
})




botaoEditar.forEach( (botao)=>{
    botao.addEventListener('click', ()=>{
        produtos.style.display = 'none';
        editarProduto.style.display = 'flex';
        titulo.textContent = "Editar Produto"
        btnEscolha_formulario_produtos.textContent = 'Meus Produtos';




        var produto = botao.parentNode.querySelector('h2').textContent;
        var preco = botao.parentNode.querySelector('p:nth-child(4)').textContent.replace("Preço: R$ ","");
        var descricao = botao.parentNode.querySelector('p:nth-child(3)').textContent;
        var imagem = botao.parentNode.querySelector('img').src;

        document.querySelector("#editar_nome").value = produto;
        document.querySelector("#editar_preco").value = preco;
        document.querySelector("#editar_descricao").value = descricao;
        document.querySelector("#nomeAntigo").value = produto;
        document.querySelector("#imagem-produto").setAttribute('src', imagem);

    })
})



botaoCancelar.addEventListener('click', ()=>{
    produtos.style.display = 'flex';
    editarProduto.style.display = 'none';
    titulo.textContent = 'Meus Carros'
    btnEscolha_formulario_produtos.textContent = 'Enviar Carros';  
})