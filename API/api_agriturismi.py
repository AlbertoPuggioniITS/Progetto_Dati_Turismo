from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import sqlite3

# Connessione con il db
conn = sqlite3.connect('../db_turismo_test.db')


app = FastAPI()

# Creazione del modello AgriturismoCreate
class AgriturismoCreate(BaseModel):
    Regione: str
    Anno: int
    Arrivi: int
    Presenze: int

# Creazione del modello AgriturismoUpdate
class AgriturismoUpdate(BaseModel):
    Regione: str
    Anno: int
    Arrivi: int
    Presenze: int

# API Post - creazione di un agriturismo
@app.post("/crea_agriturismo/")
async def crea_agriturismo(agriturismo: AgriturismoCreate):
    query = "INSERT INTO Agriturismi (Regione, Anno, Arrivi, Presenze) VALUES (?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (agriturismo.Regione, agriturismo.Anno, agriturismo.Arrivi, agriturismo.Presenze))
    conn.commit()
    return {"message": "Agriturismo creato con successo"}


# API Put - aggiornamento di un agriturismo
@app.put("/aggiorna_agriturismo/")
async def aggiorna_agriturismo(agriturismo: AgriturismoUpdate):
    query = "UPDATE Agriturismi SET Anno = ?, Arrivi = ?, Presenze = ? WHERE Regione = ?"
    cursor = conn.cursor()
    cursor.execute(query, (agriturismo.Anno, agriturismo.Arrivi, agriturismo.Presenze, agriturismo.Regione))
    conn.commit()
    return {"message": f"Dati dell'agriturismo con Regione {agriturismo.Regione} aggiornati con successo"}


# API Get - ottenimento dei dati di un agriturismo
@app.get("/arrivi_agriturismi/")
async def get_items():
    cursor = conn.cursor()
    cursor.execute("SELECT arrivi FROM Agriturismi")  # Sostituisci con il nome della tabella desiderata
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    return {"Arrivi": result}


# API Get - Ottenimento dati di un agriturismo per regione
@app.get("/arrivi_agriturismi_per_regione/{regione}")
async def get_arrivi_per_regione(regione: str):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Arrivi FROM Agriturismi WHERE Regione = ?"
    cursor.execute(query, (regione,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Arrivi": row[2]} for row in rows]

    if result:
        return {"Arrivi per Regione": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per la regione: {regione}"})


# API Get - Ottenimento dati di un agriturismo per anno
@app.get("/arrivi_agriturismi_per_anno/{anno}")
async def get_arrivi_per_anno(anno: int):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Arrivi FROM Agriturismi WHERE Anno = ?"
    cursor.execute(query, (anno,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Arrivi": row[2]} for row in rows]

    if result:
        return {"Arrivi per Anno": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per l'anno: {anno}"})


# API Get - ottenimento dati per presenze di un agriturismo
@app.get("/presenze_agriturismi/")
async def get_presenze_agriturismi():
    cursor = conn.cursor()
    cursor.execute("SELECT presenze FROM Agriturismi")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    return {"Presenze": result}


# API Get - ottenimento dati per presenze di un agriturismo per regione
@app.get("/presenze_agriturismi_per_regione/{regione}")
async def get_presenze_per_regione(regione: str):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Presenze FROM Agriturismi WHERE Regione = ?"
    cursor.execute(query, (regione,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Presenze": row[2]} for row in rows]

    if result:
        return {"Presenze per Regione": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per la regione: {regione}"})


# API Get - ottenimento dati per presenze di un agriturismo per anno
@app.get("/presenze_agriturismi_per_anno/{anno}")
async def get_presenze_per_anno(anno: int):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Presenze FROM Agriturismi WHERE Anno = ?"
    cursor.execute(query, (anno,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Presenze": row[2]} for row in rows]

    if result:
        return {"Presenze per Anno": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per l'anno: {anno}"})


# API Delete - rimozione di un agriturismo
@app.delete("/elimina_agriturismo/{regione}/{anno}")
async def elimina_agriturismo(regione: str, anno: int):
    query = "DELETE FROM Agriturismi WHERE Regione = ? AND Anno = ?"
    cursor = conn.cursor()
    cursor.execute(query, (regione, anno))
    conn.commit()
    return {"message": f"Dati dell'agriturismo con Regione {regione} e Anno {anno} eliminati con successo"}