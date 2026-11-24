(() => {
  "use strict";

  const root = document.getElementById("pdf-layers");
  if (!root) return;
  const outputs = [1, 2].map(page => root.querySelector('[data-extracted="' + page + '"]'));
  if (outputs.some(output => !output)) return;

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  const controls = element("div", "pdf-controls");
  const pages = element("fieldset", "pdf-pages");
  pages.append(element("legend", "", "페이지 선택"));
  const radios = ["1쪽 · 텍스트 PDF", "2쪽 · 스캔 PDF"].map((title, index) => {
    const label = element("label", "pdf-option");
    const radio = element("input");
    radio.type = "radio";
    radio.name = "pdf-notice-page";
    radio.value = String(index + 1);
    radio.checked = index === 0;
    label.append(radio, document.createTextNode(title));
    pages.append(label);
    return radio;
  });
  const separate = element("input");
  separate.type = "checkbox";
  separate.id = "pdf-separate";
  const separateLabel = element("label", "pdf-separate");
  separateLabel.append(separate, document.createTextNode("글자와 이미지 분리해서 보기"));
  controls.append(pages, separateLabel);

  const stage = element("div", "pdf-stage");
  stage.setAttribute("aria-hidden", "true");
  // Use the PDF's own page rendering on every surface. Projecting DOM images also
  // works for local file URLs, where WebGL image textures may be unavailable.
  const pageImage = root.dataset.pageImage;
  function sheet(kind, label) {
    const plane = element("div", "pdf-sheet pdf-sheet-" + kind);
    const image = element("img", "pdf-page-pixels");
    image.alt = "";
    image.draggable = false;
    image.src = pageImage;
    plane.append(image);
    const caption = element("span", "pdf-sheet-caption", label);
    stage.append(plane, caption);
    return { plane, image, caption };
  }
  const whole = sheet("whole", "");
  const pictures = sheet("pictures", "PDF 이미지 객체");
  const letters = sheet("letters", "PDF 텍스트 객체");
  pictures.plane.append(element("span", "pdf-paper-mask"));
  const bounds = (root.dataset.textBox || "").split(",").map(Number);
  const hasBounds = bounds.length === 4 && bounds.every(Number.isFinite) &&
    bounds[2] > 0 && bounds[3] > 0;
  if (hasBounds) {
    const [left, top, width, height] = bounds;
    root.style.setProperty("--pdf-text-left", left + "%");
    root.style.setProperty("--pdf-text-top", top + "%");
    root.style.setProperty("--pdf-text-width", width + "%");
    root.style.setProperty("--pdf-text-height", height + "%");
  }
  const description = element("p", "pdf-reading");
  description.id = "pdf-layer-observation";
  description.setAttribute("aria-live", "polite");
  const result = element("div", "pdf-result");
  const resultTitle = element("strong", "pdf-result-title");
  result.append(resultTitle);
  root.insertBefore(controls, outputs[0]);
  root.insertBefore(stage, outputs[0]);
  root.insertBefore(description, outputs[0]);
  root.insertBefore(result, outputs[0]);
  outputs.forEach(output => {
    output.dataset.empty = String(output.textContent.length === 0);
    result.append(output);
  });

  // Project a document rectangle onto screen pixels using an orthographic camera.
  // Three.js arranges the planes. The browser composites the PDF bitmaps and type.
  // With the vendor script blocked the planes use the same unrotated 2D layout.
  const three = window.THREE;
  const camera = three ? new three.OrthographicCamera(-1, 1, 1, -1, 0.1, 4000) : null;
  if (camera) {
    camera.position.z = 1000;
    camera.updateMatrixWorld();
  }
  function place(item, cx, cy, width, height, angle, viewWidth, viewHeight) {
    let a = 1, b = 0, c = 0, d = 1, x = cx - width / 2, y = cy - height / 2;
    if (camera && angle) {
      const plane = new three.Object3D();
      plane.position.set(cx - viewWidth / 2, viewHeight / 2 - cy, 0);
      plane.rotation.set(-0.11, angle, -0.035);
      plane.updateMatrixWorld();
      function toScreen(px, py) {
        const v = new three.Vector3(px, py, 0).applyMatrix4(plane.matrixWorld).project(camera);
        return [(v.x + 1) * viewWidth / 2, (1 - v.y) * viewHeight / 2];
      }
      const tl = toScreen(-width / 2, height / 2);
      const tr = toScreen(width / 2, height / 2);
      const bl = toScreen(-width / 2, -height / 2);
      x = tl[0]; y = tl[1];
      a = (tr[0] - x) / width; b = (tr[1] - y) / width;
      c = (bl[0] - x) / height; d = (bl[1] - y) / height;
    }
    item.plane.style.width = width + "px";
    item.plane.style.height = height + "px";
    item.plane.style.transform = 'matrix(' + [a, b, c, d, x, y].join(",") + ')';
    item.caption.style.left = cx + "px";
    item.caption.style.top = cy + (Math.abs(b * width) + Math.abs(d * height)) / 2 + 8 + "px";
  }
  function show(item, visible) {
    item.plane.hidden = !visible;
    item.caption.hidden = !visible;
  }
  function layout(animateSeparation = false) {
    const width = stage.clientWidth;
    if (!width) return;
    const ratio = whole.image.naturalWidth ? whole.image.naturalWidth / whole.image.naturalHeight : 1.5;
    const isTextPage = radios[0].checked;
    const paired = isTextPage && separate.checked && hasBounds;
    const stacked = paired && width < 490;
    const limit = paired && !stacked ? width * 0.43 : width * 0.84;
    const cardWidth = Math.min(440, limit);
    const cardHeight = cardWidth / ratio;
    const rowHeight = cardHeight + 52;
    const height = Math.ceil(16 + rowHeight * (stacked ? 2 : 1));
    stage.style.height = height + "px";
    if (camera) {
      camera.left = -width / 2; camera.right = width / 2;
      camera.top = height / 2; camera.bottom = -height / 2;
      camera.updateProjectionMatrix();
    }
    const firstY = 17 + cardHeight / 2;
    show(whole, !paired); show(pictures, paired); show(letters, paired);
    if (paired) {
      place(pictures, width * (stacked ? 0.5 : 0.26), firstY, cardWidth, cardHeight, -0.26, width, height);
      place(letters, width * (stacked ? 0.5 : 0.74), firstY + (stacked ? rowHeight : 0), cardWidth, cardHeight, -0.26, width, height);
      if (animateSeparation === true && pictures.plane.animate &&
          !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        // Both objects start at the same PDF page coordinates before they separate.
        const startX = (width - cardWidth) / 2;
        const startY = firstY - cardHeight / 2 + (stacked ? rowHeight / 2 : 0);
        const registered = "matrix(1,0,0,1," + startX + "," + startY + ")";
        for (const item of [pictures, letters]) {
          item.plane.animate(
            [{ transform: registered }, { transform: item.plane.style.transform }],
            { duration: 420, easing: "cubic-bezier(.2,.75,.3,1)" }
          );
        }
      }
    } else {
      whole.caption.textContent = separate.checked && !isTextPage ? "글자와 사진을 포함한 이미지 한 장" : "PDF 뷰어에 보이는 " + (isTextPage ? "1쪽" : "2쪽");
      place(whole, width / 2, firstY, cardWidth, cardHeight, separate.checked ? -0.22 : 0, width, height);
    }
  }
  function update(event) {
    const textPage = radios[0].checked;
    const index = textPage ? 0 : 1;
    let message;
    if (textPage) {
      message = separate.checked && hasBounds
        ? "1쪽의 사진과 글자를 펼쳤습니다. ‘PDF 텍스트 객체’에 있는 두 줄을 아래 추출문과 대조하세요."
        : "1쪽에는 반납함 사진과 안내 문장이 서로 다른 객체로 들어 있습니다. 글자와 이미지를 분리해 보세요.";
    } else {
      message = separate.checked
        ? "2쪽에서는 안내 문장까지 이미지 한 장에 들어 있습니다. 분리할 텍스트 객체가 없어 추출 결과가 비어 있습니다."
        : "2쪽에서도 안내 문장이 보입니다. 이 쪽을 이미지로 저장했을 때 PDF에서 꺼낼 수 있는 글자가 있는지 확인하세요.";
    }
    description.textContent = message;
    resultTitle.textContent = (index + 1) + "쪽 · 노트북에서 추출한 문자열";
    outputs.forEach((output, n) => { output.hidden = n !== index; });
    root.dataset.page = String(index + 1);
    root.dataset.separated = String(separate.checked);
    layout(Boolean(event));
  }
  for (const control of [...radios, separate]) control.addEventListener("change", update);
  whole.image.addEventListener("load", layout);
  root.classList.add("pdf-enhanced");
  if ("ResizeObserver" in window) {
    let lastWidth = -1;
    const observer = new ResizeObserver(() => {
      if (stage.clientWidth !== lastWidth) {
        lastWidth = stage.clientWidth;
        layout();
      }
    });
    observer.observe(stage);
  } else {
    window.addEventListener("resize", layout);
  }
  update();
})();
