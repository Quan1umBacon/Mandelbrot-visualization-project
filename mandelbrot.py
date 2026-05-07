import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

#Define resolution of plot
width = 800
height = int(width/4*3)
#Define axis of initial plot
re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
#Define maximum number of iterations
max_iter=400
#Define zoom factor for zoom function on click
zoom_factor = 6

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

def on_click(event):
    re_click = event.xdata 
    im_click = event.ydata
    global re_min, re_max, im_min, im_max
    re_width = re_max - re_min
    im_height = im_max - im_min
    re_min = re_click - (re_width)/(2*zoom_factor)
    re_max = re_click + (re_width)/(2*zoom_factor)
    im_min = im_click - (im_height)/(2*zoom_factor)
    im_max = im_click + (im_height)/(2*zoom_factor)
    new_plane = create_c_plane(re_min, re_max, im_min, im_max)
    result = compute_mandelbrot(new_plane)
    ax.imshow(result, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap='inferno', norm=colors.LogNorm())
    ax.set_xlabel("Re", labelpad=10, loc='right')
    ax.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
    fig.canvas.draw()

fig, ax = plt.subplots()
result_array_2d = compute_mandelbrot(c_plane)
ax.imshow(result_array_2d, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap='inferno', norm=colors.LogNorm())
ax.set_xlabel("Re", labelpad=10, loc='right')
ax.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
fig.canvas.mpl_connect('button_press_event', on_click) #Event-Handler
plt.show()

