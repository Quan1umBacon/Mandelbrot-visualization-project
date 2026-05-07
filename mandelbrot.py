import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time

start = time.time()
#Define resolution of plot
width, height = 800, 600
#Define axis of plot
re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
#Define maximum number of iterations
max_iter=300


def create_c_plane (re_min=-2.5, re_max=1, im_min=-1.25, im_max=1.25, width=width, height=height):
    c_plane_re = np.linspace(re_min,re_max,width)
    c_plane_im = np.linspace(im_min,im_max,height)
    RE, IM = np.meshgrid(c_plane_re,c_plane_im)
    C = RE + 1j*IM
    return C
    
c_plane=create_c_plane()

def compute_mandelbrot(c_plane, max_iter=max_iter):
    Z = np.zeros((c_plane.shape), dtype=complex) #aktuelle z-Werte
    iteration_count = np.zeros((c_plane.shape), dtype=int)
    active = np.ones((c_plane.shape), dtype=bool) #tracker, noch nicht entkommen 

    for i in range(max_iter):
        Z[active] = (Z**2 + c_plane)[active]
        active= abs(Z) < 2
        iteration_count[active]+= 1

    return iteration_count

result_array_2d = compute_mandelbrot(c_plane)
# plt.imshow(result_array_2d, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap='inferno', norm=colors.LogNorm())
# plt.xlabel("Re", labelpad=10, loc='right')
# plt.ylabel("Im", rotation=0, labelpad=5, loc='top')
# plt.show()

end = time.time()
print(end - start)

