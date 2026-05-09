import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

#Define resolution of plot
width = 1000
height = int(width/4*3)
#Define axis of initial plot
re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
#Define maximum number of iterations
max_iter=500
#Define zoom factor for zoom function on click
zoom_factor = 6
#
cmaps = ['inferno', 'hot', 'plasma', 'viridis', 'twilight']
cmap_index = 0

def create_c_plane (re_min=-2.5, re_max=1, im_min=-1.25, im_max=1.25, width=width, height=height):
    c_plane_re = np.linspace(re_min,re_max,width)
    c_plane_im = np.linspace(im_min,im_max,height)
    RE, IM = np.meshgrid(c_plane_re,c_plane_im)
    C = RE + 1j*IM
    return C
    
def compute_mandelbrot(c_plane, max_iter=max_iter):
    Z = np.zeros((c_plane.shape), dtype=complex) #aktuelle z-Werte
    iteration_count = np.zeros((c_plane.shape), dtype=int)
    active = np.ones((c_plane.shape), dtype=bool) #tracker, noch nicht entkommen 

    for i in range(max_iter):
        Z[active] = (Z**2 + c_plane)[active]
        active= abs(Z) < 2
        iteration_count[active]+= 1

    return iteration_count

# Left click to zoom
def on_click(event):
    re_click = event.xdata # real part of the clicked point (matplotlib converts pixel -> plot coordinates using extent)
    im_click = event.ydata # imaginary part of the clicked point
    global re_min, re_max, im_min, im_max
    re_width = re_max - re_min
    im_height = im_max - im_min
    re_min = re_click - (re_width)/(2*zoom_factor)
    re_max = re_click + (re_width)/(2*zoom_factor)
    im_min = im_click - (im_height)/(2*zoom_factor)
    im_max = im_click + (im_height)/(2*zoom_factor)
    new_plane = create_c_plane(re_min, re_max, im_min, im_max)
    result = compute_mandelbrot(new_plane)
    ax.images[0].set_data(result)
    ax.images[0].set_extent([re_min, re_max, im_min, im_max])
    ax.images[0].set_clim(result.min(), result.max())
    fig.canvas.draw()
  

# Press c for changing color map; Press r to reset to full set view
def on_key(event):
    key_press = event.key
    if key_press == 'c':
        global cmap_index
        cmap_index= (cmap_index +1) % 5
        cmap=cmaps[cmap_index]
        ax.images[0].set_cmap(cmap)
        fig.canvas.draw()
    elif key_press == 'r':
        global re_min, re_max, im_min, im_max, result_array_2d
        re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
        c_plane=create_c_plane()
        result_array_2d = compute_mandelbrot(c_plane)
        ax.images[0].set_data(result_array_2d)
        ax.images[0].set_extent([re_min, re_max, im_min, im_max])
        ax.images[0].set_clim(result_array_2d.min(), result_array_2d.max())
        fig.canvas.draw()
    
        


c_plane=create_c_plane()
fig, ax = plt.subplots()
result_array_2d = compute_mandelbrot(c_plane)
ax.imshow(result_array_2d, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap=cmaps[cmap_index], norm=colors.PowerNorm(gamma=0.5))
ax.set_xlabel("Re", labelpad=10, loc='right')
ax.set_ylabel("Im", rotation=0, labelpad=5, loc='top')

# Register on_click as a callback for mouse click events on the figure.
# Whenever the user clicks, matplotlib creates an event object containing
# click information (coordinates, button, etc.) and passes it to on_click.
fig.canvas.mpl_connect('button_press_event', on_click) #Event-Handler
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()

