(el) => {
  function getInheritedBackgroundColor(el, defaultStyle = null) {
    // get default style for current browser
    if (defaultStyle === null) {
      defaultStyle = getDefaultBackground(el.tagName);
    }
    console.log(`defaultStyle: ${defaultStyle}`);

    // get computed color for el
    var backgroundColor = window.getComputedStyle(el).backgroundColor;
    console.log(`backgroundColor: ${backgroundColor}`);

    // if we got a real value, return it
    if (backgroundColor != defaultStyle) return backgroundColor;

    // if we've reached the top parent el without getting an explicit color, return default
    if (!el.parentElement) return defaultStyle;

    // otherwise, recurse and try again on parent element
    return getInheritedBackgroundColor(el.parentElement, defaultStyle);
  }

  function getDefaultBackground(tagName) {
    // have to add to the document in order to use getComputedStyle
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
  return [backgroundColor, textColor];
};
