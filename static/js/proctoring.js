/**
 * OnlineExamSystem - AI Security & Anti-Cheating Engine
 */
class ProctoringManager {
    constructor(config) {
        this.sessionKey = config.sessionKey;
        this.analyzeFrameUrl = config.analyzeFrameUrl;
        this.logViolationUrl = config.logViolationUrl;
        this.finishExamUrl = config.finishExamUrl;
        this.csrfToken = config.csrfToken;

        this.videoElement = document.getElementById('proctorWebcamVideo');
        this.canvasElement = document.createElement('canvas');
        this.canvasCtx = this.canvasElement.getContext('2d');

        this.violationCount = 0;
        this.isExamActive = true;
        this.frameInterval = null;
        this.cameraStream = null;

        this.init();
    }

    async init() {
        console.log("Initializing AI Proctoring Engine...");
        this.setupEventBlockers();
        this.setupVisibilityListeners();
        this.setupFullscreenEnforcer();
        await this.startWebcam();
        this.startFrameAnalysisLoop();
    }

    // --- 1. Webcam Stream Initialization ---
    async startWebcam() {
        try {
            this.cameraStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 320, height: 240, facingMode: 'user' },
                audio: false
            });
            if (this.videoElement) {
                this.videoElement.srcObject = this.cameraStream;
                this.videoElement.play();
            }
        } catch (err) {
            console.error("Camera Access Error:", err);
            this.triggerViolation('CAMERA_OFF', 'Camera access denied or camera disconnected.');
        }
    }

    // --- 2. Periodic Frame Sampling & OpenCV API Call ---
    startFrameAnalysisLoop() {
        this.frameInterval = setInterval(() => {
            if (!this.isExamActive || !this.videoElement || this.videoElement.paused) return;

            try {
                this.canvasElement.width = 320;
                this.canvasElement.height = 240;
                this.canvasCtx.drawImage(this.videoElement, 0, 0, 320, 240);
                const base64Frame = this.canvasElement.toDataURL('image/jpeg', 0.6);

                fetch(this.analyzeFrameUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrfToken
                    },
                    body: JSON.stringify({
                        session_key: this.sessionKey,
                        frame: base64Frame
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'violation') {
                        this.handleViolationResponse(data);
                    }
                })
                .catch(err => console.error("Frame Post error:", err));

            } catch (e) {
                console.error("Frame capture error:", e);
            }
        }, 4000); // Check frame every 4 seconds
    }

    // --- 3. Fullscreen API Enforcer ---
    setupFullscreenEnforcer() {
        document.addEventListener('fullscreenchange', () => {
            if (!document.fullscreenElement && this.isExamActive) {
                this.triggerViolation('FULLSCREEN_EXIT', 'Exited full screen examination mode.');
            }
        });
    }

    requestFullscreenMode() {
        const docEl = document.documentElement;
        if (docEl.requestFullscreen) docEl.requestFullscreen().catch(err => console.log(err));
        else if (docEl.webkitRequestFullscreen) docEl.webkitRequestFullscreen();
        else if (docEl.msRequestFullscreen) docEl.msRequestFullscreen();
    }

    // --- 4. Tab Switch & Focus Listener ---
    setupVisibilityListeners() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden && this.isExamActive) {
                this.triggerViolation('TAB_SWITCH', 'Browser tab switched or window minimized.');
            }
        });

        window.addEventListener('blur', () => {
            if (this.isExamActive) {
                this.triggerViolation('TAB_SWITCH', 'Window focus lost (Application switch).');
            }
        });
    }

    // --- 5. Event Blockers (Right Click, Copy/Paste, Shortcuts) ---
    setupEventBlockers() {
        // Prevent Right Click
        document.addEventListener('contextmenu', e => e.preventDefault());

        // Prevent Copy, Cut, Paste, Text Selection
        document.addEventListener('copy', e => e.preventDefault());
        document.addEventListener('cut', e => e.preventDefault());
        document.addEventListener('paste', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());

        // Block Key Combos
        document.addEventListener('keydown', e => {
            // Block F12, Ctrl+C, Ctrl+V, Ctrl+U, Ctrl+Shift+I, Alt+Tab
            if (e.key === 'F12' || 
               (e.ctrlKey && (e.key === 'c' || e.key === 'v' || e.key === 'u' || e.key === 'C' || e.key === 'V' || e.key === 'U')) ||
               (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J')) ||
               (e.altKey && e.key === 'Tab')) {
                e.preventDefault();
                this.triggerViolation('TAB_SWITCH', `Blocked keyboard shortcut attempt (${e.key}).`);
            }
        });
    }

    // --- 6. Violation Handler ---
    triggerViolation(violationType, details) {
        if (!this.isExamActive) return;

        fetch(this.logViolationUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken
            },
            body: JSON.stringify({
                session_key: this.sessionKey,
                violation_type: violationType,
                details: details
            })
        })
        .then(res => res.json())
        .then(data => {
            this.handleViolationResponse(data);
        })
        .catch(err => console.error("Violation logging error:", err));
    }

    handleViolationResponse(data) {
        if (!this.isExamActive) return;

        this.violationCount = data.violation_count || (this.violationCount + 1);

        const badgeEl = document.getElementById('violationCountBadge');
        if (badgeEl) badgeEl.innerText = `${this.violationCount} / 3 Warnings`;

        if (data.auto_terminate || this.violationCount >= 3) {
            this.terminateExam("Maximum security violations (3/3) reached. Exam auto-submitted.");
        } else {
            this.showWarningModal(this.violationCount, data.details || "Security Violation Detected");
        }
    }

    showWarningModal(strikeNum, message) {
        const modalEl = document.getElementById('securityWarningModal');
        const strikeText = document.getElementById('warningStrikeText');
        const descText = document.getElementById('warningDescText');

        if (strikeText) strikeText.innerText = `Strike ${strikeNum} of 3`;
        if (descText) descText.innerText = message;

        if (modalEl && typeof bootstrap !== 'undefined') {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        } else {
            alert(`SECURITY WARNING (Strike ${strikeNum}/3):\n${message}\n\nPlease return to Full Screen mode immediately.`);
        }
    }

    terminateExam(reason) {
        if (!this.isExamActive) return;
        this.isExamActive = false;
        clearInterval(this.frameInterval);

        if (this.cameraStream) {
            this.cameraStream.getTracks().forEach(track => track.stop());
        }

        alert(`EXAM TERMINATED:\n${reason}`);
        window.location.href = this.finishExamUrl;
    }
}
