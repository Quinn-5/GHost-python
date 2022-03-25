from kubernetes import client, config

def create_volume(name:str, namespace:str, size:str, storage_class=None):
    api = client.CoreV1Api()

    spec = client.V1PersistentVolumeSpec(
        access_modes=["ReadWriteOnce"],
        capacity={"storage":size},
        persistent_volume_reclaim_policy="Delete",
        local=client.V1LocalVolumeSource(
            path=f"/mnt/kube/{namespace}/{name}"
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
        print(f"PersistentVolume creation failed:\n{e}")
        return
    print(f"PersistentVolume {name} successfully created.")
    return resp

def delete_volume(name:str):
    api = client.CoreV1Api()

    print(f"Deleting PersistentVolume {name}.")
    try:
        resp = api.delete_persistent_volume(name)
    except client.rest.ApiException as e:
        print(f"PersistentVolume deletion failed:\n{e}")
        return
    print(f"PersistentVolume {name} successfully deleted.")
    return resp

def main():
    config.load_kube_config()

    create_volume("test", "dev", "500Mi")
    input("Press Enter to continue...")
    delete_volume("test")

if __name__ == "__main__":
    main()
