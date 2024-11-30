() => {
  const images = document.querySelectorAll("img");
  const total = images.length;
  let withAltAttribute = 0;
  for (const img of images) {
    if (img.hasAttribute("alt")) withAltAttribute++;
  }
  return [total, withAltAttribute];
};
