curl -X POST http://localhost:5000/api/instagram/update -d \
  '{"profile": "sarasmedlund"}' \
  -H 'Content-Type: application/json'

curl -X GET http://localhost:5000/api/instagram/download -d \
  '{"profile": "sarasmedlund"}' \
  -H 'Content-Type: application/json'


curl -X GET http://localhost:5000/api/instagram/update/stories -d \
  '{"profile": "sarasmedlund"}' \
  -H 'Content-Type: application/json'

curl -X POST http://localhost:5000/api/gmx/account_creator/ -d \
  '{"generate": "accounts"  }' \
  ‘{"first_name": "radom", 
  "last_name": "random",
  "birthdate": "23"; "12"; "1992" }‘
  "street:" "Mühlenstr.",
  "appartment:" "4",
  "zip_code:" "40213"
  "city:" "düsseldorf"
  "recovery_contact:" "fist_name+last_name"
  -H 'Content-Type: application/json'

