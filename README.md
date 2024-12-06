# K-means MapReduce for Image Segmentation implementation
In this work k-means clustering algorithm is implemented using MapReduce (Hadoop version 2.8 or higher) framework.

#### Start hadoop

Format namenode
```bash
hdfs namenode -format
```
Start dfs and yarn, you can either go with:

```bash
start-dfs.sh
start-yarn.sh
```
or 
```bash
start-all.sh
```


You should use a virtual environment to run this project.

#### Setup virtualenv
```bash
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

or just use conda environment:

```bash
conda activate
pip install -r requirements.txt
```

To run the program, shell script ```run.sh``` should be executed. 
```bash
sh run.sh
```

It requires path to jar file and its input parameters which are:

* ```input``` - path to data file
* ```state``` - path to file that contains clusters 
* ```number``` - number of reducers 
* ```output``` - output directory 
* ```delta``` - threshold convergence (acceptable difference between 2 subsequent centroids)
* ```max``` - maximum number of iterations 
* ```distance``` - similairty measure (currently only Euclidean distance is supported)

## Workflow
The figure below denotes one iteration of MapReduce program.

![alt text][flow]

First, Centroids and Context (Configuration) are loaded into the Distributed Cache. This is done by overriding setup function in the Mapper and Reducer class. Afterwards, the input data file is split and each data point is processed by one of the map functions (in Map process). The function writes key-value pairs <Centroid, Point>, where the Centroid is the closest one to the Point. Next, Combiner is used in order to decrease the number of local writings. In this phase data points that are on the same machine are summed up and the number of those data points is recorded, Point.number variable. Now, for the optimization reasons output values are automatically shuffled and sorted by Centroids. The Reducer performs the same procedure as the Combiner, but it also checks whether centroids converged; comparing the difference between old and new centroids with delta input parameter. If a centroid converge, then the global Counter remains unchanged, otherwise, it is incremented. 

After the one iteration is done, new centroids are saved and the program checks two conditions, if the program reached the maximum number of iterations or if the Counter value is unchanged. If one of these two conditions is satisfied, then the program is finished, otherwise, the whole MapReduce process is run again with the updated centroids.

## KMeans use-cases in this project
One of the use-cases of k-means algorithm is the segmentation on MRI images, reducing the number of distinct colors of an image in order to make it easier to processing. (Far better algorithms for this purpose are available)

Numerical (RGB) values of images are saved as input data, and clusters are initialized by using the KMeans++ algorithm to ensure the output stable everytime the code is run. 
