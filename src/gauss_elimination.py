def gauss_elimination(A, b):
    """
    Solves the linear system Ax = b using Gaussian Elimination with partial pivoting and back-substitution.
    Includes checks for singular matrices, diagonal dominance, and calculates mean absolute error.

    Parameters:
    A (list of lists): Coefficient matrix (n x n)
    b (list): Constant vector (n elements)

    Returns:
    tuple: (solution vector x, mean absolute error, is_diagonally_dominant)

    Raises:
    ValueError: If matrix is singular or nearly singular
    """
    n = len(A)
    # Check diagonal dominance before any operations
    is_diagonally_dominant: bool = check_diagonal_dominance(A)

    # Create a deep copy of A to avoid modifying the input
    augmented = [row[:] for row in A]
    original_A = [row[:] for row in A]  # Keep original A for error calculation
    # Augment the matrix with b
    for i in range(n):
        augmented[i].append(b[i])

    # Forward elimination
    for i in range(n):
        # Partial pivoting
        max_row = max(range(i, n), key=lambda r: abs(augmented[r][i]))
        if abs(augmented[max_row][i]) < 1e-4:  # Stricter tolerance for singularity
            raise ValueError("Matrix is singular or nearly singular")

        if max_row != i:
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

        # Eliminate below the pivot row
        for j in range(i + 1, n):
            factor = augmented[j][i] / augmented[i][i]
            for k in range(i, n + 1):
                augmented[j][k] -= factor * augmented[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        if abs(augmented[i][i]) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular")

        sum_ax = sum(augmented[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (augmented[i][n] - sum_ax) / augmented[i][i]
        # Store the solution back into augmented matrix so we can extract it as before
        augmented[i][n] = x[i]

    # Extract solution
    solution = [row[-1] for row in augmented]

    # Calculate mean absolute error
    mae = calculate_mae(original_A, solution, b)

    return solution, mae, is_diagonally_dominant


def check_diagonal_dominance(A):
    """
    Checks if matrix A is diagonally dominant.
    A matrix is diagonally dominant if for each row, the absolute value of the diagonal
    element is greater than the sum of absolute values of all other elements in that row.
    """
    n = len(A)
    for i in range(n):
        diagonal = abs(A[i][i])
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diagonal <= row_sum:
            return False
    return True


def calculate_mae(A, x, b):
    """
    Calculates the mean absolute error between Ax and b.

    Parameters:
    A (list of lists): Original coefficient matrix
    x (list): Solution vector
    b (list): Original constant vector

    Returns:
    float: Mean absolute error
    """
    n = len(A)
    errors = []
    for i in range(n):
        # Calculate Ax for this row
        ax_i = sum(A[i][j] * x[j] for j in range(n))
        # Calculate absolute error
        errors.append(abs(ax_i - b[i]))
    return sum(errors) / n
