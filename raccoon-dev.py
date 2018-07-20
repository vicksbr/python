# Processo Seletivo Raccoon (dev)
# Author: Pedro Puzzi

from datetime import datetime
from collections import OrderedDict
import datetime
import requests
import json
import statistics
import os.path
import time 

#Funções de calculo e desvio padrão nativos do python3

def std_dev(array,mean): 
    if len(array) != 0:
        return statistics.pstdev(array,mean)
    else:
        return 0

def mean(array): 
    if len(array) != 0:
        return statistics.mean(array)
    else:
        return 0

#Função executor(): basicamente cria as variaveis necessárias e entra num loop(infinito) onde chama a função
#get_api_response a cada 1 minuto atualizando os valores de todas as métricas 

def executor():     
    dict_error_critical = {}
    g_num_total = 0 #var para debug
    array_req = []
    traceback = []    
    traceback_project = []    
    mean_request = 0 
    std_dev_request = 0
    while(True):                
        dict_error_critical,g_num_total,array_req,traceback,mean_request,std_dev_request,traceback_project = get_api_response(dict_error_critical,g_num_total,array_req,traceback,mean_request,std_dev_request,traceback_project)
        print_info(dict_error_critical,g_num_total,mean_request,std_dev_request,traceback,traceback_project)    
        time.sleep(60)
        
    
#Função get_request_json(): retorna o json dado a url e o token de autorização

def get_request_json(url,token):
    return requests.get(url, headers={'Authorization': token})


#Função get_api_response(): 
#Função que calcula e popula as variaveis necessárias e as retorna para a função executor()  
#Como não ficou bem definido como seria a saída do programa, considerei que o agrupamento por horas 
#ficaria por conta do timestamp dos logs. Achei essa ideia válida pois ai teriamos uma métrica
#que representaria em quais intervalos do dia (independente da data completa) acontecem os 
#ERROR e CRITICALS, e isso seria uma estatística interessante e cumpria o que foi pedido no documento de requisito

#Não foi pedido também a quem cada traceback pertence, mas como ficaria sem sentido pois não seria
#possível identificar de quem seria o traceback, fiz uma outra lista pareada (traceback,traceback_project) 
#para retornar o traceback e o respectivo nome do projeto 

def get_api_response(dict_error_critical,g_num_total,array_req,traceback,mean_request,std_dev_request,traceback_project):
    
    num_req = 0     #variaveis num_req e num_total p/ debug
    num_total = 0    
    url = "https://psel-logs.raccoon.ag/api/v2/logs"    
    token = "31cd410e1ebd46448ec93dea05b6a61f"
    r = get_request_json(url,token)
    json_data = json.loads(r.text)         
    for resp in json_data:
        num_total += 1
        project = resp['project']
        if 'request_duration' in resp:
            req_duration = resp["request_duration"]
            array_req.append(req_duration)            
            num_req += 1    
        if 'timestamp' in resp:
            timestamp = resp["timestamp"]
            hour = datetime.datetime.fromtimestamp(int(timestamp/1000)).strftime('%Y-%m-%d %H:%M:%S').split()[1].split(':')[0]
        if 'level' in resp:              
            error_type = resp["level"]
            if project not in dict_error_critical:                                                                                                    
                    dict_error_critical[project] = {}
            if hour not in dict_error_critical[project]:
                    dict_error_critical[project][hour] = {'error':0, 'critical':0}
            if error_type == "ERROR":
                last_value = dict_error_critical[project][hour]['error']
                dict_error_critical[project][hour]['error'] = last_value+1                    
            if error_type == "CRITICAL":
                last_value = dict_error_critical[project][hour]['critical']
                dict_error_critical[project][hour]['critical'] = last_value+1                
        if 'traceback' in resp:
            traceback.append(resp['traceback'])
            traceback_project.append(project)        
    #calculo da média e desvio padrão
    mean_request = mean(array_req)
    std_dev_request = std_dev(array_req,mean_request)        
    return dict_error_critical,g_num_total,array_req,traceback,mean_request,std_dev_request,traceback_project

#Função print_info(): Função simples que printa no stdout as métricas requisitadas 

def print_info(dict_error_critical,g_num_total,mean_request,std_dev_request,traceback,traceback_project):        
        #Pra ficar mais legivel, ficou ordenado por nomoe do projeto e hora        
        ord_list = OrderedDict(sorted(dict_error_critical.items()))
        for key, subdict in ord_list.items():
             ord_list[key] = OrderedDict(sorted(subdict.items()))
        print(json.dumps(ord_list,indent=4))
        print('\n')
        #print("num_total",g_num_total)
        print("media",mean_request)
        print("desvio padrao",std_dev_request)
        #print ("tracebacks",len(traceback))
        print("ultimos 5 tracebacks(se houverem):\n")        
        for i in range(-1,-6,-1):
            try:
                print('Projeto:',traceback_project[i])
                print(traceback[i])
                print("\n")
            except IndexError:
                continue 
        print('\n')

#main!

def main():

    print("API - Projeto Dev Raccoon")
    executor()
    
if __name__ == "__main__":
    main()

