import os
from tkinter import filedialog

import customtkinter
from typing import List, Tuple

import numpy as np

from src.gauss_jordan import gauss_jordan
from src.gauss_elimination import gauss_elimination


class EntryField(customtkinter.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            width=60,
            height=35,
            corner_radius=8,
            border_width=2,
            font=("Inter", 13),
            border_color="#404040",
            fg_color="#2d2d2d",
            text_color="#ffffff",
            placeholder_text_color="#666666",
        )


def validate_file_format(file_path):
    """Validate the contents of the input file."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines if line.strip()]
        if not lines:
            raise ValueError("File is empty")

        first_line = lines[0].replace(",", " ").split()
        num_cols = len(first_line)

        try:
            matrix = [
                [float(val) for val in line.replace(",", " ").split()] for line in lines
            ]
        except ValueError:
            raise ValueError("All values must be numeric")

        if not all(len(row) == num_cols for row in matrix):
            raise ValueError("All rows must have the same number of columns")

        return matrix

    except Exception as e:
        raise ValueError(f"Invalid file format: {str(e)}")


class AugmentedMatrixFrame(customtkinter.CTkFrame):
    def __init__(self, master, rows=3, cols=4, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = rows
        self.cols = cols
        self.entries = []
        self.configure(corner_radius=15, border_width=0, fg_color="transparent")
        self._create_widgets()

    def _create_widgets(self):
        file_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        file_frame.pack(pady=10)

        load_btn = customtkinter.CTkButton(
            file_frame,
            text="Load from File",
            command=self._load_from_file,
            font=("Inter", 13),
            height=35,
            corner_radius=8,
            fg_color="#3d5afe",
            hover_color="#3949ab",
        )
        load_btn.pack(side="left", padx=10)

        size_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        size_frame.pack(pady=10)

        customtkinter.CTkLabel(
            size_frame,
            text="Matrix Size:",
            font=("Inter", 13, "bold"),
            text_color="#cccccc",
        ).pack(side="left", padx=5)

        self.row_spinbox = EntryField(size_frame, placeholder_text="Rows")
        self.row_spinbox.pack(side="left", padx=5)
        self.row_spinbox.insert(0, str(self.rows))

        customtkinter.CTkLabel(
            size_frame, text="×", font=("Inter", 13, "bold"), text_color="#cccccc"
        ).pack(side="left", padx=5)

        self.col_spinbox = EntryField(size_frame, placeholder_text="Cols")
        self.col_spinbox.pack(side="left", padx=5)
        self.col_spinbox.insert(0, str(self.cols - 1))

        update_btn = customtkinter.CTkButton(
            size_frame,
            text="Update Size",
            command=self._update_matrix_size,
            font=("Inter", 13),
            height=35,
            corner_radius=8,
            fg_color="#3d5afe",
            hover_color="#3949ab",
        )
        update_btn.pack(side="left", padx=10)

        self.matrix_frame = customtkinter.CTkFrame(
            self,
            fg_color="#242424",
            corner_radius=12,
            border_width=1,
            border_color="#404040",
        )
        self.matrix_frame.pack(pady=15, padx=10)
        self._create_matrix_entries()

    def _load_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Matrix File",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            return

        try:
            ext = os.path.splitext(file_path)[1].lower()

            if ext == ".csv":
                matrix = np.genfromtxt(file_path, delimiter=",")
            else:
                matrix = np.genfromtxt(file_path)

            self.row_spinbox.delete(0, "end")
            self.col_spinbox.delete(0, "end")

            self.rows, self.cols = matrix.shape

            self.row_spinbox.insert(0, str(self.rows))
            self.col_spinbox.insert(0, str(self.cols - 1))

            self._update_matrix_size()

            for i in range(self.rows):
                for j in range(self.cols):
                    self.entries[i][j].delete(0, "end")
                    self.entries[i][j].insert(0, f"{matrix[i][j]:.6f}")

        except Exception as e:
            self.show_error(
                f"Error loading file: {str(e)}\n\n"
                f"Expected format:\n"
                f"- Space or comma-separated numbers\n"
                f"- Last column should be the b vector\n"
                f"- All rows must have the same number of columns"
            )

    def _create_matrix_entries(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        header_frame = customtkinter.CTkFrame(
            self.matrix_frame, fg_color="transparent", height=30
        )
        header_frame.pack(fill="x", padx=15, pady=(10, 0))

        for j in range(self.cols):
            label_text = f"x{j + 1}" if j < self.cols - 1 else "b"
            label = customtkinter.CTkLabel(
                header_frame,
                text=label_text,
                font=("Inter", 12, "bold"),
                text_color="#999999",
                width=60,
            )
            label.pack(side="left", padx=3)

        entries_frame = customtkinter.CTkFrame(
            self.matrix_frame, fg_color="transparent"
        )
        entries_frame.pack(fill="both", padx=15, pady=10)

        for i in range(self.rows):
            row_frame = customtkinter.CTkFrame(entries_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            row_entries = []
            for j in range(self.cols):
                entry = EntryField(row_frame)
                entry.pack(side="left", padx=3)
                entry.insert(0, "0")

                if j == self.cols - 2:
                    separator = customtkinter.CTkFrame(
                        row_frame, width=2, height=35, fg_color="#404040"
                    )
                    separator.pack(side="left", padx=(3, 0))

                row_entries.append(entry)
            self.entries.append(row_entries)

    def _update_matrix_size(self):
        try:
            new_rows = int(self.row_spinbox.get())
            new_cols = int(self.col_spinbox.get())
            if 1 <= new_rows <= 10 and 1 <= new_cols <= 10:
                self.rows = new_rows
                self.cols = new_cols + 1
                self._create_matrix_entries()
            else:
                raise ValueError("Matrix size must be between 1 and 10")
        except ValueError as e:
            self.show_error(str(e))

    def get_matrices(self) -> Tuple[List[List[float]], List[float]]:
        matrix_a = []
        vector_b = []

        for row in self.entries:
            matrix_row = []
            for j, entry in enumerate(row):
                try:
                    value = float(entry.get())
                    if j < len(row) - 1:
                        matrix_row.append(value)
                    else:
                        vector_b.append(value)
                except ValueError:
                    raise ValueError(f"Invalid input: {entry.get()}")
            matrix_a.append(matrix_row)

        return matrix_a, vector_b

    def show_error(self, message: str):
        error_window = customtkinter.CTkToplevel(self)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.configure(fg_color="#1a1a1a")

        customtkinter.CTkLabel(
            error_window, text=message, font=("Inter", 14), text_color="#ff5252"
        ).pack(pady=20)

        customtkinter.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            font=("Inter", 13),
            height=35,
            corner_radius=8,
            fg_color="#3d5afe",
            hover_color="#3949ab",
        ).pack(pady=10)


class MatrixCalculatorApp:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.title("Matrix Calculator")
        self.root.geometry("900x700")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self._create_widgets()

    def _create_widgets(self):
        main_frame = customtkinter.CTkFrame(
            self.root,
            corner_radius=20,
            fg_color="#1a1a1a",
            border_width=1,
            border_color="#333333",
        )
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_frame = customtkinter.CTkFrame(
            main_frame, fg_color="transparent", height=80
        )
        title_frame.pack(fill="x")

        title_label = customtkinter.CTkLabel(
            title_frame,
            text="Matrix Calculator",
            font=("Inter", 28, "bold"),
            text_color="#ffffff",
        )
        title_label.pack(pady=20)

        method_frame = customtkinter.CTkFrame(
            main_frame, fg_color="#242424", corner_radius=12, height=60
        )
        method_frame.pack(pady=15, padx=30, fill="x")

        self.method_var = customtkinter.StringVar(value="gauss_jordan")

        method_label = customtkinter.CTkLabel(
            method_frame,
            text="Select Method:",
            font=("Inter", 14, "bold"),
            text_color="#cccccc",
        )
        method_label.pack(side="left", padx=20)

        for method, text in [
            ("gauss_jordan", "Gauss-Jordan"),
            ("gauss_elimination", "Gaussian Elimination"),
        ]:
            customtkinter.CTkRadioButton(
                method_frame,
                text=text,
                variable=self.method_var,
                value=method,
                font=("Inter", 14),
                height=28,
                fg_color="#3d5afe",
                border_color="#666666",
                text_color="#ffffff",
            ).pack(side="left", padx=15)

        content_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(pady=15, fill="both", expand=True)

        input_frame = customtkinter.CTkFrame(
            content_frame,
            corner_radius=15,
            fg_color="#2d2d2d",
            border_width=1,
            border_color="#404040",
        )
        input_frame.pack(side="left", padx=10, fill="both", expand=True)

        matrix_label = customtkinter.CTkLabel(
            input_frame,
            text="Augmented Matrix [A|b]",
            font=("Inter", 18, "bold"),
            text_color="#ffffff",
        )
        matrix_label.pack(pady=(20, 10))

        self.matrix_input = AugmentedMatrixFrame(input_frame)
        self.matrix_input.pack(pady=10)

        self.calc_button = customtkinter.CTkButton(
            input_frame,
            text="Calculate",
            command=self._calculate,
            font=("Inter", 15, "bold"),
            height=45,
            corner_radius=10,
            fg_color="#3d5afe",
            hover_color="#3949ab",
        )
        self.calc_button.pack(pady=30)

        output_frame = customtkinter.CTkFrame(
            content_frame,
            corner_radius=15,
            fg_color="#2d2d2d",
            border_width=1,
            border_color="#404040",
        )
        output_frame.pack(side="right", padx=10, fill="both", expand=True)

        result_label = customtkinter.CTkLabel(
            output_frame,
            text="Results",
            font=("Inter", 18, "bold"),
            text_color="#ffffff",
        )
        result_label.pack(pady=(20, 10))

        self.result_text = customtkinter.CTkTextbox(
            output_frame,
            height=400,
            font=("JetBrains Mono", 13),
            corner_radius=10,
            fg_color="#242424",
            text_color="#ffffff",
            border_width=1,
            border_color="#404040",
        )
        self.result_text.pack(pady=15, padx=20, fill="both", expand=True)

    def format_matrix(self, matrix: List[List[float]]) -> str:
        return "\n".join([" ".join(f"{x:8.4f}" for x in row) for row in matrix])

    def _calculate(self):
        try:
            matrix_a, vector_b = self.matrix_input.get_matrices()
            self.result_text.delete("1.0", "end")

            self.result_text.insert("end", "Input Augmented Matrix [A|b]:\n")
            augmented_matrix = [row + [b] for row, b in zip(matrix_a, vector_b)]
            self.result_text.insert("end", self.format_matrix(augmented_matrix))
            self.result_text.insert("end", "\n\n")

            if self.method_var.get() == "gauss_jordan":
                solution, mae, is_diag_dominant = gauss_jordan(matrix_a, vector_b)

                if not is_diag_dominant:
                    self.result_text.insert(
                        "end",
                        "\u26a0\ufe0f Matrix is not diagonally dominant.\n\n",
                        "warning",
                    )

                self.result_text.insert("end", "Solution:\n", "header")
                for i, val in enumerate(solution):
                    self.result_text.insert("end", f"x{i + 1} = {val:8.4f}\n")

                self.result_text.insert(
                    "end", f"\nMean Absolute Error: {mae:8.4e}\n", "info"
                )

            elif self.method_var.get() == "gauss_elimination":
                solution, mae, is_diag_dominant = gauss_elimination(matrix_a, vector_b)

                if not is_diag_dominant:
                    self.result_text.insert(
                        "end",
                        "\u26a0\ufe0f Matrix is not diagonally dominant.\n\n",
                        "warning",
                    )

                self.result_text.insert("end", "Solution:\n", "header")
                for i, val in enumerate(solution):
                    self.result_text.insert("end", f"x{i + 1} = {val:8.4f}\n")

                self.result_text.insert(
                    "end", f"\nMean Absolute Error: {mae:8.4e}\n", "info"
                )

        except Exception as e:
            self.matrix_input.show_error(str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MatrixCalculatorApp()
    app.run()
