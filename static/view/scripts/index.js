var botaoTabela = document.getElementById('nav-tabela-tab');

botaoTabela.onclick = obterJogadores;

var botaoGravar = document.getElementById('gravar');

botaoGravar.onclick = gravarJogador;

function gravarJogador(){
    let nome = document.getElementById("nome").value;
    let dataNasc = document.getElementById("dataNasc").value;
    let apelido = document.getElementById("nickname").value;

    if(nome && dataNasc && apelido){

        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Basic UmVuYXRvOjEyMzQ1Ng==");
        myHeaders.append("Content-Type", "application/json");

        var data = JSON.stringify({
            "apelido": apelido,
            "dataNasc": dataNasc,
            "nome": nome,
            "jogos": [
                {
                    "id": 1,
                    "nomejogo": "teste"
                }
            ]
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: data,
        };

        fetch("https://stark-tor-83181.herokuapp.com/jogadores", requestOptions)
            .then(response => response.text())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));

    }else{
        const mensagem = document.querySelector('[data-Mensagem]');

        mensagem.className="alert alert-danger";
        mensagem.innerHTML = "Por favor, preencha todos os campos!";
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
    for(i = 0; i < listaJogadores.length; i++){
        let linha = document.createElement('tr');
        console.log(listaJogadores[i]);
        linha.innerHTML = "<td>"+ listaJogadores[i].id +"</td>" +
                          "<td>"+ listaJogadores[i].nome +"</td>" +
                          "<td>"+ listaJogadores[i].dataNasc +"</td>"+
                          "<td>"+ listaJogadores[i].apelido +"</td>";
        corpoTabela.appendChild(linha);
    }

    tabela.appendChild(corpoTabela);
    elemVisualizacao.appendChild(tabela);
}


function obterJogadores(){
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Basic UmVuYXRvOjEyMzQ1Ng==");

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
    };

    try{
        fetch("https://stark-tor-83181.herokuapp.com/jogadores", requestOptions)
          .then(response => response.json())
          .then(result =>{ 
              console.log(result);
              exibirJogadores(result);
            })
          .catch(error => console.log('error', error));
    }catch(error){
        console.log(error);
    }
}

