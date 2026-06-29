#!/usr/bin/env bash
# deploy.sh — manual one-shot deployment helper
# Usage: ./deployment/deploy.sh <git-sha>

set -euo pipefail

SHA=${1:-$(git rev-parse --short HEAD)}
REGION=${AWS_REGION:-us-east-1}
CLUSTER="deskpilot-cluster"

echo "Deploying deskpilot @ $SHA to $CLUSTER ($REGION)"

# Force new ECS deployment
for SVC in deskpilot-backend deskpilot-frontend; do
  echo "  → updating $SVC"
  aws ecs update-service \
    --cluster "$CLUSTER" \
    --service "$SVC" \
    --force-new-deployment \
    --region "$REGION" \
    --output text --query 'service.serviceName'
done

echo "Waiting for services to stabilise…"
aws ecs wait services-stable \
  --cluster "$CLUSTER" \
  --services deskpilot-backend deskpilot-frontend \
  --region "$REGION"

echo "Done."
