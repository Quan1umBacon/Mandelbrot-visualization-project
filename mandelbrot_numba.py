#---------------Imports-----------------
from numba import njit, prange
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
import time

#---------------Parameters---------------------------------
print('Welcome to infinity! With this python script you will be able to render and zoom into the Mandelbrot set!')
print('Zoom into set with left click.')
print('Press c to change color map.')
print('Press r to reset to full view.')


#Define axis of initial plot
re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
#Define initial maximum number of iterations
max_iter=600
#Set dynamic iterations 'on' or 'off'
dynamic_iterations='on'
# Set julia plots 'on' or 'off'
julia_set_active=input('Do you want to output julia sets alongside the mandelbrot set, type "on": ')
#Define resolution of plot
width=int(input('Set resolution of mandelbrot render. Numbers between 600-1900 are advised. Higher number will slow rendering: '))
#Define julia axis
j_re_min, j_re_max, j_im_min, j_im_max= -2, 2, -1.5, 1.5
#Define zoom factor for zoom function on click
zoom_factor = 4
#Define color maps to be interated through when c is pressed
colors_list = ['darkblue','blue','cyan','white','yellow','orange','red','black']
custom_cmap = LinearSegmentedColormap.from_list('mandelbrot', colors_list)
cmaps = [custom_cmap,'Greys','inferno','twilight','bone','terrain']

print('Numba compiling ...')
#---------------------------------------global variables-----------------------------------------------
height = int(width/4*3)
julia_width = 600
julia_heigth = int(julia_width/4*3)
zoom_level = 1
cmap_index = 0
max_iter_dynamic = max_iter
last_render=0
throttle_ms=130
c_now=0j
#-----------------------------------------Functions----------------------------------------------------

# Create a grid of points on the complex plane. Outputs a 2-d array with complex numbers evenly spaced over the complex plane within specified boundaries.
def create_c_plane (re_min=-2.5, re_max=1, im_min=-1.25, im_max=1.25, width=width, height=height):
    c_plane_re = np.linspace(re_min,re_max,width) # create 1d array  in re-dimension
    c_plane_im = np.linspace(im_min,im_max,height) # create 1d array in im-dimension
    RE, IM = np.meshgrid(c_plane_re,c_plane_im) # create rectangular 2d-grids of the re and im values
    C = RE + 1j*IM # fuse the grids together to create one 2d-grid of complex numbers
    return C


@njit
def iterate_z_numba(c, max_iter):
    z=0j
    num_iter=0
    while abs(z) < 2 and num_iter < max_iter:
        z = z**2 + c 
        num_iter = num_iter + 1
    return(num_iter)

@njit(parallel=True)
def compute_mandelbrot_numba(c_flat, max_iter):
    mandel_array = np.zeros(len(c_flat), dtype=np.int32) #create full-sized array, allocates full memory for numba
    for i in prange(len(c_flat)):
        mandel_array[i]=iterate_z_numba(c_flat[i], max_iter)
    return mandel_array


@njit
def iterate_z_julia_numba(z, c, max_iter):
    num_iter=0
    while abs(z) < 2 and num_iter < max_iter:
        z = z**2 + c 
        num_iter = num_iter + 1
    return(num_iter)

@njit(parallel=True)
def compute_julia(z_flat,c, max_iter):
    julia_array = np.zeros(len(z_flat), dtype=np.int32) #create full-sized array, allocates full memory for numba
    for i in prange(len(z_flat)):
        julia_array[i]=iterate_z_julia_numba(z=z_flat[i],c=c, max_iter=max_iter )
    return julia_array


# Left click to zoom
def on_click(event):
    # Variables are set as global. If they are changed in the function, they change globally
    global re_min, re_max, im_min, im_max, zoom_level, max_iter_dynamic
    #Left click - Zoom event
    if event.button == 1: #Registers Left click on mouse
        re_click = event.xdata # real part of the clicked point (matplotlib converts pixel -> plot coordinates using extent)
        im_click = event.ydata # imaginary part of the clicked point
        zoom_level*=zoom_factor # tracks the zoom factor
        if dynamic_iterations == 'on': #increases iterations maximum with increased zoom_level, if activated
            max_iter_dynamic = int(max_iter + 50*np.log10(zoom_level + 1))
        else:
            max_iter_dynamic=max_iter
        #Calculating new render area
        re_width = re_max - re_min
        im_height = im_max - im_min
        re_min = re_click - (re_width)/(2*zoom_factor)
        re_max = re_click + (re_width)/(2*zoom_factor)
        im_min = im_click - (im_height)/(2*zoom_factor)
        im_max = im_click + (im_height)/(2*zoom_factor)
        new_plane = create_c_plane(re_min, re_max, im_min, im_max) #Create complex grid on new render area
        result = compute_mandelbrot_numba(new_plane.flatten(), max_iter=max_iter_dynamic).reshape(height,width) #Compute Mandelbrot on new render area
        ax1.images[0].set_data(result) # Replaces the old mandelbrot array with the new calculated one
        ax1.images[0].set_extent([re_min, re_max, im_min, im_max]) # updates the axis labels
        ax1.images[0].set_clim(result.min(), result.max()) # updates the color-mapping on new min and max values
        cmap_name = cmaps[cmap_index] if isinstance(cmaps[cmap_index], str) else 'custom' # clear depiction of custom cmaps in plot title
        ax1.set_title(f"Zoom factor: {zoom_level} | Maximum Iterartions: {max_iter_dynamic} | Color map: {cmap_name}") # Update plot title
        fig.canvas.draw() # draw everything new with the updated information

