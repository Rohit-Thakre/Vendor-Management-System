# Vendor-Management-System

### Clone Project using this link
```
https://github.com/Rohit-Thakre/Vendor-Management-System.git
```

### To install all required packeges run in Command
```
pip install -r requirements.txt
```

### To start project run this Command
```
python manage.py runserver 
```

## End Points for API

### get all the vendors 
```
http://127.0.0.1:8000/api/vendors/
```

### Update, Delete or Get the specific vendor using  
```
http://127.0.0.1:8000/api/vendors/<int: id>/
```

### GET Performance metrix of vendor
```
http://127.0.0.1:8000/api/vendors/1/performance/
```

### Get all Purchase Orders
```
http://127.0.0.1:8000/api/purchase_orders/
```

### Update, Delete or Get the specific Purchase Order using
```
http://127.0.0.1:8000/api/purchase_orders/<int:id>/
```

### To post Ack Date
```
http://127.0.0.1:8000/api/purchase_orders/<int:id>/acknowledge/
```



