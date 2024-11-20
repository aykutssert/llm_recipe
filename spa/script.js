const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const generateBtn = document.getElementById("generate-btn");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  try {
    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (response.ok) {
      alert(`Welcome ${data.email}`);
      document.getElementById("generate-section").style.display = "block";
    } else {
      document.getElementById("login-error").innerText = data.error;
    }
  } catch (err) {
    console.error(err);
  }




});

registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;

  try {
    const response = await fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (response.ok) {
      alert("Registration successful!");
    } else {
      document.getElementById("register-error").innerText = data.error;
    }
  } catch (err) {
    console.error(err);
  }
});

generateBtn.addEventListener("click", async () => {
  const prompt = document.getElementById("prompt").value;

  try {
    const response = await fetch("http://127.0.0.1:5000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const data = await response.json();
    if (response.ok) {
      document.getElementById("recipe-result").innerText = data.response;
    } else {
      document.getElementById("recipe-result").innerText = data.error;
    }
  } catch (err) {
    console.error(err);
  }
});
