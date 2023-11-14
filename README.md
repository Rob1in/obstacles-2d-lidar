# Obstacles detection from planar lidar
[Viam module](https://docs.viam.com/extend/modular-resources/) for 2D obstacles detection as a vision service. 

<p align="center">
 <img src="https://github.com/Rob1in/obstacles-2d-lidar/blob/module/img/results.png" width=100%, height=100%>
 </p>



## Getting started

To use this module, you need a lidar in your robot. For instance, you can use [RPlidar](https://docs.viam.com/registry/examples/rplidar/).
This module implements the method `GetObjectPointClouds()` of the [vision service API](https://docs.viam.com/services/vision/#api).

### Installation with `pip install`

```
pip install -r requirements.txt
```

## Config
### Example config 
```json
{
  "services": [
    {
      "namespace": "rdk",
      "model": "viam:vision:obstacles_2d_lidar",
      "attributes": {
        "min_points_cluster": 4,
        "camera_name": "rplidar"
      },
      "name": "detector-module",
      "type": "vision"
    }
  ],
  "components": [
    {
      "namespace": "rdk",
      "type": "camera",
      "model": "viam:lidar:rplidar",
      "attributes": {
        "device_path": "/dev/tty.usbserial-0001"
      },
      "name": "rplidar",
      "depends_on": []
    }
  ],
  "modules": [
    {
      "name": "mydetector",
      "type": "local",
      "executable_path": "/path/to/your/run.sh"
    },
    {
      "executable_path": "/opt/homebrew/bin/rplidar-module",
      "name": "rplidar_module"
    }
  ]
}
```

If you want to grab the module from the [registry](https://app.viam.com/module/viam/obstacles_2d_lidar), make this change in the `modules` field:

```json
  "modules": [
    {
      "type": "registry",
      "module_id": "viam:obstacles_2d_lidar",
      "name": "whatever",
      "version": "latest"
    }
```

### Attributes description

The following attributes are available to configure your 2d obstacles detection module:

| Name | Type | Inclusion | Default | Description |
| ---- | ---- | --------- | --------| ------------ |
| `camera_name` | string | **Required** | | Camera name (planar lidar) to be used as input for detecting the obstacles. |
| `normal_vector` | string | Optional | `z` | Normal vector that defines the plan to project the 3D point cloud on. Accepted values are `x`, `y`, `z` and `auto`. If `auto` is selected, the algorithm will check if all the points belong to the same plan and project the points in this plane. `x`, `y` and `z` refer directly to PCD fields. (Choose default value for Rplidar A1).|
| `obstacles_height_mm` | float | Optional | `z` | Height of the obstacles returned by the algorithm. It can be any arbitrary value since the detector operates in a plane. |
| `dbscan_eps` | float | Optional | `0.05` | The maximum distance between two samples for one to be considered as in the neighborhood of the other. This is not a maximum bound on the distances of points within a cluster. This is the most important DBSCAN parameter to choose appropriately for your data set and distance function.|
|`dbscan_min_samples`| int | Optional | `2` |The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself. If min_samples is set to a higher value, DBSCAN will find denser clusters, whereas if it is set to a lower value, the found clusters will be more sparse. |
|`min_points_cluster`| int | Optional | `2` | Minimum number of points to define a cluster (= obstacle)  |
|`min_bbox_area`| float | Optional | `0.15` | If the area of the cluster found by dbscan in the normalized axis coordinate is bigger than `min_bbox_area`, try to refine the cluster with 2d RANSAC. |
|`ransac_min_samples`| int | Optional | `2` | Minimum number of samples chosen randomly from original data. |
|`ransac_residual_threshold`| float | Optional | `0.2` | Maximum residual for a data sample to be classified as an inlier. Points whose residuals are strictly equal to the threshold are considered as inliers. |
|`ransac_stop_probability`| float | Optional | `0.99` | RANSAC iteration stops if at least one outlier-free set of the training data is sampled in RANSAC. This requires to generate at least N samples (iterations): $N = \frac{\log(1-p)}{\log(1-w^n)}$, where $n$ is the number of points, $w$ the ratio of inliers to total points, and $p$ is `ransac_stop_probability`. |


## Deeper dive

The module works as follow:
  1. Get and decode PCD bytes from the camera. Project it onto a plane.
  2. Use DBSCAN to get a first set of clusters
  3. If one cluster is bigger than `min_bbox_area`, refine the cluster with RANSAC (2d linear model).
  4. For each cluster of points, compute the convex hull using Graham Scan. 
  5. Find minimum fitting bounding box around each convex hull using rotating calipers algorithm.
  6. Encode clusters as pcd bytes and geometries.

## References

 1. [Scikit Learn DBSCAN documentation](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
 2. [Scikit Learn Linear RANSAC documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html)
 3. [Graham Scan Algorithm](https://en.wikipedia.org/wiki/Graham_scan)
 4. [Rotating Calipers](https://en.wikipedia.org/wiki/Rotating_calipers)
 5. [**P**oint **C**loud **D**ata File Format](https://pointclouds.org/documentation/tutorials/pcd_file_format.html)

## Troubleshooting



