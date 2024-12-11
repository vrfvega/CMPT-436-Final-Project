import customtkinter

from src.gauss_jordan import gauss_jordan
from src.gaussian_elimination import gauss_elimination

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("800x400")


def gauss_button_callback():
    try:
        matrix_gauss = entryX.get()
        A = eval(matrix_gauss)

        result = gauss_elimination(A)
        result_label.configure(text=f"Result:\n{result}")
    except Exception as e:
        result_label.configure(text=f"Error: {e}")


def button_callback():
    try:  # converting input
        # stores A and b input
        matrix_i = entryM.get()
        vector_i = entryV.get()
        # converts the string input into python lists
        A = eval(matrix_i)  # should be 2D
        b = eval(vector_i)  # should be 1D

        # Gauss-Jordan method is implemented
        result = gauss_jordan(A, b)
        result_label.configure(text=f"Result:\n{result}")
    except Exception as e:
        result_label.configure(text=f"Error: {e}")


# GUI - buttons, labels, frame, etc
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)
frame_l = customtkinter.CTkFrame(master=frame)
frame_l.pack(side="left", padx=10, pady=10)
frame_r = customtkinter.CTkFrame(master=frame)
frame_r.pack(side="right", padx=10, pady=10)

label = customtkinter.CTkLabel(master=frame_l, text="Gauss-Jordan", font=("Arial", 18))
label.pack(pady=8, padx=10)
labelG = customtkinter.CTkLabel(
    master=frame_r, text="Gauss Elimination", font=("Arial", 18)
)
labelG.pack(pady=8, padx=10)
# Input boxes
entryM = customtkinter.CTkEntry(master=frame_l, placeholder_text="Enter matrix A")
entryM.pack(pady=8, padx=10)
entryV = customtkinter.CTkEntry(master=frame_l, placeholder_text="Enter vector b")
entryV.pack(pady=8, padx=10)
entryX = customtkinter.CTkEntry(master=frame_r, placeholder_text="Enter matrix")
entryX.pack(pady=8, padx=10)

button = customtkinter.CTkButton(
    master=frame_l, text="Submit GuassJordan", command=button_callback
)
button.pack(pady=8, padx=10)
buttonG = customtkinter.CTkButton(
    master=frame_r, text="Submit Gauss", command=gauss_button_callback
)
buttonG.pack(pady=8, padx=10)

result_label = customtkinter.CTkLabel(
    master=frame, text="", font=("Arial", 12), wraplength=300
)
result_label.pack(pady=20, padx=10)
root.mainloop()
