from kubernetes import client, config

def launch_deployment(deployment: client.V1Deployment, namespace="default"):
    api = client.AppsV1Api()

    print(f"Creating Deployment {name}.")
    try:
        resp = api.create_namespaced_deployment(namespace, deployment)
    except client.rest.ApiException as e:
        print(f"Deployment creation failed:\n{e}")
        return
    print(f"Deployment {name} successfully created.")
    return resp

def delete_deployment(name: str, namespace="default"):
    api = client.AppsV1Api()

    print(f"Deleting Deployment {name}.")
    try:
        resp = api.delete_namespaced_deployment(name, namespace)
    except client.rest.ApiException as e:
        print(f"Deployment deletion failed:\n{e}")
        return
    print(f"Deployment {name} successfully deleted.")
    return resp

def main():
    config.load_kube_config()

    launch_deployment(deployment)
    input("Press Enter to continue: ")
    delete_deployment(name)

if __name__ == "__main__":
    main()
