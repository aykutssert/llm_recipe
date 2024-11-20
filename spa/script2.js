document.addEventListener("DOMContentLoaded", () => {
    const loginSection = document.getElementById("login-section");
    const registerSection = document.getElementById("register-section");
    const chatSection = document.getElementById("chat-section");
  
    const goToRegister = document.getElementById("go-to-register");
    const goToLogin = document.getElementById("go-to-login");
  
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
  
    const chatOutput = document.getElementById("chat-output");
    const userInput = document.getElementById("user-input");
    const sendMessageButton = document.getElementById("send-message");
    const imageUpload = document.getElementById("image-upload");
  
    // Navigate between Login and Register
    goToRegister.addEventListener("click", (e) => {
      e.preventDefault();
      loginSection.classList.add("hidden");
      registerSection.classList.remove("hidden");
    });
  
    goToLogin.addEventListener("click", (e) => {
      e.preventDefault();
      registerSection.classList.add("hidden");
      loginSection.classList.remove("hidden");
    });
  
    // Handle Login
    loginForm.addEventListener("submit",async (e) => {
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
          loginSection.classList.add("hidden");
            chatSection.classList.remove("hidden");
        } else {
            document.getElementById("login-error").innerText = "Invalid login credentials.";
        }
      } catch (err) {
        console.error(err);
      }


    });
  
    // Handle Register
    registerForm.addEventListener("submit",async (e) => {
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
          registerSection.classList.add("hidden");
          loginSection.classList.remove("hidden");
        } else {
          document.getElementById("register-error").innerText = data.error;
        }
      } catch (err) {
        console.error(err);
      }
    });
  
    // Handle Chat Messages
    sendMessageButton.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (message) {
          // Kullanıcı mesajını oluştur ve göster
          const userMessageDiv = document.createElement("div");
          userMessageDiv.className = "user-message";
          userMessageDiv.innerText = message;
          chatOutput.appendChild(userMessageDiv);
      
          // Chat geçmişini kaydırma
          chatOutput.scrollTop = chatOutput.scrollHeight;
      
          try {
            // Backend'e mesaj gönderme
            const response = await fetch("http://127.0.0.1:5000/generate", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ prompt: message }),
            });
      
            const data = await response.json();
            if (response.ok) {
              // Bot cevabını oluştur ve göster
              const botMessageDiv = document.createElement("div");
              botMessageDiv.className = "bot-message";
              botMessageDiv.innerText = data.response;
              chatOutput.appendChild(botMessageDiv);
      
              // Chat geçmişini kaydırma
              chatOutput.scrollTop = chatOutput.scrollHeight;
            } else {
              // Hata mesajı göster
              const errorMessageDiv = document.createElement("div");
              errorMessageDiv.className = "bot-message";
              errorMessageDiv.innerText = `Error: ${data.error}`;
              chatOutput.appendChild(errorMessageDiv);
            }
          } catch (err) {
            console.error(err);
            const errorDiv = document.createElement("div");
            errorDiv.className = "bot-message";
            errorDiv.innerText = "An error occurred while connecting to the server.";
            chatOutput.appendChild(errorDiv);
          }
      
          // Input alanını temizle
          userInput.value = "";
        }
      });
      
  
    // Handle Image Upload
    imageUpload.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
        alert(`Uploaded image: ${file.name}`);
      }
    });
  });
  