# Notesbox

**Notesbox** is a Django-based web application that helps users save, organize, and manage educational YouTube videos by subject. Users can securely log in, create subject folders, add video links, and even share useful code snippets. The app supports personalized video libraries and an admin can recommend videos visible to all users.

---

## Features
- **User Authentication**: Secure login and registration system using email and password.
- **Subject-based Organization**: Users can create subjects (like folders) and add videos under each.
- **Video Management**: Add, view, and manage YouTube links with subject tags.
- **Admin Recommendations**: Admin can push recommended videos visible to all users.
- **Code Sharing**: Users can add and view code snippets related to videos or topics.
-  **Responsive UI**: Clean and minimal UI using HTML, CSS, and Django templates.

---

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default Django DB)
- **Authentication**: Django built-in user model

---

## Project Structure
```
notesbox/
├── manage.py
├── notesbox/
│ ├── settings.py
│ ├── urls.py
│ └── ...
├── main_app/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│ │ └── ...
│ └── static/
│ └── ...
└── db.sqlite3
```
## How to Use

Register/Login using email and password.

Create Subject Folders.

Use "Add Video" button to save YouTube links under subjects.

Add optional code snippets for reference.

View Admin Recommended videos at the top of your dashboard.

---

## Future Improvements
Video thumbnail previews

Search and filter options

Save timestamps or personal notes per video

Comments or discussion under each video/code

Public video/code sharing links

---

🙋‍♂️ Author
Aditya Singh
