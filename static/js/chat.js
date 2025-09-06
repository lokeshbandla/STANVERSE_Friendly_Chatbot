let synth = window.speechSynthesis;
let speaking = false;
let utter;
/* ---------------- Persistent User ID ---------------- */
function getUserId() {
  const urlParams = new URLSearchParams(window.location.search);
  let uid = urlParams.get("user_id") || localStorage.getItem("user_id");
  if (uid) {
    localStorage.setItem("user_id", uid);
    const newUrl = new URL(window.location.href);
    newUrl.searchParams.set("user_id", uid); // update URL
    window.history.replaceState(null, "", newUrl.toString());
  }
  return uid;
}
let USER_ID = getUserId();
function scrollToBottom() {
  const msgContainer = document.getElementById("messages");
  // force scroll after rendering
  requestAnimationFrame(() => {
    msgContainer.scrollTop = msgContainer.scrollHeight;
  });
}

function appendMessage(sender, text, avatar) {
  let msgDiv = document.createElement("div");
  msgDiv.className = "msg " + sender;

  let img = document.createElement("img");
  img.src = avatar;
  img.className = "avatar";

  let bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerText = text;

  if (sender === "bot") {
    let speakBtn = document.createElement("button");
    speakBtn.innerText = "🔊 Listen";
    speakBtn.className = "speak-btn";
    speakBtn.onclick = function () {
      if (!speaking) {
        utter = new SpeechSynthesisUtterance(text);
        synth.speak(utter);
        speaking = true;
        speakBtn.innerText = "⏹ Stop";
        utter.onend = function () {
          speaking = false;
          speakBtn.innerText = "🔊 Listen";
        };
      } else {
        synth.cancel();
        speaking = false;
        speakBtn.innerText = "🔊 Listen";
      }
    };
    bubble.appendChild(document.createElement("br"));
    bubble.appendChild(speakBtn);
  }

  if (sender === "user") {
    msgDiv.appendChild(bubble);
    msgDiv.appendChild(img);
  } else {
    msgDiv.appendChild(img);
    msgDiv.appendChild(bubble);
  }

  const container = document.getElementById("messages");
  container.appendChild(msgDiv);

  // ✅ Smooth auto scroll
  scrollToBottom();
}



async function sendMessage() {
  let input = document.getElementById("userInput");
  let text = input.value.trim();
  if (!text) return;

  appendMessage("user", text, "/static/images/user-avatar.png");
  input.value = "";
  document.getElementById("typing").style.display = "block";

  let res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: USER_ID, message: text }),
  });

  let data = await res.json();
  localStorage.setItem("user_id", data.user_id);
  const newUrl = new URL(window.location.href);
  newUrl.searchParams.set("user_id", data.user_id);
  window.history.replaceState(null, "", newUrl.toString());
  USER_ID = data.user_id;
  document.getElementById("typing").style.display = "none";
  appendMessage("bot", data.reply, "/static/images/bot-avatar.png");
}

function checkEnter(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

function startRecording() {
  const recognition = new (window.SpeechRecognition ||
    window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("userInput").value = transcript;
    sendMessage();
  };

  recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
  };
}
