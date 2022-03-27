from kubernetes import client, config

def create_nodeport(port:int, selector:str, namespace:str, protocol="TCP"):
    """Creates a noteport 

    Parameters:
    port (int): port of the internal service
    selector (str): service to attach to
    namespace: 

    """
    api = client.CoreV1Api()
    name = selector

    spec = client.V1ServiceSpec(
        selector = {"app": selector},
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
    except client.rest.ApiException as e:
        print(f"NodePort creation failed:\n{e}")
        return
    print(f"NodePort {name} successfully created.")
    return resp

def delete_nodeport(name:str, namespace:str):
    api = client.CoreV1Api()
    
    print(f"Deleting NodePort {name} from namespace {namespace}.")
    try:
        resp = api.delete_namespaced_service(name, namespace)
    except client.rest.ApiException as e:
        print(f"NodePort deletion failed:\n{e}")
        return
    print(f"NodePort {name} successfully deleted.")
    return resp
    

def main():
    config.load_kube_config()

    create_nodeport(25565, "test", "dev")
    input("Press Enter to continue...")
    delete_nodeport("test", "dev")

if __name__ == "__main__":
    main()
