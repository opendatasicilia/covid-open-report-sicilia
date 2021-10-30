const express = require('express');
const cors = require('cors');

const swaggerUI = require('swagger-ui-express');
const swaggerJsDoc = require('swagger-jsdoc');
const specs = require('./openapi.json')

const incidenzaRouter = require('./routes/incidenza');
const vacciniRouter = require('./routes/vaccini');

const port = process.env.PORT || 5000;
const app = express();

app.use(cors({ origin: '*' }));
app.use('/dati', express.static( '../dati'));
app.use('/assets', express.static(__dirname + '/assets'));

app.get('/', (req, res) => {
    res.redirect('/docs');
});

swaggerDoc = swaggerJsDoc(specs)

var options = {
    customCss: `
    .topbar-wrapper img {content:url('/assets/logo.png')}
    .swagger-ui .topbar {background: linear-gradient(#939393, #fafafa);}
    `,
    customSiteTitle: "COVID Reports API",
    customfavIcon: "/assets/favicon.ico"
  };

app.use("/docs", swaggerUI.serve, swaggerUI.setup(swaggerDoc, options))
app.use("/incidenza", incidenzaRouter);
app.use("/vaccini", vacciniRouter);

app.listen(port, () => console.log(`Listening on http://localhost:${port}`))
