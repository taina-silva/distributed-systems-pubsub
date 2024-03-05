import json
import copy
import scripts.portal_administrativo.protos.portal_administrativo_pb2 as pb2
import scripts.portal_administrativo.protos.portal_administrativo_pb2_grpc as pb2_grpc

class ServerActions:
    topic_alunos = 'alunos'
    topic_professores = 'professores'
    topic_disciplinas = 'disciplinas'


    @staticmethod
    def action_to_keys(action):
        ta, ca = (ServerActions.topic_alunos, 'matricula')
        tp, cp = (ServerActions.topic_professores, 'siape')
        td, cd = (ServerActions.topic_disciplinas, 'sigla')
        crd = 'id' # chave para Obtem ('r') e para Remove ('d') é id

        dict_chave, tipo_chave_entidade, crud = {
            'NovoAluno': (ta, ca, 'c'), 'ObtemAluno': (ta, crd, 'r'),
            'EditaAluno': (ta, ca, 'u'), 'RemoveAluno': (ta, crd, 'd'),
            'ObtemTodosAlunos': (ta, ca, 'ra'),

            'NovoProfessor': (tp, cp, 'c'), 'ObtemProfessor': (tp, crd, 'r'),
            'EditaProfessor': (tp, cp, 'u'), 'RemoveProfessor': (tp, crd, 'd'),
            'ObtemTodosProfessores': (tp, cp, 'ra'),

            'NovaDisciplina': (td, cd, 'c'), 'ObtemDisciplina': (td, crd, 'r'),
            'EditaDisciplina': (td, cd, 'u'), 'RemoveDisciplina': (td, crd, 'd'),
            'ObtemTodasDisciplinas': (td, cd, 'ra')       
        }[action]

        return dict_chave, tipo_chave_entidade, crud


    @staticmethod
    # recebe value como str e retorna dict (quando retorna algo)
    def crud_server(server_dict, dict_chave, tipo_chave_entidade, value, crud):

        # exemplo o dicionario dos 'alunos'
        dicionario_dados = server_dict[dict_chave]

        if crud == 'c':
            # exemplo '{'matricula': 123, 'nome': 'teste'}'
            entidade_dict = eval(value)
            # exemplo '123'
            entidade_id = str(entidade_dict[tipo_chave_entidade])
            entidade_dict.pop(tipo_chave_entidade)
            # vai colocar {'123': {'nome': 'teste'}}
            dicionario_dados[entidade_id] = entidade_dict

            return value
        
        if crud == 'u':
            # exemplo '{'matricula': 123, 'nome': 'teste'}'
            entidade_dict = eval(value)
            # exemplo '123'
            entidade_id = str(entidade_dict[tipo_chave_entidade])

            try:
                dicionario_dados.pop(entidade_id)
                dicionario_dados[entidade_id] = entidade_dict

                return value
            except:
                return None


        # no caso do 'r', value é pb2.Identificador como str (exemplo '{'id': '123'}')
        elif crud == 'r':
            try:
                # exemplo '{'matricula': 123, 'nome': 'teste'}'
                chave = eval(value)[tipo_chave_entidade]
                entidade_dict = copy.deepcopy(dicionario_dados[chave])
                entidade_dict[tipo_chave_entidade] = chave

                return entidade_dict
            except:
                return None

        # no caso do 'd', value é pb2.Identificador como str (exemplo '{'id': '123'}')
        elif crud == 'd':
            try: 
                chave = eval(value)[tipo_chave_entidade]
                entidade_dict = dicionario_dados.pop(chave)
                entidade_dict[tipo_chave_entidade] = chave

                return entidade_dict
            except:
                return None            

        # no caso do 'ra', precisa criar o value dado chave no dict do server
        elif crud == 'ra':
            # exemplo todas as 'matricula'
            todas_entidades = []
            for chave in dicionario_dados.keys():
                # criou exemplo '{'id': '123'}'
                value = str(ServerActions.__dict_from_entidade(chave,  'id'))

                todas_entidades.append(ServerActions.crud_server(server_dict, dict_chave, tipo_chave_entidade, value, 'r'))

            return iter(todas_entidades)


    # exemplo ({'matricula': '123', 'nome': 'teste'}, x, 'alunos', 'NovoAluno', f)
    # porém, recebe essa entidade como .proto
    @staticmethod
    def NovaEntidade(entidade, server_dict, topic, action, publish):
        # exemplo ('alunos', 'matricula', 'c' <-- necessariamente 'c')
        dict_chave, tipo_chave_entidade, crud = ServerActions.action_to_keys(action)

        value = str(ServerActions.__dict_from_entidade(entidade, dict_chave))

        entidade_dict = ServerActions.crud_server(server_dict, dict_chave, tipo_chave_entidade, value, crud)
        entidade_str = str(entidade_dict)        

        status = publish(topic, f"{action}-{entidade_str}")

        if status != 0:
            return pb2.Status(status = status, msg = f"Falha ao publicar '{action}-{entidade_str}' em '{topic}'.") 
        else:
            return pb2.Status(status = status, msg = f"Mensagem '{action}-{entidade_str}' publicada em '{topic}' com sucesso") 


    @staticmethod
    def EditaEntidade(entidade, server_dict, topic, action, publish):
        # exemplo ('alunos', 'matricula', 'u' <-- necessariamente 'u')
        dict_chave, tipo_chave_entidade, crud = ServerActions.action_to_keys(action)

        entidade_dict = ServerActions.__dict_from_entidade(entidade, dict_chave)
        chave = str(entidade_dict[tipo_chave_entidade])
        value = str(entidade_dict)

        # um dict ou None
        entidade_dict = ServerActions.crud_server(server_dict, dict_chave, tipo_chave_entidade, value, crud)
        

        # não achou entidade com id, logo não editou, logo não publica nada
        if entidade_dict is None:
            return pb2.Status(status = 1, msg = f"Falha ao editar entidade de chave '{chave}': entidade não encontrada.") 
        
        # achou entidade com id, logo editou, logo deve publicar
        else:
            entidade_str = str(entidade_dict)      

            status = publish(topic, f"{action}-{entidade_str}")

            if status != 0:
                return pb2.Status(status = status, msg = f"Falha ao publicar '{action}-{entidade_str}' em '{topic}'.") 
            else:
                return pb2.Status(status = status, msg = f"Mensagem '{action}-{entidade_str}' publicada em '{topic}' com sucesso") 


    # entidade é um pb2.Identificador
    @staticmethod
    def RemoveEntidade(entidade, server_dict, topic, action, publish):
        # exemplo ('alunos', 'matricula', 'd' <-- necessariamente 'd')
        dict_chave, tipo_chave_entidade, crud = ServerActions.action_to_keys(action)

        entidade_dict = ServerActions.__dict_from_entidade(entidade, tipo_chave_entidade)
        chave = str(entidade_dict[tipo_chave_entidade])
        value = str(entidade_dict)

        # um dict ou None
        entidade_dict = ServerActions.crud_server(server_dict, dict_chave, tipo_chave_entidade, value, crud)

        # não achou entidade com id, logo não removeu, logo não publica nada
        if entidade_dict is None:
            return pb2.Status(status = 1, msg = f"Falha ao remover entidade de chave '{chave}': entidade não encontrada.") 

        # achou entidade com id, logo removeu, logo deve publicar
        else:
            entidade_str = str(entidade_dict)      

            status = publish(topic, f"{action}-{entidade_str}")

            if status != 0:
                return pb2.Status(status = status, msg = f"Falha ao publicar '{action}-{entidade_str}' em '{topic}'.") 
            else:
                return pb2.Status(status = status, msg = f"Mensagem '{action}-{entidade_str}' publicada em '{topic}' com sucesso") 


    # entidade é um pb2.Identificador
    @staticmethod
    def ObtemEntidade(entidade, server_dict, action):
        # exemplo ('alunos', 'matricula', 'r' <-- necessariamente 'r')
        dict_chave, tipo_chave_entidade, crud = ServerActions.action_to_keys(action)

        entidade_dict = ServerActions.__dict_from_entidade(entidade, tipo_chave_entidade)
        value = str(entidade_dict)

        # um dict ou None
        entidade_dict = ServerActions.crud_server(server_dict, dict_chave, tipo_chave_entidade, value, crud)

        # caso ache alguma coisa, deve criar entidade (pb2.Aluno por exemplo)
        if entidade_dict is not None:
            if dict_chave == ServerActions.topic_alunos:
                return pb2.Aluno(matricula = entidade_dict['id'], nome = entidade_dict['nome'])
            elif dict_chave == ServerActions.topic_professores:
                return pb2.Professor(siape = entidade_dict['id'], nome = entidade_dict['nome'])
            else:
                return pb2.Disciplina(sigla = entidade_dict['id'], nome = entidade_dict['nome'], vagas = entidade_dict['vagas'])



    @staticmethod
    def ObtemTodasEntidades(server_dict, action):
        # exemplo ('alunos', 'matricula', 'ra' <-- necessariamente 'r')
        dict_chave, tipo_chave_entidade, crud = ServerActions.action_to_keys(action)

        # exemplo o dicionario dos 'alunos'
        dicionario_dados = server_dict[dict_chave]

        action = 'ObtemAluno' if dict_chave == ServerActions.topic_alunos else 'ObtemProfessor' if dict_chave == ServerActions.topic_professores else 'ObtemDisciplina'

        entidades = []
        for chave in dicionario_dados.keys():
            entidades.append(ServerActions.ObtemEntidade(pb2.Identificador(id=chave), server_dict, action))

        return iter(entidades)
    
    @staticmethod
    def __dict_from_entidade(entidade, dict_chave):
        if dict_chave == ServerActions.topic_alunos:
            return {'matricula': entidade.matricula, 'nome': entidade.nome}
        elif dict_chave == ServerActions.topic_professores:
            return {'siape': entidade.siape, 'nome': entidade.nome}
        elif dict_chave == ServerActions.topic_disciplinas:
            return {'sigla': entidade.sigla, 'nome': entidade.nome, 'vagas': entidade.vagas}
        else:
            return {'id': entidade.id}