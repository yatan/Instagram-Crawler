var express = require('express');
var app = express();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('./data/crawler');
var path = require('path');

var usuaris = [];

db.serialize(function() {

  db.each('SELECT * FROM users', function(err, row) {
    usuaris.push(row.nickname);
    // console.log(row.nickname);
  });

});

db.close();


app.get('/', function (req, res) {
  //res.send('Hello World!');
  res.render('index', { 
    title: 'Userlist',
    usuarios : usuaris
    });
});

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.listen(3000, function () {
  console.log('Example app listening on http://localhost:3000 !');
});