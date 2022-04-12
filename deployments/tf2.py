from kubernetes import client, config

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import resources

def create_deployment(name:str, port):
    """
    Return a deployment object for a Team Fortress 2 server based on configuration input.
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
                            name="SRCDS_PORT",
                            value=str(port)
                        ),
                        client.V1EnvVar(
                            name="SRCDS_PW",
                            value=name
                        ),
                        client.V1EnvVar(
                            name="SRCDS_HOSTNAME",
                            value=name
                        )
                    ],
                    image="cm2network/tf2",
                    image_pull_policy="Always",
                    stdin=True,
                    tty=True,
                    volume_mounts=[client.V1VolumeMount(
                        mount_path="~/tf-dedicated",
                        name=name
                    )]
                )],
                restart_policy="Always",
                volumes=[client.V1Volume(
                    name=name,
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=name
                    )
                )],
                security_context=client.V1SecurityContext(
                    allow_privilege_escalation=False,
                    run_as_group=1000,
                    run_as_user=1000
                )
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
    Deploys a Team Fortress 2 server given a name and namespace
    """

    fullname = f"{user}-{name}"

    api = client.CoreV1Api()
    np = resources.create_nodeport(fullname, 27015, "UDP")
    try:
        port = np.spec.ports[0].node_port
        resources.edit_nodeport(fullname, port, "UDP")
        deployment = create_deployment(fullname, port)
    except AttributeError:
        pass
    resources.create_claim(fullname, "6Gi")
    resources.launch_deployment(deployment)
    if "port" in locals():
        print(f"Server created. accessible at amadeus.csh.rit.edu:{port}")
        return port


def delete(name:str, user:str):
    """
    Deletes a Team Fortress 2 server with given name from a given namespace
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
