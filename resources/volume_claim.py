from kubernetes import client, config

def create_claim(volume, size:str, namespace="default"):
    api = client.CoreV1Api()
    name = volume

    spec = client.V1PersistentVolumeClaimSpec(
        access_modes=["ReadWriteOnce"],
        resources=client.V1ResourceRequirements(requests={"storage":size}),
        volume_name=volume
    )

    body = client.V1PersistentVolumeClaim(
        api_version="v1",
        metadata=client.V1ObjectMeta(name=name),
        kind="PersistentVolumeClaim",
        spec=spec
    )

    print(f"Creating PersistentVolumeClaim {name}.")
    try:
        resp = api.create_namespaced_persistent_volume_claim(namespace, body)
    except client.rest.ApiException as e:
        print(f"PersistentVolumeClaim creation failed:\n{e}")
        return
    print(f"PersistentVolumeClaim {name} successfully created.")
    return resp

def delete_claim(name, namespace="default"):
    api = client.CoreV1Api()

    print(f"Deleting PersistentVolumeClaim {name}.")
    try:
        resp = api.delete_namespaced_persistent_volume_claim(name, namespace)
    except client.rest.ApiException as e:
        print(f"PersistentVolumeClaim deletion failed:\n{e}")
        return
    print(f"PersistentVolumeClaim {name} successfully deleted.")
    return resp

def main():
    config.load_kube_config()

    create_claim("test", "500Mi", "dev")
    input("Press Enter to continue...")
    delete_claim("test", "dev")

if __name__ == "__main__":
    main()
