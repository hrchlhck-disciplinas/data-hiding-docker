import zipfile
import os

if __name__ == '__main__':
    FILE = os.environ.get('PASSWORD_FILE')

    if not FILE:
        print("Está faltando declarar a variável de ambiente FILE")
        exit(1)

    with zipfile.ZipFile(FILE, "r") as fp:
        fp.extractall(path=".")

    print("Dados extraídos com sucesso.")