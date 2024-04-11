import os
from dotenv import load_dotenv, find_dotenv
import dotenv
from src.infra.crowler.authenticator import TwitterAuthenticator


def run_menu():
    print("\n------------------------------------------\n")
    print("Não encontramos o arquivo .env")
    print("Mas ainda podemos te ajudar, escolha como:")
    print("\n------------------------------------------\n")
    print(
        "1. Criar aquivo template.\n--- Você deverá rodar esse script novamente para criar a autenticação"
    )
    print(
        "2. Rodar o assistente de autenticação\n--- A autenticação seguirá normalmente e não salvará o aquivo .env"
    )
    print(
        "3. Rodar autenticação manual\n--- O scrip abre um navegador para que você preencha seus dados para autententicar"
    )
    print("Digite qualquer outro valor para Finalizar o script\n")

    return input("Como podemos ajudar: ")


def dot_env_template(filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("TWITTER_USER=<user>\n")
        f.write("TWITTER_EMAIL=<email>\n")
        f.write("TWITTER_PASSWORD=<senha>\n")
    print("\n------------------------------------------\n")
    print(
        "Coloque suas credenciais no aquivo .env e rode esse script novamente.\nCaso renomei o arquivo, use --envfile <filename>"
    )
    print("\n------------------------------------------\n")


def auth_helper():
    print("Insira seus dados:")
    user = input("@: ")
    email = input("email: ")
    password = input("senha: ")

    print("\n------------------------------------------\n")
    print("Vamos iniciar a autenticação, você não precisa realizar nenhuma ação")
    print("\n------------------------------------------\n")

    session = TwitterAuthenticator(email, user, password)
    state = session.autenticate(auto=True)
    print(state)


def manual_auth():
    print("\n------------------------------------------\n")
    print("Siga as etapas de autenticação")
    print("\n------------------------------------------\n")
    session = TwitterAuthenticator()
    state = session.autenticate()
    print(state)


def main(args):

    if not find_dotenv(filename=args.envfile):
        variavel = run_menu()

        if variavel == "":
            return
        elif variavel == "1":
            dot_env_template(filename=args.envfile)
            return
        elif variavel == "2":
            auth_helper()
            return
        elif variavel == "3":
            manual_auth()
            return
        else:
            print("__ EOL __")
            return

    load_dotenv()
    email = os.environ["TWITTER_EMAIL"]
    user = os.environ["TWITTER_USER"]
    password = os.environ["TWITTER_PASSWORD"]

    session = TwitterAuthenticator(email, user, password)
    state = session.autenticate(auto=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="autenticate")
    parser.add_argument(
        "--auto", help="Roda o processo automaticamente", action="store_true"
    )
    parser.add_argument("--envfile", help="arquivo .env", default=".env")
    args = parser.parse_args()

    main(args)
