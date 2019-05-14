# Smart Parking Services

"Smart Parking Services" is a system of services intented to realize smart campus concept, especially in parking management. The services is made by several IST students from ITB as a project for one of their courses: II3240: Information Systems and Technology Engineering.

---

* [Language](#language)
* [List of API services](#list-of-api-services)
  + [Ticketing](#ticketing)
  + [Help](#help)
  + [Disaster](#disaster)
  + [Booking](#booking)
* [Built With](#built-with)
* [Authors](#authors)
* [License](#license)
* [Acknowledgments](#acknowledgments)

---

## Language

This services are written in **python**.

## List of API Services

### **Ticketing**

Ticketing handles both check in and check out requests for the clients.

* **URL**

  ```path
  /checkin
  /checkout
  ```

* **Method:**

  `POST`

* **Sample Call:**

  ```bash
  curl -i /checkin
  curl -i /checkout
  ```

* **Data Params**

  When sending the POST requests to the endpoints, you have to include these parameters:
  * `userID`
  * `locationID`  (there is no need for this parameter when sending POST to /checkout)

* **Success Response:**
  
  What should the status code be on success and is there any returned data? This is useful when people need to to know what their callbacks should expect!

  * **Code:** 200 <br />
  
    ```json
    {
      "ticketID": "a0785435-ebee-48a9-ad61-6599f2ff4559",
      "entryTime": "2019-05-13 17:54:09.888289",
      "exitTime": "None"
    }
    ```

    If successfull, the service will also send an e-mail to the user's registered email notifying them that they are checked in.
    Exit time will not be empty (None) as the example above for successfull check out response.

* **Error Response:**

  There are 2 error codes, 400 and 403. 400 BAD REQUEST indicates that there is something wrong which mostly is caused by client's input. For example, incomplete parameters or wrong input type. 403 FORBIDDEN is caused by trying to access endpoint that are not available for the user. For example:

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `ERR: You have already checked in.`
  * **Code:** 403 FORBIDDEN <br />
    **Content:** `ERR: You're not allowed to access this endpoint.`

### **Help**

This service is intended as a help center to help users if there's anything that might be confusing for them by simply sending a ticket including their questions. The question will then be answered by officers / admins.

* **URL**

  ```path
  /ask-help
  /answer-help
  ```

* **Method:**

  `POST`

* **Sample Call:**

  ```bash
  curl -i /ask-help
  curl -i /answer-help
  ```

* **Data Params**

  When sending POST request to `/ask-help` , you have to include these parameters:
  * `userID`
  * `question`

  When sending POST request to `/answer-help` , you have to include these parameters:
  * `helpID`
  * `answer`

* **Success Response:**
  
  What should the status code be on success and is there any returned data? This is useful when people need to to know what their callbacks should expect!

  * **Code:** 200 `/ask-help` <br />

    ```json
    {  
      "helpID": "0f648e88-cdaf-4c92-ac09-b3471a7f8649",
      "userID": "18216001",
      "question": "Hi, how are you?"
    }
    ```

  * **Code:** 200 `/answer-help` <br />

    ```json
    {  
      "helpID": "0f648e88-cdaf-4c92-ac09-b3471a7f8649",
      "question": "Hi, how are you?",
      "answer": "I'm fine, thanks! How about you?"
    }
    ```  

* **Error Response:**

  There are 2 error codes, 400 and 403. 400 BAD REQUEST indicates that there is something wrong which mostly is caused by client's input. For example, incomplete parameters or wrong input type. 403 FORBIDDEN is caused by trying to access endpoint that are not available for the user. For example:

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `ERR: You are not registered.`
  * **Code:** 403 FORBIDDEN <br />
    **Content:** `ERR: You're not allowed to access this endpoint.`

### **Disaster**

This service provides a notification system for users who parked in a specific area. The administrators may send notification to every users in an area informing them that something happened, for example a flood or a fallen tree.

* **URL**

  ```path
  /add-disaster
  /update-disaster
  ```

* **Method:**

  `POST`

* **Sample Call:**

  ```bash
  curl -X POST http://localhost:8000/add-disaster \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'locationID=Motor_Sipil&status=Hancur&description=Semua%20pohon%20tumbang'

  curl -X POST http://localhost:8000/update-disaster \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'disasterID=b88b43e6-6d8c-442b-8f6e-c176adfcde75&status=Aman&description=Pohon%20dibersihkan'
  ```

* **Data Params**

  When sending POST request to `/add-disaster` , you have to include these parameters:
  * `locationID`
  * `status`
  * `description`

  When sending POST request to `/update-disaster` , you have to include these parameters:
  * `disasterID`
  * `status`
  * `description`

* **Success Response:**

  * **Code:** 200 `/add-disaster` <br />

    ```json
    {
    "disasterID": "b88b43e6-6d8c-442b-8f6e-c176adfcde75",
    "status": "Hancur",
    "location": "Lot object (Motor_Sipil)",
    "description": "Semua pohon tumbang"
    }
    ```

  * **Code:** 200 `/update-disaster` <br />

    ```json
    {
      "disasterID": "b88b43e6-6d8c-442b-8f6e-c176adfcde75",
      "status": "Aman",
      "location": "Lot object (Motor_Sipil)",
      "description": "Pohon dibersihkan"
    }
    ```  

* **Error Response:**

  There are 2 error codes, 400 and 403. 400 BAD REQUEST indicates that there is something wrong which mostly is caused by client's input. For example, incomplete parameters or wrong input type. 403 FORBIDDEN is caused by trying to access endpoint that are not available for the user. For example:

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `ERR: No disaster found.`
  * **Code:** 403 FORBIDDEN <br />
    **Content:** `ERR: You're not allowed to access this endpoint.`

### **Booking**

This service provides a mean to book a parking space. Users may use their ID to book a space in a desired parking lot.

* **URL**

  ```path
  /add-booking
  /check-in-booking
  ```

* **Method:**

  `POST`

* **Sample Call:**

  ```bash
  curl -X POST http://localhost:8000/add-booking \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'userID=18216001&locationID=Motor_SR&bookingTime=2019-05-14%2022%3A00%3A00'

  curl -X POST http://localhost:8000/check-in-booking \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d userID=18216017
  ```

* **Data Params**

  When sending POST request to `/add-booking` , you have to include these parameters:
  * `userID`
  * `locationID`
  * `bookingTime`

  When sending POST request to `/check-in-booking` , you have to include these parameters:
  * `userID`

* **Success Response:**

  * **Code:** 200 `/add-booking` <br />

    ```json
    {
      "ticketID": "670fed0e-c992-44cf-9fa3-151c311f87bc",
      "bookingTime": "2019-05-14 22:00:00",
      "location": "Parkiran Motor SR"
    }
    ```

  * **Code:** 200 `/check-in-booking` <br />

    ```json
    {
      "bookingID": "038fa91b-1080-4c9d-a350-9cf0e3e3f28c",
      "bookingTime": "2019-05-14 23:00:00",
      "location": "Parkiran Motor SR",
      "status": "Checked In",
      "checkInTime": "2019-05-14 23:00:33.890728"
    }
    ```  

* **Error Response:**

  There are 2 error codes, 400 and 403. 400 BAD REQUEST indicates that there is something wrong which mostly is caused by client's input. For example, incomplete parameters or wrong input type. 403 FORBIDDEN is caused by trying to access endpoint that are not available for the user. For example:

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `ERR: You have not booked yet.`
  * **Code:** 403 FORBIDDEN <br />
    **Content:** `ERR: You're not allowed to access this endpoint.`

<!-- ### **Another**

---

Additional information about your API call. Try to use verbs that match both request type (fetching vs modifying) and plurality (one vs multiple).

* **URL**

  ```
  The URL Structure (path only, no root url)
  ```

* **Method:**
  
  The request type

  `GET` | `POST` | `DELETE` | `PUT`
  
* **URL Params**

  If URL params exist, specify them in accordance with name mentioned in URL section. Separate into optional and required. Document data constraints.

   **Required:**

   `id=[integer]`

   **Optional:**

   `photo_id=[alphanumeric]`

* **Data Params**

  If making a post request, what should the body payload look like? URL Params rules apply here too.

* **Success Response:**
  
  What should the status code be on success and is there any returned data? This is useful when people need to to know what their callbacks should expect!

  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`
 
* **Error Response:**

  Most endpoints will have many ways they can fail. From unauthorized access, to wrongful parameters etc. All of those should be liste d here. It might seem repetitive, but it helps prevent assumptions from being made where they should be.

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "Log in" }`

  OR

  * **Code:** 422 UNPROCESSABLE ENTRY <br />
    **Content:** `{ error : "Email Invalid" }`

* **Sample Call:**

  Just a sample call to your endpoint in a runnable format ($.ajax call or a curl request) - this makes life easier and more predictable.

* **Notes:**

  This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here. -->

## Built With

* [django](https://www.djangoproject.com) - The web framework used

## Authors

* **Rifda Annelies Az Zahra (18216001)** - [18216001](https://gitlab.com/rifdaaaz)
* **Ivan Wiryadi (18216017)** - [18216017](https://gitlab.com/m-vd12)
* **Ardji Naufal Setiawan (18216021)** - [18216021](https://gitlab.com/Ardjisetiawan)
* **Muhammad Taufik Rahman (18216030)** - [18216030](https://gitlab.com/ahmadtr)
* **Savira Dwia Nadela (18216052)** - [18216052](https://gitlab.com/saviranadela)

## License

This project is licensed under the Apache License 2.0

## Acknowledgments

* Thanks to the developers of Django, Python, and all libraries used in this project!
