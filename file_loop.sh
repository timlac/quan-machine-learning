#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
export DATA_MOUNT=/media/tim/Seagate\ Backup\ Plus\ Drive/

OUT_PATH=$DATA_MOUNT/Test/out
DOCKER_COMPOSE_PATH=/home/tim/work/su-thesis-project/OpenFace/docker-compose.yml

docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts

FILES="$DATA_MOUNT/Test/*"
for f in $FILES
do
  docker exec -it openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$f" -out_dir "$OUT_PATH"
  docker exec -it openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user
done

docker-compose -f $DOCKER_COMPOSE_PATH down