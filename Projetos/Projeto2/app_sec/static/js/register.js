function togglePassword() {
    var passwordInput = document.querySelector('.password-field');
    var passStatus = document.querySelector('.pass-status');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passStatus.classList.remove('fa-eye');
        passStatus.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        passStatus.classList.remove('fa-eye-slash');
        passStatus.classList.add('fa-eye');
    }
}

function showTooltip() {
    var tooltip = document.querySelector('.password-strength-tooltip');
    tooltip.style.display = 'block';
}
function hideTooltip() {
    var tooltip = document.querySelector('.password-strength-tooltip');
    tooltip.style.display = 'none';
}

function updateCriteriaStatus() {
    var password = document.querySelector('.password-field').value;        
    // Mínimo 12 caracteres
    updateCriterionStatus(password.length > 11, 'length12-criteria');
    
    // Incluir letras maiúsculas
    updateCriterionStatus(/[A-Z]/.test(password), 'uppercase-criteria');
    
    // Incluir números
    updateCriterionStatus(/[0-9]/.test(password), 'number-criteria');
    
    // Incluir caracteres especiais
    updateCriterionStatus(/[^A-Za-z0-9]/.test(password), 'specialchar-criteria');
}

function updateCriterionStatus(isMet, criterionId) {
    var criterion = document.getElementById(criterionId);
    if (isMet) {
        criterion.innerHTML = "&#10004; " + criterion.textContent.substring(2);
        criterion.style.color = 'green';
    } else {
        criterion.innerHTML = "&#10006; " + criterion.textContent.substring(2);
        criterion.style.color = 'red';
    }
}

function evaluatePasswordStrength() {
    
    var password = document.querySelector('.password-field').value;
    var strengthBar = document.querySelector('.password-strength-meter-bar');
    var strength = 0;

    if (password.length > 11) strength += 2;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;

    switch(strength) {
        case 0:
            strengthBar.style.width = '0%';
            strengthBar.style.backgroundColor = 'red';
            break;
        case 1:
        case 2:
            strengthBar.style.width = '25%';
            strengthBar.style.backgroundColor = 'red';
            break;
        case 3:
            strengthBar.style.width = '50%';
            strengthBar.style.backgroundColor = 'orange';
            break;
        case 4:
            strengthBar.style.width = '75%';
            strengthBar.style.backgroundColor = 'yellow';
            break;
        case 5:
            strengthBar.style.width = '100%';
            strengthBar.style.backgroundColor = 'green';
            break;
    }
    updateCriteriaStatus();
}

document.querySelector('.password-field').addEventListener('input', evaluatePasswordStrength);

document.addEventListener('DOMContentLoaded', function() {
    var passStatus = document.querySelector('.pass-status');
    var passwordStrengthMeter = document.querySelector('.password-strength-meter');

    if (passStatus) {
        passStatus.addEventListener('click', function() {
            var passwordInput = document.querySelector('.password-field');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    }

    if (passwordStrengthMeter) {
        passwordStrengthMeter.addEventListener('mouseover', function() {
            var tooltip = document.querySelector('.password-strength-tooltip');
            if (tooltip) {
                tooltip.style.display = 'block';
            }
        });

        passwordStrengthMeter.addEventListener('mouseout', function() {
            var tooltip = document.querySelector('.password-strength-tooltip');
            if (tooltip) {
                tooltip.style.display = 'none';
            }
        });
    }
});
