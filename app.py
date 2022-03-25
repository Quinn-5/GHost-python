from crypt import methods
from distutils.command.config import config
from flask import Flask, redirect, render_template, request, url_for
from kubernetes import config
import deployments

from resources import deployment

app = Flask(__name__)
config.load_kube_config()

@app.route('/', methods=['POST', 'GET'])      
def root():
    if request.method == 'POST':
        name=request.form['name']
        action=request.form['action']
        type=request.form['type']

        match type:
            case "factorio":
                fn = deployments.factorio
            case "minecraft":
                fn = deployments.minecraft
            case "terraria":
                fn = deployments.terraria
            case _:
                return render_template('index.html')
        
        match action:
            case "create":
                port = fn.deploy(name, "dev")
                return redirect(url_for("created", port=port))
            case "delete":
                fn.delete(name, "dev")
                return render_template('deleted.html', name=name)

    else:
        name=request.args.get('name')
        action=request.args.get('action')
        type=request.args.get('type')
        
        match type:
            case "factorio":
                import deployments.factorio as fn
            case "minecraft":
                import deployments.minecraft as fn
            case "terraria":
                import deployments.terraria as fn
            case _:
                return render_template('index.html')
        
        match action:
            case "create":
                port = fn.deploy(name, "dev")
                return render_template('created.html', port=port)
            case "delete":
                fn.delete(name, "dev")
                return render_template('deleted.html', name=name)
    
    return render_template('index.html')

@app.route('/created')
def created():
    port=request.form['port']
    return render_template('created.html', port=port)

@app.route('/deleted')
def deleted():
    name=request.form['name']
    return render_template('created.html', name=name)

if __name__=='__main__':
   app.run()