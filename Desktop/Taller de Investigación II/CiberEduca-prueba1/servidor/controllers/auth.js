const mysql = require('mysql');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');


const conexion = mysql.createConnection({
    host: process.env.DATABASE_HOST,
    user: process.env.DATABASE_USER,
    password:process.env.DATABASE_PASSWORD ,
    database: process.env.DATABASE,
})



exports.register = (req, res) => {


    console.log(req.body)
    res.send('form submitted')

    const {EMAIL, CONTRASENIA} = req.body;
   
    conexion.query('SELECT CORREO FROM usuario WHERE CORREO =?',[EMAIL],async (error,results)=>{
        if(error){
            console.log(error);
        }
        if(results.length>0){
            res.json({ error: err })
        }
        
        

        let hashedPassword = await bcrypt.hash(CONTRASENIA,8);
        console.log(hashedPassword);
        let sql = "INSERT INTO usuario SET ?";

        let data = {
            EMAIL: EMAIL,
            CONTRASENIA: hashedPassword,
        }
        try {
            conexion.query(sql,data, function (error, results) {
           
        });
        } catch (error) {
            if (error) {
                throw error
            } else {
                res.send(results)
            }
        }
        
    
    });
}