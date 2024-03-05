import scripts.portal_matricula.protos.portal_matricula_pb2 as pb2
import scripts.portal_administrativo.protos.portal_administrativo_pb2 as pb2_admin
import re

class ClientInput(object):
    __id_regex = re.compile(".+")
    __siape_regex = re.compile(".+")
    __matricula_regex = re.compile(".+")
    __sigla_disciplina_regex = re.compile(".+")


    @staticmethod
    def __get_input_correto__(regex):
        dado = input('Entre com a informação: ')
        resultado = re.fullmatch(regex, dado)

        while not resultado:
            dado = input('Formato incorreto (tente novamente): ')
            resultado = re.fullmatch(regex, dado)
            
        return resultado.string


    @staticmethod
    def pb2_displina_pessoa(crud):
        print('\nSigla da disciplina: ')
        sigla = ClientInput.__get_input_correto__(ClientInput.__sigla_disciplina_regex)

        print('\nMATRÍCULA do aluno ou SIAPE do professor: ')
        id = ClientInput.__get_input_correto__(ClientInput.__id_regex)

        return pb2.DisciplinaPessoa(disciplina = sigla, idPessoa = id)


    @staticmethod
    def pb2_identificador(crud):
        if crud == 'dd':
            print('\nSigla da disciplina a ser detalhada: ')
            id = ClientInput.__get_input_correto__(ClientInput.__sigla_disciplina_regex)

        if crud == 'odp':
            print('\nSiape do professor: ')
            id = ClientInput.__get_input_correto__(ClientInput.__siape_regex)

        if crud == 'oda':
            print('\nMatrícula do aluno: ')
            id = ClientInput.__get_input_correto__(ClientInput.__matricula_regex)
        
        return pb2_admin.Identificador(id = id)    
