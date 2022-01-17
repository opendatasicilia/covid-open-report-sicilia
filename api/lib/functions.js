const csv = require('csvtojson');

module.exports = {
    parse: (f, schema) => {
        let file = csv({
            flatKeys: true,
            checkType: true,
            colParser: schema
        }).fromFile(f)
        return file
    },
    filter: (array, queries) => {
        const {from, to, prov, q} = queries
        const compDate = (date) => {
            return new Date(date.replace(/-/g,'/'))
        }
        return array.filter(x => {
            return (q ? (JSON.stringify(x).toLowerCase().indexOf(q.toLowerCase()) !== -1) : true) &&
                   (prov ? (x.cod_prov == prov) : true) &&
                   (from ? (compDate(x.data) >= compDate(from)) : true) &&
                   (to ? (compDate(x.data) <= compDate(to)) : true);
        });
    }
}