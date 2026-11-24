(() => {
  const figures = document.querySelectorAll('figure[data-workflow]');
  if (!figures.length || !window.mermaid) return;
  mermaid.initialize({
    startOnLoad: false, securityLevel: 'strict', theme: 'base', htmlLabels: false,
    fontFamily: 'system-ui, sans-serif',
    themeVariables: {
      primaryColor: '#eaf4f3', primaryTextColor: '#173d43', primaryBorderColor: '#41827d',
      lineColor: '#536775', edgeLabelBackground: '#fff7d9', fontSize: '16px'
    },
    flowchart: { htmlLabels: false, curve: 'linear', nodeSpacing: 24, rankSpacing: 32 }
  });
  async function render() {
    for (const [index, figure] of Array.from(figures).entries()) {
      const diagram = figure.querySelector('.workflow-view');
      const source = figure.querySelector('script[type="text/plain"]').textContent;
      try {
        const { svg } = await mermaid.render('lesson-flow-' + index, source);
        diagram.innerHTML = svg;
        diagram.hidden = false;
        const drawing = diagram.querySelector('svg');
        const width = drawing.viewBox?.baseVal?.width;
        if (width > 0) {
          // Keep Korean node and edge labels legible on a narrow screen.
          drawing.style.minWidth = Math.ceil(width * 0.85) + 'px';
          const updateScroll = () => {
            if (diagram.scrollWidth > diagram.clientWidth + 1) {
              diagram.tabIndex = 0;
              diagram.setAttribute('role', 'region');
              diagram.setAttribute('aria-label', figure.querySelector('h3').textContent);
            } else {
              diagram.removeAttribute('tabindex');
              diagram.removeAttribute('role');
              diagram.removeAttribute('aria-label');
            }
          };
          updateScroll();
          if (window.ResizeObserver) new ResizeObserver(updateScroll).observe(diagram);
        }
      } catch (error) {
        document.getElementById('dlesson-flow-' + index)?.remove();
        console.error('교재 흐름도 표시 오류', error);
      }
    }
  }
  render();
})();
