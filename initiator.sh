#!/bin/bash

echo "************************"
echo "CRAWLER HACKEPS" 
echo "************************"

echo "Menu:"
echo "************************"
echo "1 - Inici crawler.py sense especificar seed"
echo "2 - Inici crawler.py especificant seed"
echo "************************"
echo "3 - Obtenir imatges dels perfils - get_images_from_profile.py"
echo "************************"
echo "4 - Exget_images_from_profile.pyportar users --> DB  (export_users_db.py)"
echo "5 - Exportar links --> DB (export_links_db.py)"
echo "************************"
echo "6 - Obtenir informació de les imatges via Clarifi API (get_data_from_image.py)"
echo "************************"
echo "7 - Executar server (node app.js)"
echo "************************"
read menu

case "$menu" in
1)
python crawler.py
;;
2)
python crawler.py alpersaldiran
;;
3)
python get_images_from_profile.py
;;
4)
python export_users_db.py
;;
5)
python export_links_db.py
;;
6)
python get_data_from_image.py
;;
7)
cd web/
node app.js
;;
*) echo "Opcio incorrecta"
   ;;
esac
