() => {
  const buttons = document.querySelectorAll("button, input[type=button]");
  for (const button of buttons) {
    if (!button.hasAttribute("aria-label")) {
      return false;
    }
  }
  return true;
};
