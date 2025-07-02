import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add the current directory to Python path so backend.main can be imported
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port) 