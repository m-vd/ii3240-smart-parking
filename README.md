# Sample Python Services

One paragraph of your services description goes here

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

This services are written in **python**

## List of API Services

### **Testing**

---

This is just an API for testing.

* **URL**

  ```
  /api
  ```

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** 200 <br />

* **Sample Call:**

  ```
  curl -i /api
  ```

* **Notes:**

  This is where all uncertainties, commentary, discussion etc. can go. I recommend timestamping and identifying oneself when leaving comments here.

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

* [nameko](https://www.nameko.io/) - The microservice framework used

## Authors

* **Dimas Praja Purwa Aji (10209065)** - [prajadimas](http://178.128.104.74:9000/prajadimas)
* **Novianto Budi Kurniawan (33216028)** - [noviantobudik](http://178.128.104.74:9000/noviantobudik)
* **Gery Reynaldi (23217016)** - [geryreynaldi](http://178.128.104.74:9000/geryreynaldi)

## License

This project is licensed under the Apache License 2.0

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


