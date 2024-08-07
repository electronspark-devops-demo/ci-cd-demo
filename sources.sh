source vars.sh

export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
export SERVICE_ACCOUNT_EMAIL="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
export STORAGE_BUCKET_NAME="${CLUSTER_NAME}-storage-bucket"
export STAGING_BUCKET_NAME="${CLUSTER_NAME}-staging-bucket"
export STAGING_CLUSTER_NAME="${CLUSTER_NAME}-staging"
export PRODUCTION_CLUSTER_NAME="${CLUSTER_NAME}-production"