from kubernetes import client, config

def create_nodeport(volume):
    pass

def delete_nodeport(nodeport):
    pass

def main():
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

if __name__ == "__main__":
    main()
