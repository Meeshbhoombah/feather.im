/*
 * app.js
 *
 * Connects to a peer in the NKN network and creates and broadcasts messages to
 * the connected peer.
 *
 */


const express   = require("express");
const nkn       = require("nkn-client");

const app       = express();
app.set('port', process.env.PORT || 3000)


// custom 404 page
app.use( function(req, res) {
    res.status(400)
    res.render('404')
})


// custom 500 page
app.use(function (err, req, res, next) {
    console.error(err.stack)
    res.status(500)
    res.render('500')
})


app.listen(app.get('port'), function() {
    console.log('Express servers started on http://localhost' 
        + app.get('port')
        + '; press Ctrl-C to terminate')
})


