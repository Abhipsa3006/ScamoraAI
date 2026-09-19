// =================================
// ANALYZE MESSAGE
// =================================

async function analyzeMessage() {

    const messageBox =
        document.getElementById("message");

    const button =
        document.getElementById("analyzeButton");

    const message =
        messageBox.value.trim();


    if (!message) {

        alert("Please enter a message first.");
        return;

    }


    button.disabled = true;
    button.textContent = "⏳ Analyzing...";


    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const result =
            await response.json();


        if (!response.ok) {

            alert(
                result.error ||
                "Something went wrong."
            );

            return;

        }


        // =========================
        // SHOW RESULTS
        // =========================

        document
            .getElementById("result")
            .classList.remove("hidden");


        // =========================
        // RISK SCORE
        // =========================

        const riskScore =
            document.getElementById("riskScore");

        const riskBar =
            document.getElementById("riskBar");


        riskScore.textContent =
            result.risk_score;


        riskBar.style.width = "0%";


        setTimeout(() => {

            riskBar.style.width =
                result.risk_score + "%";

        }, 100);


        // =========================
        // THREAT LEVEL
        // =========================

        const threatLevel =
            document.getElementById("threatLevel");


        threatLevel.textContent =
            result.threat_level;


        // =========================
        // CLASSIFICATION
        // =========================

        const classification =
            document.getElementById("classification");


        classification.textContent =
            result.classification;


        // =========================
        // AI CONFIDENCE
        // =========================

        document
            .getElementById("aiConfidence")
            .textContent =
            result.ai_confidence;


        // =========================
        // VISUAL STATUS
        // =========================

        const statusDot =
            document.querySelector(".status-dot");


        if (result.threat_level === "HIGH") {

            statusDot.style.background =
                "#ef4444";

            threatLevel.style.color =
                "#ef4444";

            riskBar.style.background =
                "#ef4444";

            classification.style.color =
                "#ef4444";

        }

        else if (
            result.threat_level === "MEDIUM"
        ) {

            statusDot.style.background =
                "#f59e0b";

            threatLevel.style.color =
                "#f59e0b";

            riskBar.style.background =
                "#f59e0b";

            classification.style.color =
                "#f59e0b";

        }

        else {

            statusDot.style.background =
                "#22c55e";

            threatLevel.style.color =
                "#22c55e";

            riskBar.style.background =
                "#22c55e";

            classification.style.color =
                "#22c55e";

        }


        // =========================
        // RED FLAGS
        // =========================

        const redFlags =
            document.getElementById("redFlags");


        redFlags.innerHTML = "";


        if (
            result.red_flags.length === 0
        ) {

            redFlags.innerHTML =
                "<li>✓ No major red flags detected</li>";

        }

        else {

            result.red_flags.forEach(flag => {

                const li =
                    document.createElement("li");


                li.textContent =
                    "✓ " + flag;


                redFlags.appendChild(li);

            });

        }


        // =========================
        // WHY
        // =========================

        document
            .getElementById("why")
            .textContent =
            result.why;


        // =========================
        // RECOMMENDATION
        // =========================

        document
            .getElementById("recommendation")
            .textContent =
            result.recommendation;


        // =========================
        // DETECTED URLS
        // =========================

        const urls =
            document.getElementById("urls");


        urls.innerHTML = "";


        if (
            result.urls.length === 0
        ) {

            urls.innerHTML =
                "<li>No URLs detected</li>";

        }

        else {

            result.urls.forEach(item => {

                const li =
                    document.createElement("li");


                li.textContent =
                    item.url +
                    " — Risk Score: " +
                    item.score;


                urls.appendChild(li);

            });

        }


        // =========================
        // SAVE TO HISTORY
        // =========================

        saveToHistory(
            message,
            result
        );


        // =========================
        // UPDATE DASHBOARD
        // =========================

        updateDashboard();


        // =========================
        // SCROLL TO RESULTS
        // =========================

        document
            .getElementById("result")
            .scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

    }


    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to SCAMORA AI."
        );

    }


    finally {

        button.disabled = false;

        button.textContent =
            "🔍 Analyze Message";

    }

}


// =================================
// DETECTION HISTORY
// =================================

function saveToHistory(message, result) {

    let history =
        JSON.parse(
            localStorage.getItem(
                "scamoraHistory"
            )
        ) || [];


    const historyItem = {

        message: message,

        risk_score:
            result.risk_score,

        threat_level:
            result.threat_level,

        classification:
            result.classification,

        ai_confidence:
            result.ai_confidence,

        time:
            new Date().toLocaleTimeString(
                [],
                {
                    hour: "2-digit",
                    minute: "2-digit"
                }
            )

    };


    history.unshift(historyItem);


    // Keep only latest 10 analyses

    history =
        history.slice(0, 10);


    localStorage.setItem(
        "scamoraHistory",
        JSON.stringify(history)
    );


    displayHistory();

}


// =================================
// DISPLAY HISTORY
// =================================

