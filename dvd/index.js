// Start by getting the canvas which will be defined in the notebook later 
// within a raw html block
const canvas = document.getElementById('wasmCanvas');
const ctx = canvas.getContext('2d');

// This could be abstracted to a c++ function 
ctx.fillStyle = 'red';

// This function wraps the async nature of fetching a wasm file.
// Within the dictionary (or whatever js calls it) the env field defines all
// the function we need to import into our wasm program, defined earlier with
// WASM_IMPORT. Start then resturns exports which contains all our functions
async function start() {
  const wasm = await WebAssembly.instantiateStreaming(fetch("./dvd.wasm"), {
    'env': {
      'draw_rect': (x, y, width, height) => ctx.fillRect(x, y, width, height),
      'clear_rect': (x, y, width, height) => ctx.clearRect(x, y, width, height)
    }
  });
  return wasm.instance.exports;
}

let lastTimestamp = 0;

// Here we call start asynchronously, 
// catching any errors that arise and running a lambda function once the promise is fufilled
// The lambda function runs each function, where we set up a gameloop using request animation frame
// This allows us to calculate delta time. This function is then called recursively
start().then((ex) => {
  ex.setup(canvas.offsetWidth, canvas.offsetHeight);


  function gameLoop(timestamp) {
    let dt = (timestamp - lastTimestamp) / 1000; // This is delta time in seconds
    if (dt === 0 || dt > 1) { // On the first loop we dont have a lst timestamp, so we need to initialize dt with something sane
      dt = 1 / 60;
    }
    ex.draw();
    ex.update(dt);
    lastTimestamp = timestamp;
    window.requestAnimationFrame(gameLoop);
  }

  window.requestAnimationFrame(gameLoop);
}).catch((e) => console.error(e));
