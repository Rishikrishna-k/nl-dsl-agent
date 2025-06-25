from fastapi import FastAPI
from pydantic import BaseModel
from app.main_workflow import run_workflow

app = FastAPI(title="DSL Code Generator API")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    result: str

@app.post("/generate", response_model=QueryResponse)
async def generate_dsl(request: QueryRequest):
    """Generate DSL code based on user query"""
    result = run_workflow(request.query)
    return QueryResponse(result=result.get("codegen_result", "Error: No result generated"))

@app.get("/test")
async def test_workflow():
    """Test endpoint with hardcoded query"""
    hardcoded_query = "Create a DSL rule to validate that a patient has active insurance coverage"
    result = run_workflow(hardcoded_query)
    return {
        "query": hardcoded_query,
        "result": result.get("codegen_result", "Error: No result generated"),
        "full_response": result
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "DSL Code Generator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 