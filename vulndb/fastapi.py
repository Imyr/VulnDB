from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from vulndb.scrape import process, vendor_dict
from vulndb.database import query_vulnerabilities
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VulnerabilityQuery(BaseModel):
    vendor: Optional[str] = ""
    limit: Optional[int] = 10


@app.get("/")
async def root():
    return JSONResponse(
        content={
            "name": "VulnDB Backend",
            "team_id": "5568",
            "team_name": "Divya Utsav",
            "team_institution": "Birla Institute of Technology, Mesra",
            "available_endpoints": [
                "/available_vendors",
                "/vulnerabilities/list {vendor: str, limit: int}",
            ],
        }
    )


@app.get("/available_vendors")
async def vendors():
    return JSONResponse(
        content=list(vendor_dict)
    )


@app.get("/vulnerabilities/update")
async def update():
    return JSONResponse(
        content=f"Updated {await process()} vulnerabilities.",
    )


@app.post("/vulnerabilities/list")
async def lst(query: Optional[VulnerabilityQuery] = None):
    return JSONResponse(
        content=await query_vulnerabilities(
            vendor=query.vendor if query and query.vendor else "",
            limit=query.limit if query and query.limit else 10,
        ),
    )
