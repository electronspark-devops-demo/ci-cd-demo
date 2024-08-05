# ci-cd-demo

# 设置环境变量
```bash
export PROJECT_ID=$(gcloud config get-value project)
export CLUSTER_REGION="us-central1"
export CLUSTER_NAME="cicd-demo"
export DOMAIN="demo.electronspark.xyz"

export STORAGE_BUCKET_NAME="${CLUSTER_NAME}-storage-bucket"
export BUILD_ARTIFACTS_REGISTRY="${CLUSTER_NAME}-artifacts"

export STAGING_STORAGE_BUCKET_NAME="${STORAGE_BUCKET_NAME}-staging"
export PRODUCTION_STORAGE_BUCKET_NAME="${STORAGE_BUCKET_NAME}-production"
export STAGING_STORAGE_BUCKET_NAME="${STORAGE_BUCKET_NAME}-staging"
export PRODUCTION_STORAGE_BUCKET_NAME="${STORAGE_BUCKET_NAME}-production"
export STAGING_CLUSTER_NAME="${CLUSTER_NAME}-staging"
export PRODUCTION_CLUSTER_NAME="${CLUSTER_NAME}-production"
export DEFAULT_REPO=gcr.io/$PROJECT_ID
```


```bash
gcloud storage buckets create gs://BUCKET_NAME --location=$CLUSTER_REGION
```

# 获取 GKE 集群凭据
```bash
gcloud container clusters get-credentials $STAGING_CLUSTER_NAME --region $CLUSTER_REGION
```

# 使用 Skaffold 进行部署，并指定默认的镜像仓库和域名
```bash
skaffold run -f=skaffold.yaml -p staging --default-repo=$DEFAULT_REPO
```



使用 gcloud 命令行工具创建 Cloud Build 触发器：

```bash
gcloud beta builds triggers create cloud-source-repositories \
    --name="backend-trigger" \
    --repo="YOUR_REPO_NAME" \
    --branch-pattern="^main$" \
    --build-config="backend/cloudbuild.yaml" \
    --included-files="backend/**" \
    --substitutions=_PROJECT_ID=$PROJECT_ID

gcloud beta builds triggers create cloud-source-repositories \
    --name="frontend-trigger" \
    --repo="YOUR_REPO_NAME" \
    --branch-pattern="^main$" \
    --build-config="frontend/cloudbuild.yaml" \
    --included-files="frontend/**" \
    --substitutions=_PROJECT_ID=$PROJECT_ID

gcloud beta builds triggers create cloud-source-repositories \
    --name="auth-trigger" \
    --repo="YOUR_REPO_NAME" \
    --branch-pattern="^main$" \
    --build-config="auth/cloudbuild.yaml" \
    --included-files="auth/**" \
    --substitutions=_PROJECT_ID=$PROJECT_ID

gcloud beta builds triggers create cloud-source-repositories \
    --name="blog-trigger" \
    --repo="YOUR_REPO_NAME" \
    --branch-pattern="^main$" \
    --build-config="blog/cloudbuild.yaml" \
    --included-files="blog/**" \
    --substitutions=_PROJECT_ID=$PROJECT_ID
```

应用cloud deploy配置：

```bash
gcloud deploy apply --file=deploy.yaml --region=$CLUSTER_REGION --project=$PROJECT_ID
gcloud deploy apply --file=targets.yaml --region=$CLUSTER_REGION --project=$PROJECT_ID
```
