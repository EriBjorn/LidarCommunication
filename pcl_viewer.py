import numpy as np
import open3d as o3
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.ma.bench import xs, ys


from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter



# Template for visualising 3D coordinates


def prove():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X ** 2 + Y ** 2)
    Z = np.sin(R)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


# Visualise npy file
def npyviewer():
    cloud = np.load("pointcloud.npy")
    plt.plot(cloud, 'bo')
    plt.matshow(cloud)
    plt.colorbar()
    plt.show()


def plyviewer():

    cloud = o3.io.read_point_cloud("128.pcd")  # Read the point cloud
    o3.visualization.draw_geometries([cloud])  # Visualize the point cloud





def main():
    #npyviewer()
    #prove()
    #setFPS(20)
    plyviewer()


if __name__ == '__main__':
    main()
