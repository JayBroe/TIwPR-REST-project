http://localhost:5000/

INSTRUKCJA OBSŁUGI:

STUDENT:



POST | http://localhost:5000/students/

POST ->>



PUT | http://localhost:5000/students/<indexx>

{
    "is stud": true,
    "name": "Jaqb",
    "surname": "Brzozowskiw"
}

WNIOSEK:

POST | http://localhost:5000/proporsals/

{
    "indexx":"<indexx>"
}

PUT | http://localhost:5000/proposals/<nr>

{
    "name": "Wniosek o wniosek"
}

wyjscie:

{
    "name": "",
    "nr": "13",
    "owner": {
        "indexx": "192045",
        "name": "Jaqb",
        "surname": "Brzozowskiw"
    }
}

POST | http://localhost:5000/decisions/

{
    "nr":"<nr wniosku>"
}

PUT | http://localhost:5000/decisions/<nr->

{
    "acceptance":true,
}

NAUCZYCIEL

POST | http://localhost:5000/teachers/



PUT | http://localhost:5000/teachers/<id>

{
    "name":"Jan",
    "surname":"Kowalski",
    "degree":"Profesor"
}

wyjście:

{
    "degree": "Profesor",
    "email": "Jan.Kowalski@put.poznan.pl",
    "name": "Jan",
    "surname": "Kowalski"
}

PRZEMIOT

POST | http://localhost:5000/subjects/

{
    "teacher_id" : "<teacher_id>"
}

wyjście:

{
    "forma": "",
    "identyfikator": "8c9f12a0-81b7-45cb-8dd2-184378c846c4",
    "name": "",
    "owner": {
        "email": "Jan.Kowalski@put.poznan.pl",
        "name": "Jan",
        "surname": "Kowalski"
    }
}

PUT | http://localhost:5000/subjects/<id>

{
    "name":"TIWPR",
    "form":"Seminarium"
}

wyjście:

{
    "Forma": "Wyklad",
    "name": "TIWPR",
    "owner": {
        "Imie wykladowcy": "Jan",
        "Nazwisko wykladowcy": "Kowalski"
    }
}

POST | http://localhost:5000/annoucements/

{
    "indexx":"<indexx>",
    "teacher_id":"<email prowadzącego>"
}

wyjście:

{
    "Dane adresata": {
        "imie prowadzacego": "Jan",
        "nazwisko prowadzacego": "Kowalski"
    },
    "Dane adresatow": {
        "imie studenta": "Jaqer",
        "nazwisko studenta": "Brzozowski"
    },
    "data": "2022-10-13 19:35:45.594017",
    "tresc": ""
}


PUT | http://localhost:5000/annoucements/data

{
    "content": "Prosze sie stawic w dziekanacie"
}

wyjście:

{
    "Dane adresata": {
        "imie prowadzacego": "Jan",
        "nazwisko prowadzacego": "Kowalski"
    },
    "Dane adresatow": {
        "imie studenta": "Jaqer",
        "nazwisko studenta": "Brzozowski"
    },
    "content": "Prosze sie stawic w dziekanacie",
    "data": "2022-10-13 19:35:45.594017"
}

