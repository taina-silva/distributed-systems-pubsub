import random
import sys

from paho.mqtt import client as mqtt_client

from scripts.portal_matricula.utils.client_input import ClientInput
from scripts.portal_matricula.utils.client_actions import ClientActions


class Client(object):

    def __init__(self, port):
        self.port = port

    def run(self):
        print("\nCliente iniciado, conectado à " + self.port + " prota")

        self.__choose_option__()


    def __operations_options__(self, opt):
        """Retorna (tipo_entidade, ClientInput, crud_option ('c', ..., 'ra')) dado opt entre [1,..., 15] do painel do Portal Administrativo"""

        tipo_entidade, input_opt = (
            ("disciplina_professor", ClientInput.pb2_displina_pessoa) if opt in [1, 2]
            else 
                ("disciplina_aluno", ClientInput.pb2_displina_pessoa) if opt in [3, 4]
            else
                ("identificador", ClientInput.pb2_identificador)
            
        )
        crud = (
            "add"
            if opt in [1, 3]
            else (
                "del"
                if opt in [2, 4]
                else "dd" if opt == 5 else "odp" if opt == 6 else "oda"
            )
        )
        return tipo_entidade, input_opt, crud

    def __choose_option__(self):
        option = 0

        while option >= 0 and option <= 8:
            print("\n ------------------------------------- ")
            print("|          PORTAL MATRÍCULA             |")
            print(" --------------------------------------- ")
            print("|  1.  Adicionar professor à disciplina |")
            print("|  2.  Remover professor da disciplina  |")
            print("|  3.  Adicionar aluno à disciplina     |")
            print("|  4.  Remover aluno da disciplina      |")
            print("|  5.  Detalhar disciplina              |")
            print("|  6.  Obter disciplinas de professor   |")
            print("|  7.  Obter disciplinas de aluno       |")
            print("|  8.  Exit                             |")
            print(" ------------------------------------- ")
            print("\nEscolha uma opção: ", end="")

            try:
                option = int(input())
            except:
                option = int(input("\nOpção inválida (escolha novamente): "))

            if option < 1 or option > 8:
                option = int(input("\nOpção inválida (escolha novamente): "))

            if option == 8:
                print("Obrigado!")
                break

            tipo_entidade, input_opt, crud = self.__operations_options__(option)
            entidade = input_opt(crud)  # pega o input do usuário
            response = ClientActions.crud_entidade(
                tipo_entidade, crud, entidade, self.port
            )

            print('\n')
            
            if response is not None:
                print(response)


if __name__ == "__main__":
    client = Client("50052" if len(sys.argv) <= 1 else sys.argv[1])
    client.run()
