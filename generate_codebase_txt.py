import os

def generate():
    project_dir = r"c:\Users\ASUS\OneDrive\Desktop\GEM BIDS"
    output_file = os.path.join(project_dir, "FULL_PROJECT_CODEBASE.txt")
    
    ignore_dirs = {".git", "node_modules", ".venv", "__pycache__", ".idea", ".vscode", "dist", "build"}
    ignore_files = {"FULL_PROJECT_CODEBASE.txt", "package-lock.json", "database.json"}

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("====================================================\n")
        out.write("GEMINTEL FULL PROJECT CODEBASE MASTER EXPORT\n")
        out.write("====================================================\n\n")

        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for f in sorted(files):
                if f in ignore_files or f.endswith(".png") or f.endswith(".webp") or f.endswith(".ico"):
                    continue
                file_path = os.path.join(root, f)
                rel_path = os.path.relpath(file_path, project_dir)
                out.write(f"\n\n====================================================\n")
                out.write(f"FILE: {rel_path}\n")
                out.write(f"====================================================\n")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="replace") as ref:
                        out.write(ref.read())
                except Exception as e:
                    out.write(f"Error reading file: {e}\n")

    print(f"FULL_PROJECT_CODEBASE.txt successfully updated at {output_file}")

if __name__ == "__main__":
    generate()
