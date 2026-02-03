/**
 * Pygentic AI - Frontend Application
 * Progressive loading and enhanced UX interactions
 */

(function() {
    'use strict';

    // Progressive loading messages
    const LOADING_MESSAGES = [
        'Fetching URL content...',
        'Analyzing page structure...',
        'Extracting key information...',
        'Identifying patterns...',
        'Generating SWOT analysis...',
        'Finalizing insights...',
        'Almost there...'
    ];

    let loadingMessageIndex = 0;
    let loadingInterval = null;
    let pollCount = 0;
    let pollInterval = 1000; // Start at 1s
    const MAX_POLL_INTERVAL = 5000; // Max 5s

    /**
     * Update loading message progressively
     */
    function updateLoadingMessage() {
        const statusElement = document.getElementById('loading-status');
        if (!statusElement) return;

        if (loadingMessageIndex < LOADING_MESSAGES.length - 1) {
            loadingMessageIndex++;
        }

        statusElement.textContent = LOADING_MESSAGES[loadingMessageIndex];
        statusElement.style.animation = 'fadeIn 0.3s ease-in';
    }

    /**
     * Start progressive loading messages
     */
    function startLoadingMessages() {
        loadingMessageIndex = 0;
        pollCount = 0;
        pollInterval = 1000;

        const statusElement = document.getElementById('loading-status');
        if (statusElement) {
            statusElement.textContent = LOADING_MESSAGES[0];
        }

        // Update message every 3 seconds
        if (loadingInterval) {
            clearInterval(loadingInterval);
        }

        loadingInterval = setInterval(updateLoadingMessage, 3000);
    }

    /**
     * Stop loading messages
     */
    function stopLoadingMessages() {
        if (loadingInterval) {
            clearInterval(loadingInterval);
            loadingInterval = null;
        }
        loadingMessageIndex = 0;
    }

    /**
     * Announce to screen readers
     */
    function announceToScreenReader(message, priority = 'polite') {
        const announcement = document.createElement('div');
        announcement.setAttribute('role', 'status');
        announcement.setAttribute('aria-live', priority);
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;

        document.body.appendChild(announcement);

        // Remove after announcement is made
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }

    /**
     * Smooth scroll to results and manage focus
     */
    function scrollToResults() {
        const resultsSection = document.getElementById('result-container');
        const resultsHeading = document.getElementById('results-heading');

        if (resultsSection) {
            // Announce completion to screen readers
            announceToScreenReader('Analysis complete. Results are now available.', 'assertive');

            // Scroll to results
            resultsSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });

            // Move focus to results heading for keyboard users
            if (resultsHeading) {
                setTimeout(() => {
                    resultsHeading.focus();
                }, 600);
            }
        }
    }

    /**
     * Exponential backoff for polling
     */
    function calculateNextPollInterval() {
        pollCount++;

        if (pollCount > 3) {
            pollInterval = Math.min(pollInterval * 1.5, MAX_POLL_INTERVAL);
        }

        return pollInterval;
    }

    /**
     * Initialize keyboard navigation for SWOT cards
     */
    function initializeKeyboardNavigation() {
        const cards = document.querySelectorAll('.swot-card');

        cards.forEach((card, index) => {
            card.addEventListener('keydown', function(e) {
                let targetCard = null;

                switch (e.key) {
                    case 'ArrowRight':
                    case 'ArrowDown':
                        e.preventDefault();
                        targetCard = cards[index + 1] || cards[0];
                        break;
                    case 'ArrowLeft':
                    case 'ArrowUp':
                        e.preventDefault();
                        targetCard = cards[index - 1] || cards[cards.length - 1];
                        break;
                    case 'Home':
                        e.preventDefault();
                        targetCard = cards[0];
                        break;
                    case 'End':
                        e.preventDefault();
                        targetCard = cards[cards.length - 1];
                        break;
                }

                if (targetCard) {
                    targetCard.focus();
                }
            });
        });
    }

    /**
     * Initialize form submission handler
     */
    function initializeForm() {
        const form = document.getElementById('swotSearch');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            // Announce to screen readers
            announceToScreenReader('Analysis started. Please wait while we process your request.', 'assertive');

            // Start loading messages when form is submitted
            startLoadingMessages();

            // Show spinner
            const spinner = document.getElementById('spinner');
            if (spinner) {
                spinner.classList.remove('is-hidden');
            }
        });
    }

    /**
     * Monitor for analysis completion
     */
    function monitorAnalysisCompletion() {
        const resultBox = document.getElementById('result');
        if (!resultBox) return;

        // Use MutationObserver to watch for content changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && resultBox.innerHTML.trim().length > 0) {
                    // Analysis complete
                    stopLoadingMessages();

                    // Hide spinner
                    const spinner = document.getElementById('spinner');
                    if (spinner) {
                        spinner.classList.add('is-hidden');
                    }

                    // Initialize keyboard navigation for SWOT cards
                    initializeKeyboardNavigation();

                    // Scroll to results after a brief delay
                    setTimeout(scrollToResults, 500);

                    // Add success class for animation
                    const resultContainer = document.getElementById('result-container');
                    if (resultContainer) {
                        resultContainer.classList.add('animate-in');
                    }
                }
            });
        });

        observer.observe(resultBox, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Add button press effects
     */
    function initializeButtonEffects() {
        const buttons = document.querySelectorAll('.search-button, .error-state__button');

        buttons.forEach(button => {
            button.addEventListener('mousedown', function() {
                this.style.transform = 'scale(0.95)';
            });

            button.addEventListener('mouseup', function() {
                this.style.transform = '';
            });

            button.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }

    /**
     * Initialize smooth anchor scrolling
     */
    function initializeSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#' || !href) return;

                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Initialize all features on DOM ready
     */
    function initialize() {
        initializeForm();
        monitorAnalysisCompletion();
        initializeButtonEffects();
        initializeSmoothScrolling();

        console.log('✨ Pygentic AI initialized');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }

    // Export functions for external use if needed
    window.PygenticAI = {
        startLoadingMessages,
        stopLoadingMessages,
        scrollToResults,
        announceToScreenReader
    };
})();
