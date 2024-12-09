import customtkinter


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("300x300")

def button_callback():
    try:#converting input
        matrix_i = entryM.get()
        vector_i = entryV.get()
        A=eval(matrix_i)
        b=eval(vector_i)
        result=gauss_jordan(A,b)
        result_label.configure(text=f"Result:\n{result}")
    except Exception as e:
        result_label.configure(text=f"Error: {e}")


#GUI
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=60,fill="both",expand=True)

label = customtkinter.CTkLabel(master=frame, text="Gauss-Jordan", font=("Arial", 24))
label.pack(pady=12,padx=10)

entryM=customtkinter.CTkEntry(master=frame,placeholder_text="Enter matrix A")
entryM.pack(pady=12, padx=10)
entryV = customtkinter.CTkEntry(master=frame, placeholder_text="Enter vector b")
entryV.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Submit", command=button_callback)
button.pack(pady=12, padx=10)

result_label = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 12), wraplength=300)
result_label.pack(pady=12, padx=10)
root.mainloop()
