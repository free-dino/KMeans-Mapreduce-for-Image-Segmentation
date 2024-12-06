#!/usr/bin/env bash
#!/usr/bin/env python3

# remove old file if any
rm -r -f ./tmp/*
rm -r -f ./output/*

# create some temp file
mkdir ./tmp

python3 data_prep.py --src_img ./input/* --dst_folder ./tmp

# remove old file from hdfs if any
hdfs dfs -rm -r -f /KMeans/Input
hdfs dfs -rm -r -f /KMeans/Output

# create directories on hdfs
hdfs dfs -mkdir -p /KMeans/Input
hdfs dfs -mkdir -p /KMeans/Output

# copy local input files
hdfs dfs -put ./tmp/points.txt ./tmp/clusters.txt /KMeans/Input/

# remove output files if any
hdfs dfs -rm -r -f /KMeans/Output/*

# specify input parameters
JAR_PATH=./kmeans_mapreduce.jar
MAIN_CLASS=Main
INPUT_FILE_PATH=/KMeans/Input/points.txt
STATE_PATH=/KMeans/Input/clusters.txt
NUMBER_OF_REDUCERS=1
OUTPUT_DIR=/KMeans/Output
DELTA=1000000000.0
MAX_ITERATIONS=30
DISTANCE=eucl

hadoop jar ${JAR_PATH} ${MAIN_CLASS} --input ${INPUT_FILE_PATH} \
--state ${STATE_PATH} \
--number ${NUMBER_OF_REDUCERS} \
--output ${OUTPUT_DIR} \
--delta ${DELTA} \
--max ${MAX_ITERATIONS} \
--distance ${DISTANCE}

# execute jar file
LAST_DIR="$(hdfs dfs -ls -t -C /KMeans/Output | head -1)"

# download results from hdfs
hdfs dfs -get "$LAST_DIR/part-r-00000" ./tmp
mv ./tmp/part-r-00000 ./tmp/kmeans-output.txt

python3 visualize_results.py --clusters_path ./tmp/kmeans-output.txt --src_img ./tmp/segmented_image.jpg --dst_img ./output/output_image.jpg

rm -r -f part-r-00000
rm -r -f ./tmp
