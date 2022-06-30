#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
export DATA_MOUNT=/media/tim/Seagate\ Backup\ Plus\ Drive

OUT_PATH=$DATA_MOUNT/Out
DOCKER_COMPOSE_PATH=/home/tim/work/su-thesis-project/OpenFace/docker-compose.yml

docker-compose -f "$DOCKER_COMPOSE_PATH" up -d openface && sync # sync is to wait till service starts

# create array of all elements in OUT_PATH to skip these later
mapfile -d $'\0' array < <(find "$OUT_PATH" -type f -iname "*.csv" -exec basename {} .csv ";")

find "$DATA_MOUNT/Documents" -name "*.mov" -print0 | while IFS= read -r -d '' file; do

    echo processing file: "$file"

    # get filename without extension
    filename=$(basename -- "$file")
    filename_no_extension="${filename%.*}"

    # if filename_no_extension in OUT_PATH array, then continue, e.g. skip it
    if [[ " ${array[*]} " =~ (^|[[:space:]])"$filename_no_extension"($|[[:space:]])  ]]; then
        continue
    fi

    # run Openface with docker
    docker exec openface FeatureExtraction -2Dfp -3Dfp -pdmparams -pose -aus -gaze -f "$file" -out_dir "$OUT_PATH"
    docker exec openface chown -R $UID:$UID "$DATA_MOUNT" # chown to current user
done

docker-compose -f $DOCKER_COMPOSE_PATH down