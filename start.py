import uvicorn
import os

if __name__ == "__main__":
    # Change to backend directory
    os.chdir("backend")
    
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("main:app", host="0.0.0.0", port=port) 