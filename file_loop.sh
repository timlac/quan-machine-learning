#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
export DATA_MOUNT=/home/tim/Videos

docker-compose -f /home/tim/work/su-thesis-project/OpenFace/docker-compose.yml up -d openface && sync # sync is to wait till service starts

FILES="$DATA_MOUNT/A220_normalized_audiovideo_clips/*"
for f in $FILES
do
  docker exec -it openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f $f -out_dir $DATA_MOUNT/out
  docker exec -it openface chown -R $UID:$UID $DATA_MOUNT # chown to current user
done

docker-compose -f /home/tim/work/su-thesis-project/OpenFace/docker-compose.yml down