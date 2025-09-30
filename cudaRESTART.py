import numpy as np
from numba import cuda
import gc

# Define a simple CUDA kernel
@cuda.jit
def double_elements(arr):
    idx = cuda.grid(1)
    if idx < arr.size:
        arr[idx] *= 2

# Allocate host array
host_array = np.arange(1000, dtype=np.float32)

# Allocate device array and copy data
device_array = cuda.to_device(host_array)

# Launch kernel
threads_per_block = 256
blocks_per_grid = (host_array.size + threads_per_block - 1) // threads_per_block
double_elements[blocks_per_grid, threads_per_block](device_array)

# Copy result back to host
result = device_array.copy_to_host()
print("Sample output:", result[:5])

# Cleanup
del device_array
gc.collect()
cuda.current_context().deallocations.clear()