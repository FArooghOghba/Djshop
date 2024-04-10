# Djshop: An E-Commerce Site with Django REST Framework

Djshop is an ongoing project aimed at developing an e-commerce
website using Django REST Framework. While the project is still
under development, it already incorporates various tools and
technologies for testing, linting, containerization, and development
automation.
Djshop is designed to provide a robust foundation for building
an e-commerce platform.

## Features

- **Django REST Framework**: Utilizes the powerful Django framework for building RESTful APIs.
- **User Authentication**: Includes user registration, login, and profile management functionalities.
- **Product Management**: Allows adding, updating, and deleting products.
- **Shopping Cart**: Enables users to add products to their cart and manage their cart contents.
- **Order Processing**: Supports order creation and management.
- **Testing**: Pytest is integrated for automated testing to ensure code reliability.
- **Type Checking**: Mypy is used for static type checking to enhance code quality.
- **Linting and Code Formatting**: Flake8, isort and mypy are used for linting and type-checking to maintain code quality.
- **Containerization**: Docker and Docker Compose are used for containerization, making it easier to manage dependencies and deployment.
- **Development Automation**: Utilizes Makefile for automating common development tasks.

## Installation


To set up and run this project locally, follow these steps and you can use the MakeFile commands:

1. Clone the repository:

    ```bash
    git clone https://github.com/FArooghOghba/Djshop.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Djshop
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv env
    ```

4. Activate the virtual environment:

    - On Windows:

    ```bash
    .\env\Scripts\activate
    ```

    - On macOS and Linux:

    ```bash
    source env/bin/activate
    ```

5. Install dependencies:

   ```bash
   pip install -r requirements_dev.txt
   ```

6. Run migrations:

    ```bash
    make migrate
    ```

7. spin off docker compose

   ```bash
   make docker-compose-build
   ```

8. Access the API at `http://127.0.0.1:8000/`.

## Testing

To run tests, use the following command:

   ```bash
   make pytest
   ```

## Code Quality

To check code quality and style, run the following commands:

   ```bash
   make flake8
   make mypy
   ```

## Contributing

Contributions to Djshop are welcome!
Please feel free to submit issues or pull requests.

## License

This project is licensed under the [FALAFEL-WARE LICENSE](https://github.com/FArooghOghba/Djshop/blob/master/LICENSE)
