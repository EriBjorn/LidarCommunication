import numpy as np
import open3d as o3d
import time
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

def main():
    for i in range(1,403):
        mesh = o3d.io.read_point_cloud('2020-10-26 22-08-56_vertikal/' + str(i) + '.pcd')
        #print(mesh)
        o3d.io.write_point_cloud(filename='point_clouds/pc'+str(i)+'.pcd', pointcloud=mesh, write_ascii=True, print_progress=True)
        
def get_only_value_data(path=''):
    z=[]
    if path == '':
        print('Enter a path..')
    else:
        dataset = np.load(path, 'r+')
        n = 0
        for i in np.nditer(dataset, flags=["external_loop"], order='F'):   
            for j in range(0, 24): 
                z.append(i[j])
            n = n+1  
    return z

def get_only_value_data_float(path=''):
    x = []
    y = []
    z = []
    if path == '':
        print('Enter a path..')
    else:
        dataset = np.load(path, 'r+')
        n = 0
        k = 0

        for i in np.nditer(dataset, flags=["external_loop"], order='F'):   
            for j in range(0, 24): 
                x.append(j)
                y.append(n)
                z.append(i[j])
                k = k+1
            n = n+1  
    return z


def draw_as_graph(z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(0, 24):
        for j in range(0,320):
            if z[i,j] > 0 and z[i,j] <= 400:
                ax.scatter(xs=i, ys=j, zs=z[i,j], marker='o')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.show()
    

if __name__ == "__main__":
    z_data = get_only_value_data('float_test/npy/pcl15.npy')
    z= []
    
    z.append(z_data)
    z_ = np.array(z)
    z_ = np.reshape(z_, (24,320))

    draw_as_graph(z_)