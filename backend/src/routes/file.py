from fastapi import APIRouter, UploadFile, File, status, Form
from fastapi.responses import JSONResponse
from ..schema import file
from ..utils import Query, fnMakeId
from datetime import datetime
import os
import shutil
    
router = APIRouter(prefix="/file", tags=["Files"])

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "pptx"}

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(
    user_id       : str = Form(...),
    folder_id     : str = Form(...),
    file          : UploadFile = File(...)
):
    try:
        # Extract file extension
        ext = file.filename.split(".")[-1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            return JSONResponse(
                status_code   = status.HTTP_400_BAD_REQUEST,
                content       ={
                    "status"  : False,
                    "message" : f"Invalid file type. Allowed types are: {', '.join(ALLOWED_EXTENSIONS).upper()}"
                }
            )

        # Check if user exists
        user = await Query(
            collection_name   = 'coll_users',
            operation         = 'get_one',
            query             = {
                "user_id"       : user_id
            }
        )

        if isinstance(user, JSONResponse):
            return user

        if not user:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "User not found"
                }
            )

        # Generate a unique file ID
        file_id = await fnMakeId(
            collection_name   = 'coll_files',
            prefix            = 'FILE',
            sort              = 'file_id'
        )

        if isinstance(file_id, JSONResponse):
            return file_id

        arrUserFolder  = await Query(
            collection_name   = 'coll_folders',
            operation         = 'get_one',
            query             = {
                "created_by"    : user_id,
                "folder_id"     : folder_id
            }
        )

        if isinstance(arrUserFolder, JSONResponse):
            return arrUserFolder
        
        if not arrUserFolder:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "Folder not found"
                }
            )
        
        folder_path   = arrUserFolder.get('folder_path', '')

        os.makedirs(folder_path, exist_ok = True)
        file_path     = os.path.join(folder_path, file.filename)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Store file metadata in database
        file_metadata = {
            "created_by"        : user_id,
            "file_id"           : file_id,
            "folder_id"         : folder_id,
            "file_name"         : file.filename,
            "file_ext"          : ext,
            "created_at"        : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_size"         : os.path.getsize(file_path),
            "file_path"         : file_path,
        }

        result = await Query(
            collection_name   = 'coll_files',
            operation         = 'insert_one',
            data              = file_metadata
        )

        if isinstance(result, JSONResponse):
            return result

        return JSONResponse(
            status_code         = status.HTTP_201_CREATED,
            content             = {
                "status"        : True,
                "message"       : "File uploaded successfully",
                "data": {
                    "file_id"   : file_id,
                    "file_path" : file_path,
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code         = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content             = {
                "status"        : False,
                "message"       : "Internal server error",
                "error"         : str(e),
                "error_line"    : str(e.__traceback__.tb_lineno)
            }
        )
        
@router.post("/delete", status_code = 200)
async def delete_file(
    schema: file.GetFile
):
    try:
        query = {
            "created_by"    : schema.user_id,
            "file_id"       : schema.file_id
        }
        
        get_file = await Query(
            collection_name   = 'coll_files',
            operation         = 'get_one',
            query             = query
        )
        
        if isinstance(get_file, JSONResponse):
            return get_file
        
        if not get_file:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "File not found"
                }
            )
            
        del_file = await Query(
            collection_name   = 'coll_files',
            operation         = 'delete_one',
            query             = query
        )
        
        if isinstance(del_file, JSONResponse):
            return del_file
        
        os.remove(get_file.get('file_path'))
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "File deleted successfully",
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

@router.post("/rename", status_code = 200)
async def rename_file(
    schema: file.RenameFile
):
    try:
        
        get_file = await Query(
            collection_name   = 'coll_files',
            operation         = 'get_one',
            query             = {
                "created_by"    : schema.user_id,
                "file_id"       : schema.file_id
            }
        )
        if isinstance(get_file, JSONResponse):
            return get_file
        
        if not get_file:
            return JSONResponse(
                status_code   = status.HTTP_404_NOT_FOUND,
                content       = {
                    "status"  : False,
                    "message" : "File not found"
                }
            )
            
        query = {
            "created_by"    : schema.user_id,
            "file_id"       : schema.file_id
        }
            
        update_file = await Query(
            collection_name   = 'coll_files',
            operation         = 'update_one',
            query             = query,
            data              = {
                "file_name" : schema.new_file_name,
                "file_ext"  : schema.new_file_name.split(".")[-1].lower(),
                "file_path" : os.path.join(os.path.dirname(get_file.get('file_path')), schema.new_file_name),
                "updated_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        
        if isinstance(update_file, JSONResponse):
            return update_file
        
        # Rename the file on the filesystem
        old_file_path   = get_file.get('file_path', '')
        new_file_path   = os.path.join(os.path.dirname(old_file_path), schema.new_file_name)
        
        os.rename(old_file_path, new_file_path)
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "File renamed successfully",
                "data"      : update_file,
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
@router.post("/get", status_code = 200)
async def get_file(
    schema: file.GetFile
):
    try:
        filter = {
            "created_by"    : schema.user_id,
        }
        
        if schema.file_id:
            filter["file_id"] = schema.file_id
            
        file = await Query(
            collection_name   = 'coll_files',
            operation         = 'get_many',
            query             = filter
        )
        
        if isinstance(file, JSONResponse):
            return file
        
        return JSONResponse(
            status_code   = status.HTTP_200_OK,
            content       = {
                "status"    : 'true',
                "message"   : "File fetched successfully",
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