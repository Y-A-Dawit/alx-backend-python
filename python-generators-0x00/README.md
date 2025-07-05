# Python Generators – ALX Backend

This project explores the advanced use of **Python generators** to build memory-efficient, real-time data processing workflows using SQL and MySQL. It is part of the **ALX Backend Specialization**, focused on performance-driven programming.

## 🚀 Learning Objectives

By the end of this project, you will be able to:

- Implement Python **generators** using the `yield` keyword.
- Stream large datasets from a **MySQL database** efficiently.
- Use **batch and lazy loading techniques** with paginated data.
- Perform **aggregations** like average calculation without loading all data into memory.
- Integrate **SQL queries** with Python using `mysql-connector`.

---

## 📂 Project Structure

| File                     | Description |
|--------------------------|-------------|
| `seed.py`                | Seeds the MySQL database `ALX_prodev` with user data from a CSV file. |
| `0-stream_users.py`      | Streams each user row one by one using a generator. |
| `1-batch_processing.py`  | Streams user data in batches and filters users over age 25. |
| `2-lazy_paginate.py`     | Implements lazy pagination with generators using SQL `LIMIT` and `OFFSET`. |
| `4-stream_ages.py`       | Streams user ages using a generator and computes the average age. |

---

## 🧠 Concepts Covered

- `yield` and generator functions
- Lazy iteration and streaming
- Memory efficiency in data processing
- SQL pagination using `LIMIT` and `OFFSET`
- Connecting Python to MySQL with `mysql-connector-python`

---

## 🛠️ Setup & Usage

### 1. Install Dependencies

```bash
pip install mysql-connector-python
