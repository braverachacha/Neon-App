import { showMessage } from './uiMessage.js';

export const passwordCheck = (password, msgBox) => {
  if (password.length < 8) {
    showMessage(msgBox, 'Password should be greater than 8 characters.', 'error');
    return false;
  } else if (!/[a-z]/.test(password)) {
    showMessage(msgBox, 'Password should contain at least one lowercase letter.', 'error');
    return false;
  } else if (!/[A-Z]/.test(password)) {
    showMessage(msgBox, 'Password should contain at least one uppercase letter.', 'error');
    return false;
  } else if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    showMessage(msgBox, 'Password should contain at least one special character.', 'error');
    return false;
  } else {
    console.log('Password verified successfully!');
    return true
  }
};
