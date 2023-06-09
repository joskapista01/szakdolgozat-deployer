from flask import Flask, request
import os

os.system("cp tcp-services.yaml.tpl tcp-services.yaml")

app = Flask(__name__)

configMapName = "tcp-services.yaml"

# Updates the tcp-configmap for the nginx-ingress controller with the new service
def UpdateConfigMap(key, value):
    f = open(configMapName, "a")
    f.write("\n  " + str(key) + ": \""+ value + "\"")
    f.close()
    os.system("kubectl apply -f " + configMapName)

# Http endpoint for creating servers
@app.post("/")
def createServer():
    if request.is_json:
        body = request.get_json()
        print(body)
        os.system('helm install minecraft-server-'+body['serverId']+' ./charts/minecraft-server -n servers --set replicaCount=1,fullnameOverride=minecraft-server-'+body['serverId'] )
        UpdateConfigMap(body['publicPort'], ('servers/minecraft-server-'+body['serverId']+':25565'))
        return {"msg": "success"}
    else:
        return {"error": "Request must be json!"}

# Http endpoint for stopping/restarting servers
@app.put("/")
def updateServer():
    if request.is_json:
        body = request.get_json()
        os.system('helm upgrade minecraft-server-'+body['serverId']+' ./charts/minecraft-server -n servers --set replicaCount='+str(body['replicaCount']) )
        
        return {"msg": "success"}
    else:
        return {"error": "Request must be json!"}

# Http endpoint for deleting server
@app.delete("/")
def deleteServer():
    if request.is_json:
        body = request.get_json()
        os.system('helm uninstall minecraft-server-'+body['serverId']+' -n servers')
        return {"msg": "success"}
    else:
        return {"error": "Request must be json!"}