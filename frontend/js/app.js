
/* =========================================
   KNOWLEDGEIQ - APPLICATION CONFIGURATION
========================================= */

const API_BASE_URL = window.location.origin;

const API = {
    health: `${API_BASE_URL}/health`,
    documents: `${API_BASE_URL}/documents/`,
    upload: `${API_BASE_URL}/documents/upload`,
    chat: `${API_BASE_URL}/chat/`
};


/* =========================================
   DOM ELEMENTS
========================================= */

const sidebar = document.getElementById("sidebar");
const sidebarClose = document.getElementById("sidebarClose");
const menuToggle = document.getElementById("menuToggle");

const navItems = document.querySelectorAll(".nav-item[data-page]");
const pages = document.querySelectorAll(".page");

const breadcrumbPage = document.getElementById("breadcrumbPage");

const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");

const fileInput = document.getElementById("fileInput");
const uploadArea = document.getElementById("uploadArea");

const toastContainer = document.getElementById("toastContainer");


/* =========================================
   APPLICATION STATE
========================================= */

let documentsCache = [];
let isSendingMessage = false;
let isUploading = false;

const PAGE_NAMES = {
    dashboard: "Overview",
    chat: "AI Assistant",
    documents: "Documents",
    knowledge: "Knowledge Base",
    settings: "Settings"
};


/* =========================================
   UTILITY FUNCTIONS
========================================= */

