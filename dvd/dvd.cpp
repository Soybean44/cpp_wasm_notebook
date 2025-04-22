#include <wasm.h>

int screenWidth;
int screenHeight;
float x;
float y;
float vx;
float vy;

WASM_IMPORT void draw_rect(int x, int y, int width, int height);
WASM_IMPORT void clear_rect(int x, int y, int width, int height);

WASM_EXPORT void setup(int w, int h) { // Here is all our initial setup
  screenWidth = w;
  screenHeight = h;
  x = screenWidth/2-25;
  y = screenHeight/2-25;

  // Distance traveled per second
  vx = screenWidth/2;
  vy = screenHeight/2;
}

WASM_EXPORT void draw() { // Here we do all our draw calls
  clear_rect(0, 0, screenWidth, screenHeight);
  draw_rect(x, y, 50, 50);
}

WASM_EXPORT void update(float dt) { // Here is all the update logic
  x += vx*dt;
  y += vy*dt;

  if (x > screenWidth-50 || x < 0) {
    vx = -vx;
  }
  if (y > screenHeight-50 || y < 0) {
    vy = -vy;
  }
}
