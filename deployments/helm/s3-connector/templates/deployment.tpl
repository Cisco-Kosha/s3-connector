apiVersion: apps/v1
kind: Deployment
metadata:
  name:  {{ .Values.appName }}
  labels:
    version: {{ .Values.appVersion }}
  annotations:
  name:  {{ .Values.appName }}
  labels:
    version: {{ .Values.appVersion }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app:  {{ .Values.appName }}
      version: {{ .Values.appVersion }}
  template:
    metadata:
      labels:
        app:  {{ .Values.appName }}
        version: {{ .Values.appVersion }}
    spec:
      containers:
      - name: {{ .Values.appName }}
        image: docker.io/{{ .Values.image.repository }}/{{ .Values.image.name }}:{{ .Values.image.tag }}
        resources:
          requests:
            cpu: "100m"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: {{ .Values.service.port }}
        env:
        - name: AWS_SERVER_PUBLIC_KEY
          value: {{ .Values.connector.aws_server_public_key }}
        - name: AWS_SERVER_SECRET_KEY
          value: {{ .Values.connector.aws_server_secret_key }}
        - name: BUCKET_NAME
          value: {{ .Values.connector.bucket_name }}
