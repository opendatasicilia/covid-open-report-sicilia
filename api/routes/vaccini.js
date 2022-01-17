const express = require("express");
const router = express.Router();
const func = require('../lib/functions')

/**
 * @swagger
 * components:
 *   schemas:
 *     Vaccini:
 *       type: object
 *       properties:
 *         data:
 *           type: date
 *           description: Data pubblicazione report DASOE
 *         cod_prov:
 *           type: integer
 *           description: Codice ISTAT della Provincia	
 *         pro_com_t:
 *           type: string
 *           description: Codice ISTAT del Comune	
 *         provincia:
 *           type: string
 *           description: Denominazione della Provincia
 *         comune:
 *           type: string
 *           description: Denominazione del Comune
 *         %vaccinati:
 *           type: float
 *           description: Percentuale di persone vaccinate con almeno una dose (calcolata rispetto al target)
 *         %immunizzati:
 *           type: float
 *           description: Percentuale di persone vaccinate con 2 o più dosi, persone vaccinate in monodose per pregressa infezione Covid, persone vaccinate con Janssen (calcolata rispetto al target)
 *       example:
 *         data: "2021-10-27"
 *         cod_prov: 84
 *         pro_com_t: "084002"
 *         provincia: "Agrigento"
 *         comune: "Alessandria della Rocca"
 *         %vaccinati: 84.65
 *         %immunizzati: 82.72
 */

 /**
  * @swagger
  * tags:
  *   name: Vaccini
  */

/**
 * @swagger
 * /vaccini:
 *   get:
 *     summary: Percentuali di vaccinati ed immunizzati per i comuni siciliani
 *     parameters:
 *       - in: query
 *         name: q
 *         schema:
 *           type: string
 *         description: Restituisce i campi che contengono parti della stringa <small>(es. q=Palermo)</small>
 *       - in: query
 *         name: prov
 *         schema:
 *           type: int
 *         description: Restituisce i campi appartenenti ad un particolare codice provinciale <small>(es. prov=82)</small>
 *       - in: query
 *         name: from
 *         schema:
 *           type: string
 *         description: Restituisce i campi a partire da una determinata data, in formato YYYY-MM-DD <small>(es. from=2021-10-10)</small>
 *       - in: query
 *         name: to
 *         schema:
 *           type: string
 *         description: Restituisce i campi fino ad una determinata data, in formato YYYY-MM-DD <small>(es. to=2021-10-27)</small>
 *     tags: [Vaccini]
 *     responses:
 *       200:
 *         description: Statistiche per comune
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Vaccini'
 */

/**
 * @swagger
 * /vaccini/latest:
 *   get:
 *     summary: Percentuali di vaccinati ed immunizzati per i comuni siciliani nell'ultima settimana misurata
 *     parameters:
 *       - in: query
 *         name: q
 *         schema:
 *           type: string
 *         description: Restituisce i campi che contengono parti della stringa <small>(es. q=Palermo)</small>
 *       - in: query
 *         name: prov
 *         schema:
 *           type: int
 *         description: Restituisce i campi appartenenti ad un particolare codice provinciale <small>(es. prov=82)</small>
 *     tags: [Vaccini]
 *     responses:
 *       200:
 *         description: Statistiche per comune
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Vaccini'
 */

const schema = {
    'data': "date",
    'cod_prov': "int",
    'pro_com_t': "string",
    'provincia': "string",
    'comune': "string",
    '%vaccinati': "float",
    '%immunizzati': "float",
}

const path = `${__dirname}/../../dati/vaccini/vaccini`;

router.get('/', async (req, res) => {
    const dati = await func.parse(path+'.csv', schema)
    const response = func.filter(dati, req.query);

    try{
        res.send(response)
    }
    catch(e){
        res.send(e)
    }
})

router.get('/latest', async (req, res) => {
    const dati = await func.parse(path+'-latest.csv', schema)
    const response = func.filter(dati, req.query);

    try{
        res.send(response)
    }
    catch(e){
        res.send(e)
    }
})

module.exports = router;