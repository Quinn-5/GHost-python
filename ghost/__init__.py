from flask import Flask, redirect, render_template, request, url_for
from kubernetes import config, client
import deployments

from resources import deployment

app = Flask(__name__)
config.load_kube_config()
host = client.Configuration.get_default_copy().host.strip("https://").split(":")[0]

@app.route('/', methods=['POST', 'GET'])      
def root():
    if request.method == 'POST':
        name=request.form['name']
        action=request.form['action']
        type=request.form['type']
    else:
        name=request.args.get('name')
        action=request.args.get('action')
        type=request.args.get('type')

    match type:
        case "csgo":
            fn = deployments.csgo
        case "factorio":
            fn = deployments.factorio
        case "minecraft":
            fn = deployments.minecraft
        case "terraria":
            fn = deployments.terraria
        case "tf2":
            fn = deployments.tf2
        case _:
            return render_template('index.html')
    
    match action:
        case "create":
            port = fn.deploy(name, "dev")
            return render_template('created.html', host=host, port=port)
        case "delete":
            fn.delete(name, "dev")
            return render_template('deleted.html', name=name)
    
    return render_template('index.html')

@app.route('/created')
def created():
    port=request.form['port']
    return render_template('created.html',host=host, port=port)

@app.route('/deleted')
def deleted():
    name=request.form['name']
    return render_template('created.html', name=name)

if __name__=='__main__':
   app.run()