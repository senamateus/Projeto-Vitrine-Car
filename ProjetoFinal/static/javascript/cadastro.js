const vendedorCadastro = document.querySelector("#vendedorCadastro");
vendedorCadastro.addEventListener('submit', (event) =>{
    event.preventDefault();
    let senha = document.querySelector("#senhaVendedor");  
    let repetirSenha = document.querySelector("#repetirSenhaVendedor");
    let msgErro = document.querySelector("#msgErro");

    if (senha.value !== repetirSenha.value){
        msgErro.style.display = 'block';
        return false;
    }else{
        msgErro.style.display = 'none';
        vendedorCadastro.submit();   
        return true;
    }

})