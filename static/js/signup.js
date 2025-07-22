document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signupForm');
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const strengthBar = document.querySelector('.strength-bar');
    const strengthText = document.querySelector('.strength-text');
    
    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordField = document.getElementById(targetId);
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordField.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });
    
    // Password strength indicator
    password1.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        
        // Check for length
        if (password.length >= 8) strength += 1;
        if (password.length >= 12) strength += 1;
        
        // Check for uppercase letters
        if (/[A-Z]/.test(password)) strength += 1;
        
        // Check for numbers
        if (/[0-9]/.test(password)) strength += 1;
        
        // Check for special characters
        if (/[^A-Za-z0-9]/.test(password)) strength += 1;
        
        // Update UI
        updateStrengthIndicator(strength);
    });
    
    function updateStrengthIndicator(strength) {
        const bar = document.querySelector('.strength-bar');
        const width = (strength / 5) * 100;
        
        bar.style.width = width + '%';
        
        // Change color based on strength
        if (strength <= 2) {
            bar.style.backgroundColor = '#e74c3c';
            strengthText.textContent = 'Password strength: weak';
            strengthText.style.color = '#e74c3c';
        } else if (strength <= 4) {
            bar.style.backgroundColor = '#f39c12';
            strengthText.textContent = 'Password strength: medium';
            strengthText.style.color = '#f39c12';
        } else {
            bar.style.backgroundColor = '#2ecc71';
            strengthText.textContent = 'Password strength: strong';
            strengthText.style.color = '#2ecc71';
        }
    }
    
    // Form validation
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Check if passwords match
        if (password1.value !== password2.value) {
            isValid = false;
            password2.setCustomValidity("Passwords don't match");
            password2.reportValidity();
        } else {
            password2.setCustomValidity('');
        }
        
        // Check password strength
        if (password1.value.length < 8) {
            isValid = false;
            password1.setCustomValidity("Password must be at least 8 characters long");
            password1.reportValidity();
        } else {
            password1.setCustomValidity('');
        }
        
        if (!isValid) {
            e.preventDefault();
        } else {
            // Form is valid, you could add AJAX submission here
            console.log('Form is valid, ready to submit');
        }
    });
    
    // Phone number formatting
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function(e) {
        const x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });
});