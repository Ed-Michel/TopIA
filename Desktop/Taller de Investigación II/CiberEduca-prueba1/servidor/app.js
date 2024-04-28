var express = require("express");
var mysql = require("mysql");
const dotenv = require('dotenv');
const jwt = require('jsonwebtoken');
var app = express(); // ejecutamos constructor

dotenv.config({ path: './.env' });


// Habilitar recepción JSON
app.use(express.json());

// Configuramos la conexión
const conexion = mysql.createConnection({
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD,
    database: process.env.DATABASE,
})

// Probar la conexión
conexion.connect(function (error) {
    if (error) {
        throw error;
    } else {
        console.log("Conectado a la base de datos")
    }
});

app.get("/", function (req, res) {
    res.send("<h1>Ruta de inicio</h1>")
});

// cors
const cors = require("cors");
const corsOptions = {
    origin: '*',
    credentials: true,
    optionSuccessStatus: 200,
}
app.use(cors(corsOptions))

app.get("/", function (req, res) {
    res.send("<h1>Ruta de inicio</h1>")
});

// Verbos de solicitud del cliente
// app.get();
// app.post();
// app.put();
// app.delete();

// ALUMNOS

alumnoRouter = require("./routes/alumnos")


app.use('/auth', require('./routes/auth'))

app.use("/api/alumnos", alumnoRouter);


app.use(express.urlencoded({ extended: false }));
app.use(express.json());

// Encender el servidor
app.listen("3000", function () {
    console.log("Servidor puerto 3000");
});

// Mostrar todos los grupos
app.get('/api/modulos', (req, res) => {
    conexion.query("SELECT * FROM modulo", (error, filas) => {
        if (error) {
            throw error;
        } else {
            res.header("Access-Control-Allow-Origin", "*")
            res.send(filas);
        }
    });
});

app.get('/api/infoAlumno/:id', (req, res) => {
    conexion.query("SELECT * FROM alumno where correo = ?", [req.params.id], (error, filas) => {
        if (error) {
            throw error;
        } else {
            res.header("Access-Control-Allow-Origin", "*")
            res.send(filas);
        }
    });
});


// Mostrar a un solo maestro
app.get('/api/actividades/:id', (req, res) => {

    console.log(req.params.id)
    conexion.query("SELECT * FROM ACTIVIDAD where MODID = ?", [req.params.id], (error, fila) => {
        if (error) {
            throw error;
        } else {

            res.send(fila)
        }
    })
})


app.post('/api/login',  (req, res) => {
    
    const EMAIL = req.body.EMAIL
    if (!EMAIL || EMAIL.trim() === '') {
        const error = new Error('El campo nombre es obligatorio');
        error.statusCode = 400; // Código de estado HTTP para "Bad Request"
        throw error;
      }
    conexion.query("SELECT * FROM usuario WHERE CORREO = ?", [req.body.EMAIL], (error, fila) => {
        if (error) {
            throw error;
        } 
   
    
    const token = jwt.sign({EMAIL:EMAIL},process.env.JWT_SECRETO)
    console.log(token)

    const cookiesOptions ={
        expires:new Date(Date.now()+ process.env.JWT_COOKIE_EXPIRA*24*60*1000),
        hhtpOnly:true
    }
    const respuesta = {
        token:token,
        user : fila,
        
    }
    res.send(respuesta) 
    
    })
})

module.exports = conexion;
