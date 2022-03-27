from kubernetes import client, config

def launch_deployment(deployment:client.V1Deployment, namespace:str):
    api = client.AppsV1Api()

    name = deployment.metadata.name
    print(f"Creating Deployment {deployment.metadata.name} in namespace {namespace}")
    try:
        resp = api.create_namespaced_deployment(namespace, deployment)
        print(f"Deployment {deployment.metadata.name} successfully created.")
    except client.rest.ApiException as e:
        if e.reason == "Conflict":
            print(f"Deployment {name} already exists in namespace {namespace}")
            resp = api.read_namespaced_deployment(name, namespace)
        else:
            print(f"Deployment creation failed:\n{e}")
            return
    return resp

def delete_deployment(name:str, namespace:str):
    api = client.AppsV1Api()

    print(f"Deleting Deployment {name} from namespace {namespace}.")
    try:
        resp = api.delete_namespaced_deployment(name, namespace)
    except client.rest.ApiException as e:
        if e.reason == "Not Found":
            print(f"Deployment {name} does not exist in namespace {namespace}")
        else:
            print(f"Deployment deletion failed:\n{e}")
        return
    print(f"Deployment {name} successfully deleted.")
    return resp