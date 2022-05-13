var botaoTabela = document.getElementById('nav-tabela-tab');

botaoTabela.onclick = obterJogadores;

function obterJogadores(){
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Basic UmVuYXRvOjEyMzQ1Ng==");

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
    };

    try{
        fetch("https://stark-tor-83181.herokuapp.com/jogadores", requestOptions)
          .then(response => response.text())
          .then(result =>{ 
              console.log(result);
              this.exibirJogadores(result);
            })
          .catch(error => console.log('error', error));
    }catch(error){
        console.log(error);
    }
}

function exibirJogadores(listaJogadores){
    const elemVisualizacao = document.querySelector('[data-Tabela]');
    elemVisualizacao.innerHTML = "";

    let tabela = document.createElement('table');
    tabela.className = "table table-dark table-striped"

    let cabecalho = document.createElement('thead');
    cabecalho.innerHTML = "<tr> \
            <th>Código</th> \
            <th>Nome</th> \
            <th>Data de Nascimento</th> \
            <th>Nickname</th> \
            </tr>"

    tabela.appendChild(cabecalho);

    let corpoTabela = document.createElement('tbody');
    for(jogador in listaJogadores){
        let linha = document.createElement('tr');
        linha.innerHTML = "<td>"+ jogador.id +"</td>" +
                          "<td>"+ jogador.nome +"</td>" +
                          "<td>"+ jogador.dataNasc +"</td>"+
                          "<td>"+ jogador.apelido +"</td>";
        corpoTabela.appendChild(linha);
    }

    tabela.appendChild(corpoTabela);
}
