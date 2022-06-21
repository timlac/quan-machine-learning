#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
export DATA_MOUNT=/media/tim/Seagate\ Backup\ Plus\ Drive/Test
#export DATA_MOUNT=/home/tim/Videos

OUT_PATH=$DATA_MOUNT/out_test
DOCKER_COMPOSE_PATH=/home/tim/work/su-thesis-project/OpenFace/docker-compose.yml

docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts

find "$DATA_MOUNT" -name "*.mov" -print0 | while IFS= read -r -d '' file; do
    echo "file = $file"
    docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$file" -out_dir "$OUT_PATH"
    docker exec openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user
done

docker-compose -f $DOCKER_COMPOSE_PATH down

#
#for f in $FILES
#do
#  echo "$f"
#
##  docker exec -it openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$f" -out_dir "$OUT_PATH"
##  docker exec -it openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user
#done
