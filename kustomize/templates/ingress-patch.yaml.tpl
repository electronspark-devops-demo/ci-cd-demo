- op: replace
  path: /spec/rules/0/host
  value: $DOMAIN
- op: replace
  path: /metadata/annotations/kubernetes.io~1ingress.global-static-ip-name
  value: $INGRESS_IP_NAME