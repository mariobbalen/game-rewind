# expoe todos os arquivos html (e js) da pasta do front e coloca no nginx

FROM nginx:alpine

# manda direto os arquivos, não precisa de um workdir para o nginx
COPY . /usr/share/nginx/html/

# coloca na porta 80 do container
EXPOSE 80
