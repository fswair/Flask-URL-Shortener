// URLShortener.js
export class URLShortener {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
        this.urlForm = document.getElementById('urlForm');
        this.longUrlInput = document.getElementById('longUrl');
        this.aliasInput = document.getElementById('alias');
        this.resultDiv = document.getElementById('result');
        this.shortUrlLink = document.getElementById('shortUrl');
        this.copyButton = document.getElementById('copyButton');
        this.darkModeToggle = document.getElementById('darkModeToggle');
        this.errorDiv = document.getElementById('error');

        this.init();
    }

    init() {
        document.getElementById('currentYear').textContent = new Date().getFullYear();
        this.urlForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.copyButton.addEventListener('click', () => this.copyToClipboard());
        this.darkModeToggle.addEventListener('click', () => this.toggleDarkMode());
    }

    async handleSubmit(event) {
        event.preventDefault();
        const longUrl = this.longUrlInput.value;
        const alias = this.aliasInput.value || null;

        this.clearError();

        try {
            const shortUrl = await this.shortenURL(longUrl, alias);
            this.displayResult(shortUrl);
        } catch (error) {
            console.error('Error shortening URL:', error);
            this.showError('Failed to shorten URL. Please try again.');
        }
    }

    async shortenURL(longUrl, alias) {
        const response = await fetch(`${this.apiUrl}/shorten`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ longUrl, alias }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Network response was not ok');
        }

        const data = await response.json();
        return data.shortUrl;
    }

    displayResult(shortUrl) {
        this.shortUrlLink.href = shortUrl;
        this.shortUrlLink.textContent = shortUrl;
        this.resultDiv.classList.remove('hidden');
        this.longUrlInput.value = '';
        this.aliasInput.value = '';
    }

    showError(message) {
        this.errorDiv.textContent = message;
        this.errorDiv.classList.remove('hidden');
    }

    clearError() {
        this.errorDiv.classList.add('hidden');
        this.errorDiv.textContent = '';
    }

    async copyToClipboard() {
        try {
            await navigator.clipboard.writeText(this.shortUrlLink.href);
            alert('URL copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    }

    toggleDarkMode() {
        document.documentElement.classList.toggle('dark');
    }
}
