from kubernetes import client, config

def launch_deployment(deployment):
    pass

def delete_deployment(deployment):
    pass

def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

if __name__ == "__main__":
    main()
