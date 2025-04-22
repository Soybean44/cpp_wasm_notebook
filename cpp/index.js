const canvas = document.getElementById('wasmCanvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'red';
async function start() {
  const wasm = await WebAssembly.instantiateStreaming(fetch("./dvd.wasm"), {
    'env': {
      'draw_rect': (x, y, width, height) => ctx.fillRect(x, y, width, height),
      'clear_rect': (x, y, width, height) => ctx.clearRect(x, y, width, height)
    }
  });
  return wasm.instance.exports;
}
start().then((ex) => {
  ex.setup(canvas.offsetWidth, canvas.offsetHeight);
  ex.draw;
  ex.update;
  function gameLoop(timestamp) {
    ex.draw();
    ex.update();
    window.requestAnimationFrame(gameLoop);
  }
  window.requestAnimationFrame(gameLoop);
}).catch((e) => console.error(e));




