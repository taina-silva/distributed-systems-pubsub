import sys
import grpc
import scripts.portal_administrativo.protos.portal_administrativo_pb2 as pb2
import scripts.portal_administrativo.protos.portal_administrativo_pb2_grpc as pb2_grpc

class ClientActions:

    @staticmethod
    def __crud_entidade_metodo__(tipo_entidade, crud, channel):
        return {'aluno': {'c': pb2_grpc.PortalAdministrativoStub(channel).NovoAluno,
                          'r': pb2_grpc.PortalAdministrativoStub(channel).ObtemAluno,
                          'u': pb2_grpc.PortalAdministrativoStub(channel).EditaAluno,
                          'd': pb2_grpc.PortalAdministrativoStub(channel).RemoveAluno,
                          'ra': pb2_grpc.PortalAdministrativoStub(channel).ObtemTodosAlunos
                         },
                'professor': {'c': pb2_grpc.PortalAdministrativoStub(channel).NovoProfessor,
                          'r': pb2_grpc.PortalAdministrativoStub(channel).ObtemProfessor,
                          'u': pb2_grpc.PortalAdministrativoStub(channel).EditaProfessor,
                          'd': pb2_grpc.PortalAdministrativoStub(channel).RemoveProfessor,
                          'ra': pb2_grpc.PortalAdministrativoStub(channel).ObtemTodosProfessores
                         },
             'disciplina': {'c': pb2_grpc.PortalAdministrativoStub(channel).NovaDisciplina,
                          'r': pb2_grpc.PortalAdministrativoStub(channel).ObtemDisciplina,
                          'u': pb2_grpc.PortalAdministrativoStub(channel).EditaDisciplina,
                          'd': pb2_grpc.PortalAdministrativoStub(channel).RemoveDisciplina,
                          'ra': pb2_grpc.PortalAdministrativoStub(channel).ObtemTodasDisciplinas
                         }
               }[tipo_entidade][crud]

    @staticmethod
    def crud_entidade(tipo_entidade, crud, entidade, port):
        try:
            channel = grpc.insecure_channel('localhost:' + str(port))

            crud_metodo = ClientActions.__crud_entidade_metodo__(tipo_entidade, crud, channel)
            resposta = crud_metodo(entidade) if crud != 'ra' else crud_metodo(pb2.Vazia())

            return resposta if crud != 'ra' else list(resposta)
        
        except Exception as erro:
            info = {'c': 'criar novo(a) ',
                          'r': 'obter ',
                          'u': 'editar ',
                          'd': 'remover ',
                          'ra': 'obter todos(as) '
                   }
            
            if crud in ['r', 'ra']:
                print('\nEntidade inexistente.')
            else:
                print(f'\nOcorreu um erro ao ' + info[crud] + tipo_entidade + ': ' + str(erro))

            return None
        
    