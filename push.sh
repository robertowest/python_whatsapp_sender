#!/bin/bash

git add .
git commit -m "actualizaciones"

# git push -u origin master
echo "¿Quiere subir los cambios?"
select sn in "Sí" "No"; do
    case $sn in
        Sí ) git push; break;;
        No ) exit;;
    esac
done
