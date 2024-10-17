import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse as dtparse
from vulndb.database import insert_vulnerabilities as insert


async def scrape(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json(content_type=None)


async def cisco():
    # Cisco
    # https://sec.cloudapps.cisco.com/security/center/publicationListing.x
    url = "https://sec.cloudapps.cisco.com/security/center/publicationService.x?sort=-day_sir&limit=20"
    # dict_keys(['identifier', 'title', 'version', 'firstPublished', 'lastPublished', 'workflowStatus', 'id', 'name', 'url', 'severity', 'workarounds', 'cwe', 'erpPubIds', 'cve', 'ciscoBugId', 'status', 'summary', 'totalCount', 'relatedResource'])
    count = await insert(
        [
            {
                "vendor": "Cisco",
                "id": event.get("identifier"),
                "title": event.get("title"),
                "released": dtparse(event.get("firstPublished")),
                "updated": dtparse(event.get("lastPublished")),
                "description": event.get("summary"),
                "link": event.get("url"),
            }
            for event in (await scrape(url))
        ]
    )

    return count


async def microsoft():
    # Microsoft
    # https://msrc.microsoft.com/update-guide/vulnerability
    url = "https://api.msrc.microsoft.com/sug/v2.0/en-IN/vulnerability?$orderBy=cveNumber%20desc&$filter=(releaseDate%20ge%202024-08-01T00:00:00.000Z)"
    # dict_keys(['id', 'releaseDate', 'cveNumber', 'cveTitle', 'releaseNumber', 'vulnType', 'latestRevisionDate', 'description', 'cweList', 'unformattedDescription', 'mitreText', 'mitreUrl', 'latestSoftwareReleaseId', 'olderSoftwareReleaseId', 'denialOfService', 'tag', 'issuingCna', 'severityId', 'impactId', 'langCode', 'isMariner', 'customerActionRequired', 'cweDetailsList', 'articles', 'revisions'])
    count = await insert(
        [
            {
                "vendor": "Microsoft",
                "id": event.get("id"),
                "title": event.get("cveTitle"),
                "released": dtparse(event.get("releaseDate")),
                "updated": dtparse(event.get("latestRevisionDate")),
                "description": event.get("description"),
                "link": f"https://msrc.microsoft.com/update-guide/vulnerability/{event['cveNumber']}",
            }
            for event in (await scrape(url)).get("value")
        ]
    )

    return count


async def nvidia():
    # NVIDIA
    # https://www.nvidia.com/en-us/security/
    url = "https://www.nvidia.com/content/dam/en-zz/Solutions/product-security/product-security.json"

    count = await insert(
        [
            {
                "vendor": "NVIDIA",
                "id": event.get("bulletin id"),
                "title": bs(event.get("title"), "lxml").get_text(),
                "released": dtparse(event.get("publish date")),
                "updated": dtparse(event.get("last updated")),
                "description": event.get("description"),
                "link": bs(event.get("title"), "lxml").find_all("a")[0]["href"],
            }
            for event in (await scrape(url)).get("data")
        ]
    )

    return count

vendor_dict = {
    "Cisco": cisco,
    "Microsoft": microsoft,
    "NVIDIA": nvidia,
}


async def process():
    return sum(await asyncio.gather(*map(lambda f: f(), vendor_dict.values())))
