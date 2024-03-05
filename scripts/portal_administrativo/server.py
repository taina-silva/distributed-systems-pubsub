import random
import logging
import sys 
import grpc

import scripts.portal_administrativo.protos.portal_administrativo_pb2 as pb2
import scripts.portal_administrativo.protos.portal_administrativo_pb2_grpc as pb2_grpc

from concurrent import futures
from paho.mqtt import client as mqtt_client
from scripts.portal_administrativo.utils.server_actions import ServerActions
from scripts.portal_administrativo.utils.server_service import ServerService

broker = 'broker.emqx.io'
port_mqtt = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'

dados = {ServerActions.topic_alunos: dict(), 
        ServerActions.topic_disciplinas: dict(),
        ServerActions.topic_professores: dict()}

def subscribe_topicos(client):
    def on_message(client, userdata, msg):
        print(f'\nMensagem recebida ({msg.payload.decode()} de tópico {msg.topic})')

        action = ((msg.payload.decode()).split("/")[1]).split("-")[0]
        
        # exemplo ('alunos', 'matricula', 'c')
        dict_chave, tipo_chave_entidade, crud = ServerActions.action_to_keys(action)

        value = ((msg.payload.decode()).split("/")[1]).split("-")[1]

        # exemplo (dados, 'alunos', 'matricula', value inclui chave (é str), 'c')
        ServerActions.crud_server(dados, dict_chave, tipo_chave_entidade, value, crud)


    client.subscribe(ServerActions.topic_alunos)
    client.subscribe(ServerActions.topic_professores)
    client.subscribe(ServerActions.topic_disciplinas)
    client.on_message = on_message

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Conectado ao MQTT Broker!')
        else:
            print('Falha ao conectar ao MQTT Broker, código de retorno %d\n', rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port_mqtt)

    return client

def start_server(port_, client):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    pb2_grpc.add_PortalAdministrativoServicer_to_server(
        ServerService.service(client, dados), server)
    
    server.add_insecure_port('[::]:' + port_)
    server.start()

    print('Portal Administrativo iniciado em porta '+ port_)

    return server

if __name__ == "__main__":
    logging.basicConfig()

    port_grpc = '50051' if len(sys.argv) <= 1 else sys.argv[1]

    client = connect_mqtt()
    server = start_server(port_grpc, client)

    client.loop_start()
    subscribe_topicos(client)

    server.wait_for_termination()