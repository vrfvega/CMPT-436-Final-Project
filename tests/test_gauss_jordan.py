import pytest

from src.gauss_jordan import gauss_jordan


@pytest.fixture
def tolerance():
    """Fixture to set the global tolerance level for tests."""
    return 1e-6


class TestGaussJordan:
    def verify_solution(self, coefficients, constants, solution, tolerance):
        """
        Helper method to verify if a solution satisfies the system of equations.

        Args:
            coefficients (list of lists): The coefficient matrix
            constants (list): The constants vector
            solution (list): The computed solution
            tolerance (float): Acceptable error margin

        Returns:
            bool: True if solution is valid within tolerance
        """
        n = len(coefficients)
        for i in range(n):
            # Calculate left hand side of equation
            lhs = sum(coefficients[i][j] * solution[j] for j in range(n))
            # Verify it equals right hand side within tolerance
            assert (
                abs(lhs - constants[i]) < tolerance
            ), f"Equation {i+1} not satisfied: {lhs} ≠ {constants[i]}"

    def test_system1(self, tolerance):
        # Define the augmented matrix
        matrix = [
            [3, 1, -4, 7],
            [-2, 3, 1, -5],
            [2, 0, 5, 10],
        ]

        # Extract the constants and coefficient matrix
        constants = [row[-1] for row in matrix]
        coefficients = [row[:-1] for row in matrix]

        # Perform Gauss elimination
        solution = gauss_jordan(coefficients, constants)

        # Verify the solution exists
        assert solution is not None, "No solution returned"

        # Verify we got 3 values
        assert len(solution) == 3, f"Expected 3 values, got {len(solution)}"

        # Verify the solution satisfies all equations
        self.verify_solution(coefficients, constants, solution, tolerance)

    def test_system2(self, tolerance):
        """Test case for a 3x3 system with unique solution."""
        matrix = [
            [1, -2, 4, 6],
            [8, -3, 2, 2],
            [-1, 10, 2, 4],
        ]

        constants = [row[-1] for row in matrix]
        coefficients = [row[:-1] for row in matrix]

        solution = gauss_jordan(coefficients, constants)

        assert solution is not None, "No solution returned"
        assert len(solution) == 3, f"Expected 3 values, got {len(solution)}"

        self.verify_solution(coefficients, constants, solution, tolerance)

    def test_singular_matrix(self):
        """Test case for a singular matrix that should raise ValueError."""
        # Define a singular matrix (linearly dependent rows)
        coefficients = [[1, 2], [2, 4]]
        constants = [2, 4]

        with pytest.raises(ValueError, match="Matrix is singular or nearly singular"):
            gauss_jordan(coefficients, constants)

    def test_nearly_singular_matrix(self):
        """Test case for a nearly singular matrix that should raise ValueError."""
        # Define a nearly singular matrix (almost linearly dependent rows)
        coefficients = [[1.0, 2.0], [1.0, 2.000001]]
        constants = [1, 2]

        with pytest.raises(ValueError, match="Matrix is singular or nearly singular"):
            gauss_jordan(coefficients, constants)
