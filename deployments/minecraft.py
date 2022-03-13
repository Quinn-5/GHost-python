from kubernetes import client, config
import resources

def create_deployment(name:str):
    api = client.CoreV1Api()

    spec = client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={"app":name}),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app":"mc"}
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
                            vale="false"
                        ),
                        client.V1EnvVar(
                            name="MAX_MEMORY",
                            Value="1G"
                        )
                    ],
                    image="itzg/minecraft-server",
                    image_pull_policy="Always",
                    stdin=True,
                    tty=True
                )],
                restart_policy="Always",
                volumes=[client.V1Volume()]
            )
        )
    )

    deployment = client.V1Deployment(
        api_version="v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name = name
        ),
        spec = spec
    )

    return deployment

def launch_instance():
    pass

def delete_instance():
    pass

def main():
    config.load_kube_config()

if __name__ == "__main__":
    main()
