"""Example 71: Form Data and File Upload.

Form(...) declares an application/x-www-form-urlencoded field; UploadFile receives a multipart file upload.
Both are declared as typed parameters. Run: uvicorn app:app --port 8000, then:
curl -F 'name=widget' -F 'file=@README.md' localhost:8000/upload. (co-11, co-12)
"""

from fastapi import FastAPI, File, Form, UploadFile  # => Form + UploadFile handle multipart input (co-11)

app = FastAPI()  # => the ASGI application uvicorn serves


@app.post("/upload")  # => a multipart endpoint
async def upload(name: str = Form(...), file: UploadFile = File(...)) -> dict[str, object]:  # => typed parts (co-11)
    # => Form(...) = a required form field; File(...) = a required file part (co-12)
    contents = await file.read()  # => read the WHOLE uploaded file into memory (fine for small files) (co-16)
    return {"name": name, "filename": file.filename, "size": len(contents)}  # => a summary of the upload (co-14)
