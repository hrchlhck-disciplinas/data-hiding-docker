import zipfile
import os
import requests
import hashlib

from pathlib import Path

def baixa_imagem(url: str, caminho_senha: Path) -> None:
    # Faz requisição ao URL especificado
    r = requests.get(url)

    # Salva a imagem no disco
    with open(caminho_senha, "wb") as fp:
        fp.write(r.content)

def extrai_senha(caminho_senha: Path) -> str:
    # Mudamos a extensão do arquivo que contém a senha
    novo_nome = Path(f'/{caminho_senha.stem}.zip')
    os.rename(caminho_senha, novo_nome)

    # Extraíndo a senha da imagem
    with zipfile.ZipFile(novo_nome, "r") as fp:
        fp.extractall(path=".")

    with open("senha", "r") as fp:
        # Retornando os dados do arquivo 'senha', removendo 
        # quebras de linha com o método '.strip()' 
        # e separando usuário e senha
        return fp.read().strip().split(',')

def carrega_base_usuarios(url: str) -> dict:
    r = requests.get(url).text

    # Separando em linhas e excluindo cabeçalho
    linhas = r.split('\n')[1:]

    # Separando em listas de listas, onde o primeiro campo é o usuário
    # e o segundo é a senha
    usuarios = [x.split(',') for x in linhas]

    # Transformando pares em um dicionário
    return {usuario: senha for usuario, senha in usuarios}


if __name__ == '__main__':
    FILE = os.environ.get('PASSWORD_FILE')
    PASSWORD_URL = os.environ.get('PASSWORD_URL')
    USER_DATABASE = os.environ.get('USER_DATABASE')

    if not FILE:
        print("Está faltando declarar a variável de ambiente PASSWORD_FILE")
        exit(1)
    elif not PASSWORD_URL:
        print("Está faltando declarar a variável de ambiente PASSWORD_URL")
        exit(1)
    elif not USER_DATABASE:
        print("Está faltando declarar a variável de ambiente USER_DATABASE")
        exit(1)

    FILE = Path(FILE)

    baixa_imagem(PASSWORD_URL, FILE)
    
    user, senha = extrai_senha(FILE)
    usuarios = carrega_base_usuarios(USER_DATABASE)

    hash_username = hashlib.sha256(user.encode()).hexdigest()
    hash_password = hashlib.sha256(senha.encode()).hexdigest()

    usuario = hash_username in usuarios

    if usuario and hash_password == usuarios[hash_username]:
        print('Usuário', user, 'autenticado com sucesso!')
