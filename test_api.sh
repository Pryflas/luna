#!/bin/bash

API_KEY="test-api-key-12345"
BASE_URL="http://localhost:8000"

echo "=== 1. Получение всех зданий ==="
curl -H "X-API-Key: $API_KEY" "$BASE_URL/buildings/"
echo -e "\n\n"

echo "=== 2. Получение всех видов деятельности ==="
curl -H "X-API-Key: $API_KEY" "$BASE_URL/activities/"
echo -e "\n\n"

echo "=== 3. Получение организации по ID (ID=1) ==="
curl -H "X-API-Key: $API_KEY" "$BASE_URL/organizations/1"
echo -e "\n\n"

echo "=== 4. Поиск организаций по зданию (building_id=1) ==="
curl -H "X-API-Key: $API_KEY" "$BASE_URL/organizations/?building_id=1"
echo -e "\n\n"

echo "=== 5. Поиск организаций по виду деятельности (activity_id=1) ==="
curl -H "X-API-Key: $API_KEY" "$BASE_URL/organizations/?activity_id=1"
echo -e "\n\n"

echo "=== 6. Поиск организаций по названию ==="
curl -H "X-API-Key: $API_KEY" --data-urlencode "name=Рога" -G "$BASE_URL/organizations/"
echo -e "\n\n"

echo "=== 7. Поиск организаций в радиусе (Москва, 100км) ==="
curl -H "X-API-Key: $API_KEY" "$BASE_URL/organizations/?latitude=55.7558&longitude=37.6173&radius_km=100"
echo -e "\n\n"

echo "=== 8. Поиск организаций в прямоугольнике ==="
curl -H "X-API-Key: $API_KEY" "$BASE_URL/organizations/?lat1=55.0&lon1=30.0&lat2=60.0&lon2=38.0"
echo -e "\n\n"

echo "=== 9. Проверка без API ключа (должна вернуть 422 или 403) ==="
curl "$BASE_URL/buildings/"
echo -e "\n\n"
