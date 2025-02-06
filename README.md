# Web pages manager
Web pages manager is part of [Flight ticket tracking application](https://github.com/MikhailCherepanovD/notification_service).

### Overview
This microservice serves as an intermediary between the web client and the main backend.  
It performs two key functions:  
1. Serves HTML pages to users.  
2. Acts as a proxy, forwarding API requests from the frontend to the main backend and returning responses.  

### Functionality
- Serves web pages written in HTML/CSS/JS;
- Handles user sessions;  
- Forwards API requests from the frontend to the main backend;  
- Processes and formats responses before sending them to the frontend;

### Tech Stack
- **Backend:** Flask  
- **Frontend:** HTML/CSS/JS  
- **Communication:** REST API requests to the main backend  