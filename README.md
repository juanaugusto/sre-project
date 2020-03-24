# Projeto SRE

## Como subir o Projeto SRE no seu computador local

Para começar, você deve instalar o [Docker](https://docs.docker.com/install/) no seu computador.

Feito isso, você irá precisar configurar três variáveis de ambiente:

* `API_KEY` e `API_SECRET_KEY` - Estas duas chaves são necessárias para fazer buscas por tweets usando a API do Twitter. Entre em https://developer.twitter.com e siga o passo a passo para obtê-las. 
* `HASHTAGS` - Aqui você irá informar as hashtags que a aplicação que insere os tweets no Banco de Dados irá utilizar separadas pelo caracter `;`.

```bash
# Ambientes Unix-like (Linux e MacOS)
export API_KEY="ADJGHGHHGHG"
export API_SECRET_KEY="FFFSFDDFDG"
export HASHTAGS="#openbanking;#apifirst;#devops"
export HASHTAGS="#openbanking"
```

```dos
% Ambiente Windows
setx API_KEY "ADJGHGHHGHG"
setx API_SECRET_KEY "FFFSFDDFDG"
setx HASHTAGS "#openbanking;#apifirst;#devops"
setx HASHTAGS "#openbanking"
```

Para subir as aplicações, abra um terminal/prompt, vá para o diretório raiz do projeto e execute o comando `docker-compose up -d`. Feito isso, todas as aplicações ficarão disponíveis dentro de alguns segundos.

Repare que a aplicação responsável por inserir a cada 10 minutos um tweet no banco, leva pouco mais de 1 minuto para começar a fazer as buscas na API do Twitter e inserir os tweets no banco de dados. Isso é feito para que haja tempo suficiente para que o banco de dados esteja de pé quando a inserção de tweets começar a ser feita.

Ao finalizar, não esqueça de rodar o comando `docker-compose down` na raiz do projeto.

### Como configurar pela primeira vez o Graylog para receber os logs da API REST

Em um browser qualquer, entre no endereço http://localhost:9000, preencha ambos os campos usuário e senha com o valor `admin`.

No painel superior, vá em `System` e depois clique em `Inputs`. Na próxima tela, clique em `Select Input`, selecione o valor `Gelf UDP` e clique em `Launch new input`.

Selecione então a opção `Global`, no campo `Title` dê um nome de sua preferência e clique no botão Save.

<p align="center">
  <img src="./docs/graylog-1.png" alt="Grafana image" />
</p>

<p align="center">
  <img src="./docs/graylog-2.png" alt="Grafana image" />
</p>

<p align="center">
  <img src="./docs/graylog-3.png" alt="Grafana image" />
</p>

### Como configurar pela primeira vez o Grafana com os dashboards de monitoração da API REST

Em um browser qualquer, entre no endereço http://localhost:3000, preencha ambos os campos usuário e senha com o valor `admin`.

No canto esquerdo da tela haverá um botão (+). Clique nele e em seguida clique em `Import`. Após isso clique no botão `Upload .json file`, selecione o arquivo `grafana-config.json` que se encontra no diretório `grafana` deste projeto e clique em `Load`.

<p align="center">
  <img src="./docs/grafana.png" alt="Grafana image" />
</p>

## Como rodar os testes automatizados

Para rodar os testes automatizados da aplicação que insere os tweets no banco de dados, execute o comando `docker-compose -f docker-compose.test.yml run --rm test_job` estando no diretório raiz do projeto.

Para rodar os testes automatizados da API REST, execute o comando `docker-compose -f docker-compose.test.yml run --rm test_api` estando no diretório raiz do projeto.