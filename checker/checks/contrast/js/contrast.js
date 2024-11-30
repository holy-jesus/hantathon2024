() => {
  function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
      (
        +c ^
        (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (+c / 4)))
      ).toString(16)
    );
  }

  var container = document.body,
    elems = container.getElementsByTagName("*"),
    elem,
    unwanted = ["script", "images", "input"],
    elementsWithText = [],
    uuid;
  for (elem of elems) {
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
