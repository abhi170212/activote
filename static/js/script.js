// Modern JavaScript for the premium voting system

document.addEventListener('DOMContentLoaded', function() {
    // Header scroll effect
    const header = document.getElementById('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Login modal functionality
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const closeModal = document.getElementById('closeModal');
    
    if (loginBtn && loginModal && closeModal) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loginModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
        
        closeModal.addEventListener('click', function() {
            loginModal.classList.remove('active');
            document.body.style.overflow = 'auto';
        });
        
        window.addEventListener('click', function(e) {
            if (e.target === loginModal) {
                loginModal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
        
        // Login form submission
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                e.preventDefault();
                // Simulate login process
                const submitBtn = loginForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing In...';
                submitBtn.disabled = true;
                
                setTimeout(() => {
                    submitBtn.innerHTML = '<i class="fas fa-check"></i> Success!';
                    setTimeout(() => {
                        loginModal.classList.remove('active');
                        document.body.style.overflow = 'auto';
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                        
                        // Enable vote buttons after login
                        document.querySelectorAll('.vote-btn').forEach(btn => {
                            btn.disabled = false;
                        });
                        
                        // Show success message
                        alert('Login successful! You can now vote for candidates.');
                    }, 1000);
                }, 1500);
            });
        }
    }

    // Candidate card interactions
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.disabled) {
                // Show login prompt if not logged in
                if (loginModal) {
                    loginModal.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }
                return;
            }
            
            // Voting feedback
            const candidateCard = this.closest('.candidate-card');
            const candidateName = candidateCard.querySelector('.candidate-name').textContent;
            
            // Visual feedback
            this.innerHTML = '<i class="fas fa-check"></i> Voted!';
            this.style.background = 'linear-gradient(135deg, #4ade80, #22c55e)';
            
            // Show confirmation
            alert(`Thank you for voting for ${candidateName}! Your vote has been recorded.`);
        });
    });

    // Info button interactions
    document.querySelectorAll('.info-btn').forEach(button => {
        button.addEventListener('click', function() {
            const candidateCard = this.closest('.candidate-card');
            const candidateName = candidateCard.querySelector('.candidate-name').textContent;
            const candidateRole = candidateCard.querySelector('.candidate-role').textContent;
            
            // Show candidate info
            alert(`Candidate Information:

Name: ${candidateName}
Party: ${candidateRole}

Detailed information would be displayed in a modal in a full implementation.`);
        });
    });

    // FAQ accordion
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', function() {
            const faqItem = this.parentElement;
            faqItem.classList.toggle('active');
        });
    });

    // Gallery item interactions
    document.querySelectorAll('.gallery-item').forEach(item => {
        item.addEventListener('click', function() {
            // In a full implementation, this would open a lightbox
            alert('Gallery item clicked. In a full implementation, this would open a lightbox with the full-size image.');
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn, .vote-btn, .info-btn, .social-btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add animation to cards on scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe cards for animation
    document.querySelectorAll('.candidate-card, .news-card, .gallery-item, .faq-item').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Pause news feed on hover
    const newsFeed = document.querySelector('.news-feed');
    if (newsFeed) {
        const newsItems = document.querySelector('.news-items');
        newsFeed.addEventListener('mouseenter', function() {
            newsItems.style.animationPlayState = 'paused';
        });
        
        newsFeed.addEventListener('mouseleave', function() {
            newsItems.style.animationPlayState = 'running';
        });
    }

    // Parallax effect for floating elements
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        const floatingElements = document.querySelectorAll('.floating-element');
        
        floatingElements.forEach((element, index) => {
            const speed = 0.1 + (index * 0.05);
            element.style.transform = `translateY(${scrollPosition * speed}px)`;
        });
    });

    // Scroll to Top/Bottom buttons
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    const scrollBottomBtn = document.getElementById('scrollBottomBtn');
    
    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    if (scrollBottomBtn) {
        scrollBottomBtn.addEventListener('click', function() {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        });
    }

    // Show/hide scroll buttons based on scroll position
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            if (scrollTopBtn) scrollTopBtn.style.display = 'flex';
        } else {
            if (scrollTopBtn) scrollTopBtn.style.display = 'none';
        }
    });

    // Initially hide scroll to top button
    if (scrollTopBtn) scrollTopBtn.style.display = 'none';
});

// Function to show confirmation before voting
function confirmVote(candidateName) {
    return confirm(`Are you sure you want to vote for ${candidateName}? You cannot change your vote after submission.`);
}

// Function to simulate live results update
function updateResults() {
    const progresses = document.querySelectorAll('.progress');
    if (progresses.length > 0) {
        progresses.forEach(progress => {
            const currentWidth = parseInt(progress.style.width);
            if (currentWidth < 100) {
                const newWidth = Math.min(currentWidth + Math.random() * 2, 100);
                progress.style.width = newWidth + '%';
                progress.textContent = Math.round(newWidth) + '%';
            }
        });
    }
}

// Update results every 5 seconds (simulated live update)
setInterval(updateResults, 5000);