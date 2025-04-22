#include <wasm.h>

WASM_IMPORT void draw_rect(int x, int y, int width, int height);
WASM_IMPORT void clear_rect(int x, int y, int width, int height);

class Square {
  public:
    float x;
    float y;
    int size; 

    Square(float x=0, float y=0, int size=50) : x(x), y(y), size(size) {}
    
    void render() {
      draw_rect(x, y, size, size);
    }
};

int screenWidth;
int screenHeight;
float vx;
float vy;
Square square;

WASM_EXPORT void setup(int w, int h) { // Here is all our initial setup
  int size = 50;

  screenWidth = w;
  screenHeight = h;

  square = Square(screenWidth/2 - (size/2), screenHeight/2 - (size/2), size);

  // Distance traveled per second
  vx = screenWidth/2;
  vy = screenHeight/2;
}

WASM_EXPORT void draw() { // Here we do all our draw calls
  clear_rect(0, 0, screenWidth, screenHeight);
  square.render();
}

WASM_EXPORT void update(float dt) { // Here is all the update logic
  square.x += vx*dt;
  square.y += vy*dt;

  if (square.x > screenWidth-50 || square.x < 0) {
    vx = -vx;
  }
  if (square.y > screenHeight-50 || square.y < 0) {
    vy = -vy;
  }
}
