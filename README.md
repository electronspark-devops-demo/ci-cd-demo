# ci-cd-demo

```bash
export PROJECT_ID=$(gcloud config get-value project)
export CLUSTER_REGION="us-central1"
export STAGING_CLUSTER_NAME="hello-cloudbuild"
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
