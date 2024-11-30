() => {
  const buttons = document.querySelectorAll("button, input[type=button]");
  const total = buttons.length;
  let withAriaLabel = 0;
  for (const button of buttons) {
    if (button.hasAttribute("aria-label")) withAriaLabel++;
  }
  return [total, withAriaLabel];
};
