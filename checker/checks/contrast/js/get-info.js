(el) => {
  function getInheritedBackgroundColor(el, defaultStyle = null) {
    if (defaultStyle === null) {
      defaultStyle = getDefaultBackground(el.tagName);
    }
    var backgroundColor = window.getComputedStyle(el).backgroundColor;

    if (backgroundColor != defaultStyle) return backgroundColor;
    if (!el.parentElement) return defaultStyle;

    return getInheritedBackgroundColor(el.parentElement, defaultStyle);
  }

  function getDefaultBackground(tagName) {
    var element = document.createElement(tagName);
    document.head.appendChild(element);
    var bg = window.getComputedStyle(element).backgroundColor;
    document.head.removeChild(element);
    return bg;
  }

  const computedStyle = window.getComputedStyle(el);
  const backgroundColor =
    getInheritedBackgroundColor(el) || "rgb(255, 255, 255)";
  const textColor = computedStyle.color;
  const fontSize = computedStyle.fontSize;
  return [backgroundColor, textColor, fontSize];
};
