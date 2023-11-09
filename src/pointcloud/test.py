from pointcloud.point_cloud import PointCloud, PlanarPointCloud
from pointcloud.decode_pcd import *
from pointcloud.encode_pcd import *
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

path_to_pcd = "./src/data/pointcloud_data.pcd"



def test_decode_pcd(pcd_bytes):
    pc = decode_pcd_bytes(pcd_bytes)
    return pc


def test_encode(pc):
    encoder = Encoder(pc.metadata)
    pcd_bytes = encoder.encode(pc)
    return pcd_bytes


def test_projection(path_to_pcd):
    with open(path_to_pcd, 'rb') as file:
        pcd_bytes = file.read()
    pc = decode_pcd_bytes(pcd_bytes)
    ppc1 = pc.get_planar_from_3D('detect')
    ppc2 = pc.get_planar_from_3D()
    print(ppc1.points.all() == ppc2.points.all)
    ppc1.plot()
    ppc2.plot()
    plt.show()


    
test_projection(path_to_pcd)

points = []
n_points = 10
for i in range(n_points):
    x, y = np.random.randint(-10, 10)
    z = -(x+y)
    points.append([x, y, z])
    
    
fake_pc = PointCloud(points)
ppc = fake_pc.get_planar_from_3D('detect')


# pcd_bytes2 = encode_pointcloud_to_pcd_bytes(pc)

# bunny_path =  './src/data/bunny_ascii.pcd'
# encoded_pcd_output_path  = './src/data/output_test.pcd'
# with open(encoded_pcd_output_path, 'wb') as f:
#     f.write(pcd_bytes2)

# pcd = o3d.io.read_point_cloud(encoded_pcd_output_path)
# pcd_poinnts = np.array(pcd.points)
# print(pcd_poinnts.shape)
# print(pcd_poinnts.max())


# ppc = pc.get_planar_from_3D()

# print("FINISHED")