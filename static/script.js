
// Initialize Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.addEventListener('result', (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('user-input').value = transcript;
    });

    recognition.addEventListener('error', (event) => {
        console.error("Speech recognition error:", event.error);
    });
} else {
    console.log("Speech Recognition API not supported in this browser.");
}

// Handle voice button click
document.getElementById("voice-btn").addEventListener("click", () => {
    if (recognition) {
        recognition.start();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("send-btn").addEventListener("click", sendMessage);
    document.getElementById("user-input").addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

let stage = 0;  // 0 = Name, 1 = Age, 2 = Symptoms
let patient = { name: "", age: "", symptoms: "", duration: "", additionalSymptoms: "" };

function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;  // Prevent empty input

    let chatbox = document.getElementById("chat-box");

    if (stage === 0) {
        // Stage 0: Collect Name
        patient.name = userInput;
        chatbox.innerHTML += `<p class='user'><b>You:</b> ${userInput}</p>`;
        chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Nice to meet you, <b>${patient.name}</b>! How old are you?</p>`;
        document.getElementById("user-input").placeholder = "Enter your age...";
        stage = 1;
    } 
    else if (stage === 1) {
        // Stage 1: Collect Age
        if (isNaN(userInput) || userInput <= 0 || userInput > 120) {
            chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Please enter a valid age between 1-120.</p>`;
            return;
        }
        patient.age = userInput;
        chatbox.innerHTML += `<p class='user'><b>You:</b> ${userInput} years old</p>`;
        chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Thank you, <b>${patient.name}</b>! Now, tell me about your symptoms.</p>`;
        document.getElementById("user-input").placeholder = "Describe your symptoms...";
        stage = 2;
    } 
    else if (stage === 2) {
        // Stage 2: Collect Primary Symptoms
        patient.symptoms = userInput;
        chatbox.innerHTML += `<p class='user'><b>You:</b> ${userInput}</p>`;
        chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> How long have you been experiencing these symptoms?</p>`;
        document.getElementById("user-input").placeholder = "Enter duration (e.g., 3 days)...";
        stage = 3;
    }
    else if (stage === 3) {
        // Stage 3: Collect Symptom Duration
        patient.duration = userInput;
        chatbox.innerHTML += `<p class='user'><b>You:</b> ${userInput}</p>`;
        chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Are you experiencing any additional or related symptoms? If none, type 'None'.</p>`;
        document.getElementById("user-input").placeholder = "Additional symptoms...";
        stage = 4;
    }
    else if (stage === 4) {
        // Stage 4: Collect Additional/Relative Symptoms and Send Data
        patient.additionalSymptoms = userInput;
        chatbox.innerHTML += `<p class='user'><b>You:</b> ${userInput}</p>`;
        chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Thank you! Analyzing your information, please wait...🤖</p>`;
        
        // Fetch call with the complete patient object
        fetch("/chat", {
            method: "POST",
            body: JSON.stringify(patient),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> ${data.reply}</p>`;
            chatbox.scrollTop = chatbox.scrollHeight;
        })
        .catch(error => {
            console.error("Fetch Error:", error);
            chatbox.innerHTML += `<p class='bot' style="color: red;"><b>⚠️ Dr. Lili:</b> Sorry, something went wrong.</p>`;
        });
    
        document.getElementById("user-input").placeholder = "Chat Ended. Type 'Hi' to start the conversation";
        stage = 200;  // Set to looping stage
    }

    else if (stage === 200) {
        if (userInput.trim().toLowerCase() === "hi") {
            location.reload(); // ✅ Refresh the page when user types "Hi"
        } else {
            chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Chat has ended. Please type 'Hi' to restart.</p>`;
        }
    }
    
 

    // else if (stage === 5) {
    //     // Stage 5: Collect User's Place of Residence
    //     patient.location = userInput;
    //     chatbox.innerHTML += `<p class='user'><b>You:</b> ${userInput}</p>`;
    //     chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Thanks! Looking for nearby hospitals...</p>`;
        
    //     fetch("/nearby_hospitals", {
    //         method: "POST",
    //         body: JSON.stringify({ location: patient.location }),
    //         headers: { "Content-Type": "application/json" }
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Here are some nearby hospitals:</p>`;
    //         data.hospitals.forEach(hospital => {
    //             chatbox.innerHTML += `<p class='bot'>🔹 ${hospital.name} - ${hospital.address}</p>`;
    //         });
    //         chatbox.scrollTop = chatbox.scrollHeight;
    //     })
    //     .catch(error => {
    //         console.error("Fetch Error:", error);
    //         chatbox.innerHTML += `<p class='bot' style="color: red;"><b>⚠️ Dr. Lili:</b> Sorry, something went wrong while fetching hospital data.</p>`;
    //     });
    
    //     document.getElementById("user-input").placeholder = "Ask more questions...";
    //     stage = 6;  // Move to the next stage or continuous conversation
    // }
    // else if (stage === 6) {
    //     // Stage 6: Continuous Conversation / Follow-Up Questions
    //     let followUpQuery = userInput;
    //     chatbox.innerHTML += `<p class='user'><b>You:</b> ${followUpQuery}</p>`;
    //     chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> Let me think about that... please wait.</p>`;
        
    //     // Send follow-up query to the backend
    //     fetch("/chat", {
    //         method: "POST",
    //         body: JSON.stringify({ followUp: followUpQuery, name: patient.name }),
    //         headers: { "Content-Type": "application/json" }
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         chatbox.innerHTML += `<p class='bot'><b>Dr. Lili:</b> ${data.reply}</p>`;
    //         chatbox.scrollTop = chatbox.scrollHeight;
    //     })
    //     .catch(error => {
    //         console.error("Fetch Error:", error);
    //         chatbox.innerHTML += `<p class='bot' style="color: red;"><b>⚠️ Dr. Lili:</b> Sorry, something went wrong.</p>`;
    //     });
    // }

    document.getElementById("user-input").value = "";
}


// Function to Auto-Scroll Chatbox to Latest Message
function autoScrollChat() {
    chatbox.scrollTop = chatbox.scrollHeight;
}

