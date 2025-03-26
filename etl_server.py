import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import shutil
from vector_etl import create_flow

app = FastAPI(title="ETL Pipeline Server")

@app.post("/run-etl")
async def run_etl_pipeline(config_file: UploadFile = File(...)):
    try:
        os.makedirs('uploads', exist_ok=True)
        
        config_path = os.path.join('uploads', 'config.yaml')
        with open(config_path, 'wb') as buffer:
            shutil.copyfileobj(config_file.file, buffer)
        
        flow = create_flow()
        flow.load_yaml(config_path)
        flow.execute()
        
        return JSONResponse(
            status_code=200, 
            content={
                "status": "success", 
                "message": "ETL pipeline completed successfully",
                "config_file": config_file.filename
            }
        )
    
    except Exception as e:
        return HTTPException(
            status_code=500, 
            detail=f"ETL pipeline execution failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)