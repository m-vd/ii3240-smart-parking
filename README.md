# Smart Parking Services

"Smart Parking Services" is a system of services intented to realize smart campus concept, especially in parking management. The services is made by several IST students from ITB as a project for one of their courses: II3240: Information Systems and Technology Engineering. 

---

* [Language](#language)
* [List of API services](#list-of-api-services)
  - [Testing](#testing)
  - [Another](#another)
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

  ```
  /checkin
  /checkout
  ```

* **Method:**

  `POST`

* **Sample Call:**

  ```
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
    ```
    { "ticketID": "a0785435-ebee-48a9-ad61-6599f2ff4559", 
      "entryTime": "2019-05-13 17:54:09.888289", 
      "exitTime": "None" }
    ```
    If successfull, the service will also send an e-mail to the user's registered email notifying them that they are checked in.

* **Error Response:**

  There are 2 error codes, 400 and 403. 400 BAD REQUEST indicates that there is something wrong which mostly is caused by client's input. For example, incomplete parameters or wrong input type. 403 FORBIDDEN is caused by trying to access endpoint that are not available for the user.

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `ERR: You have already checked in.`
  * **Code:** 403 FORBIDDEN <br />
    **Content:** `ERR: You're not allowed to access this endpoint.`


### **Another**

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

  This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here.

## Built With

* [django](https://www.djangoproject.com) - The web framework used

## Authors

* **Rifda Annelies Az Zahra (18216001)** - [18216001](http://178.128.104.74:9000/18216001)
* **Ivan Wiryadi (18216017)** - [18216017](http://178.128.104.74:9000/18216017)
* **Ardji Naufal Setiawan (18216021)** - [18216021](http://178.128.104.74:9000/18216021)
* **Muhammad Taufik Rahman (18216030)** - [18216030](http://178.128.104.74:9000/18216030)
* **Savira Dwia Nadela (18216052)** - [18216052](http://178.128.104.74:9000/18216052)

## License

This project is licensed under the Apache License 2.0

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


