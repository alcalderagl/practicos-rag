# Building an End-to-End Retrieval-Augmented Generation System

Welcome to the **Building an End-to-End Retrieval-Augmented Generation System** repository. This repository is designed to guide you through the process of creating a complete Retrieval-Augmented Generation (RAG) system from scratch, following a structured curriculum.

## Setup Instructions

To get started with the course:

1. Clone this repository:
   ```bash
   git clone https://github.com/CarlosCaris/practicos-rag.git
2. Create a virtual environment
    ```bash
    python -m venv .venv
    pip freeze | less to know the versions
3. Activate the environment
   ```bash
    # On Mac
    .venv/bin/activate or source .venv/bin/activate
    # On Windows
    .venv\Scripts\activate
4. Install requirements
    ```bash
    pip install -r requirements.txt or make install
5. Run app
    ```bash
    streamlit run main_app.py


# integration changes

Before commit your changes it is necessary to

1. git add `your files`
2. run the following command, IMPORTANT it is only required the first time!
    ``` bash 
    pre-commit install --hook-type pre-push
4. Run pre-commit checks manually to ensure setup
    ``` bash
    pre-commit run --all-files
5. if format and list <p style="background-color:green">passed</p>
6. proceed to `git commit -m "message"`, otherwise run the following commands and proceed to run integration changes again
    ``` bash
    make format and make tslint
7. git push origin or git push

## Table of Contents

- [Building an End-to-End Retrieval-Augmented Generation System](#building-an-end-to-end-retrieval-augmented-generation-system)
  - [Setup Instructions](#setup-instructions)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Course Outline](#course-outline)
    - [Lesson 1: Introduction to Retrieval-Augmented Generation (RAG)](#lesson-1-introduction-to-retrieval-augmented-generation-rag)
    - [Lesson 2: Document Chunking Strategies](#lesson-2-document-chunking-strategies)

## Introduction

This repository contains the materials and code needed to build a complete Retrieval-Augmented Generation (RAG) system. A RAG system combines the strengths of large language models with an external knowledge base to improve the accuracy and relevance of generated responses. Throughout this course, you'll gain hands-on experience with the various components of a RAG system, from document chunking to deployment in the cloud.

## Course Outline

### Lesson 1: Introduction to Retrieval-Augmented Generation (RAG)
- **Objective:** Understand the fundamentals of RAG and its applications.
- **Topics:**
  - Overview of RAG systems
  - Challenges in large language models (e.g., hallucinations, outdated information)
  - Basic components of a RAG system
- **Practical Task:** Set up your development environment and familiarize yourself with the basic concepts.
- **Resources:** 
  - Basics
  - More concepts

### Lesson 2: Document Chunking Strategies
- **Objective:** Learn how to effectively segment documents for better retrieval performance.
- **Topics:**
  - Chunking techniques: token-level, sentence-level, semantic-level
  - Balancing context preservation with retrieval precision
  - Small2Big and sliding window techniques
- **Practical Task:** Implement chunking strategies on a sample dataset.
- **Resources:**
  - The five levels of chunking
  - A guide to chunking
