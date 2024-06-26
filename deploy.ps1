# Deploy the app to GCP Cloud Run
docker build -t receipt-app:latest .

# Tag the Docker image
docker tag receipt-app:latest gcr.io/personal-projects-416300/receipt-app:latest

# Push the Docker image to Google Container Registry (GCR)
docker push gcr.io/personal-projects-416300/receipt-app:latest

# Deploy the app to Cloud Run
gcloud run deploy receipt-app `
  --image gcr.io/personal-projects-416300/receipt-app:latest `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --cpu 1 `
  --memory 1Gi `
  --port=5000 `
  --project=personal-projects-416300