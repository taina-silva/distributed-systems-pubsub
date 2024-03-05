import sys
import grpc
import scripts.portal_administrativo.protos.portal_administrativo_pb2 as pb2
import scripts.portal_administrativo.protos.portal_administrativo_pb2_grpc as pb2_grpc
from scripts.portal_administrativo.utils.server_actions import ServerActions

class ServerService(object):

    @staticmethod
    def service(client, dicts):
        def publish(topic, message):
            result = client.publish(topic, 'PA/' + message)
            status = result[0]

            if status == 0:
                print(f'\nPublicada mensagem ({message}) no tópico ({topic})')

            return status


        class PortalAdministrativo(pb2_grpc.PortalAdministrativo):
            def NovoAluno(self, aluno, _):
                return ServerActions.NovaEntidade(aluno, dicts, ServerActions.topic_alunos, 'NovoAluno', publish)
                
            def EditaAluno(self, aluno, _):
                return ServerActions.EditaEntidade(aluno, dicts, ServerActions.topic_alunos, 'EditaAluno', publish)
                
            def RemoveAluno(self, identificador, _):
                return ServerActions.RemoveEntidade(identificador, dicts, ServerActions.topic_alunos, 'RemoveAluno', publish)

            def ObtemAluno(self, identificador, _):
                return ServerActions.ObtemEntidade(identificador, dicts, 'ObtemAluno')
            
            def ObtemTodosAlunos(self, _, __):
                return ServerActions.ObtemTodasEntidades(dicts, 'ObtemTodosAlunos')

            # --------------------------------------------------------------

            def NovoProfessor(self, professor, _):
                return ServerActions.NovaEntidade(professor, dicts, ServerActions.topic_professores, 'NovoProfessor', publish)
                
            def EditaProfessor(self, professor, _):
                return ServerActions.EditaEntidade(professor, dicts, ServerActions.topic_professores, 'EditaProfessor', publish)
                
            def RemoveProfessor(self, identificador, _):
                return ServerActions.RemoveEntidade(identificador, dicts, ServerActions.topic_professores, 'RemoveProfessor', publish)

            def ObtemProfessor(self, identificador, _):
                return ServerActions.ObtemEntidade(identificador, dicts, 'ObtemProfessor')
            
            def ObtemTodosProfessores(self, _, __):
                return ServerActions.ObtemTodasEntidades(dicts, 'ObtemTodosProfessores')

            # --------------------------------------------------------------

            def NovaDisciplina(self, disciplina, _):
                return ServerActions.NovaEntidade(disciplina, dicts, ServerActions.topic_disciplinas, 'NovaDisciplina', publish)
                
            def EditaDisciplina(self, disciplina, _):
                return ServerActions.EditaEntidade(disciplina, dicts, ServerActions.topic_disciplinas, 'EditaDisciplina', publish)
                
            def RemoveDisciplina(self, identificador, _):
                return ServerActions.RemoveEntidade(identificador, dicts, ServerActions.topic_disciplinas, 'RemoveDisciplina', publish)

            def ObtemDisciplina(self, identificador, _):
                return ServerActions.ObtemEntidade(identificador, dicts, 'ObtemDisciplina')

            def ObtemTodasDisciplinas(self, _, __):
                return ServerActions.ObtemTodasEntidades(dicts, 'ObtemTodasDisciplinas')
            
        return PortalAdministrativo()
        
    