let token = null;

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const response = await fetch(`${window.config.API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    if (data.token) {
        token = data.token;
        localStorage.setItem('token', token);
        window.location.href = 'profile.html';
    } else {
        alert('Login failed');
    }
}

async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const email = document.getElementById('register-email').value;
    const avatar = document.getElementById('register-avatar').value;
    const response = await fetch(`${window.config.API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, email, avatar })
    });
    const data = await response.json();
    if (data.message === 'registered successfully') {
        alert('Registered successfully, please login');
        window.location.href = 'login.html';
    } else {
        alert('Registration failed');
    }
}

async function loadProfile() {
    token = localStorage.getItem('token');
    const response = await fetch(`${window.config.API_BASE_URL}/auth/user`, {
        headers: {
            'x-access-tokens': token
        }
    });
    const user = await response.json();
    document.getElementById('user-id').innerText = user.id;
    document.getElementById('user-username').innerText = user.username;
    document.getElementById('user-email').innerText = user.email;
    document.getElementById('user-avatar').src = user.avatar;
    loadUserBlogs(user.id);
}

async function updateProfile() {
    const password = document.getElementById('update-password').value;
    const email = document.getElementById('update-email').value;
    const avatar = document.getElementById('update-avatar').value;
    const response = await fetch(`${window.config.API_BASE_URL}/auth/user`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ password, email, avatar })
    });
    const data = await response.json();
    if (data.message === 'user updated') {
        alert('Profile updated');
        loadProfile();
    } else {
        alert('Update failed');
    }
}

async function loadUserBlogs(userId) {
    const response = await fetch(`${window.config.API_BASE_URL}/blog/blogs/${userId}`);
    const blogs = await response.json();
    const myBlogsList = document.getElementById('my-blogs');
    myBlogsList.innerHTML = '';
    blogs.forEach(blog => {
        const li = document.createElement('li');
        li.innerText = `${blog.title} - ${blog.content}`;
        li.innerHTML += ` <button onclick="deleteBlog(${blog.id})">Delete</button>`;
        li.innerHTML += ` <button onclick="editBlog(${blog.id})">Edit</button>`;
        myBlogsList.appendChild(li);
    });
}

async function createBlog() {
    const title = document.getElementById('blog-title').value;
    const content = document.getElementById('blog-content').value;
    const response = await fetch(`${window.config.API_BASE_URL}/blog/blogs`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ title, content })
    });
    const data = await response.json();
    if (data.message === 'Blog created!') {
        alert('Blog created');
        loadProfile();
    } else {
        alert('Creation failed');
    }
}

async function deleteBlog(blogId) {
    const response = await fetch(`${window.config.API_BASE_URL}/blog/blogs/${blogId}`, {
        method: 'DELETE',
        headers: {
            'x-access-tokens': token
        }
    });
    const data = await response.json();
    if (data.message === 'Blog deleted!') {
        alert('Blog deleted');
        loadProfile();
    } else {
        alert('Deletion failed');
    }
}

async function editBlog(blogId) {
    localStorage.setItem('editBlogId', blogId);
    window.location.href = 'blog_edit.html';
}

async function updateBlog() {
    const blogId = localStorage.getItem('editBlogId');
    const title = document.getElementById('edit-blog-title').value;
    const content = document.getElementById('edit-blog-content').value;
    const response = await fetch(`${window.config.API_BASE_URL}/blog/blogs/${blogId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'x-access-tokens': token
        },
        body: JSON.stringify({ title, content })
    });
    const data = await response.json();
    if (data.message === 'Blog updated!') {
        alert('Blog updated');
        window.location.href = 'profile.html';
    } else {
        alert('Update failed');
    }
}

async function loadAllBlogs() {
    const response = await fetch(`${window.config.API_BASE_URL}/blog/blogs`);
    const blogs = await response.json();
    const allBlogsList = document.getElementById('all-blogs');
    allBlogsList.innerHTML = '';
    blogs.forEach(blog => {
        const li = document.createElement('li');
        li.innerText = `${blog.title} by User ${blog.user_id} - ${blog.content}`;
        allBlogsList.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop();
    if (currentPage === 'profile.html') {
        loadProfile();
    } else if (currentPage === 'blogs.html') {
        loadAllBlogs();
    } else if (currentPage === 'blog_edit.html') {
        const blogId = localStorage.getItem('editBlogId');
        if (blogId) {
            fetch(`${window.config.API_BASE_URL}/blog/blogs/${blogId}`)
                .then(response => response.json())
                .then(blog => {
                    document.getElementById('edit-blog-title').value = blog.title;
                    document.getElementById('edit-blog-content').value = blog.content;
                });
        }
    }
});
