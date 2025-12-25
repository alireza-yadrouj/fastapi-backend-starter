# FastAPI Backend Starter

A starter backend project using **FastAPI** with JWT authentication, role-based access, and CRUD operations for `cases`.

---

## Features
- User registration (`/register`) and login (`/login`) with JWT
- CRUD operations on `cases` with optional filtering
- Role & Permission system (`user` and `admin`)
- Type-safe `current_user` with Pydantic `CurrentUser` model

---

## Endpoints

### Auth
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT

### Cases
- `GET /cases` - List all cases (filter by title/description)
- `POST /cases` - Create a new case
- `PATCH /cases/{case_id}` - Update a case
- `DELETE /cases/{case_id}` - Delete a case

**Notes:**
- New users default role: `user`
- Admin can manage all cases; users can manage only their own