function formatFileSize(bytes) {
    if (bytes < 1024) {
        return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}


function escapeHTML(value) {
    const element = document.createElement("div");
    element.textContent = String(value ?? "");
    return element.innerHTML;
}


function showToast(message, type = "success") {
    const toast = document.createElement("div");

    toast.className = `toast ${type}`;

    const icon = type === "success"
        ? "check-circle"
        : "alert-circle";

    const iconElement = document.createElement("i");
    iconElement.setAttribute("data-lucide", icon);

    const messageElement = document.createElement("span");
    messageElement.textContent = message;

    toast.append(iconElement, messageElement);
    toastContainer.appendChild(toast);

    if (window.lucide) {
        lucide.createIcons();
    }

    setTimeout(() => {
        toast.remove();
    }, 3500);
}


async function apiRequest(url, options = {}) {
    const response = await fetch(url, options);

    let data;

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (!response.ok) {
        throw new Error(
            data.detail || `Request failed (${response.status})`
        );
    }

    return data;
}


/* =========================================
   SIDEBAR NAVIGATION
========================================= */

function navigateToPage(pageName) {
    const targetPage = document.getElementById(`${pageName}Page`);

    if (!targetPage) {
        return;
    }

    // Hide all pages
    pages.forEach(page => {
        page.classList.remove("active");
    });

    // Show selected page
    targetPage.classList.add("active");

    // Update active navigation
    navItems.forEach(item => {
        item.classList.toggle(
            "active",
            item.dataset.page === pageName
        );
    });

    // Update breadcrumb
    breadcrumbPage.textContent =
        PAGE_NAMES[pageName] || pageName;

    // Close mobile sidebar
    sidebar.classList.remove("open");

    // Load page data
    if (pageName === "dashboard") {
        loadDashboard();
    }

    if (pageName === "documents") {
        loadDocuments();
    }
}


// Sidebar navigation
navItems.forEach(item => {
    item.addEventListener("click", () => {
        navigateToPage(item.dataset.page);
    });
});


// Buttons that navigate to another page
document.querySelectorAll("[data-navigate]").forEach(button => {
    button.addEventListener("click", () => {
        navigateToPage(button.dataset.navigate);
    });
});


// Mobile sidebar
menuToggle.addEventListener("click", () => {
    sidebar.classList.add("open");
});

sidebarClose.addEventListener("click", () => {
    sidebar.classList.remove("open");
});


// Close sidebar when clicking outside on mobile
document.addEventListener("click", event => {
    if (
        window.innerWidth <= 850 &&
        sidebar.classList.contains("open") &&
        !sidebar.contains(event.target) &&
        !menuToggle.contains(event.target)
    ) {
        sidebar.classList.remove("open");
    }
});


/* =========================================
   BACKEND HEALTH CHECK
========================================= */

async function checkBackendHealth() {
    const sidebarStatus = document.getElementById("sidebarStatus");

    const statusElements = [
        document.getElementById("sidebarStatusDot"),
        document.getElementById("topbarStatusDot")
    ];

    const topbarStatus = document.getElementById("topbarStatus");
    const apiStatus = document.getElementById("apiStatus");

    try {
        const data = await apiRequest(API.health);

        statusElements.forEach(element => {
            element.classList.remove("offline");
            element.classList.add("online");
        });

        sidebarStatus.textContent = "Connected";
        topbarStatus.textContent = "Connected";
        apiStatus.textContent = "Online";

        return data;

    } catch (error) {

        statusElements.forEach(element => {
            element.classList.remove("online");
            element.classList.add("offline");
        });

        sidebarStatus.textContent = "Disconnected";
        topbarStatus.textContent = "Disconnected";
        apiStatus.textContent = "Offline";

        console.error("Backend connection failed:", error);

        return null;
    }
}


/* =========================================
   DOCUMENT MANAGEMENT
========================================= */

async function loadDocuments() {
    const documentList = document.getElementById("documentList");

    documentList.innerHTML = `
        <div class="empty-state">
            <i data-lucide="loader-circle"></i>
            <p>Loading documents...</p>
        </div>
    `;

    if (window.lucide) {
        lucide.createIcons();
    }

    try {
        const data = await apiRequest(API.documents);

        documentsCache = data.documents || [];

        renderDocuments(documentsCache);

        return documentsCache;

    } catch (error) {

        documentList.innerHTML = `
            <div class="empty-state">
                <i data-lucide="alert-circle"></i>
                <p>Unable to load documents.</p>
            </div>
        `;

        if (window.lucide) {
            lucide.createIcons();
        }

        showToast(error.message, "error");

        return [];
    }
}


function getDocumentIcon(fileType) {
    return fileType.toLowerCase() === "pdf"
        ? "file-text"
        : "file";
}


function createDocumentRow(doc, showDelete = false) {
    const row = document.createElement("div");
    row.className = "document-row";

    const name = document.createElement("div");
    name.className = "document-name";

    const icon = document.createElement("div");
    icon.className = "document-icon";

    const iconElement = document.createElement("i");
    iconElement.setAttribute(
        "data-lucide",
        getDocumentIcon(doc.file_type)
    );

    icon.appendChild(iconElement);

    const details = document.createElement("div");

    const title = document.createElement("strong");
    title.textContent = doc.filename;

    const subtitle = document.createElement("small");
    subtitle.textContent = "Uploaded document";

    details.append(title, subtitle);
    name.append(icon, details);

    const type = document.createElement("div");
    type.className = "table-cell";
    type.textContent = doc.file_type.toUpperCase();

    const size = document.createElement("div");
    size.className = "table-cell";
    size.textContent = formatFileSize(doc.size_bytes);

    const action = document.createElement("div");

    if (showDelete) {
        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-button";
        deleteButton.title = "Delete document";

        const deleteIcon = document.createElement("i");
        deleteIcon.setAttribute("data-lucide", "trash-2");

        deleteButton.appendChild(deleteIcon);

        deleteButton.addEventListener("click", () => {
            deleteDocument(doc.filename, deleteButton);
        });

        action.appendChild(deleteButton);
    } else {
        const status = document.createElement("span");
        status.className = "status-badge";
        status.textContent = "Available";

        action.appendChild(status);
    }

    row.append(name, type, size, action);

    return row;
}

function renderDocuments(documents) {
    const documentList = document.getElementById("documentList");
    const recentDocuments = document.getElementById("recentDocuments");

    const documentCount = document.getElementById("documentCount");

    documentList.innerHTML = "";
    recentDocuments.innerHTML = "";

    documentCount.textContent =
        `${documents.length} document${documents.length !== 1 ? "s" : ""}`;

    if (documents.length === 0) {

        documentList.innerHTML = `
            <div class="empty-state">
                <i data-lucide="folder-open"></i>
                <p>No documents found. Upload your first document.</p>
            </div>
        `;

        recentDocuments.innerHTML = `
            <div class="empty-state">
                <i data-lucide="folder-open"></i>
                <p>No documents uploaded yet.</p>
            </div>
        `;

    } else {

        documents.forEach(document => {
            documentList.appendChild(
                createDocumentRow(document, true)
            );
        });

        // Display the latest five documents
        documents.slice(-5).reverse().forEach(document => {
            recentDocuments.appendChild(
                createDocumentRow(document, false)
            );
        });
    }

    document.getElementById("totalDocuments").textContent =
        documents.length;

    // ChromaDB chunk count is not currently exposed by the API.
    document.getElementById("knowledgeStatus").textContent =
        documents.length > 0 ? "Available" : "Empty";

    if (window.lucide) {
        lucide.createIcons();
    }
}


async function deleteDocument(filename, button) {
    const confirmed = confirm(
        `Are you sure you want to delete "${filename}"?`
    );

    if (!confirmed) {
        return;
    }

    button.disabled = true;

    try {
        const url = `${API.documents}${encodeURIComponent(filename)}`;

        await apiRequest(url, {
            method: "DELETE"
        });

        showToast("Document deleted successfully.");

        await loadDocuments();

        await loadDashboardStats();

    } catch (error) {

        showToast(error.message, "error");
        button.disabled = false;
    }
}


/* =========================================
   DOCUMENT UPLOAD
========================================= */

const uploadTrigger = document.getElementById("uploadTrigger");
const browseFiles = document.getElementById("browseFiles");

uploadTrigger.addEventListener("click", () => {
    fileInput.click();
});

browseFiles.addEventListener("click", () => {
    fileInput.click();
});


fileInput.addEventListener("change", event => {
    const file = event.target.files[0];

    if (file) {
        uploadDocument(file);
    }

    fileInput.value = "";
});


async function uploadDocument(file) {
    if (isUploading) {
        return;
    }

    const allowedExtensions = [".pdf", ".docx"];

    const extension = file.name
        .substring(file.name.lastIndexOf("."))
        .toLowerCase();

    if (!allowedExtensions.includes(extension)) {
        showToast("Only PDF and DOCX files are supported.", "error");
        return;
    }

    // Prevent unnecessarily large uploads in the browser.
    if (file.size > 10 * 1024 * 1024) {
        showToast("Maximum upload size is 10 MB.", "error");
        return;
    }

    isUploading = true;

    const progressContainer = document.getElementById("uploadProgress");
    const progressBar = document.getElementById("progressBar");
    const uploadMessage = document.getElementById("uploadMessage");

    progressContainer.hidden = false;
    progressBar.style.width = "20%";

    uploadMessage.textContent = "Uploading document...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        progressBar.style.width = "55%";

        const data = await apiRequest(API.upload, {
            method: "POST",
            body: formData
        });

        progressBar.style.width = "100%";

        uploadMessage.textContent =
            `${data.chunks_created} chunks indexed successfully.`;

        showToast("Document uploaded and indexed successfully.");

        await loadDocuments();

        await loadDashboardStats();

    } catch (error) {

        uploadMessage.textContent = error.message;

        showToast(error.message, "error");

    } finally {

        isUploading = false;

        setTimeout(() => {
            progressContainer.hidden = true;
            progressBar.style.width = "0%";
        }, 2500);
    }
}


