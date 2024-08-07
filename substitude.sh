#!/bin/sh

# generate deploy.yaml
sed "s/\$PROJECT_ID/$PROJECT_ID/g" deploy.yaml.tpl | \
sed "s/\$CLUSTER_REGION/$CLUSTER_REGION/g" | \
sed "s/\$STAGING_CLUSTER_NAME/$STAGING_CLUSTER_NAME/g" | \
sed "s/\$PRODUCTION_CLUSTER_NAME/$PRODUCTION_CLUSTER_NAME/g" \
> deploy.yaml

# generate patches for domain name config map
sed "s/\$DOMAIN/$DOMAIN/g" kustomize/templates/domain-config.yaml.tpl \
> kustomize/production/patches/domain-config.yaml
sed "s/\$DOMAIN/$STAGING_DOMAIN/g" kustomize/templates/domain-config.yaml.tpl \
> kustomize/staging/patches/domain-config.yaml

# generate patches for ingress
sed "s/\$DOMAIN/$DOMAIN/g" kustomize/templates/ingress-patch.yaml.tpl | \
sed "s/\$INGRESS_IP_NAME/$PRODUCTION_INGRESS_IP_NAME/g" \
> kustomize/production/patches/ingress-patch.yaml
sed "s/\$DOMAIN/$STAGING_DOMAIN/g" kustomize/templates/ingress-patch.yaml.tpl | \
sed "s/\$INGRESS_IP_NAME/$STAGING_INGRESS_IP_NAME/g" \
> kustomize/staging/patches/ingress-patch.yaml