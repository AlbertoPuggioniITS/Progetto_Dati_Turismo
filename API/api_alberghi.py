from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import sqlite3

# Connessione al db
conn = sqlite3.connect('../db_turismo_test.db')


app = FastAPI()

# Creazione del modello AlbergoCreate
class AlbergoCreate(BaseModel):
    Regione: str
    Anno: int
    Arrivi: int
    Presenze: int

# Creazione del modello AlbergoUpdate
class AlbergoUpdate(BaseModel):
    Regione: str
    Anno: int
    Arrivi: int
    Presenze: int
class EliminaAlbergoRequest(BaseModel):
    Regione: str
    Anno: int
    Arrivi: int
    Presenze: int

# API Post - Creazione di un albergo
@app.post("/crea_alberghi/")
async def crea_albergo(albergo: AlbergoCreate):
    query = "INSERT INTO Alberghi (Regione, Anno, Arrivi, Presenze) VALUES (?, ?, ?, ?)"
    cursor = conn.cursor()
    cursor.execute(query, (albergo.Regione, albergo.Anno, albergo.Arrivi, albergo.Presenze))
    conn.commit()
    return {"message": "Albergo creato con successo"}

# API Put - Aggiornamento di un albergo
@app.put("/aggiorna_alberghi/")
async def aggiorna_albergo(albergo: AlbergoUpdate):
    query = "UPDATE Alberghi SET Anno = ?, Arrivi = ?, Presenze = ? WHERE Regione = ?"
    cursor = conn.cursor()
    cursor.execute(query, (albergo.Anno, albergo.Arrivi, albergo.Presenze, albergo.Regione))
    conn.commit()
    return {"message": f"Dati degli Alberghi con Regione {albergo.Regione} aggiornati con successo"}


# API Get - ottenimento dei dati da 'Arrivi' di un albergo
@app.get("/arrivi_alberghi/")
async def get_arrivi_alberghi():
    cursor = conn.cursor()
    cursor.execute("SELECT arrivi FROM Alberghi")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    return {"Arrivi Alberghi": result}


# API Get - Ottenimento dati da 'Arrivi' di un albergo attraverso la ricerca di una regione
@app.get("/arrivi_alberghi_per_regione/{regione}")
async def get_arrivi_per_regione(regione: str):
    cursor = conn.cursor()
    query = "SELECT Regione, Anno, Arrivi FROM Alberghi WHERE Regione = ?"
    cursor.execute(query, (regione,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Arrivi": row[2]} for row in rows]

    if result:
        return {"Arrivi per Regione": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per la regione: {regione}"})


# API Get - Ottenimento dati da 'Arrivi' di un albergo attraverso la ricerca di un anno
@app.get("/arrivi_alberghi_per_anno/{anno}")
async def get_arrivi_per_anno(anno: int):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Arrivi FROM Alberghi WHERE Anno = ?"
    cursor.execute(query, (anno,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Arrivi": row[2]} for row in rows]

    if result:
        return {"Arrivi per Anno": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per l'anno: {anno}"})


# API Get - Ottenimento dati da 'Presenze' di un albergo
@app.get("/presenze_alberghi/")
async def get_presenze_alberghi():
    cursor = conn.cursor()
    cursor.execute("SELECT presenze FROM Alberghi")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    return {"Presenze": result}


# API Get - Ottenimento dati da 'Presenze' di un albergo attraverso la ricerca di una regione
@app.get("/presenze_alberghi_per_regione/{regione}")
async def get_presenze_per_regione(regione: str):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Presenze FROM Alberghi WHERE Regione = ?"
    cursor.execute(query, (regione,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Presenze": row[2]} for row in rows]

    if result:
        return {"Presenze per Regione": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per la regione: {regione}"})


# API Get - Ottenimento dati da 'Arrivi' di un albergo attraverso la ricerca di un anno
@app.get("/presenze_alberghi_per_anno/{anno}")
async def get_presenze_per_anno(anno: int):
    cursor = conn.cursor()
    query = f"SELECT Regione, Anno, Presenze FROM Alberghi WHERE Anno = ?"
    cursor.execute(query, (anno,))
    rows = cursor.fetchall()
    result = [{"Regione": row[0], "Anno": row[1], "Presenze": row[2]} for row in rows]

    if result:
        return {"Presenze per Anno": result}
    else:
        return JSONResponse(status_code=404, content={"error": f"Nessun dato trovato per l'anno: {anno}"})


# API Delete - Cancellazione di un albergo
@app.delete("/elimina_albergo/")
async def elimina_albergo(request: EliminaAlbergoRequest):
    cursor = conn.cursor()
    query = "DELETE FROM Alberghi WHERE Regione = ? AND Anno = ? AND Arrivi = ? AND Presenze = ?"
    cursor.execute(query, (request.Regione, request.Anno, request.Arrivi, request.Presenze))
    conn.commit()

    if cursor.rowcount > 0:
        return {"message": "Albergo eliminato con successo"}
    else:
        return JSONResponse(status_code=404, detail="Nessun albergo trovato per l'eliminazione")


@app.get("/media_arrivi_alberghi_per_regione/")
async def get_media_arrivi_per_regione(Regione: str):
    cursor = conn.cursor()
    query = "SELECT AVG(Arrivi) as Media_Arrivi FROM Alberghi WHERE Regione = ?"
    cursor.execute(query, (Regione,))
    result = cursor.fetchone()

    if result:
        media_arrivi = result[0]
        return {"Media Arrivi per Regione": media_arrivi}
    else:
        return JSONResponse(status_code=404, content={"error": "Nessun dato trovato per la regione specificata"})


@app.get("/media_presenze_alberghi_per_regione/")
async def get_media_presenze_per_regione(Regione: str):
    cursor = conn.cursor()
    query = "SELECT AVG(Presenze) as Media_Presenze FROM Alberghi WHERE Regione = ?"
    cursor.execute(query, (Regione,))
    result = cursor.fetchone()

    if result:
        media_presenze = result[0]
        return {"Media Presenze per Regione": media_presenze}
    else:
        return JSONResponse(status_code=404, content={"error": "Nessun dato trovato per la regione specificata"})
