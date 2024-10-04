from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from vulndb.scrape import scrape_and_insert, vendor_list
from vulndb.database import query_vulnerabilities

app = FastAPI()


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
        },
        headers={"Access-Control-Allow-Origin": "*"},
    )


@app.get("/available_vendors")
async def vendors():
    return JSONResponse(
        content=vendor_list, headers={"Access-Control-Allow-Origin": "*"}
    )


@app.get("/vulnerabilities/update")
async def update():
    return JSONResponse(
        content=f"Updated {await scrape_and_insert()} vulnarabilities.",
        headers={"Access-Control-Allow-Origin": "*"},
    )


@app.post("/vulnerabilities/list")
async def list(query: Optional[VulnerabilityQuery] = None):
    return JSONResponse(
        content=await query_vulnerabilities(
            vendor=query.vendor if query and query.vendor else "",
            limit=query.limit if query and query.limit else 10,
        ),
        headers={"Access-Control-Allow-Origin": "*"},
    )
