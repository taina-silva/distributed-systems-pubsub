import scripts.portal_administrativo.protos.portal_administrativo_pb2 as pb2
import re

class ClientInput(object):
    __matricula_regex = re.compile(".+")
    __siape_regex = re.compile(".+")
    __nome_pessoa_regex = re.compile(".+")
    __sigla_disciplina_regex = re.compile(".+")
    __nome_disciplina_regex = re.compile(".+")
    __vagas_regex = re.compile(".+")
    __ct__ = {'c': 'inserido', 'r': 'lido', 'u': 'editado', 'd': 'excluído'}


    @staticmethod
    def __get_input_correto__(regex):
        dado = input('Entre com a informação: ')
        resultado = re.fullmatch(regex, dado)

        while not resultado:
            dado = input('Formato incorreto (tente novamente): ')
            resultado = re.fullmatch(regex, dado)
            
        return resultado.string


    @staticmethod
    def pb2_aluno(crud):
        if crud == 'ra':
            return
        
        print('\nMatrícula do aluno a ser ' + ClientInput.__ct__[crud] + ' : ')
        matricula = ClientInput.__get_input_correto__(ClientInput.__matricula_regex)

        if crud == 'c' or crud == 'u':
            print('\nNome do aluno a ser ' + ClientInput.__ct__[crud] + ' : ')
            nome = ClientInput.__get_input_correto__(ClientInput.__nome_pessoa_regex)

            return pb2.Aluno(matricula = matricula, nome = nome)
        
        elif crud == 'r' or crud == 'd':
            return pb2.Identificador(id = matricula)


    @staticmethod
    def pb2_professor(crud):
        if crud == 'ra':
            return
        
        print('\nSiape do professor a ser ' + ClientInput.__ct__[crud] + ' : ')
        siape = ClientInput.__get_input_correto__(ClientInput.__siape_regex)

        if crud == 'c' or crud == 'u':
            print('\nNome do professor a ser ' + ClientInput.__ct__[crud] + ' : ')
            nome = ClientInput.__get_input_correto__(ClientInput.__nome_pessoa_regex)

            return pb2.Professor(siape = siape, nome = nome)
        
        elif crud == 'r' or crud == 'd':
            return pb2.Identificador(id = siape)


    @staticmethod
    def pb2_disciplina(crud):
        if crud == 'ra':
            return

        print('\nSigla da disciplina a ser ' + ClientInput.__ct__[crud] + ' : ')
        sigla = ClientInput.__get_input_correto__(ClientInput.__sigla_disciplina_regex)

        if crud == 'c' or crud == 'u':
            print('\nNome da disciplina a ser ' + ClientInput.__ct__[crud] + ' : ')
            nome = ClientInput.__get_input_correto__(ClientInput.__nome_disciplina_regex)

            print('\nNúmero de vagas para a disciplina: ')
            vagas = int(ClientInput.__get_input_correto__(ClientInput.__vagas_regex))

            return pb2.Disciplina(sigla = sigla, nome = nome, vagas = vagas)
        
        elif crud == 'r' or crud == 'd':
            return pb2.Identificador(id = sigla)
    
