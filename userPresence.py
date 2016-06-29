#!/usr/bin/env python
# coding: utf-8
import urllib2
import json
from datetime import datetime
from time import time, sleep 

# Token de autorização oAuth para acessar a API. Pode ser gerado um token de teste
# (O Token refere a um time especifico)
# Link para obter o token: https://api.slack.com/docs/oauth-test-tokens
SLACK_TOKEN=""
# URI do Recurso de recuperar a lista de usuarios
URL="https://slack.com/api/users.list?token="+SLACK_TOKEN+"&presence=1"
# Lista de nomes de usuario que deseja analisar a presenca.
MONITORES = ['luciannojunior', 'ericbreno', 'matheusgr']
# Intervalo em segundos para realizar a requisicao
INTERVALO = 5

# Funcao que filtra os membros. Alterações de critério devem ser feitas aqui
def filtro(membros, lista):
    for i in membros:
        if "presence" not in i or i["presence"] != "active" or i["name"] not in MONITORES:
            continue
        lista.append(i["name"])
# Loga um erro em arquivo
def log_error(erro):
    erros = open("erros.birl", "a+")
    erros.write("\n"+erro)
    erros.close()

while True:
    try:
        # Pega o timestamp atual no formato mm/dd/aaaa-hh:mm:ss
        tempo = datetime.fromtimestamp(time()).strftime("%m/%d/%Y-%H:%M:%S")
        usuarios_online = []
        # Realiza a requisicao à API do Slack
        response = urllib2.urlopen(URL)
        # Faz o parser do json recebido para python dicionario
        data = json.load(response)
        # Verifica se a requisicao ocorreu com sucesso
        if not data["ok"]:
            log_error(data["error"])
            continue
        # Popula usuarios_online com criterios especificados
        filtro(data["members"], usuarios_online)
        # Salva os dados
        log = open("log.json", "a+")
        dados = json.load(log)
        dados[tempo] = usuarios_online
        log.close()
        log = open("log.json", "w+")
        json.dump(dados, log)
        log.close()
        response.close()
        sleep(INTERVALO)
    except Exception as ex:
        log_error(str(ex.args))
