from kubernetes import client, config

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import resources

def create_deployment(name:str):
    """
    Return a deployment object for a Minecraft server based on configuration input.
    """
    api = client.CoreV1Api()

    spec = client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={"app":name}),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app":name}
            ),
            spec=client.V1PodSpec(
                containers=[client.V1Container(
                    name=name,
                    env=[
                        client.V1EnvVar(
                            name="EULA",
                            value="TRUE"
                        ),
                        client.V1EnvVar(
                            name="MOTD",
                            value="Latest Release"
                        ),
                        client.V1EnvVar(
                            name="PVP",
                            value="false"
                        ),
                        client.V1EnvVar(
                            name="MAX_MEMORY",
                            value="1G"
                        )
                    ],
                    image="itzg/minecraft-server",
                    image_pull_policy="Always",
                    stdin=True,
                    tty=True,
                    volume_mounts=[client.V1VolumeMount(
                        mount_path="/data",
                        name=name
                    )]
                )],
                restart_policy="Always",
                volumes=[client.V1Volume(
                    name=name,
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=name
                    )
                )]
            )
        )
    )

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name = name
        ),
        spec = spec
    )

    return deployment

def deploy(name:str, user:str):
    """
    Deploys a Minecraft server given a name and namespace
    """

    fullname = f"{user}-{name}"

    api = client.CoreV1Api()
    deployment = create_deployment(fullname)
    resources.create_volume(fullname, "500Mi")
    resources.create_claim(fullname, "500Mi")
    np = resources.create_nodeport(fullname, 25565)
    resources.launch_deployment(deployment)
    try:
        port = np.spec.ports[0].node_port
        print(f"Server created. accessible at amadeus.csh.rit.edu:{port}")
        return port
    except AttributeError:
        pass


def delete(name:str, user:str):
    """
    Deletes a Minecraft server with given name from a given namespace
    """

    fullname = f"{user}-{name}"

    resources.delete_deployment(fullname)
    resources.delete_nodeport(fullname)
    resources.delete_claim(fullname)
    resources.delete_volume(fullname)

def main():
    config.load_kube_config()

    name = "minecraft"
    namespace = "dev"

    deploy(name, namespace)
    input("Press Enter to continue...")
    delete(name, namespace)

if __name__ == "__main__":
    main()
