### **Title: Django COMPREDICT** / Repositoriy: saulyaka/compredict
##### **version:** 0.0.1
#### **Author:** Alla Popova
#### **Framework:** Django
#### **Data base:** Sqlite3
#### **Project status:** working/dev
### **About the project**
Web service provides a way to normalize **JSON** data collected from sensors. The data can be accessed through **JWT authentication** for security purposes. The normalization process involves removing the mean and dividing by the **standard deviation for each column** of the data to standardize it. The normalized data can then be used for further analysis or modeling.
### **Requirements:**
> - Docker version 23.0.3
> - Docker compose version v2.17.2
## **Install project:**
> Command: docker compose up
> Sever exposes on 0.0.0.0 port 8000
> Docker will create image compredict_app and start container app
### **Endpoints**
> - **documentation**  /doc/schema/docs/
> - **deviation**  /api/
> - **jwt**  /api/token/
> - **refresh token**  /api/token/refresh/
### **Test coverage report:**
        htmlcov/index.html