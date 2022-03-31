from kubernetes import client, config

def create_claim(name:str, namespace:str, size:str, storage_class=None):
    """
    Creates a PersistentVolumeClaim and applies it to the cluster

    Parameters:
        name(str): Name of PerisitentVolumeClaim. Must be the same as the PersistentVolume it attaches to
        namespace(str): Namespace for the PersistentVolumeClaim to be applied to
        size(str): Size of the claim in MiB
    """
    api = client.CoreV1Api()

    spec = client.V1PersistentVolumeClaimSpec(
        access_modes=["ReadWriteOnce"],
        resources=client.V1ResourceRequirements(requests={"storage":size}),
        storage_class_name=storage_class,
        volume_name=name
    )

    body = client.V1PersistentVolumeClaim(
        api_version="v1",
        metadata=client.V1ObjectMeta(name=name),
        kind="PersistentVolumeClaim",
        spec=spec
    )

    print(f"Creating PersistentVolumeClaim {name} in namespace {namespace}.")
    try:
        resp = api.create_namespaced_persistent_volume_claim(namespace, body)
    except client.rest.ApiException as e:
        if e.reason == "Conflict":
            print(f"PersistentVolumeClaim {name} already exists in namespace {namespace}")
            resp = api.read_namespaced_persistent_volume_claim(name, namespace)
        else:
            print(f"PersistentVolumeClaim creation failed:\n{e}")
            return
    return resp

def delete_claim(name:str, namespace:str):
    """
    Deletes a namespaced PersistentVolumeClaim from the cluster

    Parameters:
        name(str): Name of the existing PersistentVolumeClaim
        namespace(str): Namespace that the PersistentVolumeClaim exists on
    """
    api = client.CoreV1Api()

    print(f"Deleting PersistentVolumeClaim {name} from namespace {namespace}.")
    try:
        resp = api.delete_namespaced_persistent_volume_claim(name, namespace)
    except client.rest.ApiException as e:
        if e.reason == "Not Found":
            print(f"PersistentVolumeClaim {name} does not exist in namespace {namespace}")
        else:
            print(f"PersistentVolumeClaim deletion failed:\n{e}")
        return
    print(f"PersistentVolumeClaim {name} successfully deleted.")
    return resp

def main():
    config.load_kube_config()

    create_claim("test", "dev", "500Mi")
    input("Press Enter to continue...")
    delete_claim("test", "dev")

if __name__ == "__main__":
    main()
