import random
import sys

from paho.mqtt import client as mqtt_client

from scripts.portal_administrativo.utils.client_input import ClientInput
from scripts.portal_administrativo.utils.client_actions import ClientActions


class Client(object):

    def __init__(self, port):
        self.port = port

    def run(self):
        print("\nCliente iniciado, conectado à " + self.port + " porta")

        self.__choose_option__()


    def __operations_options__(self, opt):
        """Retorna (tipo_entidade, ClientInput, crud_option ('c', ..., 'ra')) dado opt entre [1,..., 15] do painel do Portal Administrativo"""

        tipo_entidade, input_opt = (
            ("aluno", ClientInput.pb2_aluno)
            if opt <= 5
            else (
                ("professor", ClientInput.pb2_professor)
                if opt <= 10
                else ("disciplina", ClientInput.pb2_disciplina)
            )
        )
        crud = (
            "c"
            if opt in [1, 6, 11]
            else (
                "r"
                if opt in [4, 9, 14]
                else "u" if opt in [2, 7, 12] else "d" if opt in [3, 8, 13] else "ra"
            )
        )
        return tipo_entidade, input_opt, crud

    def __choose_option__(self):
        option = 0

        while option >= 0 and option <= 16:
            print("\n ------------------------------------ ")
            print("|        PORTAL ADMINISTRATIVO         |")
            print(" -------------------------------------- ")
            print("|  1.  Inserir novo aluno              |")
            print("|  2.  Editar aluno                    |")
            print("|  3.  Remover aluno                   |")
            print("|  4.  Obter aluno                     |")
            print("|  5.  Obter todos os alunos           |")
            print("|  6.  Inserir novo professor          |")
            print("|  7.  Editar professor                |")
            print("|  8.  Remover professor               |")
            print("|  9.  Obter professor                 |")
            print("|  10. Obter todos os professores      |")
            print("|  11. Inserir nova disciplina         |")
            print("|  12. Edita disciplina                |")
            print("|  13. Remover disciplina              |")
            print("|  14. Obter disciplina                |")
            print("|  15. Obter todas as disciplinas      |")
            print("|  16. Exit                            |")
            print(" ------------------------------------- ")
            print("\nEscolha uma opção: ", end="")

            try:
                option = int(input())
            except:
                option = int(input("\nOpção inválida (escolha novamente)! "))

            if option < 1 or option > 16:
                option = int(input("\nOpção inválida (escolha novamente): "))

            if option == 16:
                print("Obrigado!")
                break

            tipo_entidade, input_opt, crud = self.__operations_options__(option)
            entidade = input_opt(crud)  # pega o input do usuário
            response = ClientActions.crud_entidade(
                tipo_entidade, crud, entidade, self.port
            )  # resolve todo o CRUDA ('ra'=A=ObtemTodos)

            print('\n')

            if response is not None:
                print(response)


if __name__ == "__main__":
    client = Client("50051" if len(sys.argv) <= 1 else sys.argv[1])
    client.run()
