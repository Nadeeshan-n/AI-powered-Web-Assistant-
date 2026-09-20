// Application State
let messages = [];
let isLoading = false;

// DOM Elements
const welcomeScreen = document.getElementById('welcomeScreen');
const messagesContainer = document.getElementById('messagesContainer');
const loadingIndicator = document.getElementById('loadingIndicator');
const messagesEnd = document.getElementById('messagesEnd');
const clearBtn = document.getElementById('clearBtn');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const modelSelect = document.getElementById('modelSelect');
const sendButton = document.getElementById('sendButton');
const sendIcon = document.getElementById('sendIcon');
const loadingSpinner = document.getElementById('loadingSpinner');
const themeToggleBtn = document.getElementById('themeToggleBtn');
const themeToggleText = document.getElementById('themeToggleText');
const uploadDocumentBtn = document.getElementById('uploadDocumentBtn')
const documentFile = document.getElementById('documentFile');
const uploadStatus = document.getElementById('uploadStatus');
const documentList = document.getElementById('documentList');

function getStoredTheme() {
    try {
        return localStorage.getItem('ai_assistant_theme') || 'dark';
    } catch (e) {
        return 'dark';
    }
}

function setStoredTheme(theme) {
    try {
        localStorage.setItem('ai_assistant_theme', theme);
    } catch (e) {}
}

let currentTheme = getStoredTheme();

function applyTheme(theme) {
    currentTheme = theme;
    if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        if (themeToggleText) themeToggleText.textContent = '[ LIGHT_MODE ]';
    } else {
        document.documentElement.removeAttribute('data-theme');
        if (themeToggleText) themeToggleText.textContent = '[ DARK_MODE ]';
    }
    setStoredTheme(theme);
}

function toggleTheme() {
    applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Apply initial theme
    applyTheme(currentTheme);

    // Set default model
    modelSelect.value = 'gemini';
    
    // Setup event listeners
    setupEventListeners();
    
    // Initial state
    updateSendButton();

    // Load documents 
    loadDocuments();
});

function setupEventListeners() {
    // Theme toggle
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }

    // Form submission
    chatForm.addEventListener('submit', handleSubmit);
    
    // Clear chat
    clearBtn.addEventListener('click', clearChat);
    
    // Message input events
    messageInput.addEventListener('input', handleInputChange);
    messageInput.addEventListener('keydown', handleKeyDown);
}

function handleSubmit(e) {
    e.preventDefault();
    
    const content = messageInput.value.trim();
    const model = modelSelect.value;
    
    if (!content || isLoading) return;
    
    sendMessage(content, model);
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit(e);
    }
}

function handleInputChange() {
    autoResizeTextarea();
    updateSendButton();
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    const newHeight = Math.min(messageInput.scrollHeight, 128);
    messageInput.style.height = newHeight + 'px';
}

function updateSendButton() {
    const hasContent = messageInput.value.trim().length > 0;
    sendButton.disabled = !hasContent || isLoading;
}

