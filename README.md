
# MINISRV

a converter for video formats (.mp4,.flv) to audio formats(.mp3, .wav)


## Tech Stack

**Language Used:** Python3

**Frameworks:** Flask

**DB:** Postgres, Mongo

**DevOps:** Docker, Kubernetes, Minikube






## Installation

Since this is a microservice, you have to start every service to run the project.

## Prequisite: 
Some form of kube8s cluster, postgres and mongo must be present in the system that is trying to run this project.

If you have minikube start, Please start minikube first.

```bash
  minikube start
```

Since the project uses ingresses and two test domains, you might want to map the loopback addresses to the test domains.

UNIX users:
```bash
  sudo vim /etc/hosts
```

Finally, deploy pods, services and respective configMaps and secrets to your cluster.

```bash
  kubectl apply -f manifests/
```
## License

[MIT](https://choosealicense.com/licenses/mit/)


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vidurkhanal)


