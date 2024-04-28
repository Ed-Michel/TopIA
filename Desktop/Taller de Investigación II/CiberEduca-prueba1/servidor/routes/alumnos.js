const express = require("express");
const router = express.Router();
const conexion= require("../app");

// Ruta para obtener datos de la tabla de alumnos

router.get('/api/escuela:id', (req, res) => {
    conexion.query("SELECT NOMBRE FROM escuela where clave = ?",[req.params.id], (error, filas) => {
        if (error) {
            throw error;
        } else {
            res.header("Access-Control-Allow-Origin", "*")
            res.send(filas);
        }
    });
});

module.exports = router;