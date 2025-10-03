from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPUT


router = APIRouter(prefix='/router', tags=['Отели'])


hotels = [
    {"id": 1, "title": "Sochi", "name": 'sochi'},
    {"id": 2, "title": "Dubai", "name": 'dubai'},
    {"id": 3, "title": "Мальдивы", "name": 'maldivi'},
    {"id": 4, "title": "Геленджик", "name": 'gelendzhik'},
    {"id": 5, "title": "Москва", "name": 'moscow'},
    {"id": 6, "title": "Казань", "name": 'kazan'},
    {"id": 7, "title": "Санкт-Петербург", "name": 'spb'}
]


@router.get("", summary="Получение отелей")
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
        page: int = Query(1),
        per_page: int = Query(10)
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    start_page = (page - 1) * per_page
    end_page = start_page + per_page
    paginated_hotels = hotels[start_page:end_page]
    return {
        "hotels": paginated_hotels,
        "page": page,
        "per_page": per_page,
        "total": len(hotels_)
    }
    # return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]


# body, request body
@router.post("", summary="Создание отеля")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya"
    }},
    "2":{"summary": "Дубай", "value": {
            "title": "Отель дубай 5 звезд у моря",
            "name": "dubai_fun"
        }}
    })): #embed=True - если передается один параметр
    global hotels
    hotels.append({
        "id": hotels[-1]['id'] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Обновление данных об отеле")
def full_update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def update_hotel(hotel_id: int, hotel_data: HotelPUT):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel['title'] = hotel_data.title
            if hotel_data.name:
                hotel['name'] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}/", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": "OK"}


