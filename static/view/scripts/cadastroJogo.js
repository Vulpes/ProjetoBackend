var botaoTabela = document.getElementById('nav-tabela-tab');

botaoTabela.onclick = obterJogos;

var botaoGravar = document.getElementById('gravar');

botaoGravar.onclick = gravarJogador;

function gravarJogador(){   
    let nome = document.getElementById("nome").value;
    let horasJogadas = document.getElementById("horasJogadas").value;
    
    const mensagem = document.querySelector('[data-Mensagem]');


    if(nome && horasJogadas ){

        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Basic UmVuYXRvOjEyMzQ1Ng==");
        myHeaders.append("Content-Type", "application/json");

        var data = JSON.stringify({
            "nome": nome,
            "horasJogadas": horasJogadas
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: data,
        };

        fetch("https://stark-tor-83181.herokuapp.com/jogos", requestOptions)
            .then((response) =>{ console.log(response); return response.json(); })
            .then(result => {
                console.log(result)
                if(result.id){
                    mensagem.className="alert alert-success";
                    mensagem.innerHTML = "O jogo " + result.id + " foi cadastrado com sucesso";
                }else{
                    mensagem.className = "alert alert-warning";
                    mensagem.innerHTML  = result.status;
                }
            })
            .catch(error => console.log('error', error));

    }else{
        mensagem.className="alert alert-danger";
        mensagem.innerHTML = "Por favor, preencha todos os campos!";
    }
}

function exibirJogos(listaJogos){
    const elemVisualizacao = document.querySelector('[data-Tabela]');
    elemVisualizacao.innerHTML = "";

    let tabela = document.createElement('table');
    tabela.className = "table table-dark table-striped"

    let cabecalho = document.createElement('thead');
    cabecalho.innerHTML = "<tr> \
            <th>Código</th> \
            <th>Nome</th> \
            <th>Horas Jogadas</th> \
            </tr>"

    tabela.appendChild(cabecalho);

    let corpoTabela = document.createElement('tbody');
    for(i = 0; i < listaJogos.length; i++){
        let linha = document.createElement('tr');
        console.log(listaJogos[i]);
        linha.innerHTML = "<td>"+ listaJogos[i].nome +"</td>" +
                          "<td>"+ listaJogos[i].horasJogadas +"</td>";
        corpoTabela.appendChild(linha);
    }

    tabela.appendChild(corpoTabela);
    elemVisualizacao.appendChild(tabela);
}


function obterJogos(){
    var myHeaders = new Headers();
    myHeaders.append("Authorization", "Basic UmVuYXRvOjEyMzQ1Ng==");

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
    };

    try{
        fetch("https://stark-tor-83181.herokuapp.com/jogos", requestOptions)
          .then(response => response.json())
          .then(result =>{ 
              console.log(result);
              exibirJogos(result);
            })
          .catch(error => console.log('error', error));
    }catch(error){
        console.log(error);
    }
}

