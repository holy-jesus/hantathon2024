() => {
  var container = document.body,
    elems = container.getElementsByTagName("*"),
    elem,
    unwanted = ["script", "images", "input"],
    elementsWithText = [],
    uuid;
  for (elem in elems) {
    if (
      !unwanted.includes(elem.nodeName.toLowerCase()) &&
      !elem.children.length &&
      elem.innerText
    ) {
      uuid = uuidv4();
      elem.setAttribute("AccessScan", uuid);
      elementsWithText.push(uuid);
    }
  }
  return elementsWithText;
};
