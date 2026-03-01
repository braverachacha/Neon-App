import { showMessage } from './uiMessage.js';

export const passwordCheck = (password, msgBox) => {
  // 1. Length Check
  if (password.length < 8) {
    showMessage(msgBox, 'Password should be at least 8 characters.', 'error');
    return false;
  } 
  
  // 2. Check for at least one letter (Uppercase OR Lowercase)
  else if (!/[a-zA-Z]/.test(password)) {
    showMessage(msgBox, 'Password must contain at least one letter (A-Z or a-z).', 'error');
    return false;
  } 
  
  // 3. One number OR one special character
  else if (!/[0-9!@#$%^&*(),.?":{}|<>]/.test(password)) {
    showMessage(msgBox, 'Password must contain at least one number or special character.', 'error');
    return false;
  } 
  
  // All checks passed
  else {
    return true;
  }
};
