function togglePassword(fieldNumber) {
    var passwordInput = document.querySelector('.password-field' + fieldNumber);
    var passStatus = passwordInput.nextElementSibling;

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
    var password = document.querySelector('.password-field2').value;        
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
    
var password = document.querySelector('.password-field2').value;
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
document.querySelector('.password-field2').addEventListener('input', evaluatePasswordStrength);

document.addEventListener('DOMContentLoaded', function() {
    // Toggle Password Visibility
    var togglePasswordButtons = document.querySelectorAll('.pass-status');
    togglePasswordButtons.forEach(function(button, index) {
        button.addEventListener('click', function() {
            togglePassword(index + 1);
        });
    });

    // Show and Hide Tooltip for Password Strength
    var passwordStrengthMeter = document.querySelector('.password-strength-meter');
    if (passwordStrengthMeter) {
        passwordStrengthMeter.addEventListener('mouseover', showTooltip);
        passwordStrengthMeter.addEventListener('mouseout', hideTooltip);
    }

    // Password Strength Evaluation
    var passwordField = document.querySelector('.password-field2');
    if (passwordField) {
        passwordField.addEventListener('input', evaluatePasswordStrength);
    }
});