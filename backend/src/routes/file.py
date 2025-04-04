from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
from ..schema import file
from ..utils import Query, fnMakeId
from datetime import datetime
import os
import shutil
from ..core import variables
from typing import List
from pathlib import Path
from pdf2image import convert_from_path
    
router = APIRouter(prefix="/file", tags=["Files"])

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "pptx"}

def get_user_directory(user_id: str, folder_path:Optional[str]=""):
    user_folder = os.path.join(variables.BASE_UPLOAD_DIR, user_id)
    
    if folder_path:
        user_folder = os.path.join(user_folder, folder_path)
        
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def get_file_extension(filename: str):
    return filename.split(".")[-1].lower()

# Upload Files
@router.post("/upload", status_code = 202)
async def upload_file(
    schema: file.UploadFile, 
    file: UploadFile = File(...)
):
    try:
        ext = get_file_extension(file.filename)
        if ext not in ALLOWED_EXTENSIONS:
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       = {
                    "status"    : 'false',
                    "message"   : "Invalid file type. Allowed types are: PDF, DOCX, TXT, PPTX",
                }
            )
        
        file_id = await fnMakeId(
            collection_name   = 'coll_files',
            prefix            = 'FILE',
            sort              = 'file_id'
        )
        
        if isinstance(file_id, JSONResponse):
            return file_id
        
        user_dir = get_user_directory(schema.user_id, schema.folder_path)
        
        file_path = os.path.join(user_dir, file.filename)
    
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        arrFiles = await Query(
            collection_name   = 'coll_files',
            operation         = 'find',
            filter            = {
                "user_id"       : schema.user_id,
                "file_id"       : file_id,
                "file_name"     : file.filename,
                "file_ext"      : ext,
                "created_at"    : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_size"     : os.path.getsize(file_path),
                "file_path"     : file_path,
            }
        )
        
        if isinstance(arrFiles, JSONResponse):
            return arrFiles
        
        return JSONResponse(
            status_code   = status.HTTP_201_CREATED,
            content       = {
                "status"    : 'true',
                "message"   : "File uploaded successfully",
                "data"      : {
                    "file_id"   : file_id,
                    "file_path" : file_path,
                }
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"        : 'false',
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno),
            }
        )
        
@router.post("/get-file", status_code = 200)
async def get_file(
    schema: file.GetFile
):
    try:
        filter = {"user_id"   : schema.user_id,}
        
        if schema.file_id:
            filter["file_id"] = schema.file_id
        if schema.file_name:
            filter["file_name"] = schema.file_name
        if schema.file_ext:
            filter["file_ext"] = schema.file_ext
            
        file = await Query(
            collection_name   = 'coll_files',
            operation         = 'find_one',
            filter            = filter
        )
        
        if isinstance(file, JSONResponse):
            return file
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "File retrieved successfully",
                "data"      : file,
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"        : 'false',
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno),
            }
        )
        
@router.post("/delete-file", status_code = 200)
async def delete_file(
    schema: file.GetFile
):
    try:
        filter = {"user_id"   : schema.user_id,}
        
        if schema.file_id:
            filter["file_id"] = schema.file_id
        if schema.file_name:
            filter["file_name"] = schema.file_name
        if schema.file_ext:
            filter["file_ext"] = schema.file_ext
            
        file = await Query(
            collection_name   = 'coll_files',
            operation         = 'delete_multiple',
            filter            = filter
        )
        
        if isinstance(file, JSONResponse):
            return file
        
        os.remove(file['file_path'])
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "File deleted successfully",
                "data"      : file,
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code   = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content       = {
                "status"        : 'false',
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno),
            }
        )
        
# @router.post("/pdf/convert", status_code = 200)
# async def convert_to_pdf(file: UploadFile = File(...)):
#     file_ext = file.filename.split(".")[-1].lower()
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
    
#     with open(file_path, "wb") as f:
#         f.write(file.file.read())

#     output_pdf_path = os.path.join(OUTPUT_DIR, f"{Path(file.filename).stem}.pdf")

#     if file_ext == "pdf":
#         return FileResponse(file_path, media_type="application/pdf", filename=file.filename)

#     elif file_ext == "docx":
#         convert_docx_to_pdf(file_path, output_pdf_path)

#     elif file_ext == "txt":
#         convert_txt_to_pdf(file_path, output_pdf_path)

#     elif file_ext == "pptx":
#         convert_pptx_to_pdf(file_path, output_pdf_path)

#     else:
#         return {"error": "Unsupported file format"}

#     return FileResponse(output_pdf_path, media_type="application/pdf", filename=Path(file.filename).stem + ".pdf")


# def convert_docx_to_pdf(docx_path, pdf_path):
#     doc = Document(docx_path)
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     for para in doc.paragraphs:
#         pdf.cell(200, 10, txt=para.text, ln=True, align='L')

#     pdf.output(pdf_path)


# def convert_txt_to_pdf(txt_path, pdf_path):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     with open(txt_path, "r", encoding="utf-8") as file:
#         for line in file:
#             pdf.cell(200, 10, txt=line.strip(), ln=True, align='L')

#     pdf.output(pdf_path)


# def convert_pptx_to_pdf(pptx_path, pdf_path):
#     powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
#     powerpoint.Visible = 1
#     presentation = powerpoint.Presentations.Open(os.path.abspath(pptx_path))
#     presentation.SaveAs(os.path.abspath(pdf_path), 32)  # 32 is the format for PDF
#     presentation.Close()
#     powerpoint.Quit()