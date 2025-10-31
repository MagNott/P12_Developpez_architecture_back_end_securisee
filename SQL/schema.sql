CREATE TABLE customers (
        id INTEGER NOT NULL, 
        company_name VARCHAR(100) NOT NULL, 
        creation_date DATE, 
        last_update DATE, 
        commercial_id INTEGER NOT NULL, 
        first_name VARCHAR(50) NOT NULL, 
        last_name VARCHAR(50) NOT NULL, 
        mail VARCHAR NOT NULL, 
        phone_number VARCHAR(15) NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(commercial_id) REFERENCES collaborators (id), 
        UNIQUE (mail)
)



CREATE TABLE collaborators (
        id INTEGER NOT NULL, 
        login VARCHAR(20) NOT NULL, 
        password VARCHAR(100) NOT NULL, 
        department_id INTEGER NOT NULL, 
        first_name VARCHAR(50) NOT NULL, 
        last_name VARCHAR(50) NOT NULL, 
        mail VARCHAR NOT NULL, 
        phone_number VARCHAR(15) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (login), 
        FOREIGN KEY(department_id) REFERENCES departments (id), 
        UNIQUE (mail)
)



CREATE TABLE contracts (
        id INTEGER NOT NULL, 
        contract_amount FLOAT NOT NULL, 
        amount_due FLOAT NOT NULL, 
        creation_date DATE NOT NULL, 
        customer_id INTEGER NOT NULL, 
        status_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(customer_id) REFERENCES customers (id), 
        FOREIGN KEY(status_id) REFERENCES statuses (id)
)



CREATE TABLE events (
        id INTEGER NOT NULL, 
        location VARCHAR(200) NOT NULL, 
        attendees INTEGER NOT NULL, 
        notes VARCHAR, 
        start_date DATE NOT NULL, 
        end_date DATE NOT NULL, 
        contract_id INTEGER NOT NULL, 
        collaborator_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(contract_id) REFERENCES contracts (id), 
        FOREIGN KEY(collaborator_id) REFERENCES collaborators (id)
)



CREATE TABLE departments (
        id INTEGER NOT NULL, 
        name VARCHAR(20) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
)



CREATE TABLE statuses (
        id INTEGER NOT NULL, 
        name VARCHAR(20) NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
)