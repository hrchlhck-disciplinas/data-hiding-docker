# Imagem base do Python na versão 3.10, sendo ela slim, ou seja, mais leve
FROM python:3.10-slim

# Especifica o diretório onde queremos incluir os dados
WORKDIR /app

# Instalando pacote do Python para fazer requisições HTTP
RUN pip install requests

# Adiciona o arquivo 'carrega_imagem.py' do host no diretório '/app' do container
ADD carrega_imagem.py .

# Especificando qual comando executar primeiro quando dermos 'docker run'
ENTRYPOINT ["python3", "carrega_imagem.py"]