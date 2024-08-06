# ci-cd-demo

## First set environment variables

```bash
export PROJECT_ID=$(gcloud config get-value project)
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
export CLUSTER_REGION="us-central1"
export CLUSTER_NAME="cicd-demo"
export DOMAIN="demo.electronspark.xyz"
# the owner of github repository, either user or organization
export REPO_OWNER="electronspark-devops-demo"
# the name of github repository
export REPO_NAME="ci-cd-demo"
# the name of artifact registry
export DEFAULT_REPO="ci-cd-demo"

export BUILD_PIPELINE_NAME="ci-cd-demo-trigger"
export DELIVERY_PIPELINE_NAME="ci-cd-demo-cd"

export SERVICE_ACCOUNT_EMAIL="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
export STORAGE_BUCKET_NAME="${CLUSTER_NAME}-storage-bucket"
export STAGING_BUCKET_NAME="${CLUSTER_NAME}-staging-bucket"
export STAGING_CLUSTER_NAME="${CLUSTER_NAME}-staging"
export PRODUCTION_CLUSTER_NAME="${CLUSTER_NAME}-production"
```

## Enable Google Cloud APIs needed

```bash
gcloud services enable container.googleapis.com \
    cloudbuild.googleapis.com \
    clouddeploy.googleapis.com \
    storage-component.googleapis.com \
    storage.googleapis.com \
    artifactregistry.googleapis.com
```

## Make sure the default Compute Engine service account has sufficient permissions, then add the `iam.serviceAccountUser` role, which includes the `actAs` permission for the default service account to deploy to the runtime

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
    --role="roles/clouddeploy.jobRunner"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
    --role="roles/container.developer"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
    --role="roles/clouddeploy.jobRunner"

gcloud iam service-accounts add-iam-policy-binding ${SERVICE_ACCOUNT_EMAIL} \
    --member=serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
    --role="roles/iam.serviceAccountUser" \
    --project=$PROJECT_ID
```

## Create an artifact registry to store docker images built during CI process

```bash
gcloud artifacts repositories create $DEFAULT_REPO \
  --repository-format=docker \
  --location=$CLUSTER_REGION
```

## Create Storage Bucket to keep Skaffold cache file

```bash
gcloud storage buckets create gs://$STORAGE_BUCKET_NAME --location=$CLUSTER_REGION
gsutil versioning set on gs://$STORAGE_BUCKET_NAME
gcloud storage buckets create gs://$STAGING_BUCKET_NAME --location=$CLUSTER_REGION
gsutil versioning set on gs://$STAGING_BUCKET_NAME
```

## Create an empty Skaffold cache file, so it could be downloaded when first time running the CI pipeline

```bash
gsutil cp /dev/null gs://$STORAGE_BUCKET_NAME/cache
```

## Create two GKE autopilot clusters. One for staging, and one for production.

```bash
gcloud container clusters create-auto $STAGING_CLUSTER_NAME --region $CLUSTER_REGION
gcloud container clusters create-auto $PRODUCTION_CLUSTER_NAME --region $CLUSTER_REGION
```

## Run the following command to update the configuration file of kubectl
```bash
gcloud container clusters get-credentials $STAGING_CLUSTER_NAME --region $CLUSTER_REGION
```

## Using Skaffold to build staging images, and to deploy the staging cluster
```bash
skaffold run -f=skaffold.yaml -p staging \
--default-repo=${CLUSTER_REGION}-docker.pkg.dev/${PROJECT_ID}/${DEFAULT_REPO}
```

## Create a Cloud Build Trigger that will be triggered each time the main branch of the demo git repository changes.

It will use default Compute Engine service account for image building process.

```bash
gcloud builds triggers create github --name="${BUILD_PIPELINE_NAME}" \
            --service-account="projects/${PROJECT_ID}/serviceAccounts/${SERVICE_ACCOUNT_EMAIL}" \
            --repo-owner="${REPO_OWNER}" \
            --repo-name="${REPO_NAME}" --branch-pattern="^main$" \
            --build-config="cloudbuild.yaml" \
            --region=${CLUSTER_REGION} \
            --substitutions=_REGION=${CLUSTER_REGION},_CLUSTER=hello-cloudbuild,_CACHE_URI=gs://$STORAGE_BUCKET_NAME,_DELIVERY_PIPELINE_NAME=$DELIVERY_PIPELINE_NAME,_SOURCE_STAGING_BUCKET=gs://$STAGING_BUCKET_NAME,_DEFAULT_REPO_=$DEFAULT_REPO,_PROJECT_ID=$PROJECT_ID
```

## Configure Cloud Deploy

```bash
gcloud deploy apply --file=deploy.yaml --region=$CLUSTER_REGION --project=$PROJECT_ID
```
