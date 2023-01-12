email = document.querySelector('#Login1')
password = document.querySelector('#Login2')
dropdown = document.querySelector('#div_login')

if (email && password) {
    email.addEventListener('focusin', () => dropdown.classList.add('div_login_block'));
    email.addEventListener('focusout', () => dropdown.classList.remove('div_login_block'));

    password.addEventListener('focusin', () => dropdown.classList.add('div_login_block'));
    password.addEventListener('focusout', () => dropdown.classList.remove('div_login_block'));
}
