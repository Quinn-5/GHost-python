from kubernetes import client, config

def create_nodeport(port: int, selector: str, namespace="default"):
    api = client.CoreV1Api()

    spec = client.V1ServiceSpec(
        selector = {"app": selector},
        ports = [
            client.V1ServicePort(
                port=port
            )
        ],
        type="NodePort"
    )

    body = client.V1Service(
        api_version = "v1",
        kind = "Service",
        metadata = client.V1ObjectMeta(
            name = selector
        ),
        spec = spec
    )

    resp = api.create_namespaced_service(namespace, body)

def delete_nodeport(name, namespace):
    api = client.CoreV1Api()
    resp = api.delete_namespaced_service(name, namespace)
    

def main():
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    create_nodeport(25565, "test", "dev")
    delete_nodeport("test", "dev")

if __name__ == "__main__":
    main()
