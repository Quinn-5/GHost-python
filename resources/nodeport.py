from time import sleep
from kubernetes import client, config

def create_nodeport(name:str, port:int, protocol="TCP", namespace="default"):
    """
    Creates a NodePort service and applies it to the cluster

    Parameters:
        name(str): Name of nodeport. Must be the same as the deployment it exposes
        namespace(str): Namespace for the NodePort to be applied to
        port(int): Internal port that you would like to expose. External ports for access are randomized
        protocol(int): Which transport layer protocol to forward
    """
    api = client.CoreV1Api()

    spec = client.V1ServiceSpec(
        selector = {"app": name},
        ports = [client.V1ServicePort(port=port, protocol=protocol)],
        type="NodePort"
    )

    body = client.V1Service(
        api_version = "v1",
        kind = "Service",
        metadata = client.V1ObjectMeta(name = name),
        spec = spec
    )

    print(f"Creating NodePort {name} in namespace {namespace}.")
    try:
        resp = api.create_namespaced_service(namespace, body)
        print(f"NodePort {name} successfully created.")
    except client.rest.ApiException as e:
        if e.reason == "Conflict":
            print(f"Nodeport for {name} already exists in namespace {namespace}")
            resp = api.read_namespaced_service(name, namespace)
        else:
            print(f"NodePort creation failed:\n{e}")
            return

    return resp

def delete_nodeport(name:str, namespace="default"):
    """
    Deletes a namespaced NodePort service from the cluster

    Parameters:
        name(str): Name of the existing NodePort
        namespace(str): Namespace that the NodePort exists on
    """
    api = client.CoreV1Api()
    
    print(f"Deleting NodePort {name} from namespace {namespace}.")
    try:
        resp = api.delete_namespaced_service(name, namespace)
    except client.rest.ApiException as e:
        if e.reason == "Not Found":
            print(f"NodePort {name} does not exist in namespace {namespace}")
        else:
            print(f"NodePort deletion failed:\n{e}")
        return
    print(f"NodePort {name} successfully deleted.")
    return resp
    
def edit_nodeport(name:str, port:int, protocol="TCP", namespace="default"):

    api = client.CoreV1Api()

    spec = client.V1ServiceSpec(
        selector = {"app": name},
        ports = [client.V1ServicePort(node_port=port, port=port, protocol=protocol)],
        type="NodePort"
    )

    body = client.V1Service(
        api_version = "v1",
        kind = "Service",
        metadata = client.V1ObjectMeta(name = name),
        spec = spec
    )

    for _ in range(5):
        try:
            api.read_namespaced_service(name, namespace)
            break
        except client.rest.ApiException as e:
            if e.reason == "Invalid":
                sleep(.5)
            else:
                print(e)

    print(f"Patching NodePort {name} in namespace {namespace}.")
    try:
        resp = api.replace_namespaced_service(name, namespace, body)
        print(f"NodePort {name} successfully patched.")
    except client.rest.ApiException as e:
        if e.reason == "Invalid":
            print(f"Nodeport for {name} does not exist in namespace {namespace}")
        else:
            print(f"NodePort patching failed:\n{e}")
            return

    return resp

def main():
    config.load_kube_config()

    create_nodeport("dev-test", 25565)
    input("Press Enter to continue...")
    delete_nodeport("dev-test")

if __name__ == "__main__":
    main()
