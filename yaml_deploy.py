import io
import yaml
from os import path
from kubernetes import client, config

def open_yaml(filepath: str, filename: str):
    with open(path.join(filepath, filename)) as f:
        return yaml.safe_load(f)

def create_pv(filepath: str):
    v1 = client.CoreV1Api()
    volume = open_yaml(filepath, "volume.yaml")
    try:
        resp = v1.create_persistent_volume(volume)
    except client.rest.ApiException as e:
        print(f"Error creating PersistentVolume:\n{e}")
        return
    print(f"PersistentVolume {resp.metadata.name} created.")

def create_volume_claim(filepath: str, namespace="default"):
    v1 = client.CoreV1Api()
    volume_claim = open_yaml(filepath, "volume-claim.yaml")
    try:
        resp = v1.create_namespaced_persistent_volume_claim(namespace, volume_claim)
    except client.rest.ApiException as e:
        print(f"Error creating PersistentVolumeClaim:\n{e}")
        return
    print(f"PersistentVolumeClaim {resp.metadata.name} created.")

def create_deployment(filepath: str, namespace="default"):
    v1 = client.AppsV1Api()
    deployment = open_yaml(filepath, "deployment.yaml")
    try:
        resp = v1.create_namespaced_deployment(namespace, deployment)
    except client.rest.ApiException as e:
        print(f"Error creating Deployment:\n{e}")
        return
    print(f"Deployment {resp.metadata.name} created.")

def create_nodeport(filepath: str, namespace="default"):
    v1 = client.CoreV1Api()
    node_port = open_yaml(filepath, "nodeport.yaml")
    try:
        resp = v1.create_namespaced_service(namespace, node_port)
    except client.rest.ApiException as e:
        print(f"Error creating NodePort:\n{e}")
        return
    print(f"NodePort {resp.metadata.name} created.")

def main():
    config.load_kube_config()
    manifests = path.join(path.dirname(__file__), "manifests/minecraft/")

    create_pv(manifests)
    create_volume_claim(manifests)
    create_deployment(manifests)
    create_nodeport(manifests)

if __name__ == '__main__':
    main()
