Create table bikes_and_cars.analysis_table as
select i.code_insee_commune,i.nom_arrondissement_communes, i.nombre_de_velo_dispo, c.nb_vp
from bikes_and_cars.cars as c
inner join (
select code_insee_commune,nom_arrondissement_communes, sum(capacity) as nombre_de_velo_dispo
from bikes_and_cars.bikes
group by code_insee_commune, nom_arrondissement_communes
) as i
on c.commune_code = i.code_insee_commune