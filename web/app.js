var express = require('express');
var app = express();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('./data/crawler');
var path = require('path');

var usuaris = [];

db.serialize(function () {

  db.each('SELECT * FROM users', function (err, row) {
    usuaris.push(row.nickname);
  });

});



function get_links(username) {

  return new Promise(function (resolve, reject) {

    db.serialize(function () {
      var links = [];
      db.each("SELECT * FROM links WHERE nickname=?", username, function (err, row) {
        links.push(row.link);
         //console.log(JSON.stringify(links));
         resolve(links);
      });

    });
  });

}



app.get('/', function (req, res) {
  if (typeof req.query.name !== 'undefined' && req.query.name) {
    let usuari = req.query.name;
    get_links(usuari).then( function(users){
      llista_users = [];
      llista_users = users;
      res.render('index', {
        title: 'Links from user',
        user: usuari,
        links: llista_users,
        usuarios: usuaris
      });

    }).catch(function (err) {
      console.error(err.stack);
    });
    
    //console.log(req.query.name);

  }
  else {
    res.render('index', {
      title: 'Userlist',
      usuarios: usuaris
    });
  }
});

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.listen(3000, function () {
  console.log('Example app listening on http://localhost:3000 !');
});

//db.close();