import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from typing import List

import database, crud, schemas

app = FastAPI(title="Telegram Analytics API")

DATA_ROOT = Path("../data/raw/telegram_messages")


@app.get(
    "/api/reports/top-products",
    response_model=List[schemas.TopProduct]
)
def top_products(limit: int = 10, db = Depends(database.get_db)):
    rows = crud.get_top_products(db, limit)
    return [
        schemas.TopProduct(detected_object_class=r[0], count=r[1])
        for r in rows
    ]


@app.get(
    "/api/channels/channal-activity",
    response_model=List[schemas.ChannelFolderActivity]
)
def channel_activity():
    if not DATA_ROOT.exists():
        raise HTTPException(status_code=404, detail="Raw data folder not found")

    counts = crud.get_channel_folder_activity(DATA_ROOT)
    return [
        schemas.ChannelFolderActivity(channel=chan, date_count=cnt)
        for chan, cnt in counts
    ]


@app.get(
    "/api/search/messages",
    response_model=List[str]
)
def search_messages(query: str):
    if not DATA_ROOT.exists():
        raise HTTPException(status_code=404, detail="Raw data folder not found")

    matches = crud.search_messages_fs(DATA_ROOT, query)
    if not matches:
        raise HTTPException(status_code=404, detail="No messages matched your query")
    return matches
