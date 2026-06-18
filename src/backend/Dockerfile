# usando a segunda menor tag, para que seja leve mas não tenha problema de ser incompatível com o flask
FROM python:3.12-slim

# define que todo o backend vai ficar na pasta app dentro do docker
WORKDIR /app

# instala todas as dependências necessárias dentro da pasta /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# manda tudo para o container
COPY . .

# coloca o back na porta 5000 do container
EXPOSE 5000

# executa a api
CMD ["python", "api.py"]
