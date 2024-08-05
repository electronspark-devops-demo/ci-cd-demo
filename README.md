# ci-cd-demo

# 设置环境变量
```bash
export PROJECT_ID=$(gcloud config get-value project)
export CLUSTER_REGION="us-central1"
export CLUSTER_NAME="cicd-demo"
export DOMAIN="demo.electronspark.xyz"
# the owner of github repository, either user or organization
export REPO_OWNER="electronspark-devops-demo"
# the name of github repository
export REPO_NAME="ci-cd-demo"

export SERVICE_ACCOUNT_EMAIL="$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")-compute@developer.gserviceaccount.com"

export STORAGE_BUCKET_NAME="${CLUSTER_NAME}-storage-bucket"
export STAGING_BUCKET_NAME="${CLUSTER_NAME}-staging-bucket"

export STAGING_CLUSTER_NAME="${CLUSTER_NAME}-staging"
export PRODUCTION_CLUSTER_NAME="${CLUSTER_NAME}-production"
export DEFAULT_REPO="ci-cd-demo"

export BUILD_PIPELINE_NAME="ci-cd-demo-trigger"
export DELIVERY_PIPELINE_NAME="ci-cd-demo-cd"
```



```bash
gcloud services enable container.googleapis.com \
    cloudbuild.googleapis.com \
    clouddeploy.googleapis.com \
    sourcerepo.googleapis.com \
    artifactregistry.googleapis.com \
    storage.googleapis.com
```

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


```bash
gcloud artifacts repositories create $DEFAULT_REPO \
  --repository-format=docker \
  --location=$CLUSTER_REGION
```

```bash
gcloud storage buckets create gs://$STORAGE_BUCKET_NAME --location=$CLUSTER_REGION
gsutil versioning set on gs://$STORAGE_BUCKET_NAME
gcloud storage buckets create gs://$STAGING_BUCKET_NAME --location=$CLUSTER_REGION
gsutil versioning set on gs://$STAGING_BUCKET_NAME
```

```bash
gsutil cp /dev/null gs://$STORAGE_BUCKET_NAME/cache
```

```bash
gcloud container clusters create-auto $STAGING_CLUSTER_NAME --region $CLUSTER_REGION
gcloud container clusters create-auto $PRODUCTION_CLUSTER_NAME --region $CLUSTER_REGION
```

# 获取 GKE 集群凭据
```bash
gcloud container clusters get-credentials hello-cloudbuild --region $CLUSTER_REGION
```

# 使用 Skaffold 进行部署，并指定默认的镜像仓库和域名
```bash
skaffold run -f=skaffold.yaml -p staging \
--default-repo=${CLUSTER_REGION}-docker.pkg.dev/${PROJECT_ID}/${DEFAULT_REPO} \
--file-output=/workspace/artifacts.json \
--cache-file=/workspace/cache
```


使用 gcloud 命令行工具创建 Cloud Build 触发器：
```bash
gcloud builds triggers create github --name="${BUILD_PIPELINE_NAME}" \
            --service-account="projects/${PROJECT_ID}/serviceAccounts/${SERVICE_ACCOUNT_EMAIL}" \
            --repo-owner="${REPO_OWNER}" \
            --repo-name="${REPO_NAME}" --branch-pattern="^main$" \
            --build-config="cloudbuild.yaml" \
            --region=${CLUSTER_REGION} \
            --substitutions=_REGION=${CLUSTER_REGION},_CLUSTER=hello-cloudbuild,_CACHE_URI=gs://$STORAGE_BUCKET_NAME,_DELIVERY_PIPELINE_NAME=$DELIVERY_PIPELINE_NAME,_SOURCE_STAGING_BUCKET=gs://$STAGING_BUCKET_NAME,_DEFAULT_REPO=${CLUSTER_REGION}-docker.pkg.dev/${PROJECT_ID}/${DEFAULT_REPO},_PROJECT_ID=$PROJECT_ID
```

应用cloud deploy配置：

```bash
gcloud deploy apply --file=deploy.yaml --region=$CLUSTER_REGION --project=$PROJECT_ID
```
