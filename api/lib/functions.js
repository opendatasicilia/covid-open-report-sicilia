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
    filter: (array, query) => {
        return array.filter(x =>  JSON.stringify(x).toLowerCase().indexOf(query.toLowerCase()) !== -1)
    },
    comune: (array, query) => {
        return array.filter(x => x.comune.toLowerCase().includes(query.toLowerCase()))
    }
}
