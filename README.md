# Projeto SRE

## Como subir o Projeto SRE no seu computador local

Para começar, você deve instalar o [Docker](https://docs.docker.com/install/) no seu computador.

Feito isso, você irá precisar configurar duas variáveis de ambiente:

* `BEARER_TOKEN` - Este token é necessário para fazer buscas por tweets usando a [API do Twitter](https://developer.twitter.com). Você irá precisar gerá-lo apenas uma vez
* `HASHTAGS` - Aqui você irá informar as hashtags que a aplicação que insere os tweets no Banco de Dados irá utilizar separadas pelo caracter `;`.

```bash
# Ambientes Unix-like (Linux e MacOS)
export HASHTAGS="#openbanking;#apifirst;#devops"
export HASHTAGS="#openbanking"
```

```dos
% Ambiente Windows
setx HASHTAGS "#openbanking;#apifirst;#devops"
setx HASHTAGS "#openbanking"
```

Para subir o projeto, rode em um terminal o comando ``




## Como rodar os testes automatizados