/* =========================================
   DRAG AND DROP
========================================= */

uploadArea.addEventListener("dragover", event => {
    event.preventDefault();
    uploadArea.classList.add("drag-over");
});


uploadArea.addEventListener("dragleave", event => {
    if (!uploadArea.contains(event.relatedTarget)) {
        uploadArea.classList.remove("drag-over");
    }
});


uploadArea.addEventListener("drop", event => {
    event.preventDefault();

    uploadArea.classList.remove("drag-over");

    const file = event.dataTransfer.files[0];

    if (file) {
        uploadDocument(file);
    }
});


/* =========================================
   AI CHAT
========================================= */

function removeWelcomeMessage() {
    const welcomeMessage = chatMessages.querySelector(".welcome-message");

    if (welcomeMessage) {
        welcomeMessage.remove();
    }
}


function addMessage(role, content) {
    removeWelcomeMessage();

    const message = document.createElement("div");
    message.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";

    const avatarIcon = document.createElement("i");

    avatarIcon.setAttribute(
        "data-lucide",
        role === "user" ? "user" : "brain-circuit"
    );

    avatar.appendChild(avatarIcon);

    const messageContent = document.createElement("div");
    messageContent.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    // Use textContent to safely display model output.
    bubble.textContent = content;

    const meta = document.createElement("div");
    meta.className = "message-meta";

    meta.textContent = role === "user"
        ? "You"
        : "KnowledgeIQ Assistant";

    messageContent.append(bubble, meta);
    message.append(avatar, messageContent);

    chatMessages.appendChild(message);

    if (window.lucide) {
        lucide.createIcons();
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return message;
}


function showTypingIndicator() {
    removeWelcomeMessage();

    const message = document.createElement("div");
    message.className = "message assistant";
    message.id = "typingIndicator";

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";

    const icon = document.createElement("i");
    icon.setAttribute("data-lucide", "brain-circuit");

    avatar.appendChild(icon);

    const content = document.createElement("div");
    content.className = "message-content";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    bubble.innerHTML = `
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    content.appendChild(bubble);
    message.append(avatar, content);

    chatMessages.appendChild(message);

    if (window.lucide) {
        lucide.createIcons();
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function removeTypingIndicator() {
    document.getElementById("typingIndicator")?.remove();
}


function renderSources(messageElement, sources) {
    if (!sources || sources.length === 0) {
        return;
    }

    const content = messageElement.querySelector(".message-content");

    const panel = document.createElement("div");
    panel.className = "sources-panel";

    const toggle = document.createElement("button");
    toggle.className = "sources-toggle";

    const icon = document.createElement("i");
    icon.setAttribute("data-lucide", "file-text");

    const label = document.createElement("span");
    label.textContent = `View ${sources.length} source${sources.length > 1 ? "s" : ""}`;

    toggle.append(icon, label);

    const list = document.createElement("div");
    list.className = "source-list";

    sources.forEach(source => {
        const item = document.createElement("div");
        item.className = "source-item";

        const title = document.createElement("strong");
        title.textContent = source.source || "Unknown document";

        const metadata = document.createElement("small");

        metadata.textContent =
            `${(source.file_type || "document").toUpperCase()}` +
            (source.page !== null && source.page !== undefined
                ? ` · Page ${source.page}`
                : "");

        const description = document.createElement("p");
        description.textContent = source.content || "";

        item.append(title, metadata, description);
        list.appendChild(item);
    });

    toggle.addEventListener("click", () => {
        const isOpen = list.classList.toggle("open");

        label.textContent = isOpen
            ? "Hide sources"
            : `View ${sources.length} source${sources.length > 1 ? "s" : ""}`;

        icon.setAttribute(
            "data-lucide",
            isOpen ? "chevron-up" : "file-text"
        );

        if (window.lucide) {
            lucide.createIcons();
        }
    });

    panel.append(toggle, list);
    content.appendChild(panel);

    if (window.lucide) {
        lucide.createIcons();
    }
}


async function sendMessage(question) {
    if (isSendingMessage || !question.trim()) {
        return;
    }

    isSendingMessage = true;
    sendButton.disabled = true;

    addMessage("user", question);

    chatInput.value = "";
    chatInput.style.height = "auto";

    showTypingIndicator();

    try {
        const data = await apiRequest(API.chat, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question.trim(),
                k: 4
            })
        });

        removeTypingIndicator();

        const assistantMessage = addMessage(
            "assistant",
            data.answer
        );

        renderSources(
            assistantMessage,
            data.sources || []
        );

    } catch (error) {

        removeTypingIndicator();

        addMessage(
            "assistant",
            `Sorry, something went wrong: ${error.message}`
        );

        showToast("Unable to process your question.", "error");

    } finally {

        isSendingMessage = false;
        sendButton.disabled = false;

        chatInput.focus();
    }
}


// Submit chat form
chatForm.addEventListener("submit", event => {
    event.preventDefault();

    sendMessage(chatInput.value);
});


// Enter to send, Shift + Enter for new line
chatInput.addEventListener("keydown", event => {
    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});


// Auto-resize chat input
chatInput.addEventListener("input", () => {
    chatInput.style.height = "auto";

    chatInput.style.height =
        `${Math.min(chatInput.scrollHeight, 120)}px`;
});


// Suggested questions
document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", () => {
        const question = button.dataset.question;

        sendMessage(question);
    });
});


// Clear chat
document.getElementById("clearChat").addEventListener("click", () => {
    if (isSendingMessage) {
        showToast("Please wait for the current response.", "error");
        return;
    }

    chatMessages.innerHTML = `
        <div class="welcome-message">

            <div class="welcome-icon">
                <i data-lucide="brain-circuit"></i>
            </div>

            <h2>How can I help you today?</h2>

            <p>
                Ask questions about your knowledge base
                and I'll find relevant information for you.
            </p>

            <div class="suggestion-list">

                <button class="suggestion"
                        data-question="Summarize my uploaded documents.">
                    <i data-lucide="file-text"></i>
                    Summarize my documents
                </button>

                <button class="suggestion"
                        data-question="What are the key topics in my documents?">
                    <i data-lucide="lightbulb"></i>
                    Find key topics
                </button>

                <button class="suggestion"
                        data-question="Explain the most important information in my knowledge base.">
                    <i data-lucide="search"></i>
                    Discover important insights
                </button>

            </div>

        </div>
    `;

    attachSuggestionEvents();

    if (window.lucide) {
        lucide.createIcons();
    }
});


function attachSuggestionEvents() {
    document.querySelectorAll(".suggestion").forEach(button => {
        button.addEventListener("click", () => {
            sendMessage(button.dataset.question);
        });
    });
}


/* =========================================
   DASHBOARD
========================================= */

async function loadDashboardStats() {
    const documents = await loadDocuments();

    return documents;
}


async function loadDashboard() {
    await checkBackendHealth();
    await loadDashboardStats();
}


/* =========================================
   REFRESH BUTTONS
========================================= */

document.getElementById("refreshButton").addEventListener("click", async () => {
    const icon = document.querySelector("#refreshButton i");

    icon?.classList.add("spin");

    await loadDashboard();

    setTimeout(() => {
        icon?.classList.remove("spin");
    }, 500);

    showToast("Dashboard refreshed.");
});


document.getElementById("refreshDocuments").addEventListener("click", () => {
    loadDocuments();
});


/* =========================================
   APPLICATION INITIALIZATION
========================================= */

async function initializeApp() {
    if (window.lucide) {
        lucide.createIcons();
    }

    document.getElementById("apiUrlDisplay").textContent =
        API_BASE_URL;

    await checkBackendHealth();

    await loadDashboard();

    attachSuggestionEvents();

    console.log("KnowledgeIQ initialized successfully.");
}


// Start application
document.addEventListener("DOMContentLoaded", initializeApp);