# Press c for changing color map; Press r to reset to full set view
def on_key(event):
    # Variables are set as global. If they are changed in the function, they change globally
    global cmap_index, zoom_level, max_iter_dynamic, re_min, re_max, im_min, im_max, result_array_2d 
    key_press = event.key # store, which key was pressed in variable kay_press
    if key_press == 'c':
        cmap_index= (cmap_index +1) % len(cmaps) # iterate through an index the length of the number of defined color maps
        cmap=cmaps[cmap_index] # set color map as per cmap_index
        cmap_name = cmaps[cmap_index] if isinstance(cmaps[cmap_index], str) else 'custom' # clear depiction of custom cmaps in plot title
        ax1.images[0].set_cmap(cmap) # update color map in image-object
        ax1.set_title(f"Zoom factor: {zoom_level} | Maximum Iterartions: {max_iter_dynamic} | Color map: {cmap_name}") # Update plot title
        if julia_set_active == 'on':
            ax2.images[0].set_cmap(cmap) # update color map in image-object also for julia plot
        fig.canvas.draw() # draw everything new with the updated information
    elif key_press == 'r':
        zoom_level = 1 # reset to zoom level 1 (start-default)
        max_iter_dynamic = max_iter # reset max_iterations to start default
        re_min, re_max, im_min, im_max= -2.5, 1, -1.25, 1.25
        c_plane=create_c_plane() # create default complex plane
        result_array_2d = compute_mandelbrot_numba(c_plane.flatten(),max_iter).reshape(height,width) # create mandelbrot set on default complex plane
        ax1.images[0].set_data(result_array_2d) # Replaces the old mandelbrot array with the new calculated one
        ax1.images[0].set_extent([re_min, re_max, im_min, im_max]) # updates the axis labels
        ax1.images[0].set_clim(result_array_2d.min(), result_array_2d.max()) # updates the color-mapping on new min and max values
        fig.canvas.draw() # draw everything new with the updated information

def on_motion(event):
    global last_render, c_now
    if julia_set_active == 'on':
        if event.inaxes != ax1: #checks if cursor is in plot
            return
        now =time.time()
        if now - last_render < throttle_ms / 1000: # skipps on_motion rate for a period of time
            return
        last_render = now
        re_click = event.xdata # real part of the clicked point (matplotlib converts pixel -> plot coordinates using extent)
        im_click = event.ydata # imaginary part of the clicked point
        c = re_click + 1j*im_click # create complex number that has been right clicked
        c_now = c
        julia_plane = compute_julia(j_plane.flatten(), c=c, max_iter=max_iter).reshape(julia_heigth,julia_width)
        ax2.images[0].set_data(julia_plane) # Replaces the old julia array with the new calculated one
        ax2.images[0].set_extent([j_re_min, j_re_max, j_im_min, j_im_max]) # updates the axis label
        ax2.images[0].set_clim(julia_plane.min(), julia_plane.max()) # updates the color-mapping on new min and max values
        ax2.set_title(f"Julia set at point c=: {c_now:.3f}")
        fig.canvas.draw() # draw everything new with the updated information

    
        
#---------------------------------------------------Execution------------------------------------------------------------------------------------

# Mandelbrot array creation
c_plane=create_c_plane()
result_array_2d = compute_mandelbrot_numba(c_plane.flatten(),max_iter).reshape(height,width)
# Default (0/0) Julia array creation
j_plane=create_c_plane(re_min=j_re_min, re_max=j_re_max, im_min=j_im_min, im_max=j_im_max, width=julia_width, height=julia_heigth)
julia_array_init = compute_julia(j_plane.flatten(),c=0, max_iter=max_iter).reshape(julia_heigth,julia_width)

if julia_set_active== 'on':

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    ax1.imshow(result_array_2d, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap=cmaps[cmap_index], norm=colors.PowerNorm(gamma=0.65))
    ax1.set_xlabel("Re", labelpad=10, loc='right')
    ax1.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
    cmap_name = cmaps[cmap_index] if isinstance(cmaps[cmap_index], str) else 'custom' # clear depiction of custom cmaps in plot title
    ax1.set_title(f"Zoom factor: 1 | Maximum Iterartions: {max_iter} | Color map: {cmap_name}")
    ax2.imshow(julia_array_init, origin='lower', extent=[j_re_min, j_re_max, j_im_min, j_im_max], cmap=cmaps[cmap_index], norm=colors.PowerNorm(gamma=0.65))
    ax2.set_xlabel("Re", labelpad=10, loc='right')
    ax2.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
    
else:
    fig, ax1 = plt.subplots(figsize=(16, 10))
    ax1.imshow(result_array_2d, origin='lower', extent=[re_min, re_max, im_min, im_max], cmap=cmaps[cmap_index], norm=colors.PowerNorm(gamma=0.65))
    ax1.set_xlabel("Re", labelpad=10, loc='right')
    ax1.set_ylabel("Im", rotation=0, labelpad=5, loc='top')
    ax1.set_title(f"Zoom factor: 1 | Maximum Iterartions: {max_iter} | Color map: {cmaps[cmap_index]}")
 
    
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')  
# Register on_click as a callback for mouse click events on the figure. Whenever the user clicks, 
# matplotlib creates an event object containing click information (coordinates, button, etc.) and passes it to on_click.
fig.canvas.mpl_connect('button_press_event', on_click) #Event-Handler
fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
plt.tight_layout()
plt.show()

