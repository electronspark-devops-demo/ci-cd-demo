# ci-cd-demo

## First set environment variables

在gcloud console里克隆示例仓库，修改git仓库根目录下的`vars.sh`文件，使其能够适应你的Google Cloud环境。

```bash
# the region of the resources needed
export CLUSTER_REGION="us-central1"
# the prefix of the names of staging and production clusters
export CLUSTER_NAME="cicd-demo"
# the domain name for the production ingress
export DOMAIN="demo.electronspark.xyz"
# the domain name for the staging ingress
export STAGING_DOMAIN="demo-staging.electronspark.xyz"
# the name associated with your global reserved external static IP for production ingress
export PRODUCTION_INGRESS_IP_NAME="web-ip"
# the name associated with your global reserved external static IP for staging ingress
export STAGING_INGRESS_IP_NAME="staging-ip"
# the owner of github repository, either user or organization
export REPO_OWNER="electronspark-devops-demo"
# the name of github repository
export REPO_NAME="ci-cd-demo"
# the name of artifact registry
export DEFAULT_REPO="ci-cd-demo"
# the name of the cloud build trigger
export BUILD_PIPELINE_NAME="ci-cd-demo-trigger"
# the name of the cloud deploy
export DELIVERY_PIPELINE_NAME="ci-cd-demo-cd"
```

执行以下命令导入环境变量

```bash
source sources.sh
```

并执行`substitute.sh`脚本，根据导入的环境变量修改kustomize的补丁的Cloud Deploy的configuration file，以适应你的环境。

```bash
sh substitute.sh
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

## Reserve Global Static IP

```bash
gcloud compute addresses create $PRODUCTION_INGRESS_IP_NAME \
    --global \
    --ip-version IPV4
gcloud compute addresses create $STAGING_INGRESS_IP_NAME \
    --global \
    --ip-version IPV4
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

It will use the default Compute Engine service account for the CI pipeline.

```bash
gcloud builds triggers create github --name="${BUILD_PIPELINE_NAME}" \
            --service-account="projects/${PROJECT_ID}/serviceAccounts/${SERVICE_ACCOUNT_EMAIL}" \
            --repo-owner="${REPO_OWNER}" \
            --repo-name="${REPO_NAME}" --branch-pattern="^main$" \
            --build-config="cloudbuild.yaml" \
            --region=${CLUSTER_REGION} \
            --substitutions=_REGION=${CLUSTER_REGION},_CLUSTER=hello-cloudbuild,_CACHE_URI=gs://$STORAGE_BUCKET_NAME,_DELIVERY_PIPELINE_NAME=$DELIVERY_PIPELINE_NAME,_SOURCE_STAGING_BUCKET=gs://$STAGING_BUCKET_NAME,_DEFAULT_REPO=$DEFAULT_REPO,_PROJECT_ID=$PROJECT_ID
```

## Configure Cloud Deploy

Create a cloud deploy delivery pipeline and two targets based on `deploy.yaml` file on the root path of the git repository. This will create two targets, one for deploying the staging cluster, and one for deploying the production cluster.

```bash
gcloud deploy apply --file=deploy.yaml --region=$CLUSTER_REGION --project=$PROJECT_ID
```

## Trigger the CI pipeline

现在修改代码

将刚刚的更改提交到github上去，这一动作将触发Cloud Build的CI pipeline。

```bash
git add --all
git commit -m "some changes"
git push
```

In the Google Cloud console navigation menu, click `Cloud Build` > `History`

查看刚刚的build记录

查看Cloud Trigger

展示staging domian的首页

在Cloud Trigger中将网站从staging cluster做promote操作到production cluster

展示production domain的首页




https://cloud.google.com/build/docs/automate-builds