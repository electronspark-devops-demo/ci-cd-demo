export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
export CLUSTER_REGION="us-central1"
export CLUSTER_NAME="cicd-demo"
export DOMAIN="demo.electronspark.xyz"
export STAGING_DOMAIN="demo-staging.electronspark.xyz"
export PRODUCTION_INGRESS_IP_NAME="web-ip"
export STAGING_INGRESS_IP_NAME="staging-ip"
# the owner of github repository, either user or organization
export REPO_OWNER="electronspark-devops-demo"
# the name of github repository
export REPO_NAME="ci-cd-demo"
# the name of artifact registry
export DEFAULT_REPO="ci-cd-demo"