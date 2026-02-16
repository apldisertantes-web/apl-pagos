from fastapi import FastAPI, Request
import pandas as pd
from datetime import datetime

app = FastAPI()

@app.get("/webhook")
async def verify(mode:str=None, challenge:str=None, verify_token:str=None):

    if verify_token == "ZAS_TOKEN":
        return int(challenge)

@app.post("/webhook")
async def recibir(request: Request):

    data = await request.json()

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]

        telefono = msg["from"]

        if "text" in msg:
            texto = msg["text"]["body"]
        else:
            texto = "MEDIA"

        guardar_pago(telefono, texto)

    except:
        pass

    return {"ok":True}


def guardar_pago(tel, texto):

    fila = {
        "fecha": datetime.now(),
        "telefono": tel,
        "mensaje": texto,
        "estado":"revisar"
    }

    try:
        df = pd.read_excel("pagos.xlsx")
    except:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([fila])])

    df.to_excel("pagos.xlsx", index=False)
