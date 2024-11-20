const PromptInput = document.querySelector("#chat-input");
const SendBtn = document.querySelector("#send-btn");
const ChatContainer = document.querySelector(".chat-container");
const ThemeBtn = document.querySelector("#theme-btn");
const DeleteBtn = document.querySelector("#delete-btn");

let UserPrompt= null;

// Create Chat Outgoing Div
const CreateElement =(html, ClassName)=>{
    const ChatDiv = document.createElement("div");
    ChatDiv.classList.add("chat", ClassName);
    ChatDiv.innerHTML = html;
    return ChatDiv;
}

const DataFromLocalStorage =()=>{
    let ThemeSwitcher = localStorage.getItem("Theme-Switcher");
    document.body.classList.toggle("light-mode", ThemeSwitcher === "light_mode");
    ThemeBtn.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
    const DeafaultContent = `<div class="Default-Text">
                                <h1>Introducing The ChatGPT </h1>
                                <p>Future Of Artificial Intelligence</p>
                            </div>`
    ChatContainer.innerHTML = localStorage.getItem("All-Chats") || DeafaultContent;
    
    ChatContainer.scrollTo(0, ChatContainer.scrollHeight);
}
DataFromLocalStorage();

const GetOpenAiResponses = async (IncominChatDiv)=>{


    let PElement = document.createElement("p");
    try{
    //     const response = await fetch("http://127.0.0.1:5000/generate", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ prompt: UserPrompt }),
    //     });
    
    
    //   const data = await response.json();
        PElement.textContent = "Cevap";
    }
    catch(error){
        PElement.classList.add("error");
        PElement.innerText = "Oops something went wrong while getting responses please try again";
    }
    IncominChatDiv.querySelector(".loading-dots-animation").remove();
    IncominChatDiv.querySelector(".chat-details").appendChild(PElement);
    ChatContainer.scrollTo(0, ChatContainer.scrollHeight);
    localStorage.setItem("All-Chats",ChatContainer.innerHTML)
}


const CopyResponses =(CopyBtn)=>{
  let ResponseText = CopyBtn.parentElement.querySelector("p");
  navigator.clipboard.writeText(ResponseText.textContent);
  CopyBtn.textContent = "done";
  setTimeout(()=> CopyBtn.textContent = "content_copy", 1000)
}
   

const TypyingAnimation = ()=>{
    const html = `<div class="chat-content-box">
                    <div class="chat-details">
                        <img src="https://i.ibb.co/0VDMm2X/chatbot.jpg" alt="chatbot-image">
                            <div class="loading-dots-animation">
                                <div class="loading-dot" style="--delay:0.2s;" ></div>
                                <div class="loading-dot" style="--delay:0.3s;" ></div>
                                <div class="loading-dot" style="--delay:0.4s;" ></div>
                            </div>
                    </div> 
                    <span onclick="CopyResponses(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
    const IncominChatDiv = CreateElement(html, "incoming");
    ChatContainer.appendChild(IncominChatDiv);
    ChatContainer.scrollTo(0, ChatContainer.scrollHeight);
    GetOpenAiResponses(IncominChatDiv); // Getting Generated Responses
}

const OutgoinChat =()=>{
    UserPrompt = PromptInput.value.trim();
    if(!PromptInput) return;
    const html = `<div class="chat-content-box">
                        <div class="chat-details">
                            <img src="https://i.ibb.co/tcgjS29/user.jpg" alt="user-image">
                            <p></p>
                        </div>
                    </div>`
    const OutgoinChatDiv = CreateElement(html, "outgoing");
    ChatContainer.appendChild(OutgoinChatDiv);
    OutgoinChatDiv.querySelector("p").textContent = UserPrompt;
    document.querySelector(".Default-Text")?.remove();
    ChatContainer.scrollTo(0, ChatContainer.scrollHeight);
    setTimeout(TypyingAnimation,500);
}

ThemeBtn.addEventListener("click", ()=>{
    document.body.classList.toggle("light-mode");
    localStorage.setItem("Theme-Switcher", ThemeBtn.innerText);
    ThemeBtn.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});

DeleteBtn.addEventListener("click", ()=>{
    if(confirm("Are you sure you want to delete all chats ?")){
        localStorage.removeItem("All-Chats");
    }
    DataFromLocalStorage();
})

let InitialHeight = PromptInput.scrollHeight;

PromptInput.addEventListener("input", ()=>{
    PromptInput.style.height = `${InitialHeight}px`;
    PromptInput.style.height = `${PromptInput.scrollHeight}px`;
})

PromptInput.addEventListener("keydown", (e)=>{
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800){
        e.preventDefault();
        OutgoinChat();
    }
})

SendBtn.addEventListener("click",OutgoinChat)