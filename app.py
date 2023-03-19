from flask import Flask, request
import os

os.system("cp tcp-services.yaml.tpl tcp-services.yaml")

app = Flask(__name__)

configMapName = "tcp-services.yaml"

def UpdateConfigMap(key, value):
    f = open(configMapName, "a")
    f.write("\n  " + str(key) + ": \""+ value + "\"")
    f.close()
    os.system("kubectl apply -f " + configMapName)

@app.post("/")
def createServer():
    if request.is_json:
        body = request.get_json()
        print(body)
        os.system('helm install minecraft-server-'+body['serverId']+' ./charts/minecraft-server -n servers --set replicaCount=1' )
        UpdateConfigMap(body['publicPort'], ('servers/minecraft-server-'+body['serverId']+':25565'))
        return {"msg": "success"}
    else:
        return {"error": "Request must be json!"}

@app.put("/")
def updateServer():
    if request.is_json:
        body = request.get_json()
        os.system('helm upgrade minecraft-server-'+body['serverId']+' ./charts/minecraft-server -n servers --set replicaCount='+str(body['replicaCount']) )
        
        return {"msg": "success"}
    else:
        return {"error": "Request must be json!"}

@app.delete("/")
def deleteServer():
    if request.is_json:
        body = request.get_json()
        os.system('helm uninstall minecraft-server-'+body['serverId']+' -n servers')
        return {"msg": "success"}
    else:
        return {"error": "Request must be json!"}