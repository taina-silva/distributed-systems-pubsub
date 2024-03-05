import sys
import grpc
import scripts.portal_matricula.protos.portal_matricula_pb2_grpc as pb2_grpc

class ClientActions:

    @staticmethod
    def __crud_entidade_metodo__(tipo_entidade, crud, channel):
        return {'disciplina_professor': {'add': pb2_grpc.PortalMatriculaStub(channel).AdicionaProfessor,
                                    'del': pb2_grpc.PortalMatriculaStub(channel).RemoveProfessor,
                                },
                'disciplina_aluno': {'add': pb2_grpc.PortalMatriculaStub(channel).AdicionaAluno,
                                    'del': pb2_grpc.PortalMatriculaStub(channel).RemoveAluno,
                                },
                'identificador': {'dd': pb2_grpc.PortalMatriculaStub(channel).DetalhaDisciplina,
                          'odp': pb2_grpc.PortalMatriculaStub(channel).ObtemDisciplinasProfessor,
                          'oda': pb2_grpc.PortalMatriculaStub(channel).ObtemDisciplinasAluno,
                         }
            }[tipo_entidade][crud]

    @staticmethod
    def crud_entidade(tipo_entidade, crud, entidade, port):
        try:
            channel = grpc.insecure_channel('localhost:' + str(port))

            crud_metodo = ClientActions.__crud_entidade_metodo__(tipo_entidade, crud, channel)
            resposta = crud_metodo(entidade)

            return resposta if crud in ['add', 'del', 'dd'] else list(resposta)
        
        except Exception as erro:
            info = {'add': 'adicionar ',
                    'del': 'remover ',
                    'dd': 'detalhar disciplina ',
                    'odp': 'obter disciplinas professor ',
                    'oda': 'obter disciplinas aluno '
                   }
            
            if crud == 'dd':
                print('\nDisciplina inexistente.')
            elif crud == 'odp':
                 print('\nProfessor inexistente.')
            elif crud == 'oda':
                 print('\nAluno inexistente.')
            else:
                print(f'\nOcorreu um erro ao ' + info[crud] + tipo_entidade + ': ' + str(erro))

            return None
        