# Game Rewind

Game Rewind é uma aplicação web para buscar jogos e registrar suas próprias avaliações sobre eles. A busca é feita através da API da IGDB (via Twitch), e as avaliações (nota, texto e se o jogo foi jogado) são salvas em um banco de dados MongoDB.

## Integrantes

- Mário Bernardo Balen (1136196)
- Pablo Henrique Strücker Sarturi (1136331)

## Uso de IA

- O projeto teve seu backend criado com o auxílio de IA, com constante revisões e testes separados para verificar se tudo estava conforme especificado.
  - Foram adicionados comentários pertinentes para um melhor entendimento durante as revisões.
- O frontend foi inteiramente gerado por IA.

## Funcionalidades

- Buscar jogos pelo nome, exibindo capa e nota do IGDB.
- Avaliar um jogo com nota de 0 a 5 estrelas (com meias estrelas) e um texto de review.
- Marcar um jogo como "jogado".
- Ver, editar e excluir todas as avaliações salvas em uma página separada.

## Tecnologias

- **Backend:** Python, Flask, PyMongo
- **Frontend:** HTML, CSS e JavaScript puro
- **Banco de dados:** MongoDB
- **Infraestrutura:** Docker

## Configuração

O backend precisa de algumas variáveis de ambiente, definidas em `src/backend/.env` (veja `src/backend/.env.example`):

- `TWITCH_CLIENT_ID` e `TWITCH_CLIENT_SECRET`: credenciais de um app criado em https://dev.twitch.tv/console/apps, usadas para acessar a API do IGDB.
- `MONGO_URI`: string de conexão do MongoDB (ex: `mongodb://<host>:27017`).

## Como executar

1. Suba um MongoDB (local ou via container).
2. Configure o arquivo `.env` do backend conforme descrito acima.
3. Construa e execute os containers
4. Acesse a interface em `http://localhost:8080`. A API ficará disponível em `http://localhost:5000`.

## Endpoints da API

- `GET /games?q=<nome>`: busca jogos no IGDB.
- `GET /reviews`: lista todas as avaliações salvas.
- `POST /reviews`: cria ou atualiza a avaliação de um jogo.
- `DELETE /reviews/<game_id>`: remove a avaliação de um jogo.
