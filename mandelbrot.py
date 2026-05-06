import numpy as np
import matplotlib.pyplot as plt

#Define resolution of plot
width=800
height=600

def iterate_z(c, max_iter=200):
    z=0
    num_iter=0
    while abs(z) < 2 and num_iter < max_iter:
        z = z**2 + c 
        num_iter +=1
    return(num_iter)


def create_c_plane (re_min=-2.5, re_max=1, im_min=-1.25, im_max=1.25, width=width, height=height):
    c_plane_re = np.linspace(re_min,re_max,width)
    c_plane_im = np.linspace(im_min,im_max,height)
    c_plane=[]
    for im in c_plane_im:
        for re in c_plane_re:
            c_plane.append(re + 1j*im)
    return c_plane
    
c_plane=create_c_plane()

def compute_mandelbrot(c_plane):
    iteration_array= [iterate_z(c) for c in c_plane]
    return iteration_array

iteration_array = compute_mandelbrot(c_plane)
result_array_1d= np.array(iteration_array)
result_array_2d= result_array_1d.reshape(height,width)
plt.imshow(result_array_2d)
plt.show()