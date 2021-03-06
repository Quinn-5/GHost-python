from kubernetes import client, config

def create_volume(name:str, size:str, storage_class=None):
    """
    Creates a loca PersistentVolume and applies it to the cluster

    Parameters:
        name(str): Name of PersistentVolume
        namespace(str): namespace of the rest of the deployment
        size(str): Size of the volume in MiB
    """
    api = client.CoreV1Api()

    spec = client.V1PersistentVolumeSpec(
        access_modes=["ReadWriteOnce"],
        capacity={"storage":size},
        persistent_volume_reclaim_policy="Delete",
        local=client.V1LocalVolumeSource(
            path=f"/mnt/kube/{name}"
        ),
        node_affinity=client.V1VolumeNodeAffinity(
            required=client.V1NodeSelector(
                node_selector_terms=[
                    client.V1NodeSelectorTerm(
                        match_expressions=[
                            client.V1NodeSelectorRequirement(
                                key="kubernetes.io/hostname",
                                operator="In",
                                values=["amadeus"]
                            )
                        ]
                    )
                ]
            )
        ),
        storage_class_name=storage_class
    )

    body = client.V1PersistentVolume(
        api_version="v1",
        kind="PersistentVolume",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec
    )

    print(f"Creating PersistentVolume {name}.")
    try:
        resp = api.create_persistent_volume(body)
    except client.rest.ApiException as e:
        if e.reason == "Conflict":
            print(f"PersistentVolume {name} already exists")
            resp = api.read_persistent_volume(name)
        else:
            print(f"PersistentVolume creation failed:\n{e}")
            return
    return resp

def delete_volume(name:str):
    """
    Deletes a namespaced PersistentVolume from the cluster

    Parameters:
        name(str): Name of the existing PersistentVolume
    """
    api = client.CoreV1Api()

    print(f"Deleting PersistentVolume {name}.")
    try:
        resp = api.delete_persistent_volume(name)
    except client.rest.ApiException as e:
        if e.reason == "Not Found":
            print(f"PersistentVolume {name} does not exist.")
        else:
            print(f"PersistentVolume deletion failed:\n{e}")
        return
    print(f"PersistentVolume {name} successfully deleted.")
    return resp

def main():
    config.load_kube_config()

    create_volume("dev-test", "500Mi")
    input("Press Enter to continue...")
    delete_volume("dev-test")

if __name__ == "__main__":
    main()
