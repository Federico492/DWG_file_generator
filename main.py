import os
import shutil
import tkinter as tk
from tkinter import filedialog

def create_dwg_files():
    project_number = entry_project.get()
    template_path = entry_template.get()
    project_folder = entry_folder.get()
    wdp_file_path = os.path.join(project_folder, f"{project_number}.wdp")

    if not project_number or not template_path or not project_folder:
        lbl_status.config(text="Please enter all required fields", fg="red")
        return

    os.makedirs(project_folder, exist_ok=True)

    sections = {
        "Bill of Materials": int(entry_bom.get()),
        "Electrical - AC Logic": int(entry_ac_logic.get()),
        "Electrical - DC Logic": int(entry_dc_logic.get()),
        "Electrical - Inputs and Outputs": int(entry_io.get()),
        "Pneumatics - Schematic": int(entry_pneumatics.get()),
        "Enclosures - Layout": int(entry_enclosures.get())
    }

    section_patterns = {
        "Bill of Materials": "__1",
        "Electrical - AC Logic": "-001",
        "Electrical - DC Logic": "-101",
        "Electrical - Inputs and Outputs": "-301",
        "Pneumatics - Schematic": "-401",
        "Enclosures - Layout": "-801"
    }

    created_files = []

    # Ensure the cover page is created first
    cover_filename = f"{project_number}-__0.dwg"
    cover_path = os.path.join(project_folder, cover_filename)
    shutil.copy(template_path, cover_path)
    created_files.append(cover_filename)

    # Create Bill of Materials files
    if sections["Bill of Materials"] > 0:
        bom_filename = f"{project_number}-__1.dwg"
        bom_path = os.path.join(project_folder, bom_filename)
        shutil.copy(template_path, bom_path)
        created_files.append(bom_filename)

        # Generate additional Bill of Materials pages if needed
        for i in range(1, sections["Bill of Materials"]):
            extra_bom_filename = f"{project_number}-__{i+1}.dwg"
            extra_bom_path = os.path.join(project_folder, extra_bom_filename)
            shutil.copy(template_path, extra_bom_path)
            created_files.append(extra_bom_filename)

    # Generate DWG files for other sections
    for section, count in sections.items():
        if section != "Bill of Materials" and count > 0:
            start_number = int(section_patterns[section].replace("-", "").replace("__", ""))
            for i in range(count):
                filename = f"{project_number}-{start_number + (i * 3):03}.dwg"
                file_path = os.path.join(project_folder, filename)
                shutil.copy(template_path, file_path)
                created_files.append(filename)

    # Append generated filenames to the .wdp file in correct order
    with open(wdp_file_path, "a") as wdp_file:
        for file in created_files:
            wdp_file.write(file + "\n")

    lbl_status.config(text="DWG files and WDP updated successfully!", fg="green")

# Tkinter GUI
root = tk.Tk()
root.title("AutoCAD Electrical DWG Generator")

tk.Label(root, text="Enter 50M Project Number:").grid(row=0, column=0)
entry_project = tk.Entry(root)
entry_project.grid(row=0, column=1)

tk.Label(root, text="Select Project Folder:").grid(row=1, column=0)
entry_folder = tk.Entry(root, width=40)
entry_folder.grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: entry_folder.insert(0, filedialog.askdirectory())).grid(row=1, column=2)

tk.Label(root, text="Select DWG/DWT Template:").grid(row=2, column=0)
entry_template = tk.Entry(root, width=40)
entry_template.grid(row=2, column=1)
tk.Button(root, text="Browse", command=lambda: entry_template.insert(0, filedialog.askopenfilename(filetypes=[("AutoCAD Templates", "*.dwt;*.dwg")]))).grid(row=2, column=2)

sections = ["Bill of Materials", "Electrical - AC Logic", "Electrical - DC Logic", "Electrical - Inputs and Outputs", "Pneumatics - Schematic", "Enclosures - Layout"]
entries = {}

for i, section in enumerate(sections, start=3):
    tk.Label(root, text=f"Pages for {section}:").grid(row=i, column=0)
    entry = tk.Entry(root)
    entry.insert(0, "0")
    entry.grid(row=i, column=1)
    entries[section] = entry

entry_bom = entries["Bill of Materials"]
entry_ac_logic = entries["Electrical - AC Logic"]
entry_dc_logic = entries["Electrical - DC Logic"]
entry_io = entries["Electrical - Inputs and Outputs"]
entry_pneumatics = entries["Pneumatics - Schematic"]
entry_enclosures = entries["Enclosures - Layout"]

tk.Button(root, text="Generate DWG Files", command=create_dwg_files).grid(row=len(sections) + 3, columnspan=3)
lbl_status = tk.Label(root, text="")
lbl_status.grid(row=len(sections) + 4, columnspan=3)

root.mainloop()
