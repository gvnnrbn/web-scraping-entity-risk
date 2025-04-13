from fastapi import FastAPI, HTTPException
import uvicorn
from model import EntityRiskData, OFACformat
from typing import Optional
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

app = FastAPI()

@app.get("/api/entity/{name}", response_model=EntityRiskData)
async def get_entity_risk_data(name: str):
    result1 = await scrape_ofac(name)
    if result1 is None:
        raise HTTPException(status_code=404, detail="No results found")
    data = EntityRiskData(ofacResults=result1, ofacHits=len(result1))
    return data

async def scrape_ofac(name_input: str) -> Optional[list[OFACformat]]:
    results = []
    try:
        async with async_playwright() as p:
            #iniciar instancia sin interfaz y contexto del navegador
            browser = await p.chromium.launch(headless=True) 
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://sanctionssearch.ofac.treas.gov")
            # "check" Name field before filling it
            await page.locator("#ctl00_MainContent_txtLastName").fill(name_input)
            # "check" Search button before clicking it
            await page.locator("#ctl00_MainContent_btnSearch").click()

            table = page.locator("#gvSearchResults")
            # handling no results 
            if await table.count() == 0:
                return None

            await table.locator("tr").first.wait_for()

            rows = await table.locator("tr").all()

            for row in rows:
                cells = [text.strip() for text in await row.locator("td").all_inner_texts()]

                record = OFACformat(
                    name=cells[0],
                    address=cells[1],
                    type=cells[2],
                    programs=cells[3],
                    list=cells[4],
                    score=cells[5]
                )
                results.append(record)

            await browser.close()
        return results
    except PWTimeoutError:
        raise HTTPException(status_code=504, detail="Timeout obtaining OFAC data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpecter error: {e}")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=False,
        port=8000
    )