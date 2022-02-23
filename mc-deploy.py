import yaml
from os import path
import io
from kubernetes import client, config

def create_pv(file: io.TextIOWrapper):
    v1 = client.CoreV1Api()
    vol = yaml.safe_load(file)
    resp = v1.create_persistent_volume(vol)
    print(f"Persistent volume created. status={resp.metadata.name}")
    

def create_volume_claim(file: io.TextIOWrapper):
    v1 = client.CoreV1Api()
    pvc = yaml.safe_load(file)
    resp = v1.create_namespaced_persistent_volume_claim("default", pvc)
    print(f"Persistent volume claim created. status={resp.metadata.name}")

def create_deployment(file: io.TextIOWrapper):
    v1 = client.AppsV1Api()
    dep = yaml.safe_load(file)
    resp = v1.create_namespaced_deployment("default", dep)
    print(f"Deployment created. status={resp.metadata.name}")

def create_nodeport(file: io.TextIOWrapper):
    v1 = client.CoreV1Api()
    np = yaml.safe_load(file)
    resp = v1.create_namespaced_service("default", np)
    print(f"NodePort created. status={resp.metadata.name}")

def main():
    config.load_kube_config()
    manifestDir = path.join(path.dirname(__file__), "manifests/minecraft/")

    # with open(path.join(manifestDir, "volume.yaml")) as file:
    #     create_pv(file)
    # with open(path.join(manifestDir, "volume-claim.yaml")) as file:
    #     create_volume_claim(file)
    with open(path.join(manifestDir, "deployment.yaml")) as file:
        create_deployment(file)
    # with open(path.join(manifestDir, "nodeport.yaml")) as file:
    #     create_nodeport(file)




if __name__ == '__main__':
    main()