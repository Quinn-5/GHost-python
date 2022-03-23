from kubernetes import client, config

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import resources

def create_deployment(name:str):
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

def main():
    config.load_kube_config()

    name = "minecraft"

    deployment = create_deployment(name)

    resources.launch_deployment(deployment, "dev")
    input()
    resources.delete_deployment(name, "dev")

if __name__ == "__main__":
    main()