async function sendMessage(content, model) {
    // Add user message
    const userMessage = {
        id: Date.now().toString(),
        content: content,
        type: 'user',
        timestamp: new Date()
    };
    
    messages.push(userMessage);
    displayMessage(userMessage);
    
    // Clear input and update UI
    messageInput.value = '';
    messageInput.style.height = 'auto';
    hideWelcomeScreen();
    showClearButton();
    setLoadingState(true);
    
    try {
        const doFetch = (window.fetch ? window.fetch.bind(window) : fetch);
        const response = await doFetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: content,
                model: model
            }),
        });

        const data = await response.json();
        console.log("Backend response:", data);

        let aiMessage;
        if (data.error) {
            aiMessage = {
                id: (Date.now() + 1).toString(),
                content: `Error: ${data.error}`,
                type: 'ai',
                model: model,
                timestamp: new Date()
            };
        } else {
            aiMessage = {
                id: (Date.now() + 1).toString(),
                content: data.response,
                type: 'ai',
                model: model,
                duration: data.duration,
                timestamp: new Date()
            };
        }
        
        messages.push(aiMessage);
        displayMessage(aiMessage);
        
    } catch (error) {
        const errorMessage = {
            id: (Date.now() + 1).toString(),
            content: `Error: ${error.message}`,
            type: 'ai',
            model: model,
            timestamp: new Date()
        };
        
        messages.push(errorMessage);
        displayMessage(errorMessage);
        
    } finally {
        setLoadingState(false);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function displayMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${message.type}`;
    
    const time = message.timestamp.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    });
    
    const avatarLabel = message.type === 'user' ? 'USER' : 'AI_NODE';
    const senderLabel = message.type === 'user' ? 'SESSION_USER' : 'SYSTEM_NODE';
    
    const modelBadge = message.model ? 
        `<span class="message-model">${escapeHtml(message.model.toUpperCase())}</span>` : '';
    
    const durationBadge = message.duration ? 
        `<span style="opacity: 0.7;">[LATENCY: ${message.duration.toFixed(2)}s]</span>` : '';

    const sourcesHtml =
    message.sources &&
    message.sources.length > 0
        ? `
            <div class="message-sources">
                <div class="sources-title">
                    SOURCES
                </div>

                ${message.sources.map(source => `
                    <div class="source-item">
                        <span>
                            ${escapeHtml(source.document)}
                        </span>
                        <span>
                            Page ${escapeHtml(
                                String(source.page)
                            )}
                        </span>
                    </div>
                `).join('')}
            </div>
        `
        : '';
    
    messageEl.innerHTML = `
        <div class="avatar">${avatarLabel}</div>
        <div class="message-body">
            <div class="message-meta">
                <span>${senderLabel}</span>
                ${modelBadge}
                <span>${time}</span>
                ${durationBadge}
            </div>
            <div class="message-bubble">

                <div class="message-text">
                    ${escapeHtml(message.content)}
                </div>

                ${sourcesHtml}

            </div>
        </div>
    `;


    
    messagesContainer.appendChild(messageEl);
    scrollToBottom();
}

function setLoadingState(loading) {
    isLoading = loading;
    
    // Update UI elements
    updateSendButton();
    messageInput.disabled = loading;
    
    // Toggle loading indicator and send button icon
    if (loading) {
        loadingIndicator.style.display = 'block';
        sendIcon.style.display = 'none';
        loadingSpinner.style.display = 'block';
    } else {
        loadingIndicator.style.display = 'none';
        sendIcon.style.display = 'block';
        loadingSpinner.style.display = 'none';
    }
    
    if (loading) {
        scrollToBottom();
    }
}

function hideWelcomeScreen() {
    welcomeScreen.style.display = 'none';
}

function showWelcomeScreen() {
    welcomeScreen.style.display = 'block';
}

function showClearButton() {
    clearBtn.style.display = 'flex';
}

function hideClearButton() {
    clearBtn.style.display = 'none';
}

function clearChat() {
    messages = [];
    messagesContainer.innerHTML = '';
    showWelcomeScreen();
    hideClearButton();
    setLoadingState(false);
    updateSendButton();
}

function scrollToBottom() {
    messagesEnd.scrollIntoView({ behavior: 'smooth' });
}

function setUploadStatus(message, isError = false) {

    if (!uploadStatus) return;

    uploadStatus.textContent = message;

    uploadStatus.style.color =
        isError ? '#ff6b6b' : '';
}


async function uploadDocument(file) {

    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {

        setUploadStatus(
            'Only PDF files are supported.',
            true
        );

        return;
    }

    setUploadStatus(
        'INDEXING_DOCUMENT...'
    );

    const formData = new FormData();

    formData.append(
        'file',
        file
    );

    try {

        const response = await fetch(
            '/documents/upload',
            {
                method: 'POST',
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok || data.error) {

            throw new Error(
                data.error ||
                'Upload failed.'
            );
        }

        setUploadStatus(
            `INDEXED: ${data.document} (${data.chunks} chunks)`
        );

        loadDocuments();

    } catch (error) {

        setUploadStatus(
            `ERROR: ${error.message}`,
            true
        );
    }
}
async function loadDocuments() {

    if (!documentList) return;

    try {

        const response = await fetch(
            '/documents'
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error ||
                'Failed to load documents.'
            );
        }

        documentList.innerHTML = '';

        data.documents.forEach(
            document => {

                const item =
                    document.createElement('div');

                item.className =
                    'document-item';

                item.textContent =
                    document.name;

                documentList.appendChild(
                    item
                );
            }
        );

    } catch (error) {

        documentList.textContent =
            'Unable to load documents.';
    }
}
if (uploadDocumentBtn) {

    uploadDocumentBtn.addEventListener(
        'click',
        () => documentFile.click()
    );
}


if (documentFile) {

    documentFile.addEventListener(
        'change',
        () => {

            const file =
                documentFile.files[0];

            uploadDocument(file);

            documentFile.value = '';
        }
    );
}

