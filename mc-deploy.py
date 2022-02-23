import io
import yaml
from os import path
from kubernetes import client, config

def create_pv(file: io.TextIOWrapper):
    v1 = client.CoreV1Api()
    vol = yaml.safe_load(file)
    try:
        resp = v1.create_persistent_volume(vol)
    except client.rest.ApiException as e:
        print(f"Error creating PersistentVolume:\n{e}")
        return
    print(f"PersistentVolume {resp.metadata.name} created.")
    
def create_volume_claim(file: io.TextIOWrapper, namespace="default"):
    v1 = client.CoreV1Api()
    pvc = yaml.safe_load(file)
    try:
        resp = v1.create_namespaced_persistent_volume_claim(namespace, pvc)
    except client.rest.ApiException as e:
        print(f"Error creating PersistentVolumeClaim:\n{e}")
        return
    print(f"PersistentVolumeClaim created. status={resp.metadata.name}")

def create_deployment(file: io.TextIOWrapper, namespace="default"):
    v1 = client.AppsV1Api()
    dep = yaml.safe_load(file)
    try:
        resp = v1.create_namespaced_deployment(namespace, dep)
    except client.rest.ApiException as e:
        print(f"Error creating Deployment:\n{e}")
        return
    print(f"Deployment created. status={resp.metadata.name}")

def create_nodeport(file: io.TextIOWrapper, namespace="default"):
    v1 = client.CoreV1Api()
    NodePort = yaml.safe_load(file)
    try:
        resp = v1.create_namespaced_service(namespace, NodePort)
    except client.rest.ApiException as e:
        print(f"Error creating NodePort:\n{e}")
        return
    print(f"NodePort created. status={resp.metadata.name}")

def main():
    config.load_kube_config()
    manifestDir = path.join(path.dirname(__file__), "manifests/minecraft/")

    with open(path.join(manifestDir, "volume.yaml")) as file:
        create_pv(file)
    with open(path.join(manifestDir, "volume-claim.yaml")) as file:
        create_volume_claim(file)
    with open(path.join(manifestDir, "deployment.yaml")) as file:
        create_deployment(file)
    with open(path.join(manifestDir, "nodeport.yaml")) as file:
        create_nodeport(file)

if __name__ == '__main__':
    main()
