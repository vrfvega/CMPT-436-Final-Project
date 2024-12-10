def gauss_elimination(A):
    n = len(A)  # Size of the matrix
    x = [0] * n  # Initialize the solution vector

    # Forward Elimination with Partial Pivoting
    for i in range(n - 1):
        # Find the row with the largest absolute value in column i
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j

        # Swap rows if needed
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]

        # Check if the matrix is singular
        if A[i][i] == 0:
            print("No unique solution")
            return []

        # Make elements below the pivot equal to zero
        for j in range(i + 1, n):
            m = A[j][i] / A[i][i]
            for k in range(i, n + 1):  # Iterate over each element in the row
                A[j][k] -= m * A[i][k]

    # Check if there's a unique solution
    if A[n - 1][n - 1] == 0:
        print("No unique solution")
        return []

    # Back Substitution
    x[n - 1] = A[n - 1][n] / A[n - 1][n - 1]
    for i in range(n - 2, -1, -1):
        sum_ax = 0
        for j in range(i + 1, n):
            sum_ax += A[i][j] * x[j]
        x[i] = (A[i][n] - sum_ax) / A[i][i]

    return x


def main():
    # User input for the augmented matrix
    print("Enter the augmented matrix row by row (leave an empty line to finish):")
    print("Each row should be space-separated values (coefficients followed by the constant term).")

    A = []
    while True:
        row = input()
        if not row.strip():  # Stop if the user enters an empty line
            break
        row = list(map(float, row.split()))
        A.append(row)

    # Check for a valid matrix
    n = len(A)
    if any(len(row) != n + 1 for row in A):
        print("Error: Invalid matrix. Each row must have exactly n + 1 values.")
        return

    # Solve using Gaussian elimination
    solution = gauss_elimination(A)
    if solution:
        for i, value in enumerate(solution):
            print(f"x{i + 1} = {value}")

        # Verify the solution by plugging into the equations
        print("\nVerification of the solution:")
        for i in range(len(A)):
            lhs = sum(A[i][j] * solution[j] for j in range(len(solution)))
            rhs = A[i][-1]
            print(f"Equation {i + 1}: LHS = {lhs:.4f} | RHS = {rhs:.4f}")


if __name__ == "__main__":
    main()
