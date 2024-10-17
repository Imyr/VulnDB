from motor.motor_asyncio import AsyncIOMotorClient as aiomongo
from os import environ as env
import asyncio

client = aiomongo(env["MONGODB_URL"])
db = client.vulndb.vulnerabilities


async def insert_into_database(doc):
    if await db.find_one({"vendor": doc["vendor"], "id": doc["id"]}) is None: 
        await db.insert_one(doc)
        return 1
    else:
        return 0


async def insert_vulnerabilities(docs):
    return sum(await asyncio.gather(*map(lambda x: insert_into_database(x), docs)))


async def query_vulnerabilities(vendor: str, limit: int):
    if vendor == "":
        cursor = db.find().sort("released", -1).limit(limit)
    else:
        cursor = db.find({"vendor": vendor}).sort("released", -1).limit(limit)
    vulnerabilities = []
    async for vuln in cursor:
        del vuln["_id"]
        vuln["released"] = vuln["released"].strftime("%Y-%m-%d %H:%M:%S")
        vuln["updated"] = vuln["updated"].strftime("%Y-%m-%d %H:%M:%S")
        vulnerabilities.append(vuln)
    return vulnerabilities
