import customtkinter

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("300x300")

def button_callback():
    print("test")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=60,fill="both",expand=True)

label = customtkinter.CTkLabel(master=frame, text="Gauss-Jordan", font=("Arial", 24))
label.pack(pady=12,padx=10)

entry1=customtkinter.CTkEntry(master=frame,placeholder_text="Input")
entry1.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Submit", command=button_callback)
button.pack(pady=12, padx=10)

root.mainloop()
