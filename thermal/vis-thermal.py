import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import seeed_mlx9064x

# Configuration for MLX90641 or MLX90640
CHIP_TYPE = 'MLX90640'  # Change to 'MLX90641' if using MLX90641

if CHIP_TYPE == 'MLX90641':
    mlx = seeed_mlx9064x.grove_mxl90641()
    mlx_shape = (12, 16)  # MLX90641 has 192 pixels
    frame = [0] * 192
elif CHIP_TYPE == 'MLX90640':
    mlx = seeed_mlx9064x.grove_mxl90640()
    mlx_shape = (24, 32)  # MLX90640 has 768 pixels
    frame = [0] * 768

mlx.refresh_rate = seeed_mlx9064x.RefreshRate.REFRESH_8_HZ  # The fastest for Raspberry Pi 4

# Interpolation factor
mlx_interp_val = 10  # interpolate by this factor on each dimension
mlx_interp_shape = (mlx_shape[0] * mlx_interp_val, mlx_shape[1] * mlx_interp_val)  # new shape

# Setting up the plot
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111)
fig.subplots_adjust(0.05, 0.05, 0.95, 0.95)  # remove unnecessary padding

# Initial plot
therm1 = ax.imshow(np.zeros(mlx_interp_shape), interpolation='none', cmap=plt.cm.bwr, vmin=25, vmax=45)
cbar = fig.colorbar(therm1)
cbar.set_label('Temperature [$^{\circ}$C]', fontsize=14)

fig.canvas.draw()
ax_background = fig.canvas.copy_from_bbox(ax.bbox)
fig.show()

def plot_update():
    fig.canvas.restore_region(ax_background)
    mlx.getFrame(frame)
    data_array = np.fliplr(np.reshape(frame, mlx_shape))  # reshape and flip data
    data_array = ndimage.zoom(data_array, mlx_interp_val)  # interpolate
    therm1.set_array(data_array)
    therm1.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))  # update color range
    cbar.on_mappable_changed(therm1)

    ax.draw_artist(therm1)
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()

t_array = []
while True:
    t1 = time.monotonic()
    try:
        plot_update()
    except Exception as e:
        print("Error:", e)
        continue
    t_array.append(time.monotonic() - t1)
    if len(t_array) > 10:
        t_array = t_array[1:]  # keep recent times for frame rate calculation
    print('Frame Rate: {0:2.1f} fps'.format(len(t_array) / np.sum(t_array)))
