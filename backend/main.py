from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import subprocess
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories if they don't exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("model", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")

# Serve frontend files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

@app.get("/")
def read_root():
    """Serve the main frontend page"""
    frontend_index = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_index):
        return FileResponse(frontend_index, media_type="text/html")
    return {"message": "3D Brain Anomaly Detection API", "docs": "/docs"}

@app.get("/viewer")
def get_viewer():
    file_path = os.path.join(os.path.dirname(__file__), "static", "viewer.html")
    return FileResponse(file_path, media_type="text/html")

@app.get("/viewer_vr")
def get_viewer_vr():
    file_path = os.path.join(os.path.dirname(__file__), "static", "viewer_vr.html")
    return FileResponse(file_path, media_type="text/html")

@app.post("/upload")
async def upload_mri(file: UploadFile = File(...)):
    try:
        input_path = os.path.join("input", "uploaded.nii")
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check if model exists
        model_path = os.path.join("model", "3d_unet_brats2020.pth")
        if not os.path.exists(model_path):
            return JSONResponse(
                status_code=500, 
                content={"error": "Model file not found. Please upload the model file first."}
            )

        result = subprocess.run(["python", "run_pipeline.py"], capture_output=True, text=True)

        if result.returncode != 0:
            return JSONResponse(status_code=500, content={"error": result.stderr})

        return {
            "message": "Processing complete",
            "obj_url": "/output/brain_with_tumor.obj",
            "mtl_url": "/output/brain_with_tumor.mtl",
            "glb_url": "/output/brain_with_tumor.glb"
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
def health_check():
    return {"status": "healthy"}
