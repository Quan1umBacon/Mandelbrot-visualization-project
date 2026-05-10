#---------------Imports-----------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap

#---------------Parameters---------------------------------
print('Click in plot to zoom in.')
print('Press c to change color map.')
print('Press r to reset to full view.')
#Define resolution of plot
width = 1000
#Define axis of initial plot
re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
#Define initial maximum number of iterations
max_iter=500
#Set dynamic iterations 'on' or 'off'
dynamic_iterations='on'
# Set julia plots 'on' or 'off'
julia_set_active='off'
#Define julia axis
j_re_min, j_re_max, j_im_min, j_im_max= -2, 2, -1.5, 1.5
#Define zoom factor for zoom function on click
zoom_factor = 6

#Define color maps to be interated through when c is pressed
colors_list = ['orange', 'yellow', 'white', 'cyan', 'blue', 'darkblue', 'black']
custom_cmap = LinearSegmentedColormap.from_list('mandelbrot', colors_list)
cmaps = ['Greys', custom_cmap, 'inferno','twilight','bone','terrain']

#---------------------------------------global variables-----------------------------------------------
height = int(width/4*3)
zoom_level = 1
cmap_index = 0
max_iter_dynamic = max_iter
#-----------------------------------------Functions----------------------------------------------------

def create_c_plane (re_min=-2.5, re_max=1, im_min=-1.25, im_max=1.25, width=width, height=height):
    c_plane_re = np.linspace(re_min,re_max,width)
    c_plane_im = np.linspace(im_min,im_max,height)
    RE, IM = np.meshgrid(c_plane_re,c_plane_im)
    C = RE + 1j*IM
    return C
    
def compute_mandelbrot(c_plane, max_iter=max_iter):
    Z = np.zeros((c_plane.shape), dtype=complex) #aktuelle z-Werte
    iteration_count = np.zeros((c_plane.shape), dtype=int) #array the same size as Z to track the iteration count, starts with all zeros
    active = np.ones((c_plane.shape), dtype=bool) #tracker, noch nicht entkommen   
    for i in range(max_iter):
        Z[active] = (Z**2 + c_plane)[active]
        active= abs(Z) < 2
        iteration_count[active]+= 1
    
    return iteration_count

def compute_julia(z_plane, c, max_iter=max_iter):
    Z = z_plane.copy() # Copy of the input array, to not alter the original
    iteration_count = np.zeros((z_plane.shape), dtype=int) #array the same size as Z to track the iteration count, starts with all zeros
    active = np.ones((z_plane.shape), dtype=bool) #boolean tracker; tracks each array position, if iteration is active or not
    for i in range(max_iter):
        Z[active] = (Z**2 + c)[active]
        active= abs(Z) < 2
        iteration_count[active]+= 1
    
    return iteration_count


# Left click to zoom
def on_click(event):
    global re_min, re_max, im_min, im_max, zoom_level, max_iter_dynamic
    if event.button == 1: #Left click
        re_click = event.xdata # real part of the clicked point (matplotlib converts pixel -> plot coordinates using extent)
        im_click = event.ydata # imaginary part of the clicked point
        zoom_level*=zoom_factor
        if dynamic_iterations == 'on':
            max_iter_dynamic = int(max_iter + 50*np.log10(zoom_level + 1))
        else:
            max_iter_dynamic=max_iter
        re_width = re_max - re_min
        im_height = im_max - im_min
        re_min = re_click - (re_width)/(2*zoom_factor)
        re_max = re_click + (re_width)/(2*zoom_factor)
        im_min = im_click - (im_height)/(2*zoom_factor)
        im_max = im_click + (im_height)/(2*zoom_factor)
        new_plane = create_c_plane(re_min, re_max, im_min, im_max)
        result = compute_mandelbrot(new_plane, max_iter=max_iter_dynamic)
        ax1.images[0].set_data(result)
        ax1.images[0].set_extent([re_min, re_max, im_min, im_max])
        ax1.images[0].set_clim(result.min(), result.max())
        cmap_name = cmaps[cmap_index] if isinstance(cmaps[cmap_index], str) else 'custom'
        ax1.set_title(f"Zoom factor: {zoom_level} | Maximum Iterartions: {max_iter_dynamic} | Color map: {cmap_name}")
        fig.canvas.draw()
    elif event.button == 3 and julia_set_active == 'on': #Right click
        re_click = event.xdata # real part of the clicked point (matplotlib converts pixel -> plot coordinates using extent)
        im_click = event.ydata # imaginary part of the clicked point
        c = re_click + 1j*im_click
        julia_plane = compute_julia(j_plane, c=c, max_iter=max_iter)
        ax2.images[0].set_data(julia_plane)
        ax2.images[0].set_extent([j_re_min, j_re_max, j_im_min, j_im_max])
        ax2.images[0].set_clim(julia_plane.min(), julia_plane.max())
        fig.canvas.draw()
  

