__global__ void various_matrix_mult(float *A, float *B, float *C, int m, int n, int o)
{

  const uint wA = n;
  const uint wB = o;  

  // Block index
  const uint bx = blockIdx.x;
  const uint by = blockIdx.y;

  // Thread index
  const uint tx = threadIdx.x;
  const uint ty = threadIdx.y;

  int row = blockIdx.y * %(TILE_SIZE)s + threadIdx.y;
  int col = blockIdx.x * %(TILE_SIZE)s + threadIdx.x;

  // Index of the first sub-matrix of A processed by the block
  const uint aBegin = wA * %(BLOCK_SIZE)s * by;

  // Index of the last sub-matrix of A processed by the block
  const uint aEnd = aBegin + wA - 1;

  // Step size used to iterate through the sub-matrices of A
  const uint aStep = %(BLOCK_SIZE)s;

  // Index of the first sub-matrix of B processed by the block
  const uint bBegin = %(BLOCK_SIZE)s * bx;

  // Step size used to iterate through the sub-matrices of B
  const uint bStep = %(BLOCK_SIZE)s * wB;

  // The element of the block sub-matrix that is computed by the thread
  float Csub = 0;

  // Loop over all the sub-matrices of A and B required to compute the block sub-matrix

  for (int a = aBegin, b = bBegin; a <= aEnd; a += aStep, b += bStep) 
    {
      // Shared memory for the sub-matrix of A
      __shared__ float As[%(BLOCK_SIZE)s][%(BLOCK_SIZE)s];
      // Shared memory for the sub-matrix of B
      __shared__ float Bs[%(BLOCK_SIZE)s][%(BLOCK_SIZE)s];

      // Load the matrices from global memory to shared memory, each thread loads one element of each matrix
      if (a + tx - wA * by * %(BLOCK_SIZE)s < n)
      As[ty][tx] = A[a + wA * ty + tx];
      else
      As[ty][tx] = 0.0;
      if (((b + wB*ty)-%(BLOCK_SIZE)s*bx)/wB < n)
      Bs[ty][tx] = B[b + wB * ty + tx];
      else
      Bs[ty][tx] = 0.0;

// if (a + tx - wA * by * %(BLOCK_SIZE)s < n)
// if (((b + wB*ty)-%(BLOCK_SIZE)s*bx)/wB < n)

      // Synchronize to make sure the matrices are loaded
      __syncthreads();

      // Multiply the two matrices together; each thread computes one element of the block sub-matrix

      for (int k = 0; k < %(BLOCK_SIZE)s; ++k)
        Csub += As[ty][k] * Bs[k][tx];

      // Synchronize to make sure that the preceding computation is done before loading two new sub-matrices of A and B in the next iteration
      __syncthreads();
    }

  // Write the block sub-matrix to global memory; each thread writes one element
  
  const uint c = wB * %(BLOCK_SIZE)s * by + %(BLOCK_SIZE)s * bx;
  if (row < m  && col < o)
  C[c + wB * ty + tx] = Csub;
}
