

import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": 'sochi'},
    {"id": 2, "title": "Dubai", "name": 'dubai'}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля')
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_
    # return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]


# body, request body
@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)): #embed=True - если передается один параметр
    global hotels
    hotels.append({
        "id": hotels[-1]['id'] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.put("/full_update_hotels/{hotel_id}")
def full_update_hotel(
        id: int,
        title: str,
        name: str
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id:
            hotel['title'] = title
            hotel['name'] = name
    return {"status": "OK"}


@app.patch("/update_hotels/{hotel_id}")
def update_hotel(
        id: int,
        title: str | None = Query(None),
        name: str | None = Query(None)
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id:
            if title is not None:
                hotel['title'] = title
            if name is not None:
                hotel['name'] = name
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}/")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": "OK"}




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)