# Press c for changing color map; Press r to reset to full set view
def on_key(event):
    global cmap_index, zoom_level, max_iter_dynamic, re_min, re_max, im_min, im_max, result_array_2d
    key_press = event.key
    if key_press == 'c':
        cmap_index= (cmap_index +1) % len(cmaps)
        cmap=cmaps[cmap_index]
        cmap_name = cmaps[cmap_index] if isinstance(cmaps[cmap_index], str) else 'custom'
        ax1.images[0].set_cmap(cmap)
        ax1.set_title(f"Zoom factor: {zoom_level} | Maximum Iterartions: {max_iter_dynamic} | Color map: {cmap_name}")
        if julia_set_active == 'on':
            ax2.images[0].set_cmap(cmap)
        fig.canvas.draw()
    elif key_press == 'r':
        zoom_level = 1
        max_iter_dynamic = max_iter
        re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
        c_plane=create_c_plane()
        result_array_2d = compute_mandelbrot(c_plane)
        ax1.images[0].set_data(result_array_2d)
        ax1.images[0].set_extent([re_min, re_max, im_min, im_max])
        ax1.images[0].set_clim(result_array_2d.min(), result_array_2d.max())
        fig.canvas.draw()
    
        
#---------------------------------------------------------------------------------------------------------------------------------------


c_plane=create_c_plane()
j_plane=create_c_plane(re_min=j_re_min, re_max=j_re_max, im_min=j_im_min, im_max=j_im_max)
result_array_2d = compute_mandelbrot(c_plane)
julia_array_init = compute_julia(j_plane,c=0)
if julia_set_active== 'on':

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    ax1.imshow(result_array_2d, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap=cmaps[cmap_index], norm=colors.PowerNorm(gamma=0.5))
    ax1.set_xlabel("Re", labelpad=10, loc='right')
    ax1.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
    ax1.set_title(f"Zoom factor: 1 | Maximum Iterartions: {max_iter} | Color map: {cmaps[cmap_index]}")
    ax2.imshow(julia_array_init, origin='lower', extent=[j_re_min, j_re_max, j_im_min, j_im_max], cmap=cmaps[cmap_index], norm=colors.PowerNorm(gamma=0.5))
    ax2.set_xlabel("Re", labelpad=10, loc='right')
    ax2.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
    
else:
    fig, ax1 = plt.subplots(figsize=(16, 10))
    ax1.imshow(result_array_2d, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap=cmaps[cmap_index], norm=colors.PowerNorm(gamma=0.5))
    ax1.set_xlabel("Re", labelpad=10, loc='right')
    ax1.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
    ax1.set_title(f"Zoom factor: 1 | Maximum Iterartions: {max_iter} | Color map: {cmaps[cmap_index]}")
 
    
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')  
# Register on_click as a callback for mouse click events on the figure.
# Whenever the user clicks, matplotlib creates an event object containing
# click information (coordinates, button, etc.) and passes it to on_click.
fig.canvas.mpl_connect('button_press_event', on_click) #Event-Handler
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()

