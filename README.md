### **Title: Standardization Django COMPREDICT** / Repositoriy: saulyaka/compredict
##### **version:** 0.0.1
#### **Author:** Alla Popova
#### **Framework:** Django
#### **Data base:** Sqlite3
#### **Project status:** working/dev
### **About the project**
Web service provides a way to normalize **JSON** data collected from sensors. The data can be accessed through **JWT authentication** for security purposes. The normalization process involves removing the mean and dividing by the **standard deviation for each column** of the data to standardize it. The normalized data can then be used for further analysis or modeling. A simple web interface is available.
### **Requirements:**
> Docker version 23.0.3
>
> Docker compose version v2.17.2
## **Install project:**
> Command: docker-compose up
>
> Sever exposes on port 8000
>
> Docker will create image compredict_app and start container app.
### **Endpoints**
> **documentation**
>> [/doc/schema/docs/](http:localhost:8000/doc/schema/docs/)
>
> **normalization**
>> [/api/normalization/](http:localhost:8000/api/normalization/)
>
> **jwt**
>> [/api/token/](http:localhost:8000/api/deviation/)
>
> **refresh token**
>> [/api/token/refresh/](http:localhost:8000//api/token/refresh/)
### **Test coverage report:**
        htmlcov/index.html