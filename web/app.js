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
      db.all("SELECT * FROM links WHERE nickname=?", username, function (err, rows) {
        rows.forEach(element => {
          links.push({ id: element.id , link: element.link });
        });
        // console.log(links);
        resolve(links);
      });

    });
  });

}


function get_photo_details(photo_id) {

  return new Promise(function (resolve, reject) {

    db.serialize(function () {
      var details = [];
      db.all("SELECT type, posible FROM data WHERE link_id=?", photo_id, function (err, rows) {
        rows.forEach(element => {
          details.push({ type: element.type, posible: element.posible });
        });
        //console.log(details);
        resolve(details);
      });

    });
  });

}

app.post('/buscar', function(req, res) {
  console.log(req.body);
});



app.get('/', function (req, res) {
  // User INFO
  if (typeof req.query.name !== 'undefined' && req.query.name) {
    let usuari = req.query.name;
    get_links(usuari).then(function (users) {
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
  } // Photo INFO
  else if (typeof req.query.photo !== 'undefined' && req.query.photo) {
    let photo = req.query.photo;
    get_photo_details(photo).then(function (tipos) {
      llista_tipos = [];
      llista_tipos = tipos;
      //console.log(llista_tipos);
      res.render('index', {
        title: 'Details from photo',
        photo: photo,
        tipos: llista_tipos
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