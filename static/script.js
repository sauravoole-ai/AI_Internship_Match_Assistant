const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");
const downloadBtn = document.getElementById("downloadBtn");
const askBtn = document.getElementById("askBtn");

const resumeText = document.getElementById("resumeText");
const jdText = document.getElementById("jdText");
const followupQuestion = document.getElementById("followupQuestion");

const resumeFile = document.getElementById("resumeFile");
const jdFile = document.getElementById("jdFile");

const resumeFileName = document.getElementById("resumeFileName");
const jdFileName = document.getElementById("jdFileName");

const resultBox = document.getElementById("resultBox");
const assistantAnswer = document.getElementById("assistantAnswer");
const retrievedContextWrapper = document.getElementById("retrievedContextWrapper");
const retrievedContextBox = document.getElementById("retrievedContextBox");

const loadingText = document.getElementById("loadingText");
const assistantLoading = document.getElementById("assistantLoading");
const statusPill = document.querySelector(".status-pill");

const suggestionChips = document.querySelectorAll(".suggestion-chip");

let latestResultText = "";
let latestResumeContext = "";
let latestJdContext = "";

function setStatus(text, type) {
    statusPill.textContent = text;

    statusPill.classList.remove("status-ready", "status-loading", "status-success", "status-error");

    if (type === "loading") {
        statusPill.classList.add("status-loading");
    } else if (type === "success") {
        statusPill.classList.add("status-success");
    } else if (type === "error") {
        statusPill.classList.add("status-error");
    } else {
        statusPill.classList.add("status-ready");
    }
}

function escapeHTML(text) {
    return text
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}

function formatTextToHTML(text) {
    const safeText = escapeHTML(text);
    const lines = safeText.split("\n");

    let html = "";
    let listOpen = false;

    lines.forEach((rawLine) => {
        const line = rawLine.trim();

        if (!line) {
            if (listOpen) {
                html += "</ul>";
                listOpen = false;
            }
            return;
        }

        const cleanedLine = line
            .replace(/\*\*/g, "")
            .replace(/^#+\s*/, "");

        const isHeading =
            /^\d+\.\s/.test(cleanedLine) ||
            cleanedLine.toLowerCase().includes("overall match score") ||
            cleanedLine.toLowerCase().includes("strong matching areas") ||
            cleanedLine.toLowerCase().includes("partial matching areas") ||
            cleanedLine.toLowerCase().includes("missing or weak areas") ||
            cleanedLine.toLowerCase().includes("resume weak points") ||
            cleanedLine.toLowerCase().includes("jd keywords") ||
            cleanedLine.toLowerCase().includes("project relevance analysis") ||
            cleanedLine.toLowerCase().includes("upgrade suggestions") ||
            cleanedLine.toLowerCase().includes("internship suitability verdict") ||
            cleanedLine.toLowerCase().includes("final 5-step action plan");

        const isBullet =
            cleanedLine.startsWith("- ") ||
            cleanedLine.startsWith("• ") ||
            cleanedLine.startsWith("* ");

        if (isHeading && !isBullet) {
            if (listOpen) {
                html += "</ul>";
                listOpen = false;
            }

            html += `<h3>${cleanedLine}</h3>`;
            return;
        }

        if (isBullet) {
            if (!listOpen) {
                html += "<ul>";
                listOpen = true;
            }

            const bulletText = cleanedLine.replace(/^[-•*]\s*/, "");
            html += `<li>${bulletText}</li>`;
            return;
        }

        if (listOpen) {
            html += "</ul>";
            listOpen = false;
        }

        html += `<p>${cleanedLine}</p>`;
    });

    if (listOpen) {
        html += "</ul>";
    }

    return html;
}

function resetResultBox() {
    latestResultText = "";
    latestResumeContext = "";
    latestJdContext = "";

    resultBox.classList.add("empty-result");
    resultBox.innerHTML = "<p>Your analysis will appear here in a clean reading format.</p>";

    assistantAnswer.classList.add("empty-result");
    assistantAnswer.innerHTML = "<p>After analysis, ask questions like: “Why is my score low?” or “What should I improve first?”</p>";

    retrievedContextWrapper.classList.add("hidden");
    retrievedContextBox.textContent = "Relevant resume/JD chunks will appear here after a follow-up answer.";

    followupQuestion.value = "";
    setStatus("Ready", "ready");
}

function updateFileName(input, labelElement) {
    if (input.files.length > 0) {
        labelElement.textContent = input.files[0].name;
    } else {
        labelElement.textContent = "No file selected";
    }
}

async function downloadPdfReport() {
    if (!latestResultText) {
        setStatus("Nothing to Download", "error");
        return;
    }

    downloadBtn.disabled = true;
    const oldText = downloadBtn.textContent;
    downloadBtn.textContent = "Preparing PDF";
    setStatus("Preparing PDF", "loading");

    const reportContent =
`AI Internship Match Assistant Report

Generated Analysis:
-------------------

${latestResultText}

Note:
This report is AI-generated and should be used as guidance, not as a guaranteed hiring decision.
`;

    try {
        const response = await fetch("/download-report", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                report_text: reportContent
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            setStatus(errorData.error || "PDF Failed", "error");
            downloadBtn.disabled = false;
            downloadBtn.textContent = oldText;
            return;
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = "resume_jd_analysis_report.pdf";

        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        setStatus("PDF Downloaded", "success");

        setTimeout(() => {
            setStatus("Completed", "success");
        }, 1500);

    } catch (error) {
        setStatus("PDF Failed", "error");
    }

    downloadBtn.disabled = false;
    downloadBtn.textContent = oldText;
}

resumeFile.addEventListener("change", () => {
    updateFileName(resumeFile, resumeFileName);
});

jdFile.addEventListener("change", () => {
    updateFileName(jdFile, jdFileName);
});

suggestionChips.forEach((chip) => {
    chip.addEventListener("click", () => {
        followupQuestion.value = chip.textContent;
        followupQuestion.focus();
    });
});

setStatus("Ready", "ready");

analyzeBtn.addEventListener("click", async () => {
    const resume = resumeText.value.trim();
    const jd = jdText.value.trim();

    const selectedResumeFile = resumeFile.files[0];
    const selectedJdFile = jdFile.files[0];

    if ((!resume && !selectedResumeFile) || (!jd && !selectedJdFile)) {
        latestResultText = "";
        resultBox.classList.remove("empty-result");
        resultBox.innerHTML = "<p>Please upload/paste both resume and job description.</p>";
        setStatus("Input Needed", "error");
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";
    loadingText.classList.remove("hidden");
    resultBox.classList.add("empty-result");
    resultBox.innerHTML = "<p>Preparing your analysis...</p>";
    setStatus("Analyzing", "loading");

    retrievedContextWrapper.classList.add("hidden");
    retrievedContextBox.textContent = "Relevant resume/JD chunks will appear here after a follow-up answer.";

    const formData = new FormData();
    formData.append("resume_text", resume);
    formData.append("jd_text", jd);

    if (selectedResumeFile) {
        formData.append("resume_file", selectedResumeFile);
    }

    if (selectedJdFile) {
        formData.append("jd_file", selectedJdFile);
    }

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            latestResultText = data.result;
            latestResumeContext = data.resume_text_used || resume;
            latestJdContext = data.jd_text_used || jd;

            resultBox.classList.remove("empty-result");
            resultBox.innerHTML = formatTextToHTML(data.result);
            setStatus("Completed", "success");
        } else {
            latestResultText = "";
            resultBox.classList.remove("empty-result");
            resultBox.innerHTML = `<p>Error: ${escapeHTML(data.error)}</p>`;
            setStatus("Error", "error");
        }

    } catch (error) {
        latestResultText = "";
        resultBox.classList.remove("empty-result");
        resultBox.innerHTML = "<p>Something went wrong. Please try again.</p>";
        setStatus("Error", "error");
    }

    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze My Match";
    loadingText.classList.add("hidden");
});

askBtn.addEventListener("click", async () => {
    const question = followupQuestion.value.trim();

    if (!question) {
        assistantAnswer.classList.remove("empty-result");
        assistantAnswer.innerHTML = "<p>Please type a follow-up question first.</p>";
        return;
    }

    if (!latestResultText) {
        assistantAnswer.classList.remove("empty-result");
        assistantAnswer.innerHTML = "<p>Please run a Resume–JD analysis first. Then ask your follow-up question.</p>";
        return;
    }

    askBtn.disabled = true;
    askBtn.textContent = "Thinking...";
    assistantLoading.classList.remove("hidden");
    assistantAnswer.classList.add("empty-result");
    assistantAnswer.innerHTML = "<p>Retrieving context and preparing assistant answer...</p>";

    retrievedContextWrapper.classList.add("hidden");

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                resume_text: latestResumeContext,
                jd_text: latestJdContext,
                analysis_text: latestResultText
            })
        });

        const data = await response.json();

        if (data.success) {
            assistantAnswer.classList.remove("empty-result");
            assistantAnswer.innerHTML = formatTextToHTML(data.answer);

            if (data.retrieved_context) {
                retrievedContextBox.textContent = data.retrieved_context;
                retrievedContextWrapper.classList.remove("hidden");
            }
        } else {
            assistantAnswer.classList.remove("empty-result");
            assistantAnswer.innerHTML = `<p>Error: ${escapeHTML(data.error)}</p>`;
        }

    } catch (error) {
        assistantAnswer.classList.remove("empty-result");
        assistantAnswer.innerHTML = "<p>Something went wrong while answering your follow-up question.</p>";
    }

    askBtn.disabled = false;
    askBtn.textContent = "Ask Assistant";
    assistantLoading.classList.add("hidden");
});

clearBtn.addEventListener("click", () => {
    resumeText.value = "";
    jdText.value = "";

    resumeFile.value = "";
    jdFile.value = "";

    resumeFileName.textContent = "No file selected";
    jdFileName.textContent = "No file selected";

    loadingText.classList.add("hidden");
    assistantLoading.classList.add("hidden");

    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze My Match";

    askBtn.disabled = false;
    askBtn.textContent = "Ask Assistant";

    resetResultBox();
});

copyBtn.addEventListener("click", async () => {
    if (!latestResultText) {
        setStatus("Nothing to Copy", "error");
        return;
    }

    try {
        await navigator.clipboard.writeText(latestResultText);
        const oldText = copyBtn.textContent;
        copyBtn.textContent = "Copied";
        setStatus("Copied", "success");

        setTimeout(() => {
            copyBtn.textContent = oldText;
            setStatus("Completed", "success");
        }, 1500);

    } catch (error) {
        setStatus("Copy Failed", "error");
    }
});

downloadBtn.addEventListener("click", downloadPdfReport);

const themeToggle = document.getElementById("themeToggle");

function applySavedTheme() {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
        themeToggle.textContent = "Dark Mode";
    } else {
        document.body.classList.remove("light-theme");
        themeToggle.textContent = "Light Mode";
    }
}

themeToggle.addEventListener("click", () => {
    const isLight = document.body.classList.toggle("light-theme");

    if (isLight) {
        localStorage.setItem("theme", "light");
        themeToggle.textContent = "Dark Mode";
    } else {
        localStorage.setItem("theme", "dark");
        themeToggle.textContent = "Light Mode";
    }
});

applySavedTheme();