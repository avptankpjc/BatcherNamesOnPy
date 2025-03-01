import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class BatchNameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rename the File by Batchs")
        self.root.geometry("800x600")

        # Variables
        self.selected_files = []
        self.new_name = tk.StringVar()
        self.prefix = tk.StringVar()
        self.suffix = tk.StringVar()

        # Persistencia temporal en memoria
        self.file_data = {}  # Almacena nombres originales como claves y nuevos nombres como valores

        # Variables para controlar los checkboxes (opcional)
        self.check_vars = []

        # Área – Crear Canvas y Scrollbar
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configuración del Canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Habilitar el evento MouseWheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Empaquetar Canvas y Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Construir la interfaz
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.scrollable_frame)
        main_frame.pack(padx=50, pady=20, expand=True)

        global_check_frame = tk.Frame(main_frame)
        global_check_frame.pack(pady=5)

        self.select_all_var = tk.BooleanVar(value=True)
        tk.Checkbutton(global_check_frame, text="Select All", variable=self.select_all_var, command=self.toggle_all).pack(side="left", padx=5)

        self.deselect_all_var = tk.BooleanVar()
        tk.Checkbutton(global_check_frame, text="Deselect All", variable=self.deselect_all_var, command=self.deselect_all).pack(side="left", padx=5)

        # Etiqueta para archivos seleccionados
        tk.Label(main_frame, text="Files Selected:").pack(pady=5)

        # TreeView para selección de archivos
        self.tree = ttk.Treeview(
            main_frame,
            columns=("Select", "Original", "New Name", "Status"),
            show="headings",
            height=10
        )
        self.tree.heading("Select", text="Select")
        self.tree.heading("Original", text="Original")
        self.tree.heading("New Name", text="New Name")
        self.tree.heading("Status", text="Status")
        self.tree.column("Select", width=50)
        self.tree.column("Original", width=200)
        self.tree.column("New Name", width=200)
        self.tree.column("Status", width=100)
        self.tree.pack(pady=10)

        # Vincular el evento de clic para alternar el estado del checkbox
        self.tree.bind("<ButtonRelease-1>", self.toggle_checkbox)

        # Historial de Cambios
        tk.Label(main_frame, text="History of Changes:").pack(pady=5)

        self.history_tree = ttk.Treeview(
            main_frame,
            columns=("Original", "New Name", "Status"),
            show="headings",
            height=10
        )
        self.history_tree.heading("Original", text="Original")
        self.history_tree.heading("New Name", text="New Name")
        self.history_tree.heading("Status", text="Status")
        self.history_tree.column("Original", width=200)
        self.history_tree.column("New Name", width=200)
        self.history_tree.column("Status", width=100)
        self.history_tree.pack(pady=10)

        # Botón para limpiar el historial
        tk.Button(main_frame, text="Clear History", command=self.clear_history).pack(pady=5)

        # Botón para seleccionar archivos
        tk.Button(main_frame, text="Select Files", command=self.select_files).pack(pady=5)

        tk.Label(main_frame, text="New Name:").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.new_name, width=30).pack(pady=5)

        # Entradas para Prefix y Suffix
        tk.Label(main_frame, text="Prefix:").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.prefix, width=30).pack(pady=5)

        tk.Label(main_frame, text="Suffix:").pack(pady=5)
        tk.Entry(main_frame, textvariable=self.suffix, width=30).pack(pady=5)

        # Botones para renombrar y limpiar la lista
        tk.Button(main_frame, text="Rename", command=self.rename_files).pack(pady=5)
        tk.Button(main_frame, text="Clear", command=self.clear_list).pack(pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"))
        )

        if files:
            new_files = [file for file in files if file not in self.selected_files]
            self.selected_files.extend(new_files)

            for file in new_files:
                org_name = os.path.basename(file)  # Sólo el nombre del archivo, sin la ruta
                self.check_vars.append(True)  # Checkbox seleccionado por defecto
                self.tree.insert("", "end", values=["✓", org_name, "", "Pending"])
                self.tree.tag_configure("pending", foreground="orange")

    def toggle_checkbox(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#1":  # Columna "Select"
                item_id = self.tree.identify_row(event.y)
                current_values = self.tree.item(item_id, "values")
                if len(current_values) < 4:
                    return
                current_state = current_values[0]
                new_state = "✗" if current_state == "✓" else "✓"
                self.tree.item(item_id, values=[new_state] + list(current_values[1:]))

    def toggle_all(self):
        new_state = "✓" if self.select_all_var.get() else "✗"
        for item_id in self.tree.get_children():
            current_values = self.tree.item(item_id, "values")
            if len(current_values) < 4:
                continue
            self.tree.item(item_id, values=[new_state] + list(current_values[1:]))

    def deselect_all(self):
        for item_id in self.tree.get_children():
            current_values = self.tree.item(item_id, "values")
            if len(current_values) < 4:
                continue
            self.tree.item(item_id, values=["✗"] + list(current_values[1:]))

    def rename_files(self):
        new_name = self.new_name.get().strip().replace(" ", "_")
        prefix = self.prefix.get().strip().replace(" ", "_")
        suffix = self.suffix.get().strip().replace(" ", "_")

        if not self.selected_files:
            messagebox.showwarning("Warning", "No files selected.")
            return

        if not new_name and not prefix and not suffix:
            messagebox.showwarning("Warning", "You must enter a new name, prefix, or suffix.")
            return

        try:
            next_number = 1
            # Hacemos una copia de los ítems actuales del TreeView
            tree_items = list(self.tree.get_children())
            renamed_items = []  # Almacenará tuplas (índice, item_id) para los archivos renombrados

            total_files = len(self.selected_files)
            # Iteramos sobre la lista de archivos seleccionados usando su índice
            for i in range(total_files):
                # Si no existe un ítem en el TreeView para ese índice, lo saltamos
                if i >= len(tree_items):
                    continue

                item_id = tree_items[i]
                current_values = self.tree.item(item_id, "values")
                if len(current_values) < 4:
                    continue

                # Solo procesamos si el checkbox está activo ("✓")
                if current_values[0] != "✓":
                    continue

                file_path = self.selected_files[i]
                org_name = os.path.basename(file_path)
                dir_name = os.path.dirname(file_path)
                name, ext = os.path.splitext(org_name)
                base_name = new_name if new_name else name

                updated_name = base_name
                if prefix:
                    updated_name = f"{prefix}_{updated_name}"
                if suffix:
                    updated_name = f"{updated_name}_{suffix}"

                # Independientemente del número de archivos, siempre verificamos si el nombre ya existe.
                candidate = f"{updated_name}{ext}"
                if os.path.exists(os.path.join(dir_name, candidate)):
                    # Si el nombre existe, usamos sufijo incremental para garantizar la unicidad.
                    next_number = 1
                    while os.path.exists(os.path.join(dir_name, f"{updated_name}_{next_number:03d}{ext}")):
                        next_number += 1
                    candidate = f"{updated_name}_{next_number:03d}{ext}"
                updated_name = candidate

                new_path = os.path.join(dir_name, updated_name)
                # Renombrar el archivo
                os.rename(file_path, new_path)
                # Actualizar la ruta en la lista de archivos
                self.selected_files[i] = new_path
                # Actualizar el historial en memoria (si se necesita para otros propósitos)
                self.file_data[org_name] = updated_name

                # Insertar en el historial, verificando duplicados
                exists = False
                for row in self.history_tree.get_children():
                    values = self.history_tree.item(row, "values")
                    if len(values) >= 2 and org_name == values[0] and updated_name == values[1]:
                        exists = True
                        break
                if not exists:
                    self.history_tree.insert("", "end", values=[org_name, updated_name, "Renamed"])

                # Actualizar el estado en el TreeView principal
                self.tree.item(item_id, values=["✓", org_name, updated_name, "Renamed"])

                # Almacenar información del ítem renombrado
                renamed_items.append((i, item_id))

            # Eliminar los ítems que ya fueron renombrados (en orden descendente para no afectar índices)
            for idx, item_id in sorted(renamed_items, key=lambda x: x[0], reverse=True):
                self.tree.delete(item_id)
                del self.selected_files[idx]

            messagebox.showinfo("Success", "Files renamed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_list(self):
        self.tree.delete(*self.tree.get_children())
        self.check_vars.clear()
        self.selected_files.clear()

    def clear_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        self.file_data.clear()

    # Evento para el scroll del canvas
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    app = BatchNameApp(root)
    root.mainloop()
