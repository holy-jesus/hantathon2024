(zoom) => {
  document.body.style.transform = `scale(${zoom})`;
  document.body.style.transformOrigin = "0 0";
  return null;
};
