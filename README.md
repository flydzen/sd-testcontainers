Сборка образа докера: `docker build -t stock .`
Ручной запуск: `docker run -it -d --name stock_container -p 8081:8081 stock`

В requirements.txt прописаны зависимости именно для образа докера. для тестов нужен hamcrest и testcontainer-core