#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
export DATA_MOUNT=/media/tim/Seagate\ Backup\ Plus\ Drive

OUT_PATH=$DATA_MOUNT/Out
DOCKER_COMPOSE_PATH=/home/tim/work/su-thesis-project/OpenFace/docker-compose.yml

docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts


file="$DATA_MOUNT/Documents/normalized-audio-video-clips-17/A221_neg_sur_v_2.mov"


# run Openface with docker
docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$file" -out_dir "$OUT_PATH"
docker exec openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user


docker-compose -f $DOCKER_COMPOSE_PATH down