# Assignment 2 SIO 2023/2024

## Description

This report documents Project 2 of SIO, being a follow-up of a first project, in which an online shop specializing in DETI memorabilia at the University of Aveiro was developed.

This project aims to explore the Application Security Verification Standard (ASVS) by applying its concepts to the previously developed web application. In addition to exploring and applying the ASVS, our group also explored and implemented two additional security-related features, alongside describing 9 Issues related to ASVS that our group considered that enhanced our app's security.

## Critical Audited Issues

The following issues were audited:

- Unverified Passwords Against Discovered Sets (ASVS 2.1.7);

- Weak Anti-CSRF Attacks Policies (ASVS 4.2.2);

- HTTP parameter pollution attacks (ASVS 5.1.1 and 8.3.1);

- Missing Validation of Structured Data (ASVS 5.1.4);

- Absence of secure encrypted client connections over TLS (ASVS 9.1.1, 9.1.2 and 9.1.3);

- Non-existence of data request limits (ASVS 11.1.2, 11.1.3 and 11.1.4);

- Non-existence of limits or validation of business logic actions (ASVS 11.1.5);

- Inputed Files without File Size Limit (ASVS 12.1.1);

- Missing CSP (Content Security Policy) (ASVS 14.4.3);

## Software Features Implemented

- Password strength evaluation: requiring a minimum of strength for passwords according to V2.1, with
breach verification using an external service;
    - ASVS applied now to comply with V2.1:
        - 2.1.1
        - 2.1.2
        - 2.1.3
        - 2.1.7
        - 2.1.8
        - 2.1.9
        - 2.1.12

- TOTP authentication login: enable login via one-time passwords generated with TOTP to authorize
access to the Web application
    - ASVS applied now to comply with V2.1:
        - 2.8.1
        - 2.8.2
        - 2.8.3
        - 2.8.4

## Other Issues resolved

With the implementitation of some issues and the anlysis provided by ZAP, some side related problems ended to be resolved too:

- Secure Session Cookie: Protect our app from hijacking, CSRF attacks and potential exposure of sensitive information.
    - ASVS related:
        - 3.2.3
        - 3.4.1
        - 3.4.3
        - 3.4.4

- X-Content-Type-Options Header Missing: Prevent MIME type sniffing, that could lead to XSS attacks 
    - ASVS related:
        - 14.4.4 

- Incorrect Session Logout
    - ASVS related:
        - 3.3.1

## **Authors**

| NMEC   | Name              |                  Email  |
| ------ | ----------------- | ----------------------: |
| 107186 | Vítor Santos      | vitor.mtsantos@ua.pt    |
| 107403 | João Luís         | jnluis@ua.pt            |
| 108122 | Alexandre Ribeiro | alexandrepribeiro@ua.pt |
| 108840 | José Gameiro      | jose.mcgameiro@ua.pt    |
