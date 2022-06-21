#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
export DATA_MOUNT=/media/tim/Seagate\ Backup\ Plus\ Drive/Test
#export DATA_MOUNT=/home/tim/Videos


OUT_PATH=$DATA_MOUNT/out_test
DOCKER_COMPOSE_PATH=/home/tim/work/su-thesis-project/OpenFace/docker-compose.yml

echo "$OUT_PATH"


docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts

FILES_PATH="$DATA_MOUNT"

find "$FILES_PATH" -type f -name '*.mov' -exec sh -c '
  for file do
    echo "$file"
    echo "$DATA_MOUNT"
    docker exec -it openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$file" -out_dir "$OUT_PATH"
#    docker exec -it openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user
  done
' exec-sh {} +


#docker exec -it openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$FILES_PATH/A72-normalized audio-video clips/A72_adm_p_1.mov" -out_dir "$OUT_PATH"
#docker exec -it openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user

docker-compose -f $DOCKER_COMPOSE_PATH down

#
#for f in $FILES
#do
#  echo "$f"
#
##  docker exec -it openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$f" -out_dir "$OUT_PATH"
##  docker exec -it openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user
#done
