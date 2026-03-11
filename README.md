
# StudyVault

## Overview

StudyVault is a cloud-based web application that allows users to securely upload, store, and search academic documents. The platform automatically extracts text from uploaded files and enables keyword-based searching across documents, making it easier to manage and retrieve study materials.

The application demonstrates how cloud services and modern backend technologies can be combined to build a scalable document management system.

---

## Features

* Upload documents to cloud storage
* Automatic text extraction from uploaded files
* Keyword-based document search
* Secure file storage and retrieval
* Download and delete stored files
* Simple and intuitive user interface
* Containerized deployment using Docker

---

## Tech Stack

**Backend**

* Python
* Flask

**Cloud Services**

* AWS S3 (file storage)
* AWS Textract (text extraction)

**DevOps / Deployment**

* Docker
* AWS EC2

**Frontend**

* HTML
* CSS

---

## Architecture

User uploads document

↓

Flask backend processes request

↓

File stored in AWS S3

↓

AWS Textract extracts text from document

↓

Extracted text stored for searching

↓

User can search documents by keywords

---

## Deployment

The application is deployed on a cloud server using Docker containers. An EC2 instance run the container and expose the application to the internet.

---
