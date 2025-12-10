/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
// Seleccionar la base de datos
use('SimulacionHoteles');

// Crear la colección "hoteles"
db.createCollection('hoteles');

// Crear un índice único sobre el campo idHotel
db.getCollection('hoteles').createIndex(
  { idHotel: 1 },
  { unique: true }
);

db.hoteles.insertMany(
    [
  {
    "idHotel": "h101",
    "nombre": "Grand Hotel Central",
    "estrellas": 5, 
    "admiteMascotas": false,
    "fechaApertura": "2015-06-20",
    "ubicacion": {
      "calle": "Via Laietana",
      "numero": 30,
      "codigoPostal": "08003",
      "coordenadas": { "lat": 41.38, "lon": 2.17 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 250.5, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 120.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 85.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h102",
    "nombre": "Hotel Costa Azul",
    "estrellas": 4,
    "admiteMascotas": true,
    "fechaApertura": "2018-03-12",
    "ubicacion": {
      "calle": "Avenida del Mar",
      "numero": 15,
      "codigoPostal": "11007",
      "coordenadas": { "lat": 36.53, "lon": -6.29 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 210.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 105.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 70.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h103",
    "nombre": "Montaña Real Resort",
    "estrellas": 5,
    "admiteMascotas": false,
    "fechaApertura": "2020-11-01",
    "ubicacion": {
      "calle": "Camino Alto",
      "numero": 45,
      "codigoPostal": "22700",
      "coordenadas": { "lat": 42.57, "lon": -0.55 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 300.0, "capacidad": 3, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 140.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 90.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h104",
    "nombre": "Hotel Plaza Mayor",
    "estrellas": 3,
    "admiteMascotas": true,
    "fechaApertura": "2010-09-15",
    "ubicacion": {
      "calle": "Plaza Mayor",
      "numero": 2,
      "codigoPostal": "28012",
      "coordenadas": { "lat": 40.415, "lon": -3.707 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 180.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 95.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 60.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h105",
    "nombre": "Hotel Sol Naciente",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2014-04-22",
    "ubicacion": {
      "calle": "Calle Sol",
      "numero": 88,
      "codigoPostal": "41004",
      "coordenadas": { "lat": 37.39, "lon": -5.99 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 230.0, "capacidad": 2, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 110.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 75.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h106",
    "nombre": "Hotel Riviera Blanca",
    "estrellas": 5,
    "admiteMascotas": true,
    "fechaApertura": "2017-07-08",
    "ubicacion": {
      "calle": "Paseo del Río",
      "numero": 21,
      "codigoPostal": "29670",
      "coordenadas": { "lat": 36.51, "lon": -4.88 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 280.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 130.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 90.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h107",
    "nombre": "City Hotel Norte",
    "estrellas": 3,
    "admiteMascotas": false,
    "fechaApertura": "2013-01-19",
    "ubicacion": {
      "calle": "Avenida del Prado",
      "numero": 101,
      "codigoPostal": "39011",
      "coordenadas": { "lat": 43.46, "lon": -3.8 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 160.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 85.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 55.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h108",
    "nombre": "Laguna Verde Hotel",
    "estrellas": 4,
    "admiteMascotas": true,
    "fechaApertura": "2019-05-10",
    "ubicacion": {
      "calle": "Camino del Lago",
      "numero": 9,
      "codigoPostal": "33012",
      "coordenadas": { "lat": 43.36, "lon": -5.85 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 220.0, "capacidad": 2, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 115.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 80.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h109",
    "nombre": "Hotel Mediterráneo",
    "estrellas": 5,
    "admiteMascotas": false,
    "fechaApertura": "2016-02-27",
    "ubicacion": {
      "calle": "Paseo del Mediterráneo",
      "numero": 50,
      "codigoPostal": "04638",
      "coordenadas": { "lat": 37.25, "lon": -1.87 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 320.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 150.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 95.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h110",
    "nombre": "Sierra Nevada Lodge",
    "estrellas": 4,
    "admiteMascotas": true,
    "fechaApertura": "2021-12-14",
    "ubicacion": {
      "calle": "Carretera Sierra",
      "numero": 80,
      "codigoPostal": "18196",
      "coordenadas": { "lat": 37.09, "lon": -3.39 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 260.0, "capacidad": 4, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 135.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 88.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h111",
    "nombre": "Hotel Puerta del Sol",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2012-06-30",
    "ubicacion": {
      "calle": "Calle Mayor",
      "numero": 12,
      "codigoPostal": "28013",
      "coordenadas": { "lat": 40.416, "lon": -3.703 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 240.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 120.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 75.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h112",
    "nombre": "Costa Dorada Palace",
    "estrellas": 5,
    "admiteMascotas": true,
    "fechaApertura": "2018-09-05",
    "ubicacion": {
      "calle": "Avenida Dorada",
      "numero": 101,
      "codigoPostal": "43840",
      "coordenadas": { "lat": 41.07, "lon": 1.15 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 330.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 160.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 98.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h113",
    "nombre": "Hotel Jardines del Valle",
    "estrellas": 3,
    "admiteMascotas": true,
    "fechaApertura": "2011-10-20",
    "ubicacion": {
      "calle": "Camino Verde",
      "numero": 8,
      "codigoPostal": "29130",
      "coordenadas": { "lat": 36.66, "lon": -4.57 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 150.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 85.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 60.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h114",
    "nombre": "Hotel Bosque Encantado",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2017-05-19",
    "ubicacion": {
      "calle": "Calle del Bosque",
      "numero": 33,
      "codigoPostal": "40300",
      "coordenadas": { "lat": 41.29, "lon": -3.92 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 215.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 110.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 70.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h115",
    "nombre": "Mar Azul Resort",
    "estrellas": 5,
    "admiteMascotas": true,
    "fechaApertura": "2020-08-11",
    "ubicacion": {
      "calle": "Paseo del Sol",
      "numero": 20,
      "codigoPostal": "35100",
      "coordenadas": { "lat": 27.77, "lon": -15.57 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 350.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 175.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 100.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h116",
    "nombre": "Hotel Ronda Antigua",
    "estrellas": 3,
    "admiteMascotas": false,
    "fechaApertura": "2008-04-03",
    "ubicacion": {
      "calle": "Calle Cuesta",
      "numero": 6,
      "codigoPostal": "29400",
      "coordenadas": { "lat": 36.74, "lon": -5.17 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 170.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 90.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 55.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h117",
    "nombre": "Monteverde Lodge",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2015-07-22",
    "ubicacion": {
      "calle": "Calle Nueva",
      "numero": 19,
      "codigoPostal": "24100",
      "coordenadas": { "lat": 42.46, "lon": -6.06 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 200.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 115.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 75.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h118",
    "nombre": "Hotel Bahía Serena",
    "estrellas": 4,
    "admiteMascotas": true,
    "fechaApertura": "2019-02-14",
    "ubicacion": {
      "calle": "Paseo Bahía",
      "numero": 50,
      "codigoPostal": "12594",
      "coordenadas": { "lat": 40.12, "lon": 0.07 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 240.0, "capacidad": 2, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 130.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 80.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h119",
    "nombre": "Hotel Alameda Real",
    "estrellas": 5,
    "admiteMascotas": true,
    "fechaApertura": "2016-10-09",
    "ubicacion": {
      "calle": "Avenida Real",
      "numero": 90,
      "codigoPostal": "46001",
      "coordenadas": { "lat": 39.47, "lon": -0.38 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 310.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 145.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 90.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h120",
    "nombre": "Hotel Mirador del Puerto",
    "estrellas": 3,
    "admiteMascotas": false,
    "fechaApertura": "2010-03-25",
    "ubicacion": {
      "calle": "Calle Puerto",
      "numero": 7,
      "codigoPostal": "30880",
      "coordenadas": { "lat": 37.6, "lon": -0.98 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 155.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 80.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 50.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h121",
    "nombre": "Hotel Colina Esmeralda",
    "estrellas": 4,
    "admiteMascotas": true,
    "fechaApertura": "2018-07-13",
    "ubicacion": {
      "calle": "Calle Esmeralda",
      "numero": 3,
      "codigoPostal": "33550",
      "coordenadas": { "lat": 43.4, "lon": -4.77 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 225.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 115.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 70.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h122",
    "nombre": "Hotel Costa Blanca Mar",
    "estrellas": 5,
    "admiteMascotas": false,
    "fechaApertura": "2021-06-02",
    "ubicacion": {
      "calle": "Avenida Playa",
      "numero": 42,
      "codigoPostal": "03700",
      "coordenadas": { "lat": 38.84, "lon": 0.11 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 345.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 170.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 105.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h123",
    "nombre": "Hotel Valle Dorado",
    "estrellas": 3,
    "admiteMascotas": true,
    "fechaApertura": "2009-11-30",
    "ubicacion": {
      "calle": "Camino del Valle",
      "numero": 14,
      "codigoPostal": "26580",
      "coordenadas": { "lat": 42.23, "lon": -2.03 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 145.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 75.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 50.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h124",
    "nombre": "Hotel Horizonte Azul",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2014-05-18",
    "ubicacion": {
      "calle": "Avenida Horizonte",
      "numero": 28,
      "codigoPostal": "15004",
      "coordenadas": { "lat": 43.37, "lon": -8.41 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 210.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 125.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 80.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h125",
    "nombre": "Hotel Termas del Sur",
    "estrellas": 5,
    "admiteMascotas": false,
    "fechaApertura": "2017-10-10",
    "ubicacion": {
      "calle": "Calle Termal",
      "numero": 11,
      "codigoPostal": "30600",
      "coordenadas": { "lat": 38.12, "lon": -1.3 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 320.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 155.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 95.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h126",
    "nombre": "Monte Claro Hotel",
    "estrellas": 3,
    "admiteMascotas": true,
    "fechaApertura": "2010-01-14",
    "ubicacion": {
      "calle": "Calle Clara",
      "numero": 9,
      "codigoPostal": "50015",
      "coordenadas": { "lat": 41.65, "lon": -0.89 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 160.0, "capacidad": 2, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 95.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 60.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h127",
    "nombre": "Hotel Brisas del Norte",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2018-09-09",
    "ubicacion": {
      "calle": "Calle Brisas",
      "numero": 45,
      "codigoPostal": "39005",
      "coordenadas": { "lat": 43.46, "lon": -3.81 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 220.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 130.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 85.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h128",
    "nombre": "Hotel Dunas Doradas",
    "estrellas": 5,
    "admiteMascotas": true,
    "fechaApertura": "2016-06-07",
    "ubicacion": {
      "calle": "Avenida Arena",
      "numero": 2,
      "codigoPostal": "35660",
      "coordenadas": { "lat": 28.73, "lon": -13.87 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 340.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 165.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 100.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h129",
    "nombre": "Hotel Costa Tranquila",
    "estrellas": 3,
    "admiteMascotas": true,
    "fechaApertura": "2012-03-12",
    "ubicacion": {
      "calle": "Camino Tranquilo",
      "numero": 12,
      "codigoPostal": "29700",
      "coordenadas": { "lat": 36.78, "lon": -4.1 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 150.0, "capacidad": 2, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 85.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 55.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h130",
    "nombre": "Costa Serena Spa Hotel",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2015-11-22",
    "ubicacion": {
      "calle": "Avenida Serena",
      "numero": 99,
      "codigoPostal": "07600",
      "coordenadas": { "lat": 39.49, "lon": 3.0 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 250.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 130.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 90.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h131",
    "nombre": "Hotel Vista Montaña",
    "estrellas": 3,
    "admiteMascotas": true,
    "fechaApertura": "2011-08-15",
    "ubicacion": {
      "calle": "Camino Alto",
      "numero": 17,
      "codigoPostal": "22400",
      "coordenadas": { "lat": 42.59, "lon": 0.52 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 155.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 85.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 60.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h132",
    "nombre": "Hotel Faro Marino",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2016-04-14",
    "ubicacion": {
      "calle": "Paseo del Faro",
      "numero": 200,
      "codigoPostal": "39004",
      "coordenadas": { "lat": 43.46, "lon": -3.8 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 260.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 140.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 85.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h133",
    "nombre": "Hotel Lagos del Sur",
    "estrellas": 5,
    "admiteMascotas": true,
    "fechaApertura": "2019-10-10",
    "ubicacion": {
      "calle": "Camino del Lago",
      "numero": 58,
      "codigoPostal": "33140",
      "coordenadas": { "lat": 43.48, "lon": -5.43 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 330.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 170.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 105.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h134",
    "nombre": "Hotel Oasis Urbano",
    "estrellas": 3,
    "admiteMascotas": true,
    "fechaApertura": "2014-02-11",
    "ubicacion": {
      "calle": "Calle Oasis",
      "numero": 11,
      "codigoPostal": "28004",
      "coordenadas": { "lat": 40.42, "lon": -3.7 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 165.0, "capacidad": 2, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 95.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 65.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h135",
    "nombre": "Hotel Miradores del Cielo",
    "estrellas": 4,
    "admiteMascotas": false,
    "fechaApertura": "2017-05-18",
    "ubicacion": {
      "calle": "Calle Mirador",
      "numero": 5,
      "codigoPostal": "29780",
      "coordenadas": { "lat": 36.75, "lon": -3.88 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 240.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 125.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 90.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h136",
    "nombre": "Hotel Jardín del Mar",
    "estrellas": 5,
    "admiteMascotas": true,
    "fechaApertura": "2020-03-22",
    "ubicacion": {
      "calle": "Avenida Jardín",
      "numero": 66,
      "codigoPostal": "11380",
      "coordenadas": { "lat": 36.01, "lon": -5.6 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 350.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 165.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 110.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h137",
    "nombre": "Hotel Camino Blanco",
    "estrellas": 3,
    "admiteMascotas": false,
    "fechaApertura": "2011-11-01",
    "ubicacion": {
      "calle": "Calle Blanca",
      "numero": 9,
      "codigoPostal": "15702",
      "coordenadas": { "lat": 42.87, "lon": -8.55 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 145.0, "capacidad": 2, "disponible": false },
      { "tipo": "Doble_Estandar", "precio": 75.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 55.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h138",
    "nombre": "Hotel Mareas Altas",
    "estrellas": 4,
    "admiteMascotas": true,
    "fechaApertura": "2018-07-07",
    "ubicacion": {
      "calle": "Paseo Marino",
      "numero": 22,
      "codigoPostal": "39610",
      "coordenadas": { "lat": 43.43, "lon": -3.83 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 230.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 120.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 80.0, "capacidad": 1, "disponible": true }
    ]
  },
  {
    "idHotel": "h139",
    "nombre": "Hotel Oasis del Desierto",
    "estrellas": 5,
    "admiteMascotas": false,
    "fechaApertura": "2019-03-29",
    "ubicacion": {
      "calle": "Calle Arena",
      "numero": 3,
      "codigoPostal": "04740",
      "coordenadas": { "lat": 36.76, "lon": -2.61 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 355.0, "capacidad": 3, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 180.0, "capacidad": 2, "disponible": true },
      { "tipo": "Individual", "precio": 110.0, "capacidad": 1, "disponible": false }
    ]
  },
  {
    "idHotel": "h140",
    "nombre": "Hotel Sierra Blanca",
    "estrellas": 4,
    "admiteMascotas": true,
    "fechaApertura": "2015-12-18",
    "ubicacion": {
      "calle": "Avenida Sierra",
      "numero": 55,
      "codigoPostal": "29602",
      "coordenadas": { "lat": 36.52, "lon": -4.88 }
    },
    "habitaciones": [
      { "tipo": "Suite_Junior", "precio": 245.0, "capacidad": 2, "disponible": true },
      { "tipo": "Doble_Estandar", "precio": 135.0, "capacidad": 2, "disponible": false },
      { "tipo": "Individual", "precio": 85.0, "capacidad": 1, "disponible": true }
    ]
  }
]
)
