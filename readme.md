<div align="center">

  <h1>⚡ CoProT</h1>

  <h3>Coding Problem Tracker</h3>

  <p>
    <strong>Track. Understand. Improve.</strong>
  </p>

  <p>
    A multi-user platform for tracking coding problems,<br>
    understanding problem-solving patterns, and building consistent coding habits.
  </p>

  <br>

  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
  <img src="https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white">
  <img src="https://img.shields.io/badge/Status-Backend%20MVP-success?style=for-the-badge">

  <br><br>

  <p>
    <a href="#-about">About</a> •
    <a href="#-features">Features</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-api">API</a> •
    <a href="#-setup">Setup</a> •
    <a href="#-roadmap">Roadmap</a>
  </p>

</div>

---

## 🧠 About

**CoProT (Coding Problem Tracker)** is a backend application designed to help developers keep track of the coding problems they solve across different programming platforms.

Instead of simply remembering *which problems were solved*, CoProT stores meaningful information about each problem — including its difficulty, topic, number of attempts, patterns, notes, and solved date.

The system is designed as a **multi-user application**, where every user has their own problem data and can only access or modify their own records.

> **The goal:** turn scattered coding-problem practice into structured, searchable, and meaningful data.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication

- User registration
- Email validation
- Secure password hashing
- Argon2 password hashing
- JWT authentication
- HTTP Bearer authentication
- Protected API routes
- Current-user identification

</td>

<td width="50%">

### 🧩 Problem Tracking

- Create coding problems
- View personal problems
- View individual problems
- Update problems
- Partial updates
- Delete problems
- Track attempts
- Track coding patterns
- Add notes and solved dates

</td>
</tr>

<tr>
<td>

### 👥 Multi-User Architecture

Every problem belongs to a specific user.

Database queries use the authenticated user's ID to ensure that users cannot access, modify, or delete another user's problems.

</td>

<td>

### 🛡️ API Safety

- Pydantic validation
- Parameterized SQL queries
- JWT verification
- Environment-based secrets
- HTTP status codes
- CORS configuration
- Controlled API responses

</td>
</tr>
</table>

---

## 🏗️ Architecture

CoProT follows a modular backend architecture where each part of the application has a specific responsibility.

```text
                         ┌──────────────────┐
                         │      Client      │
                         │  Web / Frontend  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │      Routes      │
                         └────────┬─────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  ▼               ▼               ▼
             ┌─────────┐    ┌──────────┐    ┌──────────┐
             │ Schemas │    │   Auth   │    │ Security │
             │ Pydantic│    │   JWT    │    │ Password │
             └─────────┘    └──────────┘    └──────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Database     │
                         │      MySQL       │
                         └──────────────────┘