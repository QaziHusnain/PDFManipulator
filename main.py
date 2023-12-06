import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfMerger, PdfFileReader, PdfFileWriter

class PDFManipulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Manipulator")

        self.merge_input_pdf_files = []
        self.merge_output_file_location = None

        self.split_input_pdf_file = None
        self.split_output_file_location = None

        self.create_widgets()

    def create_widgets(self):
        # Merge PDFs Section
        merge_label = tk.Label(self.master, text="Merge PDFs:")
        merge_label.pack(pady=10)

        self.select_merge_btn = tk.Button(self.master, text="Select PDFs to Merge", command=self.select_merge_files)
        self.select_merge_btn.pack(pady=5)

        self.merge_files_label = tk.Label(self.master, text="Selected Files: None")
        self.merge_files_label.pack(pady=5)

        # Select Output File Location for Merge
        output_label = tk.Label(self.master, text="Select Output File Location for Merge:")
        output_label.pack(pady=10)

        self.select_output_btn = tk.Button(self.master, text="Browse", command=self.select_merge_output_location)
        self.select_output_btn.pack(pady=5)

        self.output_location_label = tk.Label(self.master, text="Output Location: None")
        self.output_location_label.pack(pady=5)

        # Merge PDFs Button
        self.merge_btn = tk.Button(self.master, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_btn.pack(pady=10)

        # Split PDFs Section
        split_label = tk.Label(self.master, text="Split PDF:")
        split_label.pack(pady=10)

        self.select_split_btn = tk.Button(self.master, text="Select PDF to Split", command=self.select_split_file)
        self.select_split_btn.pack(pady=5)

        self.split_file_label = tk.Label(self.master, text="Selected File: None")
        self.split_file_label.pack(pady=5)

        # Page Range for Split
        range_label = tk.Label(self.master, text="Page Range (e.g., 1-3) for Split:")
        range_label.pack(pady=10)

        self.page_range_entry = tk.Entry(self.master)
        self.page_range_entry.pack(pady=5)

        # Select Output File Location for Split
        output_label_split = tk.Label(self.master, text="Select Output File Location for Split:")
        output_label_split.pack(pady=10)

        self.select_output_btn_split = tk.Button(self.master, text="Browse", command=self.select_split_output_location)
        self.select_output_btn_split.pack(pady=5)

        self.output_location_label_split = tk.Label(self.master, text="Output Location: None")
        self.output_location_label_split.pack(pady=5)

        # Split PDF Button
        self.split_btn = tk.Button(self.master, text="Split PDF", command=self.split_pdf)
        self.split_btn.pack(pady=10)

        # Completion Message
        self.completion_label = tk.Label(self.master, text="")
        self.completion_label.pack(pady=10)

    def select_merge_files(self):
        files = filedialog.askopenfilenames(title="Select PDF Files to Merge", filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.merge_input_pdf_files = files
            self.merge_files_label.config(text=f"Selected Files: {', '.join(files)}")

    def select_merge_output_location(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder for Merge")
        if folder_path:
            self.merge_output_file_location = folder_path
            self.output_location_label.config(text=f"Output Location: {folder_path}")

    def merge_pdfs(self):
        if self.merge_input_pdf_files and self.merge_output_file_location:
            output_file = f"{self.merge_output_file_location}/merged_output.pdf"
            merge_pdfs(self.merge_input_pdf_files, output_file)
            completion_message = f"PDFs have been merged successfully. Location: {output_file}"
            tk.messagebox.showinfo("Merge Complete", completion_message)
            self.completion_label.config(text=completion_message)
        else:
            tk.messagebox.showwarning("Select Files", "Please select PDF files, page range, and an output location.")

    def select_split_file(self):
        file_path = filedialog.askopenfilename(title="Select PDF File to Split", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.split_input_pdf_file = file_path
            self.split_file_label.config(text=f"Selected File: {file_path}")

    def select_split_output_location(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder for Split")
        if folder_path:
            self.split_output_file_location = folder_path
            self.output_location_label_split.config(text=f"Output Location: {folder_path}")

    def split_pdf(self):
        if self.split_input_pdf_file and self.split_output_file_location:
            page_range = self.page_range_entry.get()
            try:
                start_page, end_page = map(int, page_range.split('-'))
            except ValueError:
                tk.messagebox.showwarning("Invalid Page Range", "Please enter a valid page range (e.g., 1-3).")
                return

            if start_page > end_page:
                tk.messagebox.showwarning("Invalid Page Range", "End page should be greater than or equal to start page.")
                return

            output_prefix = f"{self.split_output_file_location}/split_output_page_"

            split_pdfs(self.split_input_pdf_file, start_page, end_page, output_prefix)
            completion_message = f"PDF has been split successfully. Location: {self.split_output_file_location}"
            tk.messagebox.showinfo("Split Complete", completion_message)
            self.completion_label.config(text=completion_message)
        else:
            tk.messagebox.showwarning("Select Files", "Please select a PDF file, page range, and an output location.")

def merge_pdfs(input_files, output_file):
    merger = PdfMerger()

    for file in input_files:
        merger.append(file)

    with open(output_file, 'wb') as merged_file:
        merger.write(merged_file)

def split_pdfs(input_file, start_page, end_page, output_prefix):
    pdf_reader = PdfFileReader(input_file)

    if end_page > pdf_reader.numPages:
        end_page = pdf_reader.numPages

    pdf_writer = PdfFileWriter()

    for page_num in range(start_page - 1, end_page):
        pdf_writer.addPage(pdf_reader.getPage(page_num))

    output_file = f"{output_prefix}{start_page}-{end_page}.pdf"
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFManipulatorGUI(root)
    root.mainloop()
