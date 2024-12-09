def gauss_jordan(A, b):
    """
    Solves the linear system Ax = b using Gauss-Jordan Elimination with partial pivoting.

    Parameters:
    A (list of lists): Coefficient matrix (n x n)
    b (list): Constant vector (n elements)

    Returns:
    list: Solution vector x (n elements)
    """
    n = len(A)
    # Create a deep copy of A to avoid modifying the input
    augmented = [row[:] for row in A]  # Deep copy the coefficient matrix
    # Augment the matrix with b
    for i in range(n):
        augmented[i].append(b[i])

    # Forward elimination and normalization
    for i in range(n):
        # Partial pivoting
        max_row = max(range(i, n), key=lambda r: abs(augmented[r][i]))
        if abs(augmented[max_row][i]) < 1e-4:
            raise ValueError("Matrix is singular or nearly singular")

        if max_row != i:
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

        # Normalize the pivot row
        pivot = augmented[i][i]
        for j in range(i, n + 1):
            augmented[i][j] /= pivot

        # Eliminate both below and above (full reduction)
        for j in range(n):
            if j != i:  # Skip the pivot row
                factor = augmented[j][i]
                for k in range(i, n + 1):  # Include the augmented column
                    augmented[j][k] -= factor * augmented[i][k]

    # The solution is now directly available in the augmented column
    return [row[-1] for row in augmented]
