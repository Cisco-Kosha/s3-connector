apiVersion: apps/v1
kind: Deployment
metadata:
  name:  {{ .Values.appName }}
  labels:
    version: {{ .Values.appVersion }}
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
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/path: "/metrics"
        prometheus.io/port: "{{ .Values.service.port }}"
    spec:
      containers:
      - name: {{ .Values.appName }}
        image: {{ .Values.image.org }}/{{ .Values.image.repository }}/{{ .Values.image.name }}:{{ .Values.image.tag }}
        resources:
          requests:
            cpu: "100m"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: {{ .Values.service.port }}
        env:
        - name: AWS_ACCESS_KEY_ID
          value: {{ .Values.connector.aws_access_key_id }}
        - name: AWS_SECRET_ACCESS_KEY
          value: {{ .Values.connector.aws_secret_access_key }}
        - name: BUCKET_NAME
          value: {{ .Values.connector.bucket_name }}
