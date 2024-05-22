![Service](https://img.shields.io/badge/BoulotMan-Assignment-ee4f51)
![Specs](https://github.com/sntakirutimana72/lecontinent/actions/workflows/specs.yml/badge.svg)


# Assignment: Django API

The assignment objective is to write API endpoints to interact with products and orders data in a database.

## Functionalities
- User can view all products and orders
    ```
  GET /api/products
  GET /api/orders
  ```
- User can retrieve a specific product or order from the database
    ```
  GET /api/products/<pk:int>
  GET /api/orders/<pk:int>
  ```
- User can create a new product or order
    ```
  POST /api/products
  POST /api/orders
  ```
- User can update an existing product or order record
    ```
  PUT /api/products/<pk:int>
  PUT /api/orders/<pk:int>
  ```
- User can delete an existing product or order record
    ```
  DELETE /api/products/<pk:int>
  DELETe /api/orders/<pk:int>
  ```


## 🛠️ Built with

![](https://skillicons.dev/icons?i=py,django,sqlite)


## Tools

![Utils](https://skillicons.dev/icons?i=git,github,githubactions,postman,pycharm)


## How To Set it up

1. Clone this project repo to your local environment ([Repository](...))
2. Install Pycharm, a python editor
3. Install Python ~v3.10
4. Install Pipenv ~latest
5. Open the cloned repo directory with Pycharm
6. Open the terminal within Pycharm and run
    ```shell
   $ pipenv shell
   $ pipenv install
   $ python manage.py runserver
    ```
7. Finally, with your testing tool of your choice (postman: recommended) tool, try it out


## How to run tests

```shell
$ pytest
```



## ✍️ Authors

👤 **Steve**

- GitHub: [@sntakirutimana72](https://github.com/sntakirutimana72/)
- LinkedIn: [steve-ntakirutimana](https://www.linkedin.com/in/steve-ntakirutimana/)


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).


## 📝 License

This project is [MIT](./LICENSE) licensed.
