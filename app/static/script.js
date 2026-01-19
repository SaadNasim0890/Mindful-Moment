// Geolocation State
let userLocation = { lat: null, lon: null };

async function analyzeMood() {
    const input = document.getElementById('userInput');
    const btn = document.getElementById('analyzeBtn');
    const resultSection = document.getElementById('resultSection');

    const text = input.value.trim();
    if (!text) return;

    // UI Loading State
    btn.classList.add('loading');
    btn.disabled = true;
    resultSection.classList.add('hidden');
    resultSection.style.display = 'none';

    // Try to get location (optional, non-blocking for UX speed, but good to have)
    try {
        await getUserLocation();
    } catch (e) {
        console.log("Location skipped or denied");
    }

    try {
        const payload = {
            text: text,
            user_id: "web_user"
        };

        if (userLocation.lat !== null) {
            payload.latitude = userLocation.lat;
            payload.longitude = userLocation.lon;
        }

        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        displayResult(data);

    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}

function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject("Geolocation not supported");
        } else {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    userLocation.lat = position.coords.latitude;
                    userLocation.lon = position.coords.longitude;
                    resolve();
                },
                (error) => {
                    console.log("Geolocation error:", error);
                    resolve(); // Resolve anyway to proceed without location
                },
                { timeout: 3000 } // Don't wait too long
            );
        }
    });
}

function startDictation() {
    const status = document.getElementById('voiceStatus');
    status.textContent = "Checking...";

    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        const micBtn = document.getElementById('voiceBtn');

        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        try {
            recognition.start();
            status.textContent = "Listening...";
            micBtn.style.background = "#ef4444"; // Red
            micBtn.style.color = "white";
        } catch (e) {
            status.textContent = "Error starting";
            console.error(e);
        }

        recognition.onresult = function (e) {
            document.getElementById('userInput').value = e.results[0][0].transcript;
            status.textContent = "Heard you!";
            setTimeout(() => status.textContent = "", 2000);
            recognition.stop();
            micBtn.style.background = "rgba(99, 102, 241, 0.1)";
            micBtn.style.color = "var(--primary-color)";
        };

        recognition.onerror = function (e) {
            recognition.stop();
            micBtn.style.background = "rgba(99, 102, 241, 0.1)";
            micBtn.style.color = "var(--primary-color)";
            console.error(e);

            if (e.error === 'not-allowed') {
                status.textContent = "Mic Denied";
                alert("Microphone access denied. Check browser settings.");
            } else if (e.error === 'no-speech') {
                status.textContent = "No speech";
            } else {
                status.textContent = "Error: " + e.error;
            }
        };

        recognition.onend = function () {
            micBtn.style.background = "rgba(99, 102, 241, 0.1)";
            micBtn.style.color = "var(--primary-color)";
            if (status.textContent === "Listening...") {
                status.textContent = "";
            }
        }

    } else {
        status.textContent = "Not Supported";
        alert("Voice input is not supported in this browser.");
    }
}

function displayResult(data) {
    const resultSection = document.getElementById('resultSection');

    // Update Emotion
    const emotion = data.detected_emotion.emotion;
    document.getElementById('emotionText').textContent = emotion;
    document.getElementById('emotionIcon').textContent = getEmotionIcon(emotion);

    // Update Action
    const action = data.suggested_action;
    document.getElementById('actionTitle').textContent = action.action;
    document.getElementById('actionDescription').textContent = action.description;
    document.getElementById('actionDuration').textContent = action.duration_minutes;
    document.getElementById('contextNote').textContent = action.context_note || "Suggested for you.";

    // Show Result
    resultSection.style.display = 'block';
    // Small delay to allow display:block to apply before removing hidden class for transition
    setTimeout(() => {
        resultSection.classList.remove('hidden');
    }, 10);
}

function getEmotionIcon(emotion) {
    const map = {
        'Stressed': '😫',
        'Tired': '😴',
        'Sad': '😢',
        'Confused': '🤔',
        'Happy': '😊',
        'Anxious': '😰',
        'Calm': '😌'
    };
    return map[emotion] || '😐';
}

async function loadHistory() {
    const list = document.getElementById('historyList');
    if (!list) return;

    try {
        const response = await fetch('/history');
        const data = await response.json();

        list.innerHTML = ''; // Clear loader

        if (data.length === 0) {
            list.innerHTML = '<p style="text-align:center; color:#64748b;">No moments recorded yet.</p>';
            return;
        }

        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'history-card';

            // Parse metadata
            const meta = item.metadata || {};
            const date = meta.timestamp ? new Date(meta.timestamp).toLocaleString() : 'Unknown Date';
            const emotion = meta.emotion || 'Unknown';
            const action = meta.action || 'Unknown Action';

            // Extract original text from content if possible (simple split)
            // Content format: "User felt {emotion} ({text}). Suggested: {action}."
            let userText = item.content;
            try {
                const match = item.content.match(/\((.*?)\)\. Suggested:/);
                if (match && match[1]) userText = match[1];
            } catch (e) { }

            card.innerHTML = `
                <div class="history-header">
                    <span class="history-emotion">${getEmotionIcon(emotion)} ${emotion}</span>
                    <span class="history-date">${date}</span>
                </div>
                <p class="history-content">"${userText}"</p>
                <div class="history-action">
                    <span>✨ Suggested:</span>
                    <span>${action}</span>
                </div>
            `;
            list.appendChild(card);
        });

    } catch (error) {
        console.error('Error loading history:', error);
        list.innerHTML = '<p style="text-align:center; color:red;">Failed to load history.</p>';
    }
}
