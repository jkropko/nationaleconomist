# Import Libraries or Modules

import fitz # pdf utility library https://pymupdf.readthedocs.io/en/latest/module.html
import argparse # The argparse module makes it easy to write user-friendly command-line interfaces. https://docs.python.org/3/library/argparse.html
import sys # https://docs.python.org/3/library/sys.html
import os # https://docs.python.org/3/library/os.html
import cv2 # https://pypi.org/project/opencv-python/ and geeksforgeeks.org/how-to-install-opencv-for-python-in
from pprint import pprint #https://docs.python.org/3/library/pprint.html

def get_arguments(): # Define a function
    parser = argparse.ArgumentParser(                                      # Establish container for argument specifications and has options that apply the parser                                                                            # as whole.
        description="A Python script to extract text from PDF documents.") # Description for what the parser as a whole does
                                                                           # The ArgumentParser.add_argument() method attaches individual argument specifications                                                                            # to the parser. It supports positional arguments, options that accept values, and                                                                                # on/off flags:
    
    parser.add_argument("file", help="Input PDF file")                     # Help message for an argument
    parser.add_argument("-p", "--pages", nargs="*", type=int,              # Number of times the argument can be used
                        help="The pages to extract, default is all")       
    parser.add_argument("-o", "--output-file", default=sys.stdout,         # Default value used when an argument is not provided
                        help="Output file to write text. default is standard output") 
    parser.add_argument("-b", "--by-page", action="store_true",            # Specify how an argument should be handled 
                        help="Whether to output text by page. If not specified, all text is joined and will be written together")
    # parse the arguments from the command-line
    args = parser.parse_args()                                              # ArgumentParser parses arguments through the parse_args() method. This will inspect                                                                               # the command line, convert each argument to the appropriate type and then invoke the                                                                             # appropriate action.

    input_file = args.file
    pages = args.pages
    by_page = args.by_page
    output_file = args.output_file
    # print the arguments, just for logging purposes
    pprint(vars(args))
    # load the pdf file
    pdf = fitz.open(input_file)
    if not pages:
        # if pages is not set, default is all pages of the input PDF document
        pages = list(range(pdf.page_count))
    # we make our dictionary that maps each pdf page to its corresponding file
    # based on passed arguments
    if by_page:
        if output_file is not sys.stdout:
            # if by_page and output_file are set, open all those files
            file_name, ext = os.path.splitext(output_file)
            output_files = { pn: open(f"{file_name}-{pn}{ext}", "w") for pn in pages }
        else:
            # if output file is standard output, do not open
            output_files = { pn: output_file for pn in pages }
    else:
        if output_file is not sys.stdout:
            # a single file, open it
            output_file = open(output_file, "w")
            output_files = { pn: output_file for pn in pages }
        else:
            # if output file is standard output, do not open
            output_files = { pn: output_file for pn in pages }

    # return the parsed and processed arguments
    return {
        "pdf": pdf,
        "output_files": output_files,
        "pages": pages,
    }

def extract_text(**kwargs):
    # extract the arguments
    pdf          = kwargs.get("pdf")
    output_files = kwargs.get("output_files")
    pages        = kwargs.get("pages")
    # iterate over pages
    for pg in range(pdf.page_count):
        if pg in pages:
            # get the page object
            page = pdf[pg]
            # extract the text of that page and split by new lines '\n'
            page_lines = page.get_text().splitlines()
            # get the output file
            file = output_files[pg]
            # get the number of lines
            n_lines = len(page_lines)
            for line in page_lines:
                # remove any whitespaces in the end & beginning of the line
                line = line.strip()
                # print the line to the file/stdout
                print(line, file=file)
            print(f"[*] Wrote {n_lines} lines in page {pg}")    
    # close the files
    for pn, f in output_files.items():
        if f is not sys.stdout:
            f.close()
            
if __name__ == "__main__":
    # get the arguments
    kwargs = get_arguments()
    # extract text from the pdf document
    extract_text(**kwargs)