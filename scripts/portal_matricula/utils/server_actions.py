import json
import copy
import scripts.portal_administrativo.protos.portal_administrativo_pb2 as pb2_admin
import scripts.portal_matricula.protos.portal_matricula_pb2 as pb2
import scripts.portal_matricula.protos.portal_matricula_pb2_grpc as pb2_grpc

from scripts.portal_administrativo.utils.server_actions import (
    ServerActions as admininistrativo_server_actions,
)


class ServerActions:
    topic_alunos = "alunos"
    topic_professores = "professores"
    topic_disciplinas = "disciplinas"
    topic_disciplinas_alunos = "disciplinas_alunos"
    topic_disciplinas_professor = "disciplinas_professor"

    @staticmethod
    def action_to_keys(action):
        trp, cp1, cp2, cp3, cp4 = (
            [
                ServerActions.topic_disciplinas_professor,
                ServerActions.topic_disciplinas,
                ServerActions.topic_professores,
            ],
            "disciplina",
            "idPessoa",
            "sigla",
            "siape",
        )
        tra, ca1, ca2, ca3, ca4 = (
            [
                ServerActions.topic_disciplinas_alunos,
                ServerActions.topic_disciplinas,
                ServerActions.topic_alunos,
            ],
            "disciplina",
            "idPessoa",
            "sigla",
            "matricula",
        )
        trr, tr1, tr2, tr3, tr4 = (
            [
                ServerActions.topic_disciplinas_professor,
                ServerActions.topic_disciplinas_alunos,
                ServerActions.topic_disciplinas,
                ServerActions.topic_professores,
                ServerActions.topic_alunos,
            ],
            "sigla",
            "siape",
            "matricula",
            "",
        )

        dict_chaves, tipo_chave_1, tipo_chave_2, tipo_chave_3, tipo_chave_4, crud = {
            "AdicionaProfessor": (trp, cp1, cp2, cp3, cp4, "add"),
            "RemoveProfessor": (trp, cp1, cp2, cp3, cp4, "del"),
            "AdicionaAluno": (tra, ca1, ca2, ca3, ca4, "add"),
            "RemoveAluno": (tra, ca1, ca2, ca3, ca4, "del"),
            "DetalhaDisciplina": (trr, tr1, tr2, tr3, tr4, "dd"),
            "ObtemDisciplinasProfessor": (trr, tr1, tr2, tr3, tr4, "odp"),
            "ObtemDisciplinasAluno": (trr, tr1, tr2, tr3, tr4, "oda"),
        }[action]

        return dict_chaves, tipo_chave_1, tipo_chave_2, tipo_chave_3, tipo_chave_4, crud

    @staticmethod
    # recebe value como str e retorna dict (quando retorna algo)
    def crud_server(
        server_dict,
        dict_chaves,
        tipo_chave_entidade_1,
        tipo_chave_entidade_2,
        tipo_chave_entidade_3,
        tipo_chave_entidade_4,
        value,
        crud,
    ):
        # exemplo: AdicionaProfessorDisciplina
        # recebe como str: '{'disciplina': gbc, 'idPessoa': '123'}'

        if crud == "add":
            dicionario_relacao = server_dict[dict_chaves[0]]  # disciplinas_professor
            dicionario_entidade_1 = server_dict[dict_chaves[1]]  # disciplinas
            dicionario_entidade_2 = server_dict[dict_chaves[2]]  # professores

            # exemplo '{'disciplina': gbc, 'idPessoa': '123'}'
            entidade_dict = eval(value)

            try:
                # '{'gbc': {'nome': 'gbc', 'vagas': 12}}'
                entidade_1_dict = dicionario_entidade_1[
                    entidade_dict[tipo_chave_entidade_1]
                ]
                # '{'123': {'nome': 'paulo'}}'
                entidade_2_dict = dicionario_entidade_2[
                    entidade_dict[tipo_chave_entidade_2]
                ]

                # 'gbc'
                value_1 = entidade_dict[tipo_chave_entidade_1]
                # '123'
                value_2 = entidade_dict[tipo_chave_entidade_2]

                if dict_chaves[2] == ServerActions.topic_professores:
                    # '{'gbc': '123'}'
                    dicionario_relacao[value_1] = value_2
                else:
                    # caso AdicionaAlunoDisciplina
                    try:
                        aux = dicionario_relacao[value_1]

                        if not value_2 in aux:
                            aux.append(value_2)
                            dicionario_relacao[value_1] = aux
                    except:
                        dicionario_relacao[value_1] = [value_2]

                entidade_1_dict = copy.deepcopy(entidade_1_dict)
                # '{'sigla': 'gbc', 'nome': 'gbc', 'vagas': 12}'
                entidade_1_dict[tipo_chave_entidade_3] = value_1

                entidade_2_dict = copy.deepcopy(entidade_2_dict)
                # '{'siape': '123', 'nome': 'paulo'}'
                entidade_2_dict[tipo_chave_entidade_4] = value_2

                return (entidade_1_dict, entidade_2_dict)
            except:
                return None

        elif crud == "del":
            # exemplo: RemoveProfessorDisciplina
            # recebe como str: '{'disciplina': gbc, 'idPessoa': '123'}'

            dicionario_relacao = server_dict[dict_chaves[0]]  # disciplinas_professor
            dicionario_entidade_1 = server_dict[dict_chaves[1]]  # disciplinas
            dicionario_entidade_2 = server_dict[dict_chaves[2]]  # professores

            # exemplo '{'disciplina': gbc, 'idPessoa': '123'}'
            entidade_dict = eval(value)
            
            try:
                entidade_1_dict = dicionario_entidade_1[
                    entidade_dict[tipo_chave_entidade_1]
                ]
                entidade_2_dict = dicionario_entidade_2[
                    entidade_dict[tipo_chave_entidade_2]
                ]

                value_1 = entidade_dict[tipo_chave_entidade_1]
                value_2 = entidade_dict[tipo_chave_entidade_2]

                if dicionario_entidade_2 == ServerActions.topic_professores:
                    # '{'gbc': '123'}'
                    dicionario_relacao[value_1] = None
                else:
                    # caso RemoveAlunoDisciplina
                    try:
                        aux = dicionario_relacao[value_1]

                        if value_2 in aux:
                            aux.remove(value_2)
                            dicionario_relacao[value_1] = aux
                        else:
                            return None
                    except:
                        return None

                entidade_1_dict = copy.deepcopy(entidade_1_dict)
                # '{'sigla': 'gbc', 'nome': 'gbc', 'vagas': 12}'
                entidade_1_dict[tipo_chave_entidade_1] = value_1

                entidade_2_dict = copy.deepcopy(entidade_2_dict)
                # '{'siape': '123', 'nome': 'paulo'}'
                entidade_2_dict[tipo_chave_entidade_2] = value_2

                return (entidade_1_dict, entidade_2_dict)
            except:
                return None

        # ObtemDisciplina pb2.Identificador (referente à disciplina)
        elif crud == "dd":
            dicionario_relacao_1 = server_dict[dict_chaves[0]]  # disciplinas_professor
            dicionario_relacao_2 = server_dict[dict_chaves[1]]  # disciplinas_alunos
            dicionario_entidade_1 = server_dict[dict_chaves[2]]  # disciplinas

            # '{'id': 'gbc'}'
            entidade_dict = eval(value)

            try:
                # checar se disciplina existe (está cadastrada)
                check = dicionario_entidade_1[entidade_dict["id"]]

                # checar se disciplina existe em alguma relação
                try:
                    check = dicionario_relacao_1[entidade_dict["id"]]
                except:
                    try:
                        check = dicionario_relacao_2[entidade_dict["id"]]
                    except:
                        return 0

                # pegar disciplina pelo crud de adm '{'id': 'gbc'}'
                entidade_1_dict = copy.deepcopy(server_dict[dict_chaves[2]])
                entidade_1_dict = entidade_1_dict[entidade_dict["id"]]
                entidade_1_dict[tipo_chave_entidade_1] = entidade_dict["id"]

                if entidade_1_dict is None:
                    return None

                # pegar o id do professor atrelado à disciplina
                # '{'gbc': '123'}'

                try:
                    value_2 = dicionario_relacao_1[entidade_dict["id"]]

                    # '{'id': '123'}'
                    entidade_2_dict = copy.deepcopy(server_dict[dict_chaves[3]])
                    entidade_2_dict = entidade_2_dict[value_2]
                    entidade_2_dict[tipo_chave_entidade_2] = value_2
                except:
                    entidade_2_dict = {}

                # pegar ids dos alunos atrelados à disciplina
                # '{'gbc': ['123']}'
                try:
                    value_3 = dicionario_relacao_2[entidade_dict["id"]]

                    # '{'id': '123'}'
                    entidade_3_dict = []

                    for v in value_3:
                        aux = copy.deepcopy(server_dict[dict_chaves[4]])
                        aux = aux[v]
                        aux[tipo_chave_entidade_3] = v

                        if aux is not None:
                            entidade_3_dict.append(aux)
                except:
                    entidade_3_dict = []

                return {
                    "disciplina": entidade_1_dict,
                    "professor": entidade_2_dict,
                    "alunos": entidade_3_dict,
                }
            except:
                return None

    @staticmethod
    def AdicionaPessoaEmDisciplina(entidade, server_dict, action, publish):
        dict_chaves, tipo_chave_1, tipo_chave_2, tipo_chave_3, tipo_chave_4, crud = (
            ServerActions.action_to_keys(action)
        )

        # '{'disciplina': gbc, 'idPessoa': '123'}'
        value_dict = ServerActions.__dict_from_entidade(entidade, dict_chaves[0])
        value_str = str(value_dict)

        if dict_chaves[2] == ServerActions.topic_alunos:
            disciplina = ServerActions.ObtemDisciplinaDetalhada(
                pb2_admin.Identificador(id=value_dict["disciplina"]),
                server_dict,
                "DetalhaDisciplina",
                True,
            )

            if disciplina != 0 and disciplina.disciplina.vagas == len(
                disciplina.alunos
            ):
                return pb2_admin.Status(
                    status=1,
                    msg=f"Falha ao adicionar entidade de chave '{value_dict['idPessoa']}' na disciplina de chave '{value_dict['disciplina']}'. Disciplina inexistente ou lotada.",
                )

        result = ServerActions.crud_server(
            server_dict,
            dict_chaves,
            tipo_chave_1,
            tipo_chave_2,
            tipo_chave_3,
            tipo_chave_4,
            value_str,
            crud,
        )

        if result is None:
            return pb2_admin.Status(
                status=1,
                msg=f"Falha ao adicionar entidade de chave '{value_dict['idPessoa']}' na disciplina de chave '{value_dict['disciplina']}'.",
            )

        topic = (
            ServerActions.topic_disciplinas_professor
            if dict_chaves[2] == ServerActions.topic_professores
            else ServerActions.topic_disciplinas_alunos
        )

        status = publish(topic, f"{action}-{value_str}")

        if status != 0:
            return pb2_admin.Status(
                status=status,
                msg=f"Falha ao publicar '{action}-{value_str}' em '{topic}'.",
            )
        else:
            return pb2_admin.Status(
                status=status,
                msg=f"Mensagem '{action}-{value_str}' publicada em '{topic}' com sucesso",
            )

    @staticmethod
    def RemovePessoaDeDisciplina(entidade, server_dict, action, publish):
        dict_chaves, tipo_chave_1, tipo_chave_2, _, _, crud = (
            ServerActions.action_to_keys(action)
        )

        # '{'disciplina': gbc, 'idPessoa': '123'}'
        value_dict = ServerActions.__dict_from_entidade(entidade, dict_chaves[0])
        value_str = str(value_dict)

        result = ServerActions.crud_server(
            server_dict, dict_chaves, tipo_chave_1, tipo_chave_2, _, _, value_str, crud
        )

        if result is None:
            return pb2_admin.Status(
                status=1,
                msg=f"Falha ao remover entidade de chave '{value_dict['idPessoa']}' na disciplina de chave '{value_dict['disciplina']}'.",
            )

        topic = (
            ServerActions.topic_disciplinas_professor
            if dict_chaves[2] == ServerActions.topic_professores
            else ServerActions.topic_disciplinas_alunos
        )

        status = publish(topic, f"{action}-{value_str}")

        if status != 0:
            return pb2_admin.Status(
                status=status,
                msg=f"Falha ao publicar '{action}-{value_str}' em '{topic}'.",
            )
        else:
            return pb2_admin.Status(
                status=status,
                msg=f"Mensagem '{action}-{value_str}' publicada em '{topic}' com sucesso",
            )

    @staticmethod
    def ObtemDisciplinaDetalhada(entidade, server_dict, action, from_add):
        dict_chaves, tipo_chave_1, tipo_chave_2, tipo_chave_3, _, crud = (
            ServerActions.action_to_keys(action)
        )

        # '{'id': 'gbc'}'
        value_dict = ServerActions.__dict_from_entidade(entidade, dict_chaves[2])
        value_str = str(value_dict)

        result = ServerActions.crud_server(
            server_dict,
            dict_chaves,
            tipo_chave_1,
            tipo_chave_2,
            tipo_chave_3,
            _,
            value_str,
            crud,
        )

        if from_add == True and result == 0:
            return 0

        if result != 0:
            return pb2.RelatorioDisciplina(
                disciplina=result["disciplina"],
                professor=result["professor"],
                alunos=result["alunos"],
            )

    @staticmethod
    def ObtemDisciplinasEntidade(entidade, server_dict, action):
        dict_chaves, tipo_chave_1, tipo_chave_2, tripo_chave_3, _, crud = (
            ServerActions.action_to_keys(action)
        )

        # '{'id': '123'}'
        value_dict = ServerActions.__dict_from_entidade(entidade, dict_chaves[2])
        prof_entidade = action == "ObtemDisciplinasProfessor"
        disciplinas_dict = server_dict[
            (
                ServerActions.topic_disciplinas_professor
                if prof_entidade == True
                else ServerActions.topic_disciplinas_alunos
            )
        ]
        if prof_entidade == True:
            todas_disciplinas_dict = dict(
                (k, v) for (k, v) in disciplinas_dict.items() if v == value_dict["id"]
            )
        else:
            todas_disciplinas_dict = dict(
                (k, v) for (k, v) in disciplinas_dict.items() if value_dict["id"] in v
            )

        disciplinas_list = []

        for key, value in todas_disciplinas_dict.items():
            result = ServerActions.crud_server(
                server_dict,
                dict_chaves,
                tipo_chave_1,
                tipo_chave_2,
                tripo_chave_3,
                _,
                str({"id": key}),
                "dd",
            )

            if result is not None:
                disciplinas_list.append(
                    pb2.RelatorioDisciplina(
                        disciplina=result["disciplina"],
                        professor=result["professor"],
                        alunos=result["alunos"],
                    )
                )

        return iter(disciplinas_list)

    @staticmethod
    def ObtemDisciplinasAluno(entidade, server_dict, action):
        result = ServerActions.ObtemDisciplinasEntidade(entidade, server_dict, action)

        return iter(
            map(
                lambda e: pb2.ResumoDisciplina(
                    disciplina=e.disciplina,
                    professor=e.professor,
                    totalAlunos=len(e.alunos),
                ),
                result,
            )
        )

    @staticmethod
    def __dict_from_entidade(entidade, dict_chave):
        if dict_chave in [
            ServerActions.topic_disciplinas_professor,
            ServerActions.topic_disciplinas_alunos,
        ]:
            return {"disciplina": entidade.disciplina, "idPessoa": entidade.idPessoa}
        else:
            return {"id": entidade.id}
