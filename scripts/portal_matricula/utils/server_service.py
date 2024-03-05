import sys
import grpc
import scripts.portal_matricula.protos.portal_matricula_pb2_grpc as pb2_grpc

from scripts.portal_matricula.utils.server_actions import ServerActions


class ServerService(object):

    @staticmethod
    def service(client, dicts):
        def publish(topic, message):
            result = client.publish(topic, "PM/" + message)
            status = result[0]

            if status == 0:
                print(f"\nPublicada mensagem ({message}) no tópico ({topic})")

            return status

        class PortalMatricula(pb2_grpc.PortalMatricula):
            def AdicionaProfessor(self, disciplina_pessoa, _):
                return ServerActions.AdicionaPessoaEmDisciplina(
                    disciplina_pessoa, dicts, "AdicionaProfessor", publish
                )

            def RemoveProfessor(self, disciplina_pessoa, _):
                return ServerActions.RemovePessoaDeDisciplina(
                    disciplina_pessoa, dicts, "RemoveProfessor", publish
                )

            def AdicionaAluno(self, disciplina_pessoa, _):
                return ServerActions.AdicionaPessoaEmDisciplina(
                    disciplina_pessoa, dicts, "AdicionaAluno", publish
                )

            def RemoveAluno(self, disciplina_pessoa, _):
                return ServerActions.RemovePessoaDeDisciplina(
                    disciplina_pessoa, dicts, "RemoveAluno", publish
                )

            def DetalhaDisciplina(self, identificador, _):
                return ServerActions.ObtemDisciplinaDetalhada(
                    identificador, dicts, "DetalhaDisciplina", False
                )

            def ObtemDisciplinasProfessor(self, identificador, _):
                return ServerActions.ObtemDisciplinasEntidade(
                    identificador, dicts, "ObtemDisciplinasProfessor"
                )

            def ObtemDisciplinasAluno(self, identificador, _):
                return ServerActions.ObtemDisciplinasAluno(
                    identificador, dicts, "ObtemDisciplinasAluno"
                )

        return PortalMatricula()
