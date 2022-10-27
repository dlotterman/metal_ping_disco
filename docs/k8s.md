## metal_ping_disco

The `metal_ping_disco` app is just a simple container app the can be run with a [simple deployment](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/). This example uses unsecure env declarations in the deployment file, subsitute this for your preferred secrets method. It only needs one replica.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metal-ping-disco-deployment
  labels:
    app: metal-ping-disco
spec:
  replicas: 1
  selector:
    matchLabels:
      app: metal-ping-disco
  template:
    metadata:
      labels:
        app: metal-ping-disco
    spec:
      nodeSelector:
        type: metal-ping-disco
      containers:
        - name: metal-ping-disco
          image: dlotterman/metal_ping_disco:latest
          ports:
            - containerPort: 8050
          env:
          - name: METAL_PING_DISCO_AWS_S3_BUCKET
            value: YOUR_VALUE
          - name: METAL_PING_DISCO_AWS_ACCESS_KEY_ID
            value: YOUR_VALUE
          - name: METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY
            value: YOUR_VALUE
          - name: METAL_PING_DISCO_AWS_S3_ENDPOINT
            value: https://s3.us-east-1.wasabisys.com		  
```

The pod will also need to be exposed to a public network. This step is so k8's distro / design specific it's difficult to provide an example, but with a simple design as one would get from 'k3s', 'k0s', or 'minikube', it should be as simple as:

`kubectl expose deployment/metal-ping-disco-deployment`

## metal_ping_disco_data_runner

The `data_runner` app is intended to be run as a scheduled task, in Kubernetes this is easiest with a [Kubernetes CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/):

```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: metal-ping-disco-data-runner
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: metal-ping-disco-data-runner
            image: dlotterman/metal_ping_disco_data_runner:latest
            imagePullPolicy: IfNotPresent
            env:
            - name: METAL_PING_DISCO_AWS_S3_BUCKET
              value: YOUR_VALUE
            - name: METAL_PING_DISCO_AWS_ACCESS_KEY_ID
              value: YOUR_VALUE
            - name: METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY
              value: YOUR_VALUE
            - name: METAL_PING_DISCO_AWS_S3_ENDPOINT
              value: https://s3.us-east-1.wasabisys.com
          restartPolicy: OnFailure
```		 
