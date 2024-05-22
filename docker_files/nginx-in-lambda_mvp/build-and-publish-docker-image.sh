source .env
IMAGE_TYPE=nginx-on-lambda
ACCOUNT_ID="${AWS_ACCOUNT_ID}"
REGION="${AWS_DEFAULT_REGION}"
IMAGE_NAME=${ACCOUNT_ID}.dkr.ecr.$REGION.amazonaws.com/${IMAGE_TYPE}

echo
echo "*** Logging in docker to AWS ECR"
echo
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

echo
echo "*** Building Lambda Docker image for ${IMAGE_TYPE}"
echo


docker build -t $IMAGE_NAME .


echo
echo "*** publishing image to AWS ECR"
echo
docker push $IMAGE_NAME
#
#echo
#echo "*** all done"
#echo

#echo
#echo "*** Run locally"
#echo
#docker run -it --rm -p 8080:8080 $IMAGE_NAME
#./run-with-volume.sh
