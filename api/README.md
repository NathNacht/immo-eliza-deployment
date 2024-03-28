# immo-eliza-deployment

``` bash
uvicorn app:app --reload
```

# example json

``` json
{
  "postal_code": 1210,
  "property_subtype": "FLAT_STUDIO",
  "number_of_rooms": null,
  "living_area": 33.0,
  "kitchen_type": "NOT_INSTALLED",
  "furnished": null,
  "open_fire": 0,
  "terrace": 0,
  "terrace_area": 0,
  "garden": 1,
  "garden_area": 6.0,
  "number_of_facades": 0,
  "swimming_pool": null,
  "state_of_building": "TO_BE_DONE_UP",
  "province": "brussel"
}
```
  
property_id,locality_name,postal_code,latitude,longitude,property_type,property_subtype,price,type_of_sale,number_of_rooms,living_area,kitchen_type,fully_equipped_kitchen,furnished,open_fire,terrace,terrace_area,garden,garden_area,surface_of_good,number_of_facades,swimming_pool,state_of_building,main_city,province
11141961,sint-joost-ten-node,1210,,,APARTMENT,FLAT_STUDIO,120000.0,BUY_REGULAR,,33.0,NOT_INSTALLED,1.0,,0,1.0,6.0,,,,,,TO_BE_DONE_UP,sint-joost-ten-node,brussel

