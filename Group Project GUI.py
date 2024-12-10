import customtkinter
import numpy as np

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


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("800x400")
def gauss_button_callback():
    try:
        matrix_gauss = entryX.get()
        A=eval(matrix_gauss)

        result=gauss_elimination(A)
        result_label.configure(text=f"Result:\n{result}")
    except Exception as e:
        result_label.configure(text=f"Error: {e}")

def button_callback():
    try:#converting input
        #stores A and b input
        matrix_i = entryM.get()
        vector_i = entryV.get()
        #conversts the string input into python lists
        A=eval(matrix_i) #should be 2D
        b=eval(vector_i) #should be 1D

        #Gauss-Jordan method is implemented
        result=gauss_jordan(A,b)
        result_label.configure(text=f"Result:\n{result}")
    except Exception as e:
        result_label.configure(text=f"Error: {e}")


#GUI - buttons, labels, frame, etc
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=20,fill="both",expand=True)
frame_l = customtkinter.CTkFrame(master=frame)
frame_l.pack(side="left",padx=10,pady=10)
frame_r = customtkinter.CTkFrame(master=frame)
frame_r.pack(side="right",padx=10,pady=10)

label = customtkinter.CTkLabel(master=frame_l, text="Gauss-Jordan", font=("Arial", 18))
label.pack(pady=8,padx=10)
labelG=customtkinter.CTkLabel(master=frame_r,text="Gauss Elimination",font=("Arial", 18))
labelG.pack(pady=8, padx=10)
#Input boxes
entryM=customtkinter.CTkEntry(master=frame_l,placeholder_text="Enter matrix A")
entryM.pack(pady=8, padx=10)
entryV = customtkinter.CTkEntry(master=frame_l, placeholder_text="Enter vector b")
entryV.pack(pady=8, padx=10)
entryX=customtkinter.CTkEntry(master=frame_r,placeholder_text="Enter matrix")
entryX.pack(pady=8, padx=10)

button = customtkinter.CTkButton(master=frame_l, text="Submit GuassJordan", command=button_callback)
button.pack(pady=8, padx=10)
buttonG = customtkinter.CTkButton(master=frame_r, text="Submit Gauss", command=gauss_button_callback)
buttonG.pack(pady=8, padx=10)

result_label = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 12), wraplength=300)
result_label.pack(pady=20, padx=10)
root.mainloop()