function displayHistory() {

    const historyList =
        document.getElementById(
            "historyList"
        );


    let history =
        JSON.parse(
            localStorage.getItem(
                "scamoraHistory"
            )
        ) || [];


    if (history.length === 0) {

        historyList.innerHTML = `
            <p class="empty-history">
                No messages analyzed yet.
            </p>
        `;

        return;

    }


    historyList.innerHTML = "";


    history.forEach(item => {

        const card =
            document.createElement("div");


        card.className =
            "history-item";


        let statusClass =
            "safe";


        if (
            item.threat_level === "HIGH"
        ) {

            statusClass = "high";

        }

        else if (
            item.threat_level === "MEDIUM"
        ) {

            statusClass = "medium";

        }


        card.innerHTML = `

            <div class="history-main">

                <div class="history-message">
                    ${escapeHTML(
                        item.message
                    )}
                </div>

                <div class="history-meta">

                    <span>
                        ${item.time}
                    </span>

                    <span>
                        AI Confidence:
                        ${item.ai_confidence}%
                    </span>

                </div>

            </div>


            <div class="history-result">

                <span class="history-class ${statusClass}">
                    ${item.classification}
                </span>

                <strong>
                    ${item.risk_score}/100
                </strong>

            </div>

        `;


        historyList.appendChild(card);

    });

}


// =================================
// UPDATE SECURITY DASHBOARD
// =================================

function updateDashboard() {

    const history =
        JSON.parse(
            localStorage.getItem(
                "scamoraHistory"
            )
        ) || [];


    // =========================
    // TOTAL ANALYZED
    // =========================

    const totalAnalyzed =
        history.length;


    document
        .getElementById("totalAnalyzed")
        .textContent =
        totalAnalyzed;


    // =========================
    // THREATS DETECTED
    // =========================

    const threats =
        history.filter(item =>

            item.threat_level === "HIGH" ||
            item.threat_level === "MEDIUM"

        ).length;


    document
        .getElementById("threatsDetected")
        .textContent =
        threats;


    // =========================
    // SAFE MESSAGES
    // =========================

    const safe =
        history.filter(item =>

            item.classification === "SAFE"

        ).length;


    document
        .getElementById("safeMessages")
        .textContent =
        safe;


    // =========================
    // AVERAGE RISK
    // =========================

    let averageRisk = 0;


    if (history.length > 0) {

        const totalRisk =
            history.reduce(
                (sum, item) =>
                    sum + Number(item.risk_score),
                0
            );


        averageRisk =
            Math.round(
                totalRisk / history.length
            );

    }


    document
        .getElementById("averageRisk")
        .textContent =
        averageRisk;

}


// =================================
// CLEAR HISTORY
// =================================

function clearHistory() {

    const history =
        JSON.parse(
            localStorage.getItem(
                "scamoraHistory"
            )
        ) || [];


    if (history.length === 0) {

        return;

    }


    const confirmed =
        confirm(
            "Are you sure you want to clear your detection history?"
        );


    if (!confirmed) {

        return;

    }


    localStorage.removeItem(
        "scamoraHistory"
    );


    displayHistory();

    updateDashboard();

}


// =================================
// SAFE HTML
// =================================

function escapeHTML(text) {

    const div =
        document.createElement("div");


    div.textContent = text;


    return div.innerHTML;

}


// =================================
// CLEAR ANALYSIS
// =================================

function clearAnalysis() {

    document
        .getElementById("message")
        .value = "";


    document
        .getElementById("result")
        .classList.add("hidden");


    document
        .getElementById("riskScore")
        .textContent = "0";


    document
        .getElementById("riskBar")
        .style.width = "0%";


    const threatLevel =
        document.getElementById(
            "threatLevel"
        );


    threatLevel.textContent = "-";

    threatLevel.style.color = "";


    const classification =
        document.getElementById(
            "classification"
        );


    classification.textContent = "-";

    classification.style.color = "";


    document
        .getElementById("aiConfidence")
        .textContent = "0";


    document
        .querySelector(".status-dot")
        .style.background =
        "#22c55e";


    document
        .getElementById("redFlags")
        .innerHTML = "";


    document
        .getElementById("why")
        .textContent = "";


    document
        .getElementById("recommendation")
        .textContent = "";


    document
        .getElementById("urls")
        .innerHTML = "";


    document
        .getElementById("message")
        .scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

}


// =================================
// DEMO EXAMPLES
// =================================

function useExample(type) {

    const messageBox =
        document.getElementById(
            "message"
        );


    if (type === "safe") {

        messageBox.value =
            "Hey, are you coming to college tomorrow? The class starts at 10 AM.";

    }


    else if (type === "scam") {

        messageBox.value =
            "Congratulations! You have won ₹50,000. Pay a small processing fee to receive your prize.";

    }


    else if (type === "phishing") {

        messageBox.value =
            "URGENT! Your SBI bank account will be blocked. Verify your account immediately: http://secure-bank-login.xyz";

    }


    messageBox.scrollIntoView({

        behavior: "smooth",

        block: "center"

    });


    messageBox.focus();

}


// =================================
// LOAD DATA WHEN PAGE OPENS
// =================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        displayHistory();

        updateDashboard();

    }
);