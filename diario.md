# Diário de Desenvolvimento

## Erros de Aplicação

### Erro de Firewall
Devido ao firewall da faculdade, a API da Twitch que utilizamos para buscar os jogos acabava sendo bloqueada. A solução rápida e prática foi de alterar a rede.

### Erro de CORS
Ao integrar o front com o back, durante as leituras ocorriam erros de CORS (vide imagem abaixo), e para solucionar, foram colocados os seguintes trechos de código na API para permitir as requisições sem maiores verificações de segurança.

![Erro Cors](/imagens/erro_cors.png)

```python
# ajusta problema de CORS que acontecia ao se comunicar com o front
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    return response

# manda as infos do CORS para dizer que pode mandar a requisição real, pois o CORS deu o ok
@app.route("/reviews", methods=["OPTIONS"])
@app.route("/reviews/<int:game_id>", methods=["OPTIONS"])
def reviews_preflight(game_id=None):
    return "", 204
```

Obs.: O navegador manda um OPTIONS antes da requisição real para perguntar se pode fazer aquela chamada (CORS). Sem `methods=["OPTIONS"]`, essa rota também respondia aos GET de verdade, devolvendo vazio em vez do JSON e causando o erro abaixo.

![Erro Cors](/imagens/erro_cors2.png)

## Erros de Infra

### Erro de Decodificação

Ao rodar o `docker compose up`, ocorreu um erro de decodificação, devido a um espaço desnecessário.

![Erro Compose](/imagens/erro_teste_dockerc.png)

### Erros MongoDB

Ao tentar rodar novamente, o usuário e senha do banco de dados não foi identificado, devido ao docker-compose estar na pasta raiz, e o arquivo env estar na pasta de backend.

![Erro Usuário e Senha](/imagens/erro_user_e_pass.png)

O seguinte erro ocorreu devido a falta da seção de volumes.

![Erro volumes](/imagens/falta_volume.webp)

### Erros Env

A API precisa de valores de autenticação vindos do `.env` entretanto os mesmos não estavam sendo buscados, primeiramente por um erro de compilação ao chamar o método responsável para fazer isso.

![Erro Compilação](/imagens/erro_backend.jpeg)

E após isso, devido a não declaração no `docker-compose`, a URL de autenticação retornava com erro, pois a autenticação tentava ser realizada com valores vazios. Para corrigir, foi preciso declarar o `environment` no serviço do compose.

```yaml
environment: # necessário enviar para serem usadas pela api
    TWITCH_CLIENT_ID: ${TWITCH_CLIENT_ID}
    TWITCH_CLIENT_SECRET: ${TWITCH_CLIENT_SECRET}
    MONGO_URI: ${MONGO_URI}